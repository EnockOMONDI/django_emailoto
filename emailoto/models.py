from django.contrib.auth import models


class EmailOtoAuthUser(models.AbstractBaseUser):
    username = models.CharField(max_length=120, unique=True)

    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
