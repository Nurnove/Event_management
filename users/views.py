from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm,LoginForm,AssignRoleForm,CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event,Category

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()
    
@login_required
@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_events': Event.objects.count(),
        'total_categories': Category.objects.count(),
        'total_participants': User.objects.filter(groups__name='Participant').count(),
    }
    return render(request, 'admin/admin_dashboard.html', context)

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, id, token):
    try:
        user = User.objects.get(id=id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')

@login_required
@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request,id):
    user = User.objects.get(id=id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


@login_required
@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form=CreateGroupForm()  
    if request.method == "POST":
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create_group')

    return render(request, 'admin/create_group.html', {'form': form})

 