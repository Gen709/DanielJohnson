import csv
import string

import openpyxl
from openpyxl.utils import get_column_letter

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone

from .models import RegularTeacher, SchoolAdmin, SpecialtyTeacher
from school.models import Group, Classification
from datetime import datetime

class ExtractTeacher():
    def __init__(self, request):
        self.request = request
        self.file_name = request.FILES['csv_file'] 

    def get_csv_reader(self):
        reader = []
        # with open(self.file_name, mode='r', newline='', encoding='utf-8-sig') as file:
        r = csv.DictReader(self.file_name.read().decode('utf-8-sig').splitlines())
        for row in r:
            capitalized_row = {key.upper(): value for key, value in row.items()}
            reader.append(capitalized_row)
                
        return reader         
    
    def identify_extract(self, reader):
        teacher_extract_row_list = ['GROUPE', 'NOM', 'LOCAUX', 'MATIERES']
        if [k for k in reader[0].keys()] == teacher_extract_row_list:
            return "regular_teacher_extract"

    def get_excel_reader(self):
        workbook = openpyxl.load_workbook(self.file_name)
        sheet = workbook.active
        reader = []
        header = [cell.value for cell in sheet[1]]
        print(header)
        for row in sheet.iter_rows(min_row=2):
            row_data = {}
            for idx, cell in enumerate(row):
                if header[idx]:
                    row_data[header[idx].upper()] = cell.value
                else:
                    row_data[header[idx]] = " "
            reader.append(row_data)
            
        return reader

    def get_reader(self):
        if self.file_name.name.endswith('.csv'):
            reader = self.get_csv_reader()
        elif self.file_name.name.endswith('.xlsx'):
            reader = self.get_excel_reader()
        return reader

    def create_group(self):
        reader = self.get_reader()
        group_name_list = [teacher_dict["GROUPE"] for teacher_dict in reader if '-' not in teacher_dict["GROUPE"]]
        updated_group_list = [Group.objects.update_or_create(nom=groupe_name) for groupe_name in group_name_list]
        return updated_group_list
    
    def associate_classification_to_groupe(self):
        """Classification relates Administrators to cycles, and the second number
            in a group name relates the group to the cycle
        """
        classification = Classification.objects.all()
        for classi in classification:
            print(classi)
            if len(classi.nom) == 1: # classification de JV
                for g in Group.objects.all():
                    if string.ascii_lowercase.index(classi.nom.lower()) == int(g.nom[1]):
                        print(classi.nom, g.nom, int(g.nom[1]))
                        g.classification = classi
                        g.save()

    def create_regular_teacher(self, reader):
        operation_list = []
        plain_text_password = "General-Vanier"
        hashed_password = make_password(plain_text_password)
        for regular_teacher_dict in reader:
            prenom_nomfamille = regular_teacher_dict["NOM"].split()
            prenom = prenom_nomfamille[0]
            nom_famille = " ".join(prenom_nomfamille[1:])
            try:
                g = Group.objects.get(nom=regular_teacher_dict["GROUPE"])
        
            except:
                g = None
            # print(prenom_nomfamille, prenom, nom_famille, g)   
            RegularTeacher.objects.update_or_create(
                                                    password = hashed_password,
                                                    username = prenom[:3]+nom_famille[:3], 
                                                    first_name = prenom, 
                                                    last_name = nom_famille, 
                                                    email = "", 
                                                    group = g, 
                                                    matière = regular_teacher_dict["MATIERES"])
            operation_list.append(RegularTeacher)
            
        return operation_list            

    def update_regularteacher_data(self):
        reader = self.get_reader()
        updated_group_obj_list = self.create_group()
        self.associate_classification_to_groupe()
        updated_regular_teacher = self.create_regular_teacher(reader)
        return {"updated_group_obj_list": updated_group_obj_list,
                "updated_regular_teacher": updated_regular_teacher}
    
    def update_data(self):
        reader = self.get_reader()
        if self.identify_extract(reader) == "regular_teacher_extract":
            self.update_regularteacher_data()
        elif self.identify_extract(reader) == "specialty_teacher_extract":
            pass
        elif self.identify_extract(reader) == "schooladministrator_extract":
            pass