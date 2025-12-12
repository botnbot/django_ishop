from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = "catalog/templates/catalog/custom_clearable_file_input.html"
    clear_checkbox_label = "Удалить текущее изображение"
