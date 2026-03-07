# compliance/management/commands/export_control_report.py
import csv
from django.core.management.base import BaseCommand
from django.db.models import OuterRef, Subquery
from irap.models import Control, ControlAssessment, EvidenceUsage, EvidenceLink

class Command(BaseCommand):
    help = "Export control-centric report (CSV)"

    def add_arguments(self, parser):
        parser.add_argument("--path", default="control_report.csv")

    def handle(self, *args, **options):
        path = options["path"]

        latest_assessment = ControlAssessment.objects.filter(
            control_id=OuterRef("pk")
        ).order_by("-assessment_date", "-created_at")

        qs = Control.objects.all().annotate(
            latest_status=Subquery(latest_assessment.values("status")[:1]),
            latest_date=Subquery(latest_assessment.values("assessment_date")[:1]),
            latest_notes=Subquery(latest_assessment.values("notes")[:1]),
        ).select_related("control_set")

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "control_set", "control_id", "control_name", "control_version",
                "latest_status", "latest_assessment_date", "latest_assessment_notes",
                "evidence_name", "evidence_type", "evidence_usage_notes",
                "evidence_link"
            ])

            for c in qs:
                usages = EvidenceUsage.objects.filter(control=c).select_related("evidence")
                if not usages.exists():
                    w.writerow([str(c.control_set), c.control_id, c.name, c.version,
                                c.latest_status, c.latest_date, c.latest_notes,
                                "", "", "", ""])
                    continue

                for u in usages:
                    link = EvidenceLink.objects.filter(evidence=u.evidence).values_list("url_or_reference", flat=True).first() or ""
                    w.writerow([
                        str(c.control_set), c.control_id, c.name, c.version,
                        c.latest_status, c.latest_date, c.latest_notes,
                        u.evidence.name, u.evidence.type, u.notes,
                        link
                    ])

        self.stdout.write(self.style.SUCCESS(f"Exported: {path}"))
