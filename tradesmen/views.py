from django.shortcuts import render, redirect
from .models import Job, Category
from .forms import JobForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
#part added for customer service
from django.core.mail import send_mail
from .forms import CustomerServiceForm
#login part
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import UserRegistrationForm
from .models import User


def customer_service(request):
    if request.method == 'POST':
        form = CustomerServiceForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                'Customer Service',
                f'Email: {email}\nMessage: {message}',
                'tradehub.dz@gmail.com',
                ['tradehub.dz@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'customer_service_success.html')
    else:
        form = CustomerServiceForm()
    
    return render(request, 'customer_service.html', {'form': form})
#******************************************

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # Set the user for the job
            job.save()

            job_data = {
                'title': job.title,
                'description': job.description,
                'profile_image': job.profile_image.url if job.profile_image else '',
                'label': job.label,
                'posted': job.posted.strftime('%Y-%m-%d')
            }

            return JsonResponse({'job': job_data})
        else:
            return JsonResponse({'error': 'Invalid form data'})

    return JsonResponse({'error': 'Invalid request method'})

@login_required
def delete_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.user != request.user:
            raise PermissionDenied("You don't have permission to delete this job.")

        job.delete()
        return JsonResponse({'message': 'Job deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})



def index(request):
    jobs = Job.objects.all().order_by('-posted')
    return render(request, 'index.html', {'jobs': jobs})
#registration form

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration.html', {'form': form})


def user_page(request, username):
    user = User.objects.get(username=username)
    jobs = user.jobs.all()
    context = {'user': user, 'jobs': jobs}
    return render(request, 'tradesmen/user_page.html', context)