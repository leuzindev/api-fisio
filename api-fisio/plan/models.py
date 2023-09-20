from django.db import models
from account.models import User
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    title = models.CharField(
        max_length=255
    )
    description = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')


class Exercise(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    plans = models.ManyToManyField(Plan)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = _('exercise')
        verbose_name_plural = _('exercises')

    def __str__(self):
        return self.name


class ExerciseVideo(models.Model):
    name = models.CharField()
    video_file = models.FileField(
        upload_to='videos/',
        null=True,
        verbose_name=""
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name
