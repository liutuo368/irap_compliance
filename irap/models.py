from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class ControlSet(TimeStampedModel):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("name", "version")
        ordering = ["name", "version"]

    def __str__(self):
        return f"{self.name} {self.version}".strip()


class Control(TimeStampedModel):
    control_set = models.ForeignKey(ControlSet, on_delete=models.CASCADE, related_name="controls")
    control_id = models.CharField(max_length=128)  # e.g., "AC-2" or ISM identifier
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = ("control_set", "control_id", "version")
        indexes = [
            models.Index(fields=["control_id"]),
            models.Index(fields=["name"]),
        ]
        ordering = ["control_set__name", "control_id"]

    def __str__(self):
        return f"{self.control_id} - {self.name}"


class ControlAssessment(TimeStampedModel):
    class Status(models.TextChoices):
        NOT_ASSESSED = "not_assessed", "Not assessed"
        PASS_ = "pass", "Pass"
        PARTIAL = "partial", "Partial"
        FAIL = "fail", "Fail"
        N_A = "n_a", "Not applicable"

    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name="assessments")
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NOT_ASSESSED)
    notes = models.TextField(blank=True)
    assessment_date = models.DateField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["control", "-assessment_date"]),
            models.Index(fields=["status"]),
        ]
        ordering = ["-assessment_date", "-created_at"]

    def __str__(self):
        return f"{self.control.control_id} @ {self.assessment_date} = {self.status}"


class Evidence(TimeStampedModel):
    class EvidenceType(models.TextChoices):
        POLICY = "policy", "Policy"
        PROCEDURE = "procedure", "Procedure"
        DIAGRAM = "diagram", "Architecture diagram"
        TICKET = "ticket", "Change ticket"
        LOG = "log", "Log / monitoring"
        ATTESTATION = "attestation", "Interview / attestation"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64, choices=EvidenceType.choices, default=EvidenceType.OTHER)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=16, default="v1.0")

    # M2M to Control via EvidenceUsage
    controls = models.ManyToManyField(Control, through="EvidenceUsage", related_name="evidence_items")

    class Meta:
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["name"]),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name

    @staticmethod
    def _increment_version(version_value):
        """
        Simple versioning for prototype: v1.0 -> v1.1 -> v1.2.
        """
        if not version_value or not version_value.startswith("v"):
            return "v1.0"
        try:
            major, minor = version_value[1:].split(".", 1)
            return f"v{int(major)}.{int(minor) + 1}"
        except (ValueError, TypeError):
            return "v1.0"

    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        previous = None
        if is_update:
            previous = Evidence.objects.filter(pk=self.pk).first()

        if not self.version:
            self.version = "v1.0"

        should_track_change = (
            previous is not None
            and (
                previous.name != self.name
                or previous.type != self.type
                or previous.description != self.description
            )
        )

        if should_track_change:
            old_version = previous.version or "v1.0"
            change_note = getattr(self, "_change_note", "") or "Updated evidence details"

            EvidenceHistory.objects.create(
                evidence=previous,
                version=old_version,
                description=previous.description,
                snapshot={
                    "name": previous.name,
                    "type": previous.type,
                    "description": previous.description,
                    "version": old_version,
                },
                change_note=change_note,
            )
            self.version = self._increment_version(old_version)

        super().save(*args, **kwargs)


class EvidenceHistory(models.Model):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name="history_entries")
    version = models.CharField(max_length=16)
    description = models.TextField(blank=True)
    snapshot = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    change_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["evidence", "-created_at"]),
            models.Index(fields=["version"]),
        ]

    def __str__(self):
        return f"EvidenceHistory({self.evidence_id}, {self.version})"


class EvidenceLink(TimeStampedModel):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name="links")
    url_or_reference = models.TextField()  # URL, file path, confluence page id, etc.
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Link({self.evidence_id})"


class EvidenceUsage(TimeStampedModel):
    """
    Join table: Control <-> Evidence, with relationship-level notes
    """
    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name="evidence_usages")
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name="evidence_usages")
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("control", "evidence")
        indexes = [
            models.Index(fields=["control", "evidence"]),
        ]

    def __str__(self):
        return f"{self.control.control_id} <= {self.evidence.name}"


class Boundary(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("name",)
        ordering = ["name"]

    def __str__(self):
        return self.name


class BoundaryAssociation(TimeStampedModel):
    """
    Join table: Evidence <-> Boundary, with relationship-level notes.
    Evidence can be scoped to boundaries (optional).
    """
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name="boundary_associations")
    boundary = models.ForeignKey(Boundary, on_delete=models.CASCADE, related_name="evidence_associations")
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("evidence", "boundary")
        indexes = [
            models.Index(fields=["boundary"]),
            models.Index(fields=["evidence", "boundary"]),
        ]

    def __str__(self):
        return f"{self.evidence.name} @ {self.boundary.name}"
