from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'price']

    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если продукт уже существует, делаем поле необязательным
        if self.instance.pk:
            self.fields['image'].required = False

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None and price < 0:
            raise ValidationError(f'Цена не может быть отрицательной')

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(f'Слово {word} запрещщено')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(f'Слово {word} запрещщено')
        return description