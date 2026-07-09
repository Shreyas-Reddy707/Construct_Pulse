from sqlalchemy.orm import Query
from sqlalchemy import or_
from app.core.exceptions import ValidationException

def apply_search(query: Query, search_term: str, search_fields: list) -> Query:
    if not search_term or not search_term.strip() or not search_fields:
        return query
    
    term = f"%{search_term.strip()}%"
    return query.filter(or_(*[field.ilike(term) for field in search_fields]))

def apply_sort(query: Query, sort_by: str, sort_order: str, sortable_fields: dict, default_sort_field: str, default_sort_order: str = "desc") -> Query:
    final_sort_by = sort_by if sort_by else default_sort_field
    final_sort_order = (sort_order if sort_order else default_sort_order).lower()

    if final_sort_by not in sortable_fields:
        raise ValidationException(f"Invalid sort field: {final_sort_by}")

    sort_col = sortable_fields[final_sort_by]
    
    if final_sort_order == "desc":
        return query.order_by(sort_col.desc())
    return query.order_by(sort_col.asc())
