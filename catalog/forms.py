from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class CustomClearableFileInput(forms.ClearableFileInput):
    clear_checkbox_label = "Удалить текущее изображение"


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=CustomClearableFileInput)

    class Meta:
        model = Product
        fields = ["name", "description", "category", "image", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(f'Слово "{word}" запрещено')
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(f'Слово "{word}" запрещено')
        return description

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание"}
        )
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите цену"}
        )
