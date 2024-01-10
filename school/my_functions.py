
import openpyxl
from .models import Matiere
import os
import io

def handle_uploaded_file(file):
    file_path = os.path.join('uploads', file.name)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def upload_data_from_excel(file_path):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(io.BytesIO(file_path))
    # workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Delete previous instances
    Matiere.objects.all().delete()

    # Iterate through rows and create new instances
    for row in sheet.iter_rows(min_row=2, values_only=True):
        Matiere.objects.create(
            school_code=row[0],
            subject_code=row[1],
            description=row[2],
            category=row[3],
            visible_to_parents=row[4],
            mat_2nd=row[5]
        )
