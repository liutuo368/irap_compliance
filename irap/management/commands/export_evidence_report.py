import csv
from django.core.management.base import BaseCommand
from irap.models import Evidence, EvidenceUsage

class Command(BaseCommand):
    help = "Export evidence-centric report (CSV)"

    def add_arguments(self, parser):
        parser.add_argument("--path", default="evidence_report.csv")

    def handle(self, *args, **options):
        path = options["path"]

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["evidence_name", "evidence_type", "controls_supported_count", "controls_supported"])

            for e in Evidence.objects.all():
                controls = EvidenceUsage.objects.filter(evidence=e).select_related("control")
                control_ids = [u.control.control_id for u in controls]
                w.writerow([e.name, e.type, len(control_ids), ",".join(control_ids)])

        self.stdout.write(self.style.SUCCESS(f"Exported: {path}"))
