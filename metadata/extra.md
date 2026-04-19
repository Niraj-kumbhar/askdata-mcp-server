## Cross-Table Reference

### Entity Relationship Summary

```
employees (300K rows)
    ├── dept_emp     (331K rows)  ──→ departments (9 rows)
    ├── dept_manager (24 rows)   ──→ departments (9 rows)
    ├── titles       (443K rows)
    └── salaries     (2.8M rows)
```

### Universal Pattern: Temporal Filtering

All junction and history tables (`dept_emp`, `dept_manager`, `titles`, `salaries`) use a
`from_date` / `to_date` pair to represent time periods.

| Scenario | Filter |
|----------|--------|
| Current record | `to_date = '9999-01-01'` |
| Record at specific date D | `from_date <= 'D' AND to_date > 'D'` |
| Full history | No date filter |
| Active between two dates | `from_date < 'end' AND to_date > 'start'` |

> **Note:** `titles.to_date` is nullable — use `(to_date = '9999-01-01' OR to_date IS NULL)`
> for current titles. All other `to_date` columns are NOT NULL.

### Key Sentinel Value

`to_date = '9999-01-01'` is used consistently as a **sentinel/magic value** meaning
"this record is currently active / has no end date." This is a design pattern, not a real date.

### ON DELETE CASCADE Chain

Deleting a row from `employees` automatically cascades to:
- `dept_emp` (all department assignments for that employee)
- `dept_manager` (all management records for that employee)
- `titles` (all title records for that employee)
- `salaries` (all salary records for that employee)

Deleting a row from `departments` automatically cascades to:
- `dept_emp` (all employee assignments to that department)
- `dept_manager` (all management records for that department)