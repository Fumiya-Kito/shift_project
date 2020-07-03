from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
from .forms import ShiftCreateForm
from django.contrib.auth.decorators import login_required 
from . import mixins
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Shift

# User = get_user_model()

class MonthCalendar(LoginRequiredMixin, mixins.MonthCalendarMixin, generic.TemplateView):
    template_name = 'shift/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class MonthWithFormsCalendar(LoginRequiredMixin, mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'shift/month_with_forms.html'
    model = Shift
    date_field = 'date'
    time_field = 'start_time'
    form_class = ShiftCreateForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        # context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        # user_pk = self.kwargs['user_pk']
        # user = get_object_or_404(User, pk=user_pk)
        # context['user'] = user
        # context['start_time'] = form.cleaned_data["start_time"]

        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            shifts = formset.save(commit=False)
            for shift in shifts:
                if shift.is_work != False:
                    shift.user = request.user
                    # shift.start_time = form.cleaned_data["start_time"] 
                    # shift.end_time = form.cleaned_data["end_time"] 

                    shift.save()
                    

            return redirect('month_with_forms')

        return render(request, self.template_name, context)


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


