from time import strftime
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=128, blank=True, null=True)

    SKILL = 0
    LESSON = 1

    TYPE_CHOICES = [(SKILL, "Skill"), (LESSON,"Lesson")]

    type = models.IntegerField(choices=TYPE_CHOICES, default=SKILL, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=128)
    outcome = models.TextField(max_length=144)
    description = models.TextField(max_length=2**9, blank=True, null=True)
    parent_lesson = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    link = models.URLField(blank=True)
    active = models.BooleanField(default=False)
    skills = models.ManyToManyField('Skill', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=64)
    outcome = models.TextField(max_length=144, null=False)
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    parent_skills = models.ManyToManyField('self', blank=True, symmetrical=False)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def is_learning(self):
        return self.lesson_set.filter(active=True, tags__name='theory').exists()
    
    def is_in_use(self):
        """return true if there's a lesson of type practice (a project) related to this skill that is active."""
        return self.lesson_set.filter(active=True, tags__name='practice').exists()



class TimePeriod(models.Model):
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    outcome = models.TextField(max_length=144, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.lesson.name + ": " + self.start.strftime("%d, %b %Y") + " - " + self.end.strftime("%d, %b %Y")
