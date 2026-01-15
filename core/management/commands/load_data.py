from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
import pandas as pd
import os
from core.models import District, Taluka, School, Student, DDPIProfile, BEOProfile, PrincipalProfile


class Command(BaseCommand):
    help = 'Load data from Excel files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school-file',
            type=str,
            default='school_list.xlsx',
            help='Path to the school list Excel file'
        )
        parser.add_argument(
            '--student-file',
            type=str,
            default='student_list.xlsx',
            help='Path to the student list Excel file'
        )

    def handle(self, *args, **options):
        school_file = options['school_file']
        student_file = options['student_file']
        
        # If relative paths, make them absolute from the project root
        if not os.path.isabs(school_file):
            from django.conf import settings
            school_file = os.path.join(settings.BASE_DIR, school_file)
        
        if not os.path.isabs(student_file):
            from django.conf import settings
            student_file = os.path.join(settings.BASE_DIR, student_file)
        
        # Debug: List files in current directory and BASE_DIR
        self.stdout.write(f'Current working directory: {os.getcwd()}')
        self.stdout.write(f'BASE_DIR: {settings.BASE_DIR}')
        self.stdout.write(f'Looking for school file: {school_file}')
        self.stdout.write(f'Looking for student file: {student_file}')
        
        # List xlsx files in BASE_DIR
        xlsx_files = []
        try:
            for file in os.listdir(settings.BASE_DIR):
                if file.endswith('.xlsx'):
                    xlsx_files.append(file)
            self.stdout.write(f'Found .xlsx files in BASE_DIR: {xlsx_files}')
        except Exception as e:
            self.stdout.write(f'Error listing BASE_DIR: {str(e)}')
        
        # Check if files exist
        if not os.path.exists(school_file):
            self.stdout.write(self.style.ERROR(f'School file not found: {school_file}'))
            return
        
        if not os.path.exists(student_file):
            self.stdout.write(self.style.ERROR(f'Student file not found: {student_file}'))
            return
        
        try:
            with transaction.atomic():
                self.load_data(school_file, student_file)
            self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {str(e)}'))

    def load_data(self, school_file, student_file):
        # Step 1: Create user groups
        self.stdout.write('Creating user groups...')
        ddpi_group, created = Group.objects.get_or_create(name='DDPI')
        if created:
            self.stdout.write(self.style.SUCCESS('Created DDPI group'))
        
        beo_group, created = Group.objects.get_or_create(name='BEO')
        if created:
            self.stdout.write(self.style.SUCCESS('Created BEO group'))
        
        principal_group, created = Group.objects.get_or_create(name='Principal')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Principal group'))

        # Step 2: Create Belagavi District
        self.stdout.write('Creating Belagavi District...')
        district, created = District.objects.get_or_create(name='BELAGAVI')
        if created:
            self.stdout.write(self.style.SUCCESS('Belagavi District created'))
        else:
            self.stdout.write('Belagavi District already exists')

        # Step 3: Load talukas from school list
        self.stdout.write('Loading talukas...')
        school_df = pd.read_excel(school_file)
        unique_talukas = school_df['Block Name'].unique()
        
        talukas_created = 0
        for taluka_name in unique_talukas:
            taluka, created = Taluka.objects.get_or_create(
                name=taluka_name,
                district=district
            )
            if created:
                talukas_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'{talukas_created} talukas created, {len(unique_talukas) - talukas_created} already existed'))

        # Step 4: Load schools
        self.stdout.write('Loading schools...')
        schools_created = 0
        schools_updated = 0
        
        for _, row in school_df.iterrows():
            udise_code = str(row['Udise Code']).strip()
            school_name = str(row['School Name']).strip()
            block_name = str(row['Block Name']).strip()
            
            # Skip if essential data is missing
            if pd.isna(row['Udise Code']) or pd.isna(row['School Name']) or pd.isna(row['Block Name']):
                continue
                
            try:
                taluka = Taluka.objects.get(name=block_name, district=district)
                
                # Determine school type (boys/girls/coed)
                type_str = str(row['Type']).lower()
                if 'boys' in type_str and 'girls' not in type_str:
                    school_type = 'boys'
                elif 'girls' in type_str and 'boys' not in type_str:
                    school_type = 'girls'
                else:
                    school_type = 'coed'
                
                # Determine location
                location_str = str(row['School Location']).lower()
                if 'urban' in location_str:
                    location = 'urban'
                else:
                    location = 'rural'
                
                # Determine medium of instruction
                medium_str = str(row['medinstr1']).lower()
                if 'urdu' in medium_str:
                    medium = 'urdu'
                elif 'english' in medium_str:
                    medium = 'english'
                elif 'marathi' in medium_str:
                    medium = 'marathi'
                else:
                    medium = 'kannada'
                
                school, created = School.objects.get_or_create(
                    udise_code=udise_code,
                    defaults={
                        'name': school_name,
                        'taluka': taluka,
                        'type': school_type,
                        'school_type': str(row['Management']) if not pd.isna(row['Management']) else 'Government',
                        'location': location,
                        'medium': medium,
                    }
                )
                
                if created:
                    schools_created += 1
                else:
                    # Update existing school
                    school.name = school_name
                    school.taluka = taluka
                    school.type = school_type
                    school.school_type = str(row['Management']) if not pd.isna(row['Management']) else 'Government'
                    school.location = location
                    school.medium = medium
                    school.save()
                    schools_updated += 1
                    
            except Taluka.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Taluka not found: {block_name}'))
                continue
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing school {udise_code}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'{schools_created} schools created, {schools_updated} schools updated'))

        # Step 5: Load students
        self.stdout.write('Loading students...')
        student_df = pd.read_excel(student_file)
        students_created = 0
        students_updated = 0
        
        for _, row in student_df.iterrows():
            udise_code = str(row['Udise code']).strip()
            sts_number = str(row['SATS  No.']).strip()
            student_name = str(row['Student Name']).strip()
            
            # Skip if essential data is missing
            if pd.isna(row['Udise code']) or pd.isna(row['SATS  No.']) or pd.isna(row['Student Name']):
                continue
            
            try:
                school = School.objects.get(udise_code=udise_code)
                
                # Determine gender
                gender_str = str(row['Gender']).lower()
                if gender_str == 'b':
                    gender = 'male'
                elif gender_str == 'g':
                    gender = 'female'
                else:
                    gender = 'other'
                
                # Get standard
                standard = int(row['Standard']) if not pd.isna(row['Standard']) else 1
                
                student, created = Student.objects.get_or_create(
                    sts_number=sts_number,
                    school=school,
                    defaults={
                        'name': student_name,
                        'gender': gender,
                        'standard': standard,
                    }
                )
                
                if created:
                    students_created += 1
                else:
                    # Update existing student
                    student.name = student_name
                    student.gender = gender
                    student.standard = standard
                    student.save()
                    students_updated += 1
                    
            except School.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'School not found: {udise_code}'))
                continue
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing student {sts_number}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'{students_created} students created, {students_updated} students updated'))

        # Step 6: Create user accounts
        self.stdout.write('Creating user accounts...')
        
        # Create DDPI account for Belagavi district
        ddpi_username = 'belagavi_ddpi'
        ddpi_password = 'ddpi@0831'
        
        ddpi_user, created = User.objects.get_or_create(
            username=ddpi_username,
            defaults={
                'email': f'{ddpi_username}@prerane.in',
                'first_name': 'DDPI',
                'last_name': 'Belagavi',
                'is_staff': True,
            }
        )
        
        if created:
            ddpi_user.set_password(ddpi_password)
            ddpi_user.save()
            self.stdout.write(self.style.SUCCESS(f'DDPI user created: {ddpi_username}'))
        else:
            self.stdout.write(f'DDPI user already exists: {ddpi_username}')
        
        # Assign DDPI user to DDPI group
        ddpi_user.groups.add(ddpi_group)
        
        # Create or update DDPI profile
        ddpi_profile, created = DDPIProfile.objects.get_or_create(
            user=ddpi_user,
            defaults={'district': district}
        )
        if not created:
            ddpi_profile.district = district
            ddpi_profile.save()

        # Create BEO accounts for each taluka
        beo_created = 0
        for taluka in Taluka.objects.filter(district=district):
            beo_username = taluka.name.lower().replace(' ', '_')
            beo_password = taluka.name[::-1].lower()  # Reverse of taluka name
            
            beo_user, created = User.objects.get_or_create(
                username=beo_username,
                defaults={
                    'email': f'{beo_username}@prerane.in',
                    'first_name': 'BEO',
                    'last_name': taluka.name,
                    'is_staff': True,
                }
            )
            
            if created:
                beo_user.set_password(beo_password)
                beo_user.save()
                beo_created += 1
            
            # Assign BEO user to BEO group
            beo_user.groups.add(beo_group)
            
            # Create or update BEO profile
            beo_profile, created = BEOProfile.objects.get_or_create(
                user=beo_user,
                defaults={'taluka': taluka}
            )
            if not created:
                beo_profile.taluka = taluka
                beo_profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'{beo_created} BEO accounts created'))

        # Create Principal accounts for each school
        principal_created = 0
        for school in School.objects.filter(taluka__district=district):
            principal_username = school.udise_code.lower()
            principal_password = school.udise_code[::-1].lower()  # Reverse of UDISE code
            
            principal_user, created = User.objects.get_or_create(
                username=principal_username,
                defaults={
                    'email': f'{principal_username}@prerane.in',
                    'first_name': 'Principal',
                    'last_name': school.name[:50],  # Limit last name length
                    'is_staff': True,
                }
            )
            
            if created:
                principal_user.set_password(principal_password)
                principal_user.save()
                principal_created += 1
            
            # Assign Principal user to Principal group
            principal_user.groups.add(principal_group)
            
            # Create or update Principal profile
            principal_profile, created = PrincipalProfile.objects.get_or_create(
                user=principal_user,
                defaults={'school': school}
            )
            if not created:
                principal_profile.school = school
                principal_profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'{principal_created} Principal accounts created'))
        
        self.stdout.write(self.style.SUCCESS('Data loading completed successfully!'))
        self.stdout.write(self.style.SUCCESS('User groups (DDPI, BEO, Principal) assigned successfully!'))
        self.stdout.write(self.style.WARNING('All users should change their passwords after first login.'))