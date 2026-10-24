# Food Surplus Collection, Matching & Redistribution Management System

A local Flask + MySQL web prototype for Review 3. It uses the existing `food_surplus_db` schema and includes a dashboard, record search, CRUD screens, form validation, and the `deliverysummary` view.

## Tech stack

- **Backend:** Python with Flask
- **Database:** MySQL, using the InnoDB storage engine
- **Database driver:** `mysql-connector-python`
- **Frontend:** HTML, CSS, and Jinja templates rendered by Flask
- **Configuration:** Environment variables loaded from `.env` with `python-dotenv`

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
```

Create a file named `.env` in the project folder and add your local MySQL connection settings:

```dotenv
FLASK_SECRET_KEY=replace-with-a-random-secret
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-local-mysql-password
DB_NAME=food_surplus_db
```

Replace the example values with your own settings. Keep `.env` private: it is excluded by `.gitignore` and must not be pushed to GitHub. The app defaults to `127.0.0.1` (your own computer) and is intended for local use.

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Keep the terminal window open while using the application; press `Control+C` to stop the server.

## Database backup and restore

The supplied `database/food_surplus_backup.sql` is a backup of the schema and sample records. **Do not import it over your current database unless you intentionally want to replace that database.** The dump contains `DROP TABLE` statements. To restore it as a separate copy, first create a separate database and edit the dump's `USE`/database context if required, or use a dedicated test MySQL instance. For Review 3, the preferred approach is to connect to your already existing `food_surplus_db`.

The form relies on MySQL to generate record IDs. If your existing database gives a “Field '…ID' doesn't have a default value” error when adding a record, run the entire `database/enable_auto_increment.sql` script in MySQL Workbench with `food_surplus_db` selected. It temporarily removes and restores the related foreign keys while updating the six primary-key columns; it does not delete existing records. Newly created databases from `database/food_surplus_db.sql` already have auto-incrementing IDs.

## GitHub setup

You can push the project source code to GitHub even though the app and MySQL database run only on your computer. GitHub stores the files; it does not run this Flask app or host your local MySQL database. Other people who clone the project need to install the requirements, configure their own `.env`, and create or restore their own database.

Before pushing, review the files you plan to share. Never commit `.env`, passwords, API keys, or real/private records. The SQL files can contain sample data and schema details, so inspect them before making the repository public. `.env` is already listed in `.gitignore`; do not force-add it.

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
