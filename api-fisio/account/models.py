import re

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

    def get_professionals(self):
        return self.filter(role=User.PHYSIOTHERAPIST)

    def get_patients(self):
        return self.filter(role=User.PATIENT)


class User(AbstractBaseUser, PermissionsMixin):
    PATIENT = 1
    PHYSIOTHERAPIST = 2
    USER_ROLES = (
        (PATIENT, 'Paciente'),
        (PHYSIOTHERAPIST, 'Fisioterapeuta'),
    )

    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'),
                _('invalid'))]
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    role = models.PositiveSmallIntegerField(
        'Role',
        choices=USER_ROLES,
        default=PATIENT
    )
    avatar = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[
            validators.RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
            ),
        ],
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)

            if self.role == self.PATIENT:
                Patient.objects.create(user=self)
            elif self.role == self.PHYSIOTHERAPIST:
                Physiotherapist.objects.create(user=self)
        else:
            old_role = User.objects.get(pk=self.pk).role

            if self.role != old_role:
                if old_role == self.PATIENT:
                    self.patient.delete()
                    Physiotherapist.objects.create(user=self)
                elif old_role == self.PHYSIOTHERAPIST:
                    self.physiotherapist.delete()
                    Patient.objects.create(user=self)

            super().save(*args, **kwargs)


class Physiotherapist(models.Model):
    FREE = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    SUBSCRIPTIONS_TYPES = (
        (FREE, 'Gratis'),
        (BRONZE, 'Bronze'),
        (SILVER, 'Prata'),
        (GOLD, 'Ouro'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.PositiveSmallIntegerField(
        'Subscription',
        choices=SUBSCRIPTIONS_TYPES,
        default=FREE
    )

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plans = models.ManyToManyField('plan.Plan', blank=True)
    physiotherapist = models.ForeignKey(
        Physiotherapist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients'
    )

    def __str__(self):
        return self.user.username
