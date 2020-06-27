from django.urls import path
from . import views

urlpatterns = [
    path('shift_create/', views.shift_create, name='shift_create'),
    # 月間カレンダー表示
    path('', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/<int:day>', views.MonthCalendar.as_view(), name='month'),
    # 月間カレンダー一括
    path('month_with_forms/',views.MonthWithFormsCalendar.as_view(), name='month_with_forms' ),
    path('month_with_forms/<int:year>/<int:month>/<int:day>',views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
]