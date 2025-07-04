from django import forms

from .models import ProductoHuevo


class ProductoHuevoPrecioForm(forms.ModelForm):
    class Meta:
        model = ProductoHuevo
        fields = [
            "peso",
            "precio_compra",
            "precio_tentativo_cajon",
            "precio_tentativo_medio_cajon",
            "precio_tentativo_3maples",
            "precio_tentativo_maple",
            "activo",
        ]
        widgets = {
            "peso": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "precio_compra": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": 0}
            ),
            "precio_tentativo_cajon": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": 0}
            ),
            "precio_tentativo_medio_cajon": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": 0}
            ),
            "precio_tentativo_3maples": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": 0}
            ),
            "precio_tentativo_maple": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": 0}
            ),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
