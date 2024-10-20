from django.shortcuts import render

# Create your views here.

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.shortcuts import get_object_or_404

'''
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
'''


def index(request):
    latest_question_list = Question.objects.all()
    template = 'polls/index.html'
    return render(request, template, context = {'latest_question_list': latest_question_list})


def detail(request, pk):
    try:
        q = Question.objects.get(pk=pk)
    except:
        raise Http404('Question does not exist')        
    # return HttpResponse(f'You\'re looking at question {q.question_text}')
    return render(request, 'polls/detail.html', {'q': q})

def results(request, pk):
    q = get_object_or_404(Question, pk=pk)
    # response = F'You\'re looking at the results of question {q.question_text}'
    # return HttpResponse(response % q)
    return render(request, 'polls/results.html',{'q': q})

def vote(request, pk):
    # return HttpResponse(f'You \'re voting on question {pk}')  
    q = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'q': q
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(q.id,)))