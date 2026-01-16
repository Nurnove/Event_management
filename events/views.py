from django.shortcuts import render,redirect
from events.forms import EventForm,CategoryForm
from events.models import Event,Category,RSVP
from django.contrib.auth.models import User
from datetime import date
from django.contrib import messages
from django.db.models import Q, Count
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from users.views import is_admin,is_organizer,is_participant





@login_required
def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants')

    query = request.GET.get('q')
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    user_groups = set(
        request.user.groups.values_list('name', flat=True)
    )    
    organizer_or_admin= 'Admin' in user_groups or 'Organizer' in user_groups


    
    

    return render(request, 'event_list.html', {'events': events , "organizer_or_admin":organizer_or_admin})
# @login_required
# def event_detail(request, id):
#     event = Event.objects.prefetch_related('User').filter(id=id).first()
#     if event is None:
#         pass
#     return render(request, 'event_detail.html', {'event': event})

@login_required
@permission_required('events.add_event', login_url='no_permission')
def event_create(request):
    form=EventForm()
    
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():

            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('event_create')
            
    return render(request,"eventform.html",{"form":form })


@login_required
@permission_required('events.change_event', login_url='no_permission')
def event_update(request, id):
    event = Event.objects.filter(id=id).first()
    if not event:
         return redirect('event_list')
    form = EventForm(instance=event)
    if request.method == "POST":
         form = EventForm(request.POST,request.FILES, instance=event)
         if form.is_valid():

            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event_list')
    return render(request, 'eventform.html', {'form': form})


@login_required
@permission_required('events.delete_event', login_url='no_permission')
def event_delete(request, id):
    if request.method == 'POST':
         event = Event.objects.get(id=id)
         event.delete()
         return redirect('event_list')
    return redirect('event_list')

@login_required
@user_passes_test(is_admin,login_url='no_permission')
def participant_list(request):
    participants = User.objects.prefetch_related('events').all()
    return render(request, 'participant_list.html', {'participants': participants})

# def participant_create(request):
#     form=ParticipantForm()
#     if request.method == "POST":
#         form = ParticipantForm(request.POST)
#         if form.is_valid():

#             form.save()
#             return redirect('participant_list')
            
#     return render(request, 'participant_form.html', {'form': form})

@login_required
@user_passes_test(is_admin,login_url='no_permission')
def delete_participant(request,id):
    if request.method == "POST":
        participant=User.objects.get(id=id)
        participant.delete()
        return redirect('participant_list')
    return redirect('participant_list')



@login_required
@permission_required('events.change_category',login_url='no_permission')
def category_list(request):
    categories = Category.objects.all()
    
    return render(request,'category_list.html',{"categories":categories})

@login_required
@permission_required('events.add_category',login_url='no_permission')
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('add_category')
    return render(request, "category_form.html", {"form": form})

@login_required
@permission_required('events.change_category',login_url='no_permission')
def update_category(request,id):
    category=Category.objects.get(id=id)
    form=CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category update successfully.")
            return redirect('category_list')
    return render(request, "category_form.html", {"form": form})


@login_required
@permission_required('events.delete_category',login_url='no_permission')
def delete_category(request,id):
    if request.method == 'POST':
         category=Category.objects.get(id=id)
         category.delete()
         return redirect('category_list')
    return redirect('category_list')

@login_required
def rsvp_event(request, id):
    if request.method == 'POST':
        event =Event.objects.get(id=id)

        rsvp, created = RSVP.objects.get_or_create(
        user=request.user,
        event=event
        )

        if created:
            messages.success(request, "RSVP successful! Confirmation email sent.")
        else:
            messages.info(request, "You already RSVP'd for this event.")
    

        return redirect('event_list')
    
@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')

    return redirect('no_permission')

@login_required
@user_passes_test(is_organizer, login_url='no_permission')
def organizer_dashboard(request):
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
        
    event_count = Event.objects.aggregate(
    total_events=Count('id'),
    upcoming_events=Count('id', filter=Q(date__gt=today)),
    past_events=Count('id', filter=Q(date__lt=today)),
)

    context = {
        'total_participants': User.objects.count(),
        'event_count': event_count,
        'events': events,
        'event_list_title': event_list_title,
    }
    return render(request, 'dashboard/organizer_dashboard.html',context)
 
@login_required 
@user_passes_test(is_participant, login_url='no_permission') 
def participant_dashboard(request): 
    events = (
    Event.objects
    .filter(rsvp__user=request.user)
    .select_related('category')
    .prefetch_related('participants')
    
    )

    return render(request, 'dashboard/participant_dashboard.html', { 'events': events })   

# Create your views here.
