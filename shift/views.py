from django.shortcuts import render, redirect
from .forms import ShiftCreateForm
from django.contrib.auth.decorators import login_required 
from . import mixins
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class MonthCalendar(LoginRequiredMixin, mixins.MonthCalendarMixin, generic.TemplateView):
    template_name = 'shift/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

@login_required
def shift_create(request):
    shift_form = ShiftCreateForm(request.POST or None)

    if request.method == "POST" and shift_form.is_valid():
        shift = shift_form.save(commit=False)
        shift.user = request.user
        shift.save() 
        return redirect('list')

    context = {
        'shift_form':shift_form,
    }
    return render(request,'shift/shift_create.html', context)


