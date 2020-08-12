from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, SubjectForm, TopicForm, QuestionForm, ChoiceForm
from .models import Test, Question, Choice, Topic, Subject, CompositeObjective
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import HttpResponseRedirect
import re,random

def home(request):
   
    return render(request, 'cbts_app/home.html')

def about(request):
    return render(request, 'cbts_app/about.html')

def sign_in(request):
    return render(request, 'cbts_app/sign-in.html')

def register(request):
    
  
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        
        
        if form.is_valid():
            user = form.save()
            if (request.POST.get("type",'') == 'Student'):
                group = Group.objects.get(name='Student')
                user.groups.add(group)
                print('add to student')
            elif (request.POST.get("type",'') == 'Teacher'):
                group = Group.objects.get(name='Teacher')
                user.groups.add(group)
                print('add to teacher')
            print(True)
            return redirect('cbts-sign_in')
        else:
            
            print(False)
        
    else:
        form = UserRegisterForm()
        

    context = {
            'form' : form,
            
    }
    return render(request, 'cbts_app/register.html', context)


def student(request):
    return render(request, 'cbts_app/student.html')


def overview(request):
    
    

    test_all = Test.objects.all()
    context = {'test_all' : test_all,}
    return render(request, 'cbts_app/overview.html', context)



def test(request):
    if request.method == 'GET':

        if len(request.GET) > 1:
            print(request.GET)
            answers = list(request.GET.values())
            cnt = {}
            print(answers)
            score = 0
            total = 0
            for i in range(0, len(answers) - 2, 2):
                if(float(answers[i]) > 0):
                    cnt[answers[i+1]] = cnt.get(answers[i+1],0) + 1
                score = score + float(answers[i])
            total = float(answers[-1])
            
            percentage = score / total * 100

            print(cnt)
            context = {'score' : score, 'total' : total, 'percentage' : percentage, 'cnt' : cnt}
            
            return render(request, 'cbts_app/test.html', context)
        else:
            #query all data
            current_title = request.GET.get('title','')
            current_test = Test.objects.get(title=current_title)
            q1 = Question.objects.filter(test=current_test, difficulty=2, topic=Topic.objects.get(title='Plus'))
            q2 = Question.objects.filter(test=current_test, difficulty=1, topic=Topic.objects.get(title='Minus'))
            #all_question = Question.objects.filter(test=current_test)
            all_question = q1 | q2
            questions_answers = {}
            totalscore = 0
            for q in all_question:
                l = {}
                
                choices = Choice.objects.filter(question=q).order_by('?')
                for c in choices:
                    totalscore = totalscore + c.point
                    l.update({c.choice : [q.topic.title, q.id, c.point]})
                questions_answers.update({q.title : l})
            r = list(questions_answers.items())
            random.shuffle(r)
            questions_answers = dict(r)
            questions_answers.update({'totalscore' : totalscore})
            print(questions_answers)

            context = {'list' : questions_answers}
            return render(request, 'cbts_app/test.html', context)
    return render(request, 'cbts_app/test.html')


def result(request):
    if request.method == 'GET':
        print('...')
    return render(request, 'cbts_app/result.html')

def create_subject(request):
    #form = TestForm()

    subject_form = SubjectForm(initial={'teacher' : request.user})
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        
        print(request.POST)

        if subject_form.is_valid:
            request.session['title'] = request.POST['title']
            subject_form.save()

        if request.POST['todo'] == 'save':
            return redirect('cbts-overview')
        elif request.POST['todo'] == 'continue':
            return redirect('cbts-create-topic')
            
    context = {'form' : subject_form}
    return render(request, 'cbts_app/create-subject.html', context)

def create_topic(request):
    subject_name = request.session['title']
    print("subject name = ", subject_name)
    subject_obj = Subject.objects.get(title=subject_name)
    print(subject_obj)
    
   
    topic_form = TopicForm(initial={'subject' : subject_obj})
    
    if request.method == 'POST':

        topic_form = TopicForm(request.POST)
        print(request.POST)
        if request.POST['todo'] == 'stop':
            return redirect('cbts-overview')

        if topic_form.is_valid:
            topic_form.save()
            topics_obj = Topic.objects.filter(subject=subject_obj)
            topics_size = topics_obj.count()

            current_obj = topics_obj[topics_size - 1]

            for topic_obj in topics_obj:
                CompositeObjective(subject=subject_obj, topic1=current_obj, topic2=topic_obj).save()
            


        
    
    topics_obj = Topic.objects.filter(subject=subject_obj)
    
    print(topics_obj)
    context = {'form' : topic_form, 'topics' : topics_obj}

    return render(request, 'cbts_app/create-topic.html', context)

def view_subject(request):
    subjects = Subject.objects.filter(teacher=request.user)
    context = {'subjects' : subjects}

    if request.method == 'POST':
        print('POST =', request.POST)
        request.session['title'] = request.POST['title']
        request.session.save()

        if request.POST['todo'] == 'add topics':
            return redirect('cbts-create-topic')
        elif request.POST['todo'] == 'add questions':
            return redirect('cbts-create-question')

    return render(request, 'cbts_app/view-subject.html', context)

def create_question(request):
    print('title=', request.session['title'])
    subject_obj = Subject.objects.get(title=request.session['title'])
    questions = Question.objects.filter(subject=subject_obj)
    question_form = QuestionForm(initial={'subject' : subject_obj})
    question_form.fields['topic'].queryset = CompositeObjective.objects.filter(subject=subject_obj)
    
    print( question_form.fields['topic'].queryset)
    

    if request.method == 'POST':
        
        print(request.POST)

        if 'todo' in request.POST and request.POST['todo'] == 'edit choice':
            request.session['qnumber'] = request.POST['qnumber']
            return redirect('cbts-create-choice')
        

        question_form = QuestionForm(request.POST)
        

        if question_form.is_valid():
            question_form.save()
            request.session['nquestion'] = request.POST['nquestion']
            question_form = QuestionForm(initial={'subject' : subject_obj})
            question_form.fields['topic'].queryset = Topic.objects.filter(subject=subject_obj)
            
        
    context = {'form' : question_form, 'questions' : questions}
    return render(request, 'cbts_app/create-question.html', context)

def create_choice(request):
    choice_form = ChoiceForm()
    question_obj = Question.objects.get(id=int(request.session['qnumber']))
    choices = Choice.objects.filter(question=question_obj)
    context = {'form' : choice_form, 'choices' : choices}
    if request.method == 'POST':
        print(request.POST)
        choice_form = ChoiceForm(request.POST)

        if choice_form.is_valid:
            choice_form.save()

    return render(request, 'cbts_app/create-choice.html', context)