# Food Surplus Collection, Matching & Redistribution Management System

A local Flask + MySQL web prototype for Review 3. It uses the existing `food_surplus_db` schema and includes a dashboard, record search, CRUD screens, form validation, and the `deliverysummary` view.

## Features

- Dashboard counts for donors, donations, food categories, recipients, volunteers, and redistributions.
- List and search records in all six base tables.
- Add, view, edit, and delete records (deletes are submitted with POST; MySQL foreign keys protect referenced records).
- Dropdowns for foreign-key relationships.
- Validation for positive donation/allocation quantities, expiry after listing, positive shelf life, non-negative capacities, and feedback ratings from 1–5.
- Allocation validation to stop total allocations for a donation from exceeding its quantity.
- Delivery summary report using the existing `deliverysummary` database view.

## Requirements

- Python 3.10 or newer recommended.
- MySQL Server running locally.
- The existing database `food_surplus_db` restored/available in MySQL.

## Run on macOS

Open Terminal in this project folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with the MySQL username and password you use in Workbench. Do not commit `.env` to GitHub.

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Keep the terminal window open while using the application; press `Control+C` to stop the server.

## Database backup and restore

The supplied `database/food_surplus_backup.sql` is a backup of the schema and sample records. **Do not import it over your current database unless you intentionally want to replace that database.** The dump contains `DROP TABLE` statements. To restore it as a separate copy, first create a separate database and edit the dump's `USE`/database context if required, or use a dedicated test MySQL instance. For Review 3, the preferred approach is to connect to your already existing `food_surplus_db`.

The form relies on MySQL to generate record IDs. If your existing database gives a “Field '…ID' doesn't have a default value” error when adding a record, run the entire `database/enable_auto_increment.sql` script in MySQL Workbench with `food_surplus_db` selected. It temporarily removes and restores the related foreign keys while updating the six primary-key columns; it does not delete existing records. Newly created databases from `database/food_surplus_db.sql` already have auto-incrementing IDs.

## GitHub setup

1. Create an empty repository named `food-surplus-management-system` on GitHub.
2. From this folder, run:

```bash
git init
git add .
git status
git commit -m "Build Food Surplus Review 3 prototype"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/food-surplus-management-system.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your own GitHub username. Check `git status` before committing and confirm `.env` is not listed.

## Test checklist

See `docs/TEST_CASES.md` for the initial manual test plan. Record actual results and screenshots after running the app against your MySQL database.

## Important scope note

This is a college prototype intended for local demonstration. It is not production-hardened: before any public deployment, add authentication/authorization, CSRF protection, stricter server-side input handling, audit logging, and a least-privilege MySQL user. Do not expose the local MySQL server to the public internet.
