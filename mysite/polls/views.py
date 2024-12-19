from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic import UpdateView, CreateView

from .forms import RegistrationForm, LoginForm, EditUserForm, ChoiceForm, QuestionForm
from .models import Question, Choice, User


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('polls:profile')
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('polls:index')
    return render(request, 'delete_profile.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


@login_required
def detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user in question.voters.all():
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор.'
        })
    else:
        question.total_votes += 1
        question.save()
        selected_choice.votes += 1
        selected_choice.save()

        question.voters.add(request.user)

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# views.py
class CreatePollView(View):
    template_name = 'polls/create_poll.html'
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=5)  # Позволяет добавлять до 5 вариантов

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm()
        formset = self.ChoiceFormSet(queryset=Choice.objects.none())
        return render(request, self.template_name, {
            'question_form': question_form,
            'formset': formset,
        })

    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST, request.FILES)
        formset = self.ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()  # Сохраняем вопрос

            # Сохраняем каждый вариант ответа
            for choice_form in formset:
                if choice_form.cleaned_data:  # Проверяем, что данные формы не пустые
                    choice = choice_form.save(commit=False)  # Не сохраняем сразу
                    choice.question = question  # Привязываем вариант ответа к вопросу
                    choice.save()  # Сохраняем вариант ответа

            return redirect('polls:index')  # Перенаправление на главную страницу после создания опроса

        return render(request, self.template_name, {
            'question_form': question_form,
            'formset': formset,
        })

