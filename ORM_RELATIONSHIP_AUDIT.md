# SQLAlchemy ORM Relationship Audit

## 1. Root Cause
The `InvalidRequestError: Mapper[User(users)] has no property 'company'` is caused by a structural code insertion error in `models.py`. The entire `Session` model class definition was accidentally pasted *inside* the middle of the `User` class definition. As a result, all of the SQLAlchemy relationships and properties that were supposed to belong to `User` (e.g., `company`, `department`, `contractor`, `attendances`, `assigned_sites`, and the `@property` getters) were inadvertently assigned to the `Session` class instead. 

When SQLAlchemy attempts to build the bidirectional relationship between `Company` and `User` (since `Company` defines `users = relationship("User", back_populates="company")`), it searches the `User` class for the `company` property and fails because it was stolen by `Session`.

## 2. Exact Files Involved
- `backend/app/models/models.py` (specifically lines 299 - 354)

## 3. Exact Relationship Mismatch
- **Model declaring `back_populates="company"`:** `Company` (Line 273: `users = relationship("User", back_populates="company")`).
- **Does `User` define `company`?** No. `User` ends at line 315. It has the foreign key `company_id`, but lacks the relationship property.
- **Does `Company` define `users`?** Yes, it expects `User` to have `company`.
- **Where did it go?** The `Session` class defines `company = relationship("Company", back_populates="users")` on line 334. `Session` also defines `department`, `contractor`, `attendances`, and `assigned_sites` referencing `User`'s foreign keys and back_populates.
- **Bidirectional Consistency:** Broken. `Company` points to `User`, but `Session` points back to `Company`, creating an impossible cyclic graph because `Session` lacks a `company_id` foreign key.

## 4. Why SQLAlchemy Throws This Error
SQLAlchemy evaluates `relationship` strings at runtime (during the first query execution or when `registry.configure()` is called). When processing `Company.users = relationship("User", back_populates="company")`, it inspects the `User` mapper to link the `company` property back to `Company.users`. Because `User` does not have a `company` property (it is inside `Session`), it immediately aborts with the `InvalidRequestError`.

## 5. Smallest Possible Fix
Relocate the `Session` class definition so it does not interrupt the `User` class. 

Specifically, cut lines 317 to 332:
```python
class Session(Base):
    __tablename__ = "sessions"
    # ... fields ...
    user = relationship("User")
```
And paste them *after* line 354 (below all the `@property` methods belonging to `User`). This restores all relationships (`company`, `department`, etc.) back into the `User` class where they belong.

## 6. Confidence Level
**100%**
The code inspection explicitly confirms that `Session` was injected between `User`'s column definitions and `User`'s relationship definitions.

---
**CERTIFICATION**
ROOT CAUSE IDENTIFIED
*(Repository code was not modified during this audit)*
