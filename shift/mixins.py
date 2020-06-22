import calendar
from collections import deque
import datetime
import itertools
from django import forms

class BaseCalendarMixin:
    first_weekday = 5 #土曜始まり
    week_names = ['月', '火', '水', '木', '金', '土', '日']

    def setup_calendar(self):
        # ? calendar.Calendarクラスのインスタンス化
        # ? monthdatescalendarメソッドの利用：first_weekdayの対応を行っている
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        # ? dequeを使ってfirst_weekdayからweek_namesをシフトする。
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    # 月間カレンダー機能 Mixin
    def get_previous_half(self, date):
        # 前月を返す
        # ? dateオブジェクトはわかるけどなぜ、datetime.dateじゃないんだろ？
        if date.day <= 15:
            if date.month == 1:
                return date.replace(year=date.year-1, month=12, day=16)
            else:
                return date.replace(month=date.month-1, day=16)
        else:
            return date.replace(month=date.month, day=1)
    
    def get_next_half(self, date):
        # 次を返す
        if date.day > 15:
            if date.month == 12:
                return date.replace(year=date.year+1, month=1, day=1)
            else:
                return date.replace(month=date.month+1, day=1)    
        else:
            return date.replace(month=date.month, day=16)
    
    def get_half_days(self, date):
        # 月の前半の日を返す
        if date.day<=15:
            return [self._calendar.monthdatescalendar(date.year, date.month)[i] for i in range(3)]
        return [self._calendar.monthdatescalendar(date.year, date.month)[i] for i in range(2,5)]
        

    def get_current_month(self):
        # 現在の月を返す
        day = self.kwargs.get('day')
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year and day:
            month = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        # 月間カレンダー情報の入った辞書を返す
        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_half_days': self.get_half_days(current_month),
            'month_current': current_month,
            'half_previous': self.get_previous_half(current_month),
            'half_next': self.get_next_half(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data




class WeekCalendarMixin(BaseCalendarMixin):
    #? 週間カレンダー機能

    def get_week_days(self):
        # ?その週の全ての日を返す
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        
        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:
                return week


    # TODO 2weekにすること

    def get_week_calendar(self):
        self.setup_calendar()
        # ここを1~15 or 16~最終日 にしたい
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
        }
        return calendar_data