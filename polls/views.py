from django.http import HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render

from polls.models import Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:4]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    #output = '<br><br>'.join([p.question_text for p in latest_question_list])
    #output = latest_question_list
    #return HttpResponse(template.render(context))

def index1(request):#test index
    return HttpResponse("Hello, letter[a-d]!")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    #return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


