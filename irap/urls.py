from django.urls import path
from . import views

app_name = "irap"

urlpatterns = [
    path("controls/", views.control_list, name="control_list"),
    path("controls/<int:pk>/", views.control_detail, name="control_detail"),
    path("controls/<int:control_id>/link-evidence/", views.link_evidence_to_control, name="link_evidence"),
    path("controls/<int:control_id>/create-and-link-evidence/", views.create_and_link_evidence, name="create_and_link_evidence"),

    path("evidence/", views.evidence_list, name="evidence_list"),
    path("evidence/<int:pk>/", views.evidence_detail, name="evidence_detail"),
    path("evidence/<int:evidence_id>/add-boundary/", views.add_boundary_to_evidence, name="add_boundary_to_evidence"),
    path("reports/traceability/", views.traceability_report, name="traceability_report"),
]
