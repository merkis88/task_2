from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo and photo.size > 2 * 1024 * 1024:  # 2 МБ в байтах
            raise forms.ValidationError("Размер изображения не должен превышать 2 МБ.")
        return photo

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }
