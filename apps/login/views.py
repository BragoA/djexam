from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Job, UserJob
import bcrypt

def default(request):
    return render(request, 'djexam/index.html')

def add_user(request):
    errors=User.objects.validator(request.POST)
    if len(errors) == 0:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['id'] = user.id
    else:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    return redirect('/success')

def check(request):
    request.session.clear()
    if User.objects.filter(email=request.POST['email']).count()==0:
        request.session['message'] = 'Email or Password are not applicable'
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/success')
        else:
            request.session['message'] = 'Email or Password are not applicable'
            return redirect('/')


def logged(request):
    context ={
        'logInInfo' : User.objects.get(id = request.session['id']),
        'alljobs' : Job.objects.all()
    }
    print(context)
    return render(request, 'djexam/success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def jobcreate(request):
    return render(request, 'djexam/jobpost.html')

def logjob(request):
    errors=User.objects.post_validator(request.POST)
    if len(errors) == 0:
        user = User.objects.get(id = request.session['id'])
        Job.objects.create(job_name = request.POST['job_name'], job_loc = request.POST['job_loc'], job_desc = request.POST['job_desc'], poster = user)
    else:
        for key, error in errors.items():
            messages.error(request, error)
            return redirect('/createjob')
    return redirect('/success')

def viewjob(request, number):
    request.session['mine'] = 0   
    context = {
        'theJob' : Job.objects.get(id=number)
    }
    return render(request, 'djexam/jobview.html', context)

def viewmyjob(request, number):
    request.session['mine'] = 1
    context = {
        'theJob' : UserJob.objects.get(id=number)
    }
    return render(request, 'djexam/jobview.html', context)


def addjob(request, number):
    recipient = User.objects.get(id = request.session['id'])
    thejob = Job.objects.get(id = number)
    UserJob.objects.create(job_name = thejob.job_name, job_loc = thejob.job_loc, job_desc = thejob.job_desc, created_at=thejob.created_at, poster=recipient)
    thejob.delete()
    return redirect('/success')

def editjob(request, number):
    context = {
        'theJob' : Job.objects.get(id = number)
    }
    return render(request, 'djexam/jobedit.html', context)

def makeedit(request):
    errors=User.objects.post_validator(request.POST)
    jobId = request.POST['jobId']
    if len(errors) == 0:
        editing = Job.objects.get(id = request.POST['jobId'])
        editing.job_name = request.POST['job_name']
        editing.job_desc = request.POST['job_desc']
        editing.job_loc = request.POST['job_loc']
        editing.save()
    else:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect(f'/{jobId}/edit')
    return redirect('/success')

def canceljob(request, number):
    job = Job.objects.get(id = number)
    job.delete()
    return redirect('/success')

def finishjob(request, number):
    job = UserJob.objects.get(id=number)
    job.delete()
    return redirect('/success')

# Create your views here.
