from datetime import datetime, timedelta

from django.db import models

from rest_framework.exceptions import ParseError, NotFound, ValidationError

class Tikee(models.Model):
    tikee_id = models.CharField(max_length=24, primary_key=True)

class BaseSequence(models.Model):
    tikee_id = models.ForeignKey('Tikee', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    start = models.DateTimeField()
    upload_to_cloud = models.BooleanField(default=True)
    image_format = models.CharField(max_length=10, default="jpeg")
    keep_local_copy = models.BooleanField(default=False)
    sequence_id = models.BigIntegerField(default=0)
    shooting_status = models.CharField(max_length=100, null=True)
    nb_images_on_sd = models.IntegerField(default=0)
    nb_images_uploaded = models.IntegerField(default=0)

    class Meta:
        abstract = True

class ShortSequence(BaseSequence):
    interval = models.IntegerField(default=10)
    duration = models.IntegerField(default=86400)
    end = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.end = self.start + timedelta(minutes=self.duration * self.interval)

        items_overlapping_start = ShortSequence.objects.filter(start__gte = self.start, start__lte = self.end).exists()

        items_overlapping_end = ShortSequence.objects.filter(end__gte = self.start, end__lte = self.end).exists()

        items_enveloping = ShortSequence.objects.filter(start__lte=self.start, end__gte=self.end).exists()

        if items_overlapping_start or items_overlapping_end or items_enveloping:
            raise ValidationError(detail='two sequences overlap', code = ValidationError.status_code)
        else:
            super(ShortSequence, self).save(*args, **kwargs)

class LongSequence(BaseSequence):
    infinite_duration = models.BooleanField(default=False)
    end = models.DateTimeField()

    def save(self, *args, **kwargs):
        items_overlapping_start = LongSequence.objects.filter(start__gte = self.start, start__lte = self.end).exists()

        items_overlapping_end = LongSequence.objects.filter(end__gte = self.start, end__lte = self.end).exists()

        items_enveloping = LongSequence.objects.filter(start__lte=self.start, end__gte=self.end).exists()

        if items_overlapping_start or items_overlapping_end or items_enveloping:
            raise ValidationError(detail='two sequences overlap', code = ValidationError.status_code)
        else:
            super(LongSequence, self).save(*args, **kwargs)

class XRequestId(models.Model):
    name = models.CharField(max_length=24)
    date = models.DateTimeField()

    class Meta:
        ordering = ['date']