# IRAP Compliance Prototype (Django)

This project is a lightweight prototype for demonstrating core IRAP compliance workflows:

- control management
- evidence management
- control-evidence traceability
- basic evidence version tracking and change history

It is designed for coursework/demo use (simple architecture, clear UI, SQLite backend).

## 1. Project Scope

The system models the following entities:

- `ControlSet` and `Control`
- `Evidence`
- `EvidenceUsage` (Control <-> Evidence relationship)
- `EvidenceLink` (reference URL/path for evidence)
- `Boundary` and `BoundaryAssociation`
- `ControlAssessment`
- `EvidenceHistory` (version history snapshots)

## 2. Implemented Features

### Control

- Control list page
- Control detail page
- Manual create Control page
- Link existing evidence to a control
- Create new evidence and link it to a control in one step

### Evidence

- Evidence list page
- Evidence detail page
- Edit evidence page
- Edit evidence reference fields:
  - link/reference (`url_or_reference`)
  - link description

### Traceability

- Traceability report page (evidence-centric aggregation)
- Reuse counts and link/boundary aggregation for presentation

### Evidence Versioning (prototype-level)

- Current evidence version field (default `v1.0`)
- Automatic version increment on update (`v1.0 -> v1.1 -> v1.2 ...`)
- Automatic history snapshot on update (stores previous state)
- Change note support when editing evidence
- Version history displayed in evidence detail UI
- Read-only snapshot view for historical entries

## 3. Tech Stack

- Python
- Django
- SQLite
- Bootstrap 5 (via CDN)
- openpyxl (for Excel import command)

## 4. Local Setup

From project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django openpyxl
python manage.py migrate
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/controls/`

## 5. Data Input Options

### Option A: Manual UI

- Create controls from `Controls -> Create Control`
- Add/link evidence from each control detail page
- Edit evidence from evidence detail page

### Option B: Import from Excel workbook

```bash
python manage.py import_irap_xlsx --xlsx "C:\absolute\path\to\your_file.xlsx"
```

Useful optional arguments:

- `--control-set-name`
- `--control-set-version`
- `--control-set-description`
- `--dry-run`

## 6. Export Reports

### Control-centric CSV

```bash
python manage.py export_control_report --path "exports/control_report.csv"
```

### Evidence-centric CSV

```bash
python manage.py export_evidence_report --path "exports/evidence_report.csv"
```

## 7. Main Pages (Demo Flow)

For a short presentation demo:

1. `Controls` page: show control catalog and create-control entry point
2. Control detail: show linked evidence and create/link workflow
3. `Evidence` page: open one artifact and show:
   - current version
   - updated timestamp
   - version history list
   - snapshot view of historical versions
4. `Traceability` page: show evidence reuse/reporting view

## 8. Notes and Limitations

- This is a prototype, not a production-ready system.
- Authentication/authorization is intentionally minimal.
- Evidence link editing currently updates the first stored link for an evidence item (sufficient for demo workflow).
- SQLite is used for simplicity and portability.

## 9. Project Structure

```text
compliance/
├─ compliance/                 # Django project settings and root urls
├─ irap/                       # Domain app (models, views, forms, commands)
│  ├─ management/commands/     # import/export scripts
│  ├─ migrations/
│  ├─ models.py
│  ├─ views.py
│  └─ forms.py
├─ templates/irap/             # HTML templates
├─ static/irap/                # static assets
└─ manage.py
```

## 10. Quick Verification Checklist

After startup, verify:

- Controls list page loads
- New control can be created
- Evidence can be created and linked to a control
- Evidence can be edited with change note
- Version increments after evidence update
- Version history appears on evidence detail page
- Traceability report displays reuse metrics
