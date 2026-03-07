from django.contrib import admin
from .models import (
    ControlSet, Control, ControlAssessment,
    Evidence, EvidenceLink, EvidenceUsage,
    Boundary, BoundaryAssociation
)

@admin.register(ControlSet)
class ControlSetAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "updated_at")
    search_fields = ("name", "version")

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ("control_id", "name", "control_set", "version", "updated_at")
    search_fields = ("control_id", "name")
    list_filter = ("control_set",)

@admin.register(ControlAssessment)
class ControlAssessmentAdmin(admin.ModelAdmin):
    list_display = ("control", "status", "assessment_date", "updated_at")
    list_filter = ("status", "assessment_date")
    search_fields = ("control__control_id", "control__name")

class EvidenceLinkInline(admin.TabularInline):
    model = EvidenceLink
    extra = 0

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("type",)
    inlines = [EvidenceLinkInline]

@admin.register(EvidenceUsage)
class EvidenceUsageAdmin(admin.ModelAdmin):
    list_display = ("control", "evidence", "updated_at")
    search_fields = ("control__control_id", "evidence__name")

@admin.register(Boundary)
class BoundaryAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    search_fields = ("name",)

@admin.register(BoundaryAssociation)
class BoundaryAssociationAdmin(admin.ModelAdmin):
    list_display = ("evidence", "boundary", "updated_at")
    search_fields = ("evidence__name", "boundary__name")
    list_filter = ("boundary",)
