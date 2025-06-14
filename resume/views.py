from django.shortcuts import render, get_object_or_404, redirect
from .models import SiteConfiguration, Skill, Interest, Testimonial, Service, Project, WorkExperience, Education, Certificate, SkillCategory
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
# Create your views here.
def home(request):
    config = SiteConfiguration.load()
    return render(request, 'index.html', {'config': config})


def about(request):
    config = SiteConfiguration.load()
    skills = Skill.objects.all().order_by('order')
    interests = Interest.objects.all()
    testimonial = Testimonial.objects.all()
    context = {
        'config': config,
        'skills': skills,
        'interests': interests,
        'testimonial': testimonial,
        }
    return render(request, 'about.html', context)


def services(request):
    service = Service.objects.all()
    return render(request, 'services.html', {'service': service})


def projects(request):
    projects = Project.objects.all().prefetch_related('technologies', 'images')
    return render(request, 'projects.html', {'projects': projects})


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('technologies', 'images'), slug=slug)
    return render(request, 'project_detail.html', {'project': project})

def resume(request):
    context = {
        'config': SiteConfiguration.load(),
        'work_experiences': WorkExperience.objects.all(),
        'educations': Education.objects.all(),
        'certificates': Certificate.objects.all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skill_set').all(),
    }
    return render(request, 'resume.html', context)

from django.contrib.messages import get_messages
def contact(request):
    config = SiteConfiguration.load()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                subject=f"New Contact Form Submission: {form.cleaned_data['subject']}",
                message=f"""
                    Name: {form.cleaned_data['name']}
                    Email: {form.cleaned_data['email']}
                    Message: {form.cleaned_data['message']}
                    """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # or your named URL
    else:
        form = ContactForm()

    storage = get_messages(request)
    return render(request, 'contact.html', {
        'form': form,
        'config': config,
        'messages': storage
    })
