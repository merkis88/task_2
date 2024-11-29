from django import forms

from .models import Order


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Разрешаем множественный выбор файлов


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):  # Если передан список файлов
            result = [single_file_clean(d, initial) for d in data]
        else:  # Если один файл
            result = single_file_clean(data, initial)
        return result


class CreateOrderForm(forms.ModelForm):
    photos = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Order
        fields = ['title', 'description']  # Поля из модели Order

    def clean_photos(self):
        photos = self.cleaned_data.get('photos', [])
        len_photos = len(photos)
        if len_photos > 3 or len_photos == 0:  # Проверяем, что загружено не больше трёх файлов
            raise forms.ValidationError("Вы можете загрузить не более 3 фотографий и не должно быть пустой")
        for photo in photos:
            if photo.size > 2 * 1024 * 1024:  # Ограничение размера файла до 2 МБ
                raise forms.ValidationError("Размер каждого изображения не должен превышать 2 МБ.")
        return photos
