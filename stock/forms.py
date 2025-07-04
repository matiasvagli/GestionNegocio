from decimal import Decimal, InvalidOperation

from django import forms

from .models import (
    Compra,
    LineaVenta,
    Venta,
)


class VentaForm(forms.ModelForm):
    # Usar CharField para evitar procesamiento automático de locale
    importe_total = forms.CharField(
        label="Total del ticket ($)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Ejemplo: 5000 o 1500000",
                "inputmode": "decimal",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import datetime

        self.fields["fecha"].initial = datetime.date.today()
        self.fields["fecha"].widget = forms.HiddenInput()

    def clean_importe_total(self):
        """Limpia y valida el campo importe_total"""
        value = self.cleaned_data.get("importe_total")

        if value is None or value == "":
            return None

        # Convertir string a decimal
        if isinstance(value, str):
            cleaned_value = value.strip().replace(" ", "").replace("$", "").replace(",", ".")

            try:
                result = Decimal(cleaned_value)
                return result
            except InvalidOperation:
                raise forms.ValidationError("Ingrese un número válido. Ejemplo: 5000 o 1500000.50")

        try:
            result = Decimal(str(value))
            return result
        except (InvalidOperation, TypeError):
            raise forms.ValidationError("Ingrese un número válido.")

    def save(self, commit=True):
        """Método save personalizado para manejar el campo importe_total"""
        instance = super().save(commit=False)

        # Asignar el valor limpio del importe_total
        if "importe_total" in self.cleaned_data:
            instance.importe_total = self.cleaned_data["importe_total"]

        if commit:
            instance.save()
        return instance

    class Meta:
        model = Venta
        fields = ["fecha", "facturada"]
        widgets = {
            "facturada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class LineaVentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].error_messages = {"required": "Este campo es requerido"}
        # Hacer campos opcionales inicialmente
        self.fields["subcategoria"].required = False
        self.fields["unidad"].required = False
        self.fields["cantidad"].required = False
        # Forzar que siempre aparezca la opción 'E' en subcategoría
        self.fields["subcategoria"].choices = [
            ("E", "E"),
            ("1", "1"),
            ("2", "2"),
            ("M", "M"),
            ("3", "3"),
            ("4", "4"),
            ("S", "S"),
            ("R", "R"),
        ]

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        subcategoria = cleaned_data.get("subcategoria")
        unidad = cleaned_data.get("unidad")
        cantidad = cleaned_data.get("cantidad")

        # Si es huevos, exigir todos los campos
        if categoria and categoria.lower() in ["blancos", "color"]:
            if not subcategoria:
                self.add_error("subcategoria", "Este campo es requerido para categorías de huevos.")
            if not unidad:
                self.add_error("unidad", "Este campo es requerido para categorías de huevos.")
            if not cantidad:
                self.add_error("cantidad", "Este campo es requerido para categorías de huevos.")

        # Si es otros, limpiar campos de huevos
        elif categoria and categoria.lower() == "otros":
            cleaned_data["subcategoria"] = None
            cleaned_data["unidad"] = None
            cleaned_data["cantidad"] = None

        return cleaned_data

    class Meta:
        model = LineaVenta
        fields = ["categoria", "subcategoria", "unidad", "cantidad"]
        widgets = {
            "categoria": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "subcategoria": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "unidad": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control form-control-lg", "min": 0.01, "step": "0.01"}
            ),
        }


class CompraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import datetime

        self.fields["fecha"].initial = datetime.date.today()
        self.fields["fecha"].widget = forms.HiddenInput()
        self.fields["categoria"].error_messages = {"required": "Este campo es requerido"}

    class Meta:
        model = Compra
        fields = ["fecha", "categoria", "subcategoria", "unidad", "cantidad", "precio_unitario"]
        widgets = {
            "categoria": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "subcategoria": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "unidad": forms.Select(attrs={"class": "form-control form-control-lg"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control form-control-lg", "min": 0.01, "step": "0.01"}
            ),
            "precio_unitario": forms.NumberInput(
                attrs={"class": "form-control form-control-lg", "step": "0.01", "min": 0}
            ),
        }
