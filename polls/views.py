from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render

from polls.models import Choice, Question

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


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
    #return HttpResponse("You're voting on question %s." % question_id)
    p = get_object_or_404(Question, pk=question_id)
    f=open(os.path.join(BASE_DIR, 'logfile1'),'w+')
    f.write("+++views-votes:+++\n"+str(p)+"\n")
    #f.write(("len:",len(p)))
    f.write(str(p.__dict__))
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        f.write("\n\nselected_choice:"+str(selected_choice)+" type :"+
                str(selected_choice.__class__)+"\n\ndict -> "+str(selected_choice.__dict__))
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        #Always return an HttResponseRediret after successfully dealing 
        #with POST data. This prevents data from being posted twice if a 
        #user hits the Back button.
        #return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        HRR = HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        f.write("\n\n\nHttpResponseRedirect: "+str(HRR)+"\n\n"+str(HRR.__dict__))
        f.write("\n----views - votes----\n")
        f.close()
        return HRR
        
    



