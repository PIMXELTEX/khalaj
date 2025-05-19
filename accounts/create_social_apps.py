from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get the site
site = Site.objects.get(id=1)

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

print("Social apps created successfully!")