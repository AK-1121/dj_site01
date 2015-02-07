from django.core.urlresolvers import reverse
#from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic

#Is better to use reletive import instead of hardcoded import:
#from polls.models import Choice, Question # <-hardcorded import
from .models import Choice, Question

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        """Return the last five published questions
           (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:15]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    p = get_object_or_404(Question, pk=question_id)
    f=open(os.path.join(BASE_DIR, 'logfile1'),'w+')
    f.write("+++views-votes:+++\n"+str(p)+str(type(p))+"\nxxxxxxxx\n")
    #f.write(("len:",len(p)))
    f.write(str(p.__dict__))
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        f.write("\n\nselected_choice:"+str(selected_choice)+" type :"+
                str(selected_choice.__class__)+"\nDdict -> "+str(selected_choice.__dict__))
        f.write("\n!!!!!!\nRequesttt:"+ str(request))
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
        

#=============my try:===============
#import re
def test1(request):
    response = HttpResponse("Text only, please.")
    response_redir=HttpResponseRedirect("Text, please.") 
    f=open(os.path.join(BASE_DIR, 'log_test1'),'w+')
    f.write("Request:  \n"+str(request.COOKIES.values())+">>\n\n"+
            str(request.get_host())+"- request.get_host()\n\n"+
            str(request.get_full_path())+"<-get_full_path\n\n"+
            str(request.is_secure())+"<-request.is_secure()\n\n"+
            "Type:"+str(type(request))+"\n"+
            str(request)+"\n\n"+str(request.__dict__)[0])
    f.write("\n========================\nResponSe:\n")
    f.write(str(response)+"\n\n"+str(response.__dict__)+"\n\n"+
            str(type(response))+"<-Type\n\n"+
            str(response.status_code)+" <-status_code\n\n"+
            str(response.content)+" <-response_content\n\n"+
            str(response.streaming)+" -streaming\n\n"+
            str(response.reason_phrase)+" reason_phrase\n\n")
            
            
    f.close()
    #return response
    #return response_redir
    return render(request, 'polls/test-test1.html', {
        #'question': p,
        'error_message': "You didn't select a choice.",
        'request_path': request.path,
        })

    



