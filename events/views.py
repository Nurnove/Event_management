from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventForm,CategoryForm,ParticipantForm
from events.models import Event,Participant,Category
from datetime import date
from django.contrib import messages
from django.db.models import Q, Count, Max, Min, Avg
from django.utils.timezone import now



def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('Participants')

    query = request.GET.get('q')
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)

    return render(request, 'event_list.html', {'events': events})

def event_detail(request, id):
    event = Event.objects.prefetch_related('Participants').filter(id=id).first()
    if event is None:
        pass
    return render(request, 'event_detail.html', {'event': event})


def event_create(request):
    form=EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('event_create')
            
    return render(request,"eventform.html",{"form":form})

def event_update(request, id):
    event = Event.objects.filter(id=id).first()
    if not event:
         return redirect('event_list')
    form = EventForm(instance=event)
    if request.method == "POST":
         form = EventForm(request.POST, instance=event)
         if form.is_valid():

            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event_list')
    return render(request, 'eventform.html', {'form': form})

def event_delete(request, id):
    if request.method == 'POST':
         event = Event.objects.get(id=id)
         event.delete()
         return redirect('event_list')
    return redirect('event_list')

def participant_list(request):
    participants = Participant.objects.prefetch_related('event')
    return render(request, 'participant_list.html', {'participants': participants})

def participant_create(request):
    form=ParticipantForm()
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('participant_list')
            
    return render(request, 'participant_form.html', {'form': form})

def dashboard(request):
    today = now().date()
    type = request.GET.get('type', 'today')

    if type == 'upcoming':
        events = Event.objects.filter(date__gt=today)
        event_list_title = "Upcoming Events"
    elif type == 'past':
        events = Event.objects.filter(date__lt=today)
        event_list_title = "Past Events"
    elif type == 'total':
        events = Event.objects.all()
        event_list_title = "All Events"
    else:
        events = Event.objects.filter(date=today)
        event_list_title = "Today's Events"

    context = {
        'total_participants': Participant.objects.count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gt=today).count(),
        'past_events': Event.objects.filter(date__lt=today).count(),
        'events': events,
        'event_list_title': event_list_title,
    }
    return render(request, 'dashboard.html',context)


         
    
    

# Create your views here.
