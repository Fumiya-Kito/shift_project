from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    is_work = models.NullBooleanField(verbose_name='出勤', default=False)
    all_day = models.BooleanField(verbose_name='終日', default=False)
    start_time = models.TimeField(verbose_name='開始時間',default=datetime.time(8,0))
    end_time = models.TimeField(verbose_name='終了時刻',default=datetime.time(17,0))
    create_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s " + str(self.date) + " shift"