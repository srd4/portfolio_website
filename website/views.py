from django.shortcuts import render
from skill_set.models import Skill, Lesson
from django.db.models import Count
from .forms import WorkWithMe



def work_with_me_form(request):
    form = WorkWithMe()

    form.fields["email"].widget.attrs['placeholder'] = "Your email adress"
    form.fields["name"].widget.attrs['placeholder'] = "Your full name"
    form.fields["message"].widget.attrs['placeholder'] = "How can I help you?"

    if request.method == 'POST':
        form = WorkWithMe(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'website/work_with_me_form_success_div.html')

    return render(request, 'website/work_with_me_form_div.html', {'form': form})
        
# div views.

def skill_set_div(request):
    skill_set = Skill.objects.all().order_by('-level')

    if request.GET.get('detail') == 'mid':
        template = 'website/skill_set_div_mid.html'
    else:
        template = 'website/skill_set_div_simple.html'
        skill_set = skill_set[0:7]

    return render(request, template, {'skill_set': skill_set})



def practice_lesson_set_div(request):
    practice_lesson_set = Lesson.objects.filter(tags__name='project').annotate(num_skills=Count('skills')).order_by('-num_skills')

    if request.GET.get('detail') == 'mid':
        template = 'website/practice_lesson_set_div_mid.html'
    else:
        template = 'website/practice_lesson_set_div_simple.html'
        practice_lesson_set = practice_lesson_set[:7]

    return render(request, template, {'practice_lesson_set': practice_lesson_set})


# website views.

def home(request):
    return render(request, 'website/home.html')

def portfolio(request):
    return render(request, 'website/portfolio.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')