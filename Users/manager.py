from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, PhoneNumber, password=None,):

        if not email:
            raise ValueError('Email must be provided')

        user = self.model(email=self.normalize_email(
            email), PhoneNumber=PhoneNumber)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, PhoneNumber, password=None):

        user = self.create_user(
            email, PhoneNumber, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
