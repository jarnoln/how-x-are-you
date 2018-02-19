from django.shortcuts import get_object_or_404, render
from survey import models


def submit_survey(request, survey_name):
    survey = get_object_or_404(models.Survey, name=survey_name)
    reference = models.Reference.objects.filter(survey=survey).first()
    answer_list = []
    score = 0
    nscore = 0
    for question in survey.question_set.all():
        key = 'q-{}'.format(question.id)
        answer_value = int(request.POST.get(key, '0'))
        points = answer_value  # Value between -2 and +2 (0 being no comment)
        npoints = answer_value + 2  # Value between 0 and 4 (2 being no comment)
        answer_list.append({'question': question,
                            'answer': answer_value,
                            'points': points,
                            'npoints': npoints
                            })
        score += points
        nscore += npoints
        # print('{}:{}'.format(question.title, answer_value))

    max_score = survey.question_set.count() * 2
    nmax_score = survey.question_set.count() * 4
    pct = 0
    npct = 0
    if max_score > 0:
        pct = float(score * 100) / max_score
        npct = float(nscore * 100) / nmax_score

    if reference:
        feedback = reference.feedback(npct)
    else:
        feedback = None

    context = {
        'survey': survey,
        'reference': reference,
        'feedback': feedback,
        'answers': answer_list,
        'score': score,
        'nscore': nscore,
        'max_score': max_score,
        'nmax_score': nmax_score,
        'pct': pct,
        'npct': npct
    }
    return render(request, 'survey/result.html', context)
    # return HttpResponseRedirect(reverse('survey'))
