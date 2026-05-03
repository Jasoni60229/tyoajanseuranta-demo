"""
Työajanseurantaohjelmiston demo

Tämä on yksinkertainen Flask-sovellus ammattikorkeakoulun projektia varten.
Sovelluksessa on kaksi testiroolia: toimitusjohtaja ja työntekijä.
Tietoja säilytetään muistissa ohjelman ajon aikana, joten erillistä tietokantaa
tai integraatioita ei tarvita demoa varten.
"""

from datetime import date, datetime, time, timedelta
from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)
app.secret_key = "demo-salainen-avain"

# Testityöntekijät. Projektin rajauksen mukaisesti uusia työntekijöitä ei voi lisätä.
EMPLOYEES = [
    {"id": 1, "name": "Anna Aaltonen"},
    {"id": 2, "name": "Matti Meikäläinen"},
    {"id": 3, "name": "Liisa Laine"},
    {"id": 4, "name": "Pekka Puro"},
    {"id": 5, "name": "Sara Salonen"},
]

# Työaikakirjaukset ovat testidataa.
# status: avoin, odottaa, hyväksytty
ENTRIES = [
    {"id": 1, "employee_id": 1, "work_date": "2026-04-27", "start": "08:00", "end": "16:00", "status": "odottaa"},
    {"id": 2, "employee_id": 1, "work_date": "2026-04-28", "start": "08:05", "end": "16:10", "status": "hyväksytty"},
    {"id": 3, "employee_id": 2, "work_date": "2026-04-27", "start": "09:00", "end": "17:00", "status": "odottaa"},
    {"id": 4, "employee_id": 3, "work_date": "2026-04-27", "start": "08:15", "end": "15:45", "status": "odottaa"},
    {"id": 5, "employee_id": 4, "work_date": "2026-04-28", "start": "08:00", "end": "16:00", "status": "hyväksytty"},
]


def get_employee(employee_id):
    """Palauttaa työntekijän id:n perusteella."""
    return next((employee for employee in EMPLOYEES if employee["id"] == employee_id), None)


def get_entry(entry_id):
    """Palauttaa työaikakirjauksen id:n perusteella."""
    return next((entry for entry in ENTRIES if entry["id"] == entry_id), None)


def next_entry_id():
    """Muodostaa seuraavan vapaan työaikakirjauksen id:n."""
    if not ENTRIES:
        return 1
    return max(entry["id"] for entry in ENTRIES) + 1


def current_user():
    """Palauttaa kirjautuneen käyttäjän tiedot session perusteella."""
    role = session.get("role")
    employee_id = session.get("employee_id")
    employee = get_employee(employee_id) if employee_id else None
    return {"role": role, "employee": employee}


def require_role(role):
    """Tarkistaa, että käyttäjällä on oikea rooli."""
    if session.get("role") != role:
        flash("Sinulla ei ole oikeutta avata tätä näkymää.", "error")
        return False
    return True


def calculate_hours(start_value, end_value):
    """Laskee työajan tunteina alkamis- ja päättymisajan perusteella."""
    if not start_value or not end_value:
        return "-"
    start_time = datetime.strptime(start_value, "%H:%M")
    end_time = datetime.strptime(end_value, "%H:%M")
    difference = end_time - start_time
    hours = difference.total_seconds() / 3600
    return f"{hours:.2f} h"


def employee_name(employee_id):
    employee = get_employee(employee_id)
    return employee["name"] if employee else "Tuntematon"


def find_open_entry(employee_id):
    """Etsii työntekijän avoimen työajanseurannan."""
    return next(
        (
            entry
            for entry in ENTRIES
            if entry["employee_id"] == employee_id and entry["status"] == "avoin"
        ),
        None,
    )


def missing_day_exceptions():
    """
    Muodostaa poikkeamalistan kirjaamattomista arkipäivistä.
    Demossa tarkastetaan viimeiset viisi arkipäivää.
    """
    exceptions = []
    today = date.today()
    checked_days = []
    day = today - timedelta(days=1)

    while len(checked_days) < 5:
        if day.weekday() < 5:
            checked_days.append(day.isoformat())
        day -= timedelta(days=1)

    for employee in EMPLOYEES:
        employee_dates = {
            entry["work_date"] for entry in ENTRIES if entry["employee_id"] == employee["id"]
        }
        for checked_day in checked_days:
            if checked_day not in employee_dates:
                exceptions.append({"employee": employee["name"], "date": checked_day, "reason": "Työaikakirjaus puuttuu"})

    return exceptions


@app.context_processor
def inject_helpers():
    """Mahdollistaa apufunktioiden käytön HTML-pohjissa."""
    return dict(
        current_user=current_user,
        employee_name=employee_name,
        calculate_hours=calculate_hours,
    )


@app.route("/", methods=["GET", "POST"])
def login():
    """Kirjautumisnäkymä, jossa käyttäjä valitsee testiroolin."""
    if request.method == "POST":
        role = request.form.get("role")
        employee_id = request.form.get("employee_id", type=int)

        if role == "ceo":
            session.clear()
            session["role"] = "ceo"
            flash("Kirjauduit toimitusjohtajana.", "success")
            return redirect(url_for("ceo_employee_view"))

        if role == "employee" and get_employee(employee_id):
            session.clear()
            session["role"] = "employee"
            session["employee_id"] = employee_id
            flash("Kirjauduit työntekijänä.", "success")
            return redirect(url_for("employee_home"))

        flash("Valitse rooli ja tarvittaessa työntekijä.", "error")

    return render_template("login.html", employees=EMPLOYEES)


@app.route("/logout")
def logout():
    session.clear()
    flash("Kirjauduit ulos.", "success")
    return redirect(url_for("login"))


@app.route("/employee")
def employee_home():
    """Työntekijän etusivu: työajan aloitus ja lopetus."""
    if not require_role("employee"):
        return redirect(url_for("login"))

    employee_id = session["employee_id"]
    open_entry = find_open_entry(employee_id)
    return render_template("employee.html", open_entry=open_entry)


@app.route("/employee/start", methods=["POST"])
def start_work():
    """Aloittaa työntekijän työajanseurannan."""
    if not require_role("employee"):
        return redirect(url_for("login"))

    employee_id = session["employee_id"]
    if find_open_entry(employee_id):
        flash("Työajanseuranta on jo käynnissä.", "error")
        return redirect(url_for("employee_home"))

    now = datetime.now()
    ENTRIES.append(
        {
            "id": next_entry_id(),
            "employee_id": employee_id,
            "work_date": now.date().isoformat(),
            "start": now.strftime("%H:%M"),
            "end": "",
            "status": "avoin",
        }
    )
    flash("Työajanseuranta aloitettu.", "success")
    return redirect(url_for("employee_home"))


@app.route("/employee/stop", methods=["POST"])
def stop_work():
    """Lopettaa työntekijän avoimen työajanseurannan."""
    if not require_role("employee"):
        return redirect(url_for("login"))

    employee_id = session["employee_id"]
    open_entry = find_open_entry(employee_id)
    if not open_entry:
        flash("Avoinna olevaa työajanseurantaa ei löytynyt.", "error")
        return redirect(url_for("employee_home"))

    open_entry["end"] = datetime.now().strftime("%H:%M")
    open_entry["status"] = "odottaa"
    flash("Työajanseuranta lopetettu ja kirjaus siirretty hyväksyttäväksi.", "success")
    return redirect(url_for("employee_home"))


@app.route("/employee/entries")
def employee_entries():
    """Työntekijän aikaisemmat työaikakirjaukset."""
    if not require_role("employee"):
        return redirect(url_for("login"))

    employee_id = session["employee_id"]
    entries = [entry for entry in ENTRIES if entry["employee_id"] == employee_id]
    entries.sort(key=lambda item: item["work_date"], reverse=True)
    return render_template("employee_entries.html", entries=entries)


@app.route("/ceo")
def ceo_employee_view():
    """Toimitusjohtajan työntekijäkohtainen tarkastelu."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    selected_employee_id = request.args.get("employee_id", default=EMPLOYEES[0]["id"], type=int)
    selected_entries = [entry for entry in ENTRIES if entry["employee_id"] == selected_employee_id]
    selected_entries.sort(key=lambda item: item["work_date"], reverse=True)

    return render_template(
        "ceo_employees.html",
        employees=EMPLOYEES,
        selected_employee_id=selected_employee_id,
        entries=selected_entries,
    )


@app.route("/ceo/edit/<int:entry_id>", methods=["GET", "POST"])
def ceo_edit_entry(entry_id):
    """Toimitusjohtaja voi muokata työaikakirjausta."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    entry = get_entry(entry_id)
    if not entry:
        flash("Työaikakirjausta ei löytynyt.", "error")
        return redirect(url_for("ceo_employee_view"))

    if request.method == "POST":
        work_date = request.form.get("work_date")
        start = request.form.get("start")
        end = request.form.get("end")

        if not work_date or not start or not end:
            flash("Täytä päivämäärä, aloitusaika ja lopetusaika.", "error")
            return render_template("edit_entry.html", entry=entry)

        entry["work_date"] = work_date
        entry["start"] = start
        entry["end"] = end
        if entry["status"] == "avoin":
            entry["status"] = "odottaa"
        flash("Työaikakirjaus tallennettu.", "success")
        return redirect(url_for("ceo_employee_view", employee_id=entry["employee_id"]))

    return render_template("edit_entry.html", entry=entry)


@app.route("/ceo/exceptions")
def ceo_exceptions():
    """Toimitusjohtajan poikkeamien tarkastelu."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    exceptions = missing_day_exceptions()
    return render_template("ceo_exceptions.html", exceptions=exceptions)


@app.route("/ceo/approvals")
def ceo_approvals():
    """Toimitusjohtajan työaikojen hyväksymisnäkymä."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    pending_entries = [entry for entry in ENTRIES if entry["status"] == "odottaa"]
    pending_entries.sort(key=lambda item: item["work_date"], reverse=True)
    return render_template("ceo_approvals.html", entries=pending_entries)


@app.route("/ceo/approve/<int:entry_id>", methods=["POST"])
def approve_entry(entry_id):
    """Hyväksyy yksittäisen työaikakirjauksen."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    entry = get_entry(entry_id)
    if not entry:
        flash("Hyväksyttävää kirjausta ei löytynyt.", "error")
    else:
        entry["status"] = "hyväksytty"
        flash("Työaikakirjaus hyväksytty.", "success")
    return redirect(url_for("ceo_approvals"))


@app.route("/ceo/approve-all", methods=["POST"])
def approve_all_entries():
    """Hyväksyy kaikki odottavat työaikakirjaukset."""
    if not require_role("ceo"):
        return redirect(url_for("login"))

    count = 0
    for entry in ENTRIES:
        if entry["status"] == "odottaa":
            entry["status"] = "hyväksytty"
            count += 1

    flash(f"Hyväksyttiin {count} työaikakirjausta.", "success")
    return redirect(url_for("ceo_approvals"))


if __name__ == "__main__":
    app.run(debug=True)
