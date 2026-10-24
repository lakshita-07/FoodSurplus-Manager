# Review 3 demonstration notes

## Suggested demo sequence

1. Open dashboard and explain the six entity tables plus the `deliverysummary` view.
2. Open Donors and search for `Fresh Mart`.
3. Add a donor using a new email address, then show it in the list.
4. Edit the donor and show the updated value.
5. Open Donations and show donor/category foreign-key dropdowns.
6. Try an invalid donation quantity or expiry time and show the validation message.
7. Open Redistributions and demonstrate the delivery status and allocation fields.
8. Open Delivery summary and explain that it joins `REDISTRIBUTION`, `DONATION`, and `RECIPIENT`.
9. Explain that MySQL primary keys, foreign keys, unique constraints, and check constraints support data integrity.

## Architecture

Browser (HTML/CSS) → Flask routes and validation → MySQL Connector/Python → `food_surplus_db` tables and `deliverysummary` view.

## Before submission

- Run each test in `TEST_CASES.md` and record the actual result.
- Take genuine screenshots of the working app.
- Check that `.env` is not committed to GitHub.
- Confirm your faculty's rubric and adapt the report/presentation to its exact format.
