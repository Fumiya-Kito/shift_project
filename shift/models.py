<<<<<<< HEAD
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone



class Shift(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField('日付')
    is_work = models.BooleanField(verbose_name='出勤', default=False, null=True)
    all_day = models.BooleanField(verbose_name='終日', default=False)
    start_time = models.TimeField(verbose_name='開始時間',default=datetime.time(8,0))
    end_time = models.TimeField(verbose_name='終了時刻',default=datetime.time(17,0))
    create_at = models.DateTimeField(default=timezone.now)
    # description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s " + str(self.date) + " shift"

# TODO 月のテーブル（モデル）を作って、

# class Month(models.Model):
#     user
#     shift
=======
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    is_work = models.NullBooleanField(verbose_name='is_work', default=None)
    all_day = models.BooleanField(verbose_name='all_day', default=False)
    start_time = models.TimeField(default=datetime.time(8,0))
    end_time = models.TimeField(default=datetime.time(17,0))
    create_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s " + str(self.pk) + " shift"
>>>>>>> origin/master
