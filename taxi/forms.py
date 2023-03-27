from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                "Ensure that the license number "
                f"is {self.LICENSE_LENGTH} characters"
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "The first three characters must be capital letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last 5 characters must be a number"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Driver
        fields = "__all__"
