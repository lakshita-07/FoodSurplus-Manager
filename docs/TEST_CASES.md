# Review 3 — Manual Test Cases

Fill the **Actual Result** and **Status** columns after running the application. Capture screenshots of the dashboard, list/search, add/edit forms, validation message, and delivery summary for the review evidence.

| ID | Feature | Test input/action | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| TC01 | Database connection | Start app with correct `.env` credentials | Dashboard shows counts for six base tables | To be tested | Pending |
| TC02 | Read | Open Donors | Existing donor records appear | To be tested | Pending |
| TC03 | Search | Search donor name `Fresh Mart` | Matching donor appears | To be tested | Pending |
| TC04 | Create | Add a donor with a unique email and required name | Record is saved and appears in list | To be tested | Pending |
| TC05 | Required validation | Submit a donor without DonorName | Form blocks submission | To be tested | Pending |
| TC06 | Unique constraint | Add a donor using an existing email | Database rejects duplicate email with a visible error | To be tested | Pending |
| TC07 | Update | Edit an existing donor's city | Updated value appears in list | To be tested | Pending |
| TC08 | Delete | Delete a donor not referenced by a donation | Record is deleted | To be tested | Pending |
| TC09 | Referential integrity | Try deleting a donor referenced by a donation | MySQL foreign key prevents deletion and app displays an error | To be tested | Pending |
| TC10 | Donation quantity | Add donation with quantity 0 or negative | Validation rejects quantity | To be tested | Pending |
| TC11 | Expiry validation | Set expiry before or equal to listing time | Validation rejects the date range | To be tested | Pending |
| TC12 | Foreign key selection | Add donation and choose a donor/category from dropdowns | IDs map to existing donor/category records | To be tested | Pending |
| TC13 | Allocation limit | Allocate more than the remaining donation quantity | Validation rejects allocation | To be tested | Pending |
| TC14 | Feedback rating | Enter a rating outside 1–5 | Validation rejects rating | To be tested | Pending |
| TC15 | View/report | Open Delivery summary | Joined food, recipient, quantity and status appear | To be tested | Pending |

**Evidence to collect:** one screenshot per major feature and a brief note on any failed test and its correction. Do not mark tests as passed until they have actually been run.
