from django import forms
from django.forms import widgets


class FilmForm(forms.Form):
    category = forms.CharField(label="Категория фильма")
    name = forms.CharField(label="Название фильма")
    text = forms.CharField(label="Описание фильма", widget=forms.Textarea)
    avatar = forms.ImageField(label="Аватар", required=False)

    def __init__(self, *args, **kwargs):
        is_editing = kwargs.pop('is_editing', False)
        super().__init__(*args, **kwargs)

        if is_editing:
            # Отключаем обязательность для всех полей при редактировании
            for field in self.fields.values():
                field.required = False

