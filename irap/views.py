from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from django.contrib import messages
from .models import Control, Evidence, EvidenceUsage, EvidenceLink, BoundaryAssociation
from .forms import (
    LinkExistingEvidenceForm,
    CreateEvidenceAndLinkForm,
    AddBoundaryToEvidenceForm,
    EvidenceEditForm,
)
from django.db.models import Count


def control_list(request):
    controls = Control.objects.select_related("control_set").all().order_by("control_id")
    return render(request, "irap/control_list.html", {"controls": controls})


def control_detail(request, pk):
    control = get_object_or_404(
        Control.objects.select_related("control_set").prefetch_related(
            "evidence_usages__evidence__links",
            "evidence_usages__evidence__boundary_associations__boundary",
            "assessments",
        ),
        pk=pk,
    )

    latest_assessment = control.assessments.order_by("-assessment_date", "-id").first()

    link_form = LinkExistingEvidenceForm()
    create_form = CreateEvidenceAndLinkForm()

    context = {
        "control": control,
        "latest_assessment": latest_assessment,
        "link_form": link_form,
        "create_form": create_form,
    }
    return render(request, "irap/control_detail.html", context)


def link_evidence_to_control(request, control_id):
    control = get_object_or_404(Control, pk=control_id)

    if request.method == "POST":
        form = LinkExistingEvidenceForm(request.POST)
        if form.is_valid():
            evidence = form.cleaned_data["evidence"]
            notes = form.cleaned_data["notes"]

            try:
                EvidenceUsage.objects.create(
                    control=control,
                    evidence=evidence,
                    notes=notes,
                )
                messages.success(request, "Existing evidence linked successfully.")
            except IntegrityError:
                messages.warning(request, "This evidence is already linked to the control.")

    return redirect("irap:control_detail", pk=control.pk)


def create_and_link_evidence(request, control_id):
    control = get_object_or_404(Control, pk=control_id)

    if request.method == "POST":
        form = CreateEvidenceAndLinkForm(request.POST)
        if form.is_valid():
            evidence = form.save()

            EvidenceUsage.objects.create(
                control=control,
                evidence=evidence,
                notes=form.cleaned_data["usage_notes"],
            )

            if form.cleaned_data["url_or_reference"]:
                EvidenceLink.objects.create(
                    evidence=evidence,
                    url_or_reference=form.cleaned_data["url_or_reference"],
                    description=form.cleaned_data["link_description"],
                )

            messages.success(request, "Evidence created and linked successfully.")

    return redirect("irap:control_detail", pk=control.pk)


def evidence_list(request):
    evidence_items = Evidence.objects.all().order_by("name")
    return render(request, "irap/evidence_list.html", {"evidence_items": evidence_items})


def evidence_detail(request, pk):
    evidence = get_object_or_404(
        Evidence.objects.prefetch_related(
            "links",
            "evidence_usages__control__control_set",
            "boundary_associations__boundary",
            "history_entries",
        ),
        pk=pk,
    )

    boundary_form = AddBoundaryToEvidenceForm()

    reuse_count = evidence.evidence_usages.count()
    history_entries = evidence.history_entries.all()
    selected_history = None
    history_id = request.GET.get("history")
    if history_id:
        selected_history = history_entries.filter(pk=history_id).first()

    context = {
        "evidence": evidence,
        "reuse_count": reuse_count,
        "boundary_form": boundary_form,
        "history_entries": history_entries,
        "selected_history": selected_history,
    }
    return render(request, "irap/evidence_detail.html", context)


def evidence_edit(request, pk):
    evidence = get_object_or_404(Evidence, pk=pk)

    if request.method == "POST":
        form = EvidenceEditForm(request.POST, instance=evidence)
        if form.is_valid():
            evidence_obj = form.save(commit=False)
            evidence_obj._change_note = form.cleaned_data.get("change_note", "")
            evidence_obj.save()
            messages.success(request, "Evidence updated with version history.")
            return redirect("irap:evidence_detail", pk=evidence.pk)
    else:
        form = EvidenceEditForm(instance=evidence)

    return render(request, "irap/evidence_edit.html", {"form": form, "evidence": evidence})


def add_boundary_to_evidence(request, evidence_id):
    evidence = get_object_or_404(Evidence, pk=evidence_id)

    if request.method == "POST":
        form = AddBoundaryToEvidenceForm(request.POST)
        if form.is_valid():
            boundary = form.cleaned_data["boundary"]
            notes = form.cleaned_data["notes"]

            BoundaryAssociation.objects.get_or_create(
                evidence=evidence,
                boundary=boundary,
                defaults={"notes": notes}
            )

    return redirect("irap:evidence_detail", pk=evidence.pk)


def traceability_report(request):
    evidence_items = (
        Evidence.objects.annotate(
            reuse_count=Count("evidence_usages", distinct=True),
            link_count=Count("links", distinct=True),
            boundary_count=Count("boundary_associations", distinct=True),
        )
        .order_by("-reuse_count", "name")
    )

    return render(request, "irap/traceability_report.html", {
        "evidence_items": evidence_items
    })
