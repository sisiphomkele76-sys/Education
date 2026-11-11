from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import UserProfile, MedicationReminder, PrescribedMedication, TreatmentResource, Blog
from .forms import UserRegistrationForm, MedicationReminderForm

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, preferred_language=form.cleaned_data['preferred_language'])
            login(request, user)
            messages.success(request, "Akaunti yakho ivulwe ngempumelelo!")
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    reminders = MedicationReminder.objects.filter(user=request.user, is_active=True)
    prescribed_meds = PrescribedMedication.objects.all()
    
    if request.method == 'POST':
        form = MedicationReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, "Isikhumbuzo samayeza sigciniwe!")
            return redirect('profile')
    else:
        form = MedicationReminderForm()

    context = {
        'profile': request.user.profile,
        'reminders': reminders,
        'prescribed_meds': prescribed_meds,
        'form': form
    }
    return render(request, 'profile.html', context)

@login_required
def delete_reminder_view(request, reminder_id):
    reminder = get_object_or_404(MedicationReminder, id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, "Isikhumbuzo sisusiwe.")
    return redirect('profile')

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_cms_view(request):
    resources = TreatmentResource.objects.all()
    meds = PrescribedMedication.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_resource':
            res_id = request.POST.get('id')
            TreatmentResource.objects.filter(id=res_id).delete()
            messages.success(request, "Outdated information removed successfully.")
            return redirect('admin_cms')

    return render(request, 'admin_cms.html', {'resources': resources, 'meds': meds})