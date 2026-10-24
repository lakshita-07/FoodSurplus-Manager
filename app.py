import os
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import mysql.connector
from mysql.connector import Error
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.context_processor
def inject_tables():
    return {"tables": TABLES}

app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-review3-change-this-key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "food_surplus_db"),
}

# Metadata matches the supplied food_surplus_db.sql backup.
TABLES = {
    "DONOR": {
        "label": "Donors", "pk": "DonorID", "title": "DonorName",
        "columns": ["DonorID", "DonorName", "DonorType", "Phone", "Email", "City", "Status"],
        "fields": ["DonorName", "DonorType", "Phone", "Email", "Address", "City", "Pincode", "RegDate", "Status"],
        "types": {"DonorName":"text", "DonorType":"text", "Phone":"text", "Email":"email", "Address":"text", "City":"text", "Pincode":"text", "RegDate":"date", "Status":"text"},
        "required": ["DonorName"], "search": ["DonorName", "DonorType", "Phone", "Email", "City", "Status"],
    },
    "FOOD_CATEGORY": {
        "label": "Food categories", "pk": "CategoryID", "title": "CategoryName",
        "columns": ["CategoryID", "CategoryName", "StorageRequirement", "ShelfLifeHours"],
        "fields": ["CategoryName", "StorageRequirement", "ShelfLifeHours"],
        "types": {"CategoryName":"text", "StorageRequirement":"text", "ShelfLifeHours":"int"},
        "required": ["CategoryName", "ShelfLifeHours"], "search": ["CategoryName", "StorageRequirement"],
    },
    "DONATION": {
        "label": "Donations", "pk": "DonationID", "title": "FoodName",
        "columns": ["DonationID", "FoodName", "DonorID", "CategoryID", "Quantity", "Unit", "ExpiryDateTime", "Status"],
        "fields": ["DonorID", "CategoryID", "FoodName", "Quantity", "Unit", "ListingDateTime", "ExpiryDateTime", "PrepDateTime", "PickupAddress", "Status"],
        "types": {"DonorID":"fk_donor", "CategoryID":"fk_category", "FoodName":"text", "Quantity":"decimal", "Unit":"text", "ListingDateTime":"datetime", "ExpiryDateTime":"datetime", "PrepDateTime":"datetime", "PickupAddress":"text", "Status":"text"},
        "required": ["DonorID", "CategoryID", "FoodName"], "search": ["FoodName", "Unit", "PickupAddress", "Status"],
    },
    "RECIPIENT": {
        "label": "Recipients", "pk": "RecipientID", "title": "RecipientName",
        "columns": ["RecipientID", "RecipientName", "RecipientType", "Phone", "City", "CapacityKg", "Status"],
        "fields": ["RecipientName", "RecipientType", "Phone", "Email", "Address", "City", "CapacityKg", "ContactPerson", "RegDate", "Status"],
        "types": {"RecipientName":"text", "RecipientType":"text", "Phone":"text", "Email":"email", "Address":"text", "City":"text", "CapacityKg":"decimal", "ContactPerson":"text", "RegDate":"date", "Status":"text"},
        "required": ["RecipientName"], "search": ["RecipientName", "RecipientType", "Phone", "Email", "City", "Status"],
    },
    "VOLUNTEER": {
        "label": "Volunteers", "pk": "VolunteerID", "title": "VolunteerName",
        "columns": ["VolunteerID", "VolunteerName", "Phone", "OperatingZone", "AvailabilityStatus", "VehicleType", "VehicleCapacityKg"],
        "fields": ["VolunteerName", "Phone", "Email", "OperatingZone", "AvailabilityStatus", "VehicleType", "VehicleCapacityKg"],
        "types": {"VolunteerName":"text", "Phone":"text", "Email":"email", "OperatingZone":"text", "AvailabilityStatus":"text", "VehicleType":"text", "VehicleCapacityKg":"decimal"},
        "required": ["VolunteerName"], "search": ["VolunteerName", "Phone", "Email", "OperatingZone", "AvailabilityStatus", "VehicleType"],
    },
    "REDISTRIBUTION": {
        "label": "Redistributions", "pk": "RedistribID", "title": "RedistribID",
        "columns": ["RedistribID", "DonationID", "RecipientID", "VolunteerID", "QuantityAllocated", "MatchDateTime", "DeliveryStatus", "FeedbackRating"],
        "fields": ["DonationID", "RecipientID", "VolunteerID", "QuantityAllocated", "MatchDateTime", "DispatchDateTime", "DeliveryDateTime", "DeliveryStatus", "FeedbackRating", "FeedbackComments"],
        "types": {"DonationID":"fk_donation", "RecipientID":"fk_recipient", "VolunteerID":"fk_volunteer", "QuantityAllocated":"decimal", "MatchDateTime":"datetime", "DispatchDateTime":"datetime", "DeliveryDateTime":"datetime", "DeliveryStatus":"text", "FeedbackRating":"int", "FeedbackComments":"text"},
        "required": ["DonationID", "RecipientID", "QuantityAllocated"], "search": ["DeliveryStatus", "FeedbackComments"],
    },
}

FK_OPTIONS = {
    "fk_donor": ("DONOR", "DonorID", "DonorName"),
    "fk_category": ("FOOD_CATEGORY", "CategoryID", "CategoryName"),
    "fk_donation": ("DONATION", "DonationID", "FoodName"),
    "fk_recipient": ("RECIPIENT", "RecipientID", "RecipientName"),
    "fk_volunteer": ("VOLUNTEER", "VolunteerID", "VolunteerName"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def field_options(field_type):
    if field_type not in FK_OPTIONS:
        return []
    table, key, label = FK_OPTIONS[field_type]
    return fetch_all(f"SELECT `{key}` AS id, `{label}` AS label FROM `{table}` ORDER BY `{label}`")


def get_form_fields(table_name, row=None):
    meta = TABLES[table_name]
    output = []
    for name in meta["fields"]:
        field_type = meta["types"].get(name, "text")
        value = (row or {}).get(name, "")
        if isinstance(value, (datetime, date)):
            value = value.strftime("%Y-%m-%dT%H:%M" if field_type == "datetime" else "%Y-%m-%d")
        elif value is None:
            value = ""
        output.append({"name": name, "type": field_type, "value": value,
                       "required": name in meta.get("required", []),
                       "options": field_options(field_type) if field_type in FK_OPTIONS else []})
    return output


def parse_value(field, raw):
    if raw == "":
        return None
    field_type = field["type"]
    if field_type in ("fk_donor", "fk_category", "fk_donation", "fk_recipient", "fk_volunteer", "int"):
        return int(raw)
    if field_type == "decimal":
        value = Decimal(raw)
        if not value.is_finite():
            raise ValueError(f"{field['name']} must be a valid number.")
        return value
    if field_type == "date":
        return date.fromisoformat(raw)
    if field_type == "datetime":
        return datetime.fromisoformat(raw)
    return raw.strip()


def validate_business_rules(table_name, values, current_pk=None):
    if table_name == "DONATION":
        qty = values.get("Quantity")
        if qty is not None and qty <= 0:
            raise ValueError("Donation quantity must be greater than zero.")
        listing, expiry = values.get("ListingDateTime"), values.get("ExpiryDateTime")
        if listing and expiry and expiry <= listing:
            raise ValueError("Expiry date/time must be later than listing date/time.")
    if table_name == "FOOD_CATEGORY" and values.get("ShelfLifeHours") is not None and values["ShelfLifeHours"] <= 0:
        raise ValueError("Shelf life must be greater than zero.")
    if table_name == "RECIPIENT" and values.get("CapacityKg") is not None and values["CapacityKg"] < 0:
        raise ValueError("Recipient capacity cannot be negative.")
    if table_name == "VOLUNTEER" and values.get("VehicleCapacityKg") is not None and values["VehicleCapacityKg"] < 0:
        raise ValueError("Vehicle capacity cannot be negative.")
    if table_name == "REDISTRIBUTION":
        qty = values.get("QuantityAllocated")
        if qty is not None and qty <= 0:
            raise ValueError("Allocated quantity must be greater than zero.")
        rating = values.get("FeedbackRating")
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError("Feedback rating must be between 1 and 5.")
        donation_id = values.get("DonationID")
        if donation_id is not None and qty is not None:
            params = [donation_id]
            sql = "SELECT Quantity FROM DONATION WHERE DonationID = %s"
            if current_pk is not None:
                sql += " AND DonationID = %s"
                params.append(donation_id)
            donation = fetch_one(sql, tuple(params))
            if donation is not None and donation["Quantity"] is not None:
                allocated_sql = "SELECT COALESCE(SUM(QuantityAllocated),0) AS total FROM REDISTRIBUTION WHERE DonationID = %s"
                allocated_params = [donation_id]
                if current_pk is not None:
                    allocated_sql += " AND RedistribID <> %s"
                    allocated_params.append(current_pk)
                already = fetch_one(allocated_sql, tuple(allocated_params))["total"] or Decimal("0")
                if already + qty > donation["Quantity"]:
                    remaining = donation["Quantity"] - already
                    raise ValueError(f"Allocation exceeds remaining donation quantity ({remaining} available).")


@app.route("/")
def index():
    counts = {}
    error = None
    try:
        for table_name, meta in TABLES.items():
            result = fetch_one(f"SELECT COUNT(*) AS total FROM `{table_name}`")
            counts[table_name] = result["total"]
        status_rows = fetch_all("SELECT DeliveryStatus, COUNT(*) AS total FROM REDISTRIBUTION GROUP BY DeliveryStatus ORDER BY DeliveryStatus")
        recent = fetch_all("SELECT RedistribID, FoodName, RecipientName, QuantityAllocated, DeliveryStatus FROM deliverysummary ORDER BY RedistribID DESC LIMIT 5")
    except Error as exc:
        error = str(exc)
        status_rows, recent = [], []
    return render_template("index.html", counts=counts, tables=TABLES, status_rows=status_rows, recent=recent, error=error)


@app.route("/table/<table_name>")
def table_view(table_name):
    if table_name not in TABLES:
        flash("Unknown table.", "error")
        return redirect(url_for("index"))
    meta = TABLES[table_name]
    search = request.args.get("q", "").strip()
    sql = f"SELECT * FROM `{table_name}`"
    params = []
    if search:
        clauses = [f"CAST(`{column}` AS CHAR) LIKE %s" for column in meta.get("search", [])]
        if clauses:
            sql += " WHERE " + " OR ".join(clauses)
            params = [f"%{search}%"] * len(clauses)
    sql += f" ORDER BY `{meta['pk']}` DESC"
    try:
        rows = fetch_all(sql, tuple(params))
        error = None
    except Error as exc:
        rows, error = [], str(exc)
    return render_template("table.html", table_name=table_name, meta=meta, rows=rows, search=search, error=error)


@app.route("/view/<table_name>/<int:record_id>")
def view_record(table_name, record_id):
    if table_name not in TABLES:
        return redirect(url_for("index"))
    meta = TABLES[table_name]
    row = fetch_one(f"SELECT * FROM `{table_name}` WHERE `{meta['pk']}` = %s", (record_id,))
    if not row:
        flash("Record not found.", "error")
        return redirect(url_for("table_view", table_name=table_name))
    return render_template("record.html", table_name=table_name, meta=meta, row=row)


@app.route("/add/<table_name>", methods=["GET", "POST"])
def add_record(table_name):
    if table_name not in TABLES:
        return redirect(url_for("index"))
    meta = TABLES[table_name]
    if request.method == "POST":
        fields = get_form_fields(table_name)
        try:
            values = {f["name"]: parse_value(f, request.form.get(f["name"], "")) for f in fields}
            missing = [name for name in meta.get("required", []) if values.get(name) in (None, "")]
            if missing:
                raise ValueError("Required fields missing: " + ", ".join(missing))
            validate_business_rules(table_name, values)
            columns = list(values.keys())
            placeholders = ", ".join(["%s"] * len(columns))
            sql = f"INSERT INTO `{table_name}` ({', '.join(f'`{c}`' for c in columns)}) VALUES ({placeholders})"
            conn = get_connection()
            try:
                cur = conn.cursor()
                cur.execute(sql, tuple(values[c] for c in columns))
                conn.commit()
            finally:
                cur.close(); conn.close()
            flash(f"{meta['label']} record added successfully.", "success")
            return redirect(url_for("table_view", table_name=table_name))
        except (ValueError, InvalidOperation, Error) as exc:
            flash(f"Could not add record: {exc}", "error")
            return render_template("form.html", table_name=table_name, meta=meta, fields=get_form_fields(table_name, request.form), mode="Add")
    try:
        fields = get_form_fields(table_name)
    except Error as exc:
        flash(f"Could not load form options: {exc}", "error")
        fields = get_form_fields(table_name)
    return render_template("form.html", table_name=table_name, meta=meta, fields=fields, mode="Add")


@app.route("/edit/<table_name>/<int:record_id>", methods=["GET", "POST"])
def edit_record(table_name, record_id):
    if table_name not in TABLES:
        return redirect(url_for("index"))
    meta = TABLES[table_name]
    original = fetch_one(f"SELECT * FROM `{table_name}` WHERE `{meta['pk']}` = %s", (record_id,))
    if not original:
        flash("Record not found.", "error")
        return redirect(url_for("table_view", table_name=table_name))
    if request.method == "POST":
        fields = get_form_fields(table_name, original)
        try:
            values = {f["name"]: parse_value(f, request.form.get(f["name"], "")) for f in fields}
            missing = [name for name in meta.get("required", []) if values.get(name) in (None, "")]
            if missing:
                raise ValueError("Required fields missing: " + ", ".join(missing))
            validate_business_rules(table_name, values, current_pk=record_id)
            assignments = ", ".join(f"`{column}` = %s" for column in values)
            conn = get_connection()
            try:
                cur = conn.cursor()
                cur.execute(f"UPDATE `{table_name}` SET {assignments} WHERE `{meta['pk']}` = %s", tuple(values.values()) + (record_id,))
                conn.commit()
            finally:
                cur.close(); conn.close()
            flash("Record updated successfully.", "success")
            return redirect(url_for("table_view", table_name=table_name))
        except (ValueError, InvalidOperation, Error) as exc:
            flash(f"Could not update record: {exc}", "error")
            return render_template("form.html", table_name=table_name, meta=meta, fields=get_form_fields(table_name, request.form), mode="Edit", record_id=record_id)
    return render_template("form.html", table_name=table_name, meta=meta, fields=get_form_fields(table_name, original), mode="Edit", record_id=record_id)


@app.route("/delete/<table_name>/<int:record_id>", methods=["POST"])
def delete_record(table_name, record_id):
    if table_name not in TABLES:
        return redirect(url_for("index"))
    meta = TABLES[table_name]
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM `{table_name}` WHERE `{meta['pk']}` = %s", (record_id,))
        conn.commit()
        flash("Record deleted." if cur.rowcount else "Record not found.", "success")
    except Error as exc:
        if conn:
            conn.rollback()
        flash(f"Could not delete record. It may be referenced by another record. Details: {exc}", "error")
    finally:
        if conn:
            cur.close(); conn.close()
    return redirect(url_for("table_view", table_name=table_name))


@app.route("/delivery-summary")
def delivery_summary():
    try:
        rows = fetch_all("SELECT * FROM deliverysummary ORDER BY RedistribID")
        error = None
    except Error as exc:
        rows, error = [], str(exc)
    return render_template("summary.html", rows=rows, error=error)


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", message="The page you requested was not found."), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
