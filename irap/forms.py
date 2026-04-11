from django import forms
from .models import Control, ControlSet, Evidence, EvidenceUsage, Boundary, BoundaryAssociation, EvidenceLink

class LinkExistingEvidenceForm(forms.Form):
    evidence = forms.ModelChoiceField(
        queryset=Evidence.objects.all().order_by("name"),
        empty_label="Select existing evidence"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )


class CreateEvidenceAndLinkForm(forms.ModelForm):
    usage_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Why this evidence supports the control"
    )
    url_or_reference = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Evidence link / reference"
    )
    link_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Link description"
    )

    class Meta:
        model = Evidence
        fields = ["name", "type", "description"]


class AddBoundaryToEvidenceForm(forms.Form):
    boundary = forms.ModelChoiceField(
        queryset=Boundary.objects.all().order_by("name")
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2})
    )


class EvidenceEditForm(forms.ModelForm):
    change_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Change note",
        help_text="Describe what changed in this update."
    )
    url_or_reference = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Evidence link / reference"
    )
    link_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Link description"
    )

    class Meta:
        model = Evidence
        fields = ["name", "type", "description"]


class ControlCreateForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = ["control_set", "control_id", "name", "description", "version"]

    control_set = forms.ModelChoiceField(
        queryset=ControlSet.objects.all().order_by("name", "version"),
        empty_label=None
    )


class BoundaryCreateForm(forms.ModelForm):
    class Meta:
        model = Boundary
        fields = ["name", "description"]