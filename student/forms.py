# forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')


from .models import Student

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         exclude = ['etat_situation', 'comite_clinique', 'date_ref_comite_clinique', 'code']

#         def __init__(self, *args, **kwargs):
#             super(StudentForm, self).__init__(*args, **kwargs)
#             # Set certain fields as invisible (hidden)
#             self.fields['is_student'].widget = forms.HiddenInput()
#             self.fields['created_by'].widget = forms.HiddenInput()
#             self.fields['date_created'].widget = forms.HiddenInput()
#             self.fields['date_is_student_changed'].widget = forms.HiddenInput()
#             # Add more fields to hide as needed

