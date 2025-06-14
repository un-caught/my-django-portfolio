from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField

# Create your models here.

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Israel's Portfolio")
    owner_name = models.CharField(max_length=100, default="Israel Korodele")
    bio = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    profile_image = CloudinaryField('image', blank=True, null=True)

    def save(self, *args, **kwargs):
        #Ensure only one instance exists
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
        
    def __str__(self):
        return "Site Configuration"
    

class SkillCategory(models.Model):
    """Categories for grouping skills (e.g., Frontend, Backend, DevOps)"""
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    """Technical skills to display"""
    name = models.CharField(max_length=50)
    category = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, blank=True)
    proficiency = models.PositiveIntegerField(default=50, help_text="Scale of 1-100")
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects showcase"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Skill)
    featured_image = CloudinaryField('image', null=True)  # Main featured image
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_completed']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')
    alt_text = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"
    

class WorkExperience(models.Model):
    """Professional experience timeline"""
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.position} at {self.company}"

class Education(models.Model):
    """Education history"""
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"

class Certificate(models.Model):
    """Professional certifications"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    """Client/colleague testimonials"""
    author = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    author_image = CloudinaryField('image', blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Testimonial from {self.author}"
    

class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome class or custom icon")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name



class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        help_text="Bootstrap Icon class name, e.g., 'bi-code-slash'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
