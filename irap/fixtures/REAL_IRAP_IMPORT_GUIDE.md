# Import real IRAP Excel workbook

This project now includes a management command to import an IRAP workbook directly:

`python manage.py import_irap_xlsx --xlsx "/absolute/path/to/workbook.xlsx"`

## 1) Install dependency (once per venv)

```bash
pip install openpyxl
```

## 2) Expected sheet names

The importer looks for these sheets (case-insensitive):

- Required:
  - `Controls`
  - `Evidence`
- Optional:
  - `EvidenceUsage`
  - `EvidenceLinks`
  - `Boundaries`
  - `BoundaryAssociations`
  - `Assessments`

## 3) Expected columns (aliases supported)

### Controls (required)

- `control_id` (aliases: `controlid`, `ismid`, `id`)
- `name` (aliases: `controlname`, `title`)
- `description` (optional)
- `version` (optional)

### Evidence (required)

- `name` (aliases: `evidencename`, `artifact`)
- `type` (optional)
- `description` (optional)

### EvidenceUsage (optional)

- `control_id` (aliases: `controlid`, `ismid`, `control`)
- `evidence_name` (aliases: `evidencename`, `evidence`, `artifact`)
- `notes` (optional; aliases: `usagenotes`, `rationale`)

### EvidenceLinks (optional)

- `evidence_name` (aliases: `evidencename`, `evidence`, `artifact`)
- `url_or_reference` (aliases: `reference`, `url`)
- `description` (optional)

### Boundaries (optional)

- `name` (aliases: `boundaryname`)
- `description` (optional)

### BoundaryAssociations (optional)

- `evidence_name` (aliases: `evidencename`, `evidence`, `artifact`)
- `boundary_name` (aliases: `boundaryname`, `boundary`)
- `notes` (optional)

### Assessments (optional)

- `control_id` (aliases: `controlid`, `ismid`, `control`)
- `status` (mapped to `pass/partial/fail/not_assessed/n_a`)
- `notes` (optional)
- `assessment_date` (optional; if missing, today is used)

## 4) Example command for your workbook

```bash
python manage.py import_irap_xlsx \
  --xlsx "/Users/tuoliu/Desktop/System security plan annex template (September 2025).xlsx" \
  --control-set-name "ISM Real Dataset" \
  --control-set-version "September 2025" \
  --control-set-description "Imported from real IRAP SSP annex workbook."
```

Use `--dry-run` first to validate parsing without writing:

```bash
python manage.py import_irap_xlsx \
  --xlsx "/Users/tuoliu/Desktop/System security plan annex template (September 2025).xlsx" \
  --dry-run
```

## 5) Export imported data as fixture (for repeatable demos)

```bash
python manage.py dumpdata irap --indent 2 > irap/fixtures/real_irap_fixture.json
```

Then load later with:

```bash
python manage.py loaddata irap/fixtures/real_irap_fixture.json
```
