from django.core.management.base import BaseCommand
from main.models import Voter
import openpyxl

class Command(BaseCommand):
    help = 'Import voters from Excel file with dynamic column mapping and debug headers'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['excel_file']
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # Print all headers for debugging
        headers = {}
        header_values = []
        for idx, cell in enumerate(sheet[1]):
            val = cell.value
            header_values.append(val)
            if val is not None:
                headers[val.strip().lower()] = idx

        self.stdout.write(self.style.SUCCESS(f"Detected headers: {header_values}"))

        required_columns = ['id', 'roll', 'name of students', 'class', 'sec']
        for col in required_columns:
            if col not in headers:
                self.stdout.write(self.style.ERROR(f"Missing required column: {col}"))
                return

        for row in sheet.iter_rows(min_row=2, values_only=True):
            id_value = row[headers['id']]
            roll_number = row[headers['roll']]
            name = row[headers['name of students']]
            student_class = row[headers['class']]
            section = row[headers['sec']]

            if not name:
                continue

            voting_id = str(id_value)

            Voter.objects.get_or_create(
                voting_id=voting_id,
                defaults={
                    'roll_number': str(roll_number),
                    'name': name,
                    'student_class': str(student_class),
                    'section': section
                }
            )

        self.stdout.write(self.style.SUCCESS('Voters imported successfully'))
