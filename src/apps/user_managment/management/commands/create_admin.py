from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create super user'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help="Define an admin's name.")
        parser.add_argument('-p', '--password', type=str, help="Define an admin's password.")
        parser.add_argument('-e', '--email', type=str, help="Define an admin's email.")

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        email = kwargs['email']
        try:
            User = get_user_model()
            Profile = User.profile.related.related_model
            user = User.objects.create_superuser(username=username, email=email, password=password)
            Profile.objects.create(user=user, created_by=user)
        except IntegrityError as err:
            logger.warning(str(err))

