# forms.py
from django import forms
from django.forms import HiddenInput

from .models import EtatDeLaSituation

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')


from django import forms
from .models import EtatDeLaSituation

class EtatDeLaSituationForm(forms.ModelForm):
    class Meta:
        model = EtatDeLaSituation
        fields = ['text', 'student', 'creator', 'modifier']
        widgets = {
            'student': HiddenInput(),
            'creator': HiddenInput(),
            # 'creation_date': HiddenInput(),
            'modifier': HiddenInput(),
            # 'modification_date': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 5, 'class': 'no-border'})  # Customize the widget for the 'text' field
        self.fields['text'].label = ''  # Remove the label for the 'text' field
        self.fields['text'].help_text = ''  # Remove the help text for the 'text' field

    # Optionally, you can override save to handle the 'student' ID from the view
    def save(self, commit=True, student_id=None):
        instance = super().save(commit=False)
        if student_id:
            instance.student_id = student_id
        if commit:
            instance.save()
        return instance
        