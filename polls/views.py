from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.db.models import Sum

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    total_votes = question.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0

    # Add percentage manually to each choice
    for choice in question.choice_set.all():
        if total_votes > 0:
            choice.percentage = round((choice.votes / total_votes) * 100, 1)
        else:
            choice.percentage = 0

    return render(request, 'polls/results.html', {
        'question': question,
        'total_votes': total_votes
    })
