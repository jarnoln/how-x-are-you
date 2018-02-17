from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from survey import models


class HomeView(TemplateView):
    template_name = 'survey/home.html'


def submit_survey(request, survey_name):
    survey = get_object_or_404(models.Survey, name=survey_name)
    answer_list = []
    score = 0
    nscore = 0
    for question in survey.question_set.all():
        key = 'q-{}'.format(question.id)
        answer_value = int(request.POST.get(key, '0'))

        points = answer_value  # Value between -10 and +10 (0 being no comment)
        npoints = (answer_value + 10) / 2  # Value between 0 and 10 (5 being no comment)
        answer_list.append({'question': question,
                            'answer': answer_value,
                            'points': points,
                            'npoints': npoints
                            })
        score += points
        nscore += npoints
        # print('{}:{}'.format(question.title, answer_value))

    max_score = survey.question_set.count() * 10
    pct = 0
    npct = 0
    if max_score > 0:
        pct = float(score * 100) / max_score
        npct = float(nscore * 100) / max_score

    context = {
        'survey': survey,
        'answers': answer_list,
        'score': score,
        'nscore': nscore,
        'max_score': max_score,
        'pct': pct,
        'npct': npct
    }
    return render(request, 'survey/result.html', context)
    # return HttpResponseRedirect(reverse('survey'))
