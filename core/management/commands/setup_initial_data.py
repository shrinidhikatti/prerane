# core/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from core.models import District, DDPIProfile

class Command(BaseCommand):
    help = 'Set up initial data for the education management system'

    def handle(self, *args, **options):
        # Create user groups
        ddpi_group, created = Group.objects.get_or_create(name='DDPI')
        if created:
            self.stdout.write(self.style.SUCCESS('Created DDPI group'))
        
        beo_group, created = Group.objects.get_or_create(name='BEO')
        if created:
            self.stdout.write(self.style.SUCCESS('Created BEO group'))
        
        principal_group, created = Group.objects.get_or_create(name='Principal')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Principal group'))

        # Create sample district
        district, created = District.objects.get_or_create(name='Sample District')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Sample District'))

        # Create sample DDPI user if it doesn't exist
        ddpi_username = 'ddpi_sample'
        if not User.objects.filter(username=ddpi_username).exists():
            ddpi_user = User.objects.create_user(
                username=ddpi_username,
                password='ddpi123',
                first_name='Sample',
                last_name='DDPI',
                email='ddpi@example.com'
            )
            ddpi_user.groups.add(ddpi_group)
            
            DDPIProfile.objects.create(
                user=ddpi_user,
                district=district
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created DDPI user: {ddpi_username} (password: ddpi123)'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('Initial data setup completed successfully!')
        )