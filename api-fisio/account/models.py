import re

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    avatar = models.CharField(
        max_length=255,
        blank=True
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
