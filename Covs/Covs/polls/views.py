from django.contrib  import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
import datetime

from .forms import PollForm, EditPollForm, CandidateForm

from .models import Candidate, Poll, Vote


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def polls_list(request):
                
            #    Renders the pools_list.html template which has 
            #    the list of all the currently available polls
    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format(settings.LOGIN_URL, request.path))
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)

@login_required
def add_poll(request):
    if request.method =="POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            new_candidate1 = Candidate(
                            poll = new_poll,
                            candidate_name = form.cleaned_data['candidate1']
                            ).save()
            new_candidate2 = Candidate(
                            poll = new_poll,
                            candidate_name = form.cleaned_data['candidate2']
                            ).save()
            messages.success(
                request, 
                'Poll and candidates added!',
                extra_tags='alert alert-success alert-dismissible fade show'
                )
            return redirect('polls:list')
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/add_poll.html', context)


@login_required
def delete_poll(request,  poll_id):
    poll   = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
             poll.delete()
             messages.success(
                             request,
                             'Poll Deleted Successfully',
                             extra_tags='alert alert-success alert-dismissible fade show'
                             )
             return redirect('polls:list')
    
    return render(request, 'polls/delete_poll_confirm.html', { 'poll':poll })


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')
    
    if request.method == "POST":
         form = EditPollForm(request.POST, instance=poll)

         if form.is_valid():
             form.save()
             messages.success(
                             request,
                             'Poll Edit Successfull',
                             extra_tags='alert alert-success alert-dismissible fade show'
                             )
             return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)
    
    return render(request, 'polls/edit_poll.html', {'form':form, 'poll':poll })

@login_required
def add_candidate(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')
    
    if request.method == "POST":
         form = CandidateForm(request.POST)
         if form.is_valid():
             new_candidate = form.save(commit=False)
             new_candidate.poll = poll
             new_candidate.save()
             messages.success(
                             request,
                             'candidate Added Successfully',
                             extra_tags='alert alert-success alert-dismissible fade show'
                             )
             return redirect('polls:list')
    else:
        form = CandidateForm() 
    return render(request, 'polls/add_candidate.html', {'form': form})

@login_required
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(candidate, id=candidate_id)
    poll   = get_object_or_404(Poll, id=candidate.poll.id)
    if request.user != poll.owner:
        return redirect('/')
    
    if request.method == "POST":
         form = CandidateForm(request.POST, instance=candidate)
         if form.is_valid():
             form.save()
             messages.success(
                             request,
                             'candidate Edited Successfully',
                             extra_tags='alert alert-success alert-dismissible fade show'
                             )
             return redirect('polls:list')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'polls/add_candidate.html', {'form':form, 'edit_mode': True, 'candidate':candidate})

@login_required
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(candidate, id=candidate_id)
    poll   = get_object_or_404(Poll, id=candidate.poll.id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
             candidate.delete()
             messages.success(
                             request,
                             'candidate Deleted Successfully',
                             extra_tags='alert alert-success alert-dismissible fade show'
                             )
             return redirect('polls:list')
    
    return render(request, 'polls/delete_candidate_confirm.html', { 'candidate':candidate })

@login_required
def poll_detail(request, poll_id):

            #    Render the poll_detail.html template
            #     which allows a user to vote on th candidates of a poll

            # poll = Poll.objects.get(id=poll_id)
                

    poll = get_object_or_404(Poll,id=poll_id)
    user_can_vote = poll.user_can_vote(request.user)
    context = { 'poll':poll, 'user_can_vote':user_can_vote}
    return render(request, 'polls/poll_detail.html', context)

def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll,id=poll_id)
    if not poll.user_can_vote(request.user):
         messages.error(request,
                             'Can not vote more than once, already voted for ',
                             extra_tags='alert alert-danger  alert-dismissible fade show'
                             )
         return HttpResponseRedirect(reverse("polls:detail", args=(poll_id,)))

    candidate_id = request.POST.get('candidate')
    if candidate_id:
        candidate = Candidate.objects.get(id=candidate_id)
        new_vote =Vote(user=request.user, poll=poll, candidate=candidate)
        new_vote.save()
        candidate.votes += 1
        candidate.save()
    else:
        messages.error(request,'You have not yet voted for ')
        return HttpResponseRedirect(reverse("polls:detail", args=(poll_id,)))
    return redirect('polls:list')

def all_results(request):
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/results.html', context)