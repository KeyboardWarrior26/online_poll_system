from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count, Sum
from .models import Question, Choice
from django.http import JsonResponse

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a valid choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices_with_votes = question.choice_set.annotate(vote_count=Count('votes'))
    total_votes = choices_with_votes.aggregate(total=Sum('vote_count'))['total'] or 0

    for choice in choices_with_votes:
        choice.percentage = round((choice.vote_count / total_votes) * 100, 1) if total_votes > 0 else 0

    return render(request, 'polls/results.html', {
        'question': question,
        'choices': choices_with_votes,
        'total_votes': total_votes,
    })


def health_check(request):
    return JsonResponse({'status': 'ok'})
