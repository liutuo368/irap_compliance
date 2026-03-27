from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("irap", "0002_alter_boundary_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="evidence",
            name="version",
            field=models.CharField(default="v1.0", max_length=16),
        ),
        migrations.CreateModel(
            name="EvidenceHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("version", models.CharField(max_length=16)),
                ("description", models.TextField(blank=True)),
                ("snapshot", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("change_note", models.TextField(blank=True)),
                ("evidence", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="history_entries", to="irap.evidence")),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.AddIndex(
            model_name="evidencehistory",
            index=models.Index(fields=["evidence", "-created_at"], name="irap_eviden_evidenc_0d1178_idx"),
        ),
        migrations.AddIndex(
            model_name="evidencehistory",
            index=models.Index(fields=["version"], name="irap_eviden_version_895f93_idx"),
        ),
    ]
