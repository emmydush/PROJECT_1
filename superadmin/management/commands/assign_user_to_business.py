from django.core.management.base import BaseCommand
from superadmin.models import Business
from authentication.models import User

class Command(BaseCommand):
    help = 'Assign a user to a business'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('business_id', type=int, help='ID of the business')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
            business = Business.objects.get(id=options['business_id'])
            
            # Assign the user as the owner of the business
            business.owner = user
            business.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully assigned user "{user.username}" as owner of business "{business.company_name}"'
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{options["username"]}" does not exist')
            )
        except Business.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Business with ID "{options["business_id"]}" does not exist')
            )