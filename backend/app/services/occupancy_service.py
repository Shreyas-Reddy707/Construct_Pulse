from typing import List, Optional, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.models import (
    Attendance, User, Department, Contractor, 
    OccupancySnapshot, AttendanceStatus, IdentityType, SnapshotSource,
    Site, UserRole
)
from app.schemas.schemas import (
    OccupancyQuery, OccupancySummary, OccupancyWorker,
    DepartmentOccupancy, ContractorOccupancy, VisitorOccupancy,
    OccupancyDashboard, OccupancySnapshotResponse
)

class OccupancyService:
    @classmethod
    def _enforce_tenant_isolation(cls, session: Session, current_user: User, query: OccupancyQuery) -> OccupancyQuery:
        from app.core.exceptions import ResourceNotFoundException, ValidationException, AuthorizationException
        if current_user.role == UserRole.COMPANY_ADMIN:
            if query.site_id:
                site = session.query(Site).filter(Site.id == query.site_id, Site.company_id == current_user.company_id).first()
                if not site:
                    raise ResourceNotFoundException("Site not found")
            else:
                raise ValidationException("site_id is required")
        elif current_user.role == UserRole.SITE_MANAGER:
            if not query.site_id:
                 raise ValidationException("site_id is required")
            valid_site = any(s.id == query.site_id for s in current_user.assigned_sites)
            if not valid_site:
                 raise AuthorizationException("Not assigned to this site")
        elif current_user.role == UserRole.WORKER:
            raise AuthorizationException("Workers cannot access occupancy data")
        return query

    @staticmethod
    def _build_base_query(session: Session, query: OccupancyQuery):
        """
        Builds the foundational query for active occupancy.
        """
        yesterday = datetime.now(timezone.utc) - timedelta(hours=24)
        q = session.query(Attendance).join(User, Attendance.user_id == User.id).filter(
            Attendance.status == AttendanceStatus.CHECKED_IN,
            Attendance.check_out_time.is_(None),
            Attendance.check_in_time >= yesterday
        )

        if query.site_id:
            q = q.filter(Attendance.site_id == query.site_id)
        if query.department_id:
            q = q.filter(User.department_id == query.department_id)
        if query.contractor_id:
            q = q.filter(User.contractor_id == query.contractor_id)
        if not query.include_visitors:
            q = q.filter(User.identity_type != IdentityType.VISITOR)

        return q

    @staticmethod
    def _get_base_filters(query: OccupancyQuery) -> List[Any]:
        filters = [
            Attendance.status == AttendanceStatus.CHECKED_IN,
            Attendance.check_out_time.is_(None)
        ]
        if query.site_id:
            filters.append(Attendance.site_id == query.site_id)
        return filters

    @classmethod
    def get_dashboard(cls, session: Session, query: OccupancyQuery, current_user: User) -> OccupancyDashboard:
        """
        Aggregates multiple occupancy metrics into a single dashboard projection.
        Performs aggregations in Python from a single atomic database query to guarantee consistency.
        """
        query = cls._enforce_tenant_isolation(session, current_user, query)
        base_filters = cls._get_base_filters(query)
        
        q = session.query(
            User.identity_type,
            Department.id.label('department_id'),
            Department.name.label('department_name'),
            Contractor.id.label('contractor_id'),
            Contractor.name.label('contractor_name')
        ).join(
            User, Attendance.user_id == User.id
        ).outerjoin(
            Department, User.department_id == Department.id
        ).outerjoin(
            Contractor, User.contractor_id == Contractor.id
        ).filter(*base_filters)

        if not query.include_visitors:
            q = q.filter(User.identity_type != IdentityType.VISITOR)

        # Single atomic fetch guarantees mathematical consistency
        rows = q.all()
        
        total_present = len(rows)
        active_workers = 0
        active_visitors = 0
        active_contractors = 0
        
        dept_counts = {}
        cont_counts = {}

        for row in rows:
            if row.identity_type == IdentityType.WORKER:
                active_workers += 1
            elif row.identity_type == IdentityType.VISITOR:
                active_visitors += 1
            elif row.identity_type == IdentityType.CONTRACTOR_REPRESENTATIVE:
                active_contractors += 1

            if row.department_id:
                if row.department_id not in dept_counts:
                    dept_counts[row.department_id] = {'name': row.department_name, 'count': 0}
                dept_counts[row.department_id]['count'] += 1

            if row.contractor_id:
                if row.contractor_id not in cont_counts:
                    cont_counts[row.contractor_id] = {'name': row.contractor_name, 'count': 0}
                cont_counts[row.contractor_id]['count'] += 1

        dept_breakdown = [
            DepartmentOccupancy(department_id=d_id, department_name=d_data['name'], worker_count=d_data['count'])
            for d_id, d_data in dept_counts.items()
        ]
        cont_breakdown = [
            ContractorOccupancy(contractor_id=c_id, contractor_name=c_data['name'], worker_count=c_data['count'])
            for c_id, c_data in cont_counts.items()
        ]
        visitor_breakdown = VisitorOccupancy(visitor_count=active_visitors)

        summary = OccupancySummary(
            total_present=total_present,
            active_workers=active_workers,
            active_visitors=active_visitors,
            active_contractors=active_contractors,
            site_id=query.site_id or "all",
            timestamp=datetime.now(timezone.utc)
        )

        return OccupancyDashboard(
            summary=summary,
            department_breakdown=dept_breakdown,
            contractor_breakdown=cont_breakdown,
            visitor_breakdown=visitor_breakdown,
            total_occupancy=total_present,
            capacity=None,
            remaining_capacity=None
        )

    @classmethod
    def get_muster_list(cls, session: Session, query: OccupancyQuery, current_user: User) -> List[OccupancyWorker]:
        """
        Returns a paginated list of workers currently occupying a site.
        """
        query = cls._enforce_tenant_isolation(session, current_user, query)
        q = cls._build_base_query(session, query)
        
        q = session.query(
            Attendance,
            User,
            Department.name.label("department_name"),
            Contractor.name.label("contractor_name")
        ).join(
            User, Attendance.user_id == User.id
        ).outerjoin(
            Department, User.department_id == Department.id
        ).outerjoin(
            Contractor, User.contractor_id == Contractor.id
        ).filter(
            Attendance.status == AttendanceStatus.CHECKED_IN,
            Attendance.check_out_time.is_(None)
        )

        if query.site_id:
            q = q.filter(Attendance.site_id == query.site_id)
        if query.department_id:
            q = q.filter(User.department_id == query.department_id)
        if query.contractor_id:
            q = q.filter(User.contractor_id == query.contractor_id)
        if not query.include_visitors:
            q = q.filter(User.identity_type != IdentityType.VISITOR)

        q = q.order_by(Attendance.check_in_time.desc())
        q = q.offset(query.skip).limit(query.limit)

        rows = q.all()
        return [
            OccupancyWorker(
                attendance_id=att.id,
                worker_id=user.id,
                worker_name=user.name,
                identity_type=user.identity_type.value,
                department_name=department_name,
                contractor_name=contractor_name,
                check_in_time=att.check_in_time
            )
            for att, user, department_name, contractor_name in rows
        ]

    @classmethod
    def _map_snapshot_to_dto(cls, snapshot: OccupancySnapshot) -> OccupancySnapshotResponse:
        return OccupancySnapshotResponse(
            snapshot_id=snapshot.id,
            site_id=snapshot.site_id,
            captured_at=snapshot.timestamp,
            snapshot_source=snapshot.snapshot_source,
            captured_by=snapshot.captured_by,
            total_occupancy=snapshot.total_workers,
            department_breakdown=snapshot.department_breakdown,
            contractor_breakdown=snapshot.contractor_breakdown,
            visitor_breakdown=snapshot.visitor_breakdown if snapshot.visitor_breakdown else {}
        )

    @classmethod
    def capture_snapshot(
        cls, 
        session: Session, 
        site_id: str, 
        current_user: User,
        source: SnapshotSource = SnapshotSource.MANUAL,
        commit: bool = True
    ) -> OccupancySnapshotResponse:
        """
        Calculates current occupancy and explicitly stores a snapshot.
        """
        query = OccupancyQuery(site_id=site_id)
        query = cls._enforce_tenant_isolation(session, current_user, query)
        dashboard = cls.get_dashboard(session, query, current_user)

        dept_dict = {d.department_name: d.worker_count for d in dashboard.department_breakdown}
        cont_dict = {c.contractor_name: c.worker_count for c in dashboard.contractor_breakdown}
        vis_dict = {"visitor_count": dashboard.visitor_breakdown.visitor_count}

        snapshot = OccupancySnapshot(
            site_id=site_id,
            total_workers=dashboard.total_occupancy,
            department_breakdown=dept_dict,
            contractor_breakdown=cont_dict,
            visitor_breakdown=vis_dict,
            snapshot_source=source,
            captured_by=current_user.id,
            snapshot_version=1
        )
        
        session.add(snapshot)
        if commit:
            session.commit()
            session.refresh(snapshot)
        else:
            session.flush()
        
        return cls._map_snapshot_to_dto(snapshot)

    @classmethod
    def get_snapshot(cls, session: Session, snapshot_id: str) -> Optional[OccupancySnapshotResponse]:
        snapshot = session.query(OccupancySnapshot).filter(OccupancySnapshot.id == snapshot_id).first()
        if snapshot:
            return cls._map_snapshot_to_dto(snapshot)
        return None

    @classmethod
    def list_snapshots(cls, session: Session, site_id: str, current_user: User, skip: int = 0, limit: int = 100) -> List[OccupancySnapshotResponse]:
        query = OccupancyQuery(site_id=site_id)
        cls._enforce_tenant_isolation(session, current_user, query)
        snapshots = session.query(OccupancySnapshot).filter(
            OccupancySnapshot.site_id == site_id
        ).order_by(OccupancySnapshot.timestamp.desc()).offset(skip).limit(limit).all()
        return [cls._map_snapshot_to_dto(s) for s in snapshots]
