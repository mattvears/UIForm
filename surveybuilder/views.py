from django.http import HttpResponse
from survey.surveybuilder.models import UIForm, Question, Answer
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import send_mail


def list(request):
    surveys = UIForm.objects.all()
    return render_to_response('survey/list.html', 
                              { 'surveys': surveys }, 
                              context_instance=RequestContext(request))

def email(request, survey_id):
    s = get_object_or_404(UIForm, pk=survey_id)
    if request.POST.has_key('addr') == True:
      send_mail('Check out this UIForm!', 
                '<a href="http://django.confusiontechnology.com/survey/' + 
                survey_id + 
                '/">Check out this UIForm!</a>',
                'nobody@confusiontechnology.com',
                [request.POST['addr']],
                fail_silently = False)
      return HttpResponse("An email has been sent, it should arrive shortly.")
    else:
        return HttpResponse("No email address :(")

def view(request, survey_id):
    s = get_object_or_404(UIForm, pk=survey_id)

    can_vote = False
    is_owner = False
    if request.user.is_authenticated():
        if request.user == s.owner:
            is_owner = True
        else:
            can_vote = True

    questions = Question.objects.filter(form=s.id)
    return render_to_response('survey/view.html', 
                              {'survey': s,                    
                               'questions': questions,
                               'can_vote': can_vote,
                               'is_owner': is_owner,
                               'is_preview': False},
                              context_instance=RequestContext(request))

@login_required
def preview(request, survey_id):
    s = get_object_or_404(UIForm, pk=survey_id)
    if s.owner == request.user:
        questions = Question.objects.filter(form=s.id)
        return render_to_response('survey/view.html',
                                  {'survey': s,
                                   'questions': questions,
                                   'can_vote': True,
                                   'is_owner': False,
                                   'is_preview': True },
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse("You don't have permissions to preview this survey.")

@login_required
def create(request): 
    if request.POST.has_key('title') == True:
        new_form = UIForm()
        new_form.title = request.POST['title']
        new_form.description = request.POST['description']
        new_form.owner_id = request.user.id
        new_form.save()
        return redirect(''.join(['/survey/', str(new_form.id), '/']))
    else:
        return render_to_response('survey/create.html',
                                  {},
                                  context_instance=RequestContext(request))

@login_required
def add_question(request, survey_id):
   survey = get_object_or_404(UIForm, pk=survey_id)

   if request.POST.has_key('datatype') == True:
       q = Question()
       q.form = survey
       q.datatype = request.POST['datatype']
       q.text = request.POST['text']
       q.save()

       return redirect(''.join(['/survey/', str(survey.id), '/']))
   else:      
       return render_to_response('survey/add_question.html',
                                 {'survey_id': survey_id },
                                 context_instance=RequestContext(request))


@login_required
def answer(request, survey_id):
    survey = get_object_or_404(UIForm, pk=survey_id)

    for question_id in request.POST.keys():
        if question_id != 'csrfmiddlewaretoken':
            q = Question(pk=question_id)
            if q:
                ans =  Answer()
                ans.form = survey
                ans.question = q
                ans.user = request.user
                ans.value = request.POST[question_id]
                ans.save()

    survey_url = ''.join(['/survey/', str(survey.id), '/'])
    return redirect(survey_url)
