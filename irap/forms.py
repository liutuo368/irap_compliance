from django import forms
from .models import Evidence, Boundary

class LinkExistingEvidenceForm(forms.Form):
    evidence = forms.ModelChoiceField(
        queryset=Evidence.objects.all().order_by("name"),
        empty_label="Select existing evidence",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )


class CreateEvidenceAndLinkForm(forms.ModelForm):
    usage_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Why this evidence supports the control"
    )
    url_or_reference = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        label="Evidence link / reference"
    )
    link_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        label="Link description"
    )

    class Meta:
        model = Evidence
        fields = ["name", "type", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class EditEvidenceForm(forms.ModelForm):
    """
    Edit only the evidence artifact metadata.
    Relationship-level justifications (EvidenceUsage.notes, BoundaryAssociation.notes)
    are edited through the control/evidence relationship UIs.
    """

    class Meta:
        model = Evidence
        fields = ["name", "type", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class AddBoundaryToEvidenceForm(forms.Form):
    boundary = forms.ModelChoiceField(
        queryset=Boundary.objects.all().order_by("name"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
    )