from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import (
    District, Taluka, School, Student, Subject, Assignment, TaskEvaluation,
    DDPIProfile, BEOProfile, PrincipalProfile
)


class Command(BaseCommand):
    help = 'Clear all data from the database except superuser accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL data from the database except superuser accounts.\n'
                    'Use --confirm flag to proceed: python manage.py clear_all_data --confirm'
                )
            )
            return

        self.stdout.write(self.style.WARNING('Starting data deletion...'))
        
        try:
            with transaction.atomic():
                self.clear_all_data()
            self.stdout.write(self.style.SUCCESS('All data cleared successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing data: {str(e)}'))

    def clear_all_data(self):
        # Delete in reverse order of dependencies to avoid foreign key constraints
        
        # 1. Delete TaskEvaluations
        task_evaluations_count = TaskEvaluation.objects.count()
        TaskEvaluation.objects.all().delete()
        self.stdout.write(f'Deleted {task_evaluations_count} task evaluations')

        # 2. Delete Assignments
        assignments_count = Assignment.objects.count()
        Assignment.objects.all().delete()
        self.stdout.write(f'Deleted {assignments_count} assignments')

        # 3. Delete Students
        students_count = Student.objects.count()
        Student.objects.all().delete()
        self.stdout.write(f'Deleted {students_count} students')

        # 4. Delete User Profiles
        ddpi_profiles_count = DDPIProfile.objects.count()
        DDPIProfile.objects.all().delete()
        self.stdout.write(f'Deleted {ddpi_profiles_count} DDPI profiles')

        beo_profiles_count = BEOProfile.objects.count()
        BEOProfile.objects.all().delete()
        self.stdout.write(f'Deleted {beo_profiles_count} BEO profiles')

        principal_profiles_count = PrincipalProfile.objects.count()
        PrincipalProfile.objects.all().delete()
        self.stdout.write(f'Deleted {principal_profiles_count} Principal profiles')

        # 5. Delete non-superuser Users (but keep superusers)
        regular_users = User.objects.filter(is_superuser=False)
        regular_users_count = regular_users.count()
        regular_users.delete()
        self.stdout.write(f'Deleted {regular_users_count} regular user accounts (kept superusers)')

        # 6. Delete Schools
        schools_count = School.objects.count()
        School.objects.all().delete()
        self.stdout.write(f'Deleted {schools_count} schools')

        # 7. Delete Talukas
        talukas_count = Taluka.objects.count()
        Taluka.objects.all().delete()
        self.stdout.write(f'Deleted {talukas_count} talukas')

        # 8. Delete Districts
        districts_count = District.objects.count()
        District.objects.all().delete()
        self.stdout.write(f'Deleted {districts_count} districts')

        # 9. Delete Subjects
        subjects_count = Subject.objects.count()
        Subject.objects.all().delete()
        self.stdout.write(f'Deleted {subjects_count} subjects')

        self.stdout.write(self.style.SUCCESS('Data clearing completed successfully!'))
        self.stdout.write(self.style.SUCCESS('Superuser accounts have been preserved.'))