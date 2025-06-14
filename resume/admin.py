from django.contrib import admin
from .models import SiteConfiguration, Skill, SkillCategory, Interest, Testimonial, Service, Project, ProjectImage, Certificate, Education, WorkExperience

# Register your models here.

admin.site.register(SiteConfiguration)
admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(Interest)
admin.site.register(Testimonial)
admin.site.register(Service)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Certificate)
admin.site.register(Education)
admin.site.register(WorkExperience)