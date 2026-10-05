from django import forms
from .models import Item, CAMPUS_LOCATIONS

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title', 'category', 'item_type', 'primary_image', 'additional_image',
            'location', 'specific_location_details', 'date_occurred',
            'description', 'secret_mark_question', 'current_custody'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Casio Scientific Calculator fx-991EX'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'item_type': forms.Select(attrs={'class': 'form-select', 'id': 'itemTypeSelect'}),
            'primary_image': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'specific_location_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Academic Bldg 1, 3rd floor Lab 2 back row'}),
            'date_occurred': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe identifiable marks, color, brand, condition...'}),
            'secret_mark_question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. What sticker is placed on the battery cover? (For FOUND items only)'}),
            'current_custody': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')
        secret_mark_question = cleaned_data.get('secret_mark_question')

        # If it's a found item, encourage a verification question for claim security
        if item_type == 'FOUND' and not secret_mark_question:
            self.add_error('secret_mark_question', 'Please provide a secret verification question so the rightful owner can verify it before claiming.')
        return cleaned_data
