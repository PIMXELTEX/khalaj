from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

class Command(BaseCommand):
    help = 'Sets up social apps for Google and Facebook authentication'

    def handle(self, *args, **options):
        # Get or create the site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'localhost'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created site'))

        # Create Google SocialApp
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': 'YOUR_GOOGLE_CLIENT_ID',  # Replace with your Google Client ID
                'secret': 'YOUR_GOOGLE_CLIENT_SECRET',  # Replace with your Google Client Secret
            }
        )
        if created:
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('Created Google social app'))
        else:
            self.stdout.write(self.style.SUCCESS('Google social app already exists'))

        # Create Facebook SocialApp
        facebook_app, created = SocialApp.objects.get_or_create(
            provider='facebook',
            defaults={
                'name': 'Facebook',
                'client_id': 'YOUR_FACEBOOK_APP_ID',  # Replace with your Facebook App ID
                'secret': 'YOUR_FACEBOOK_APP_SECRET',  # Replace with your Facebook App Secret
            }
        )
        if created:
            facebook_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('Created Facebook social app'))
        else:
            self.stdout.write(self.style.SUCCESS('Facebook social app already exists')) 