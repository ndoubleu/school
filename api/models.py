from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext as _

DAY_OF_THE_WEEK = {
    'monday' : _(u'Monday'),
    'tuesday' : _(u'Tuesday'),
    'wednesday' : _(u'Wednesday'),
    'thursday' : _(u'Thursday'),
    'friday' : _(u'Friday'),
    'saturday' : _(u'Saturday'), 
    'sunday' : _(u'Sunday'),
}
class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=10 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)

class Subject(models.Model):
    subject = models.CharField(max_length=100)
    day = DayOfTheWeekField()
    time = models.TimeField()

    def __str__(self) -> str:
        return f'{self.subject} on {self.day} at {self.time}'

class Group(models.Model):
    group = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return f'{self.group}'
    
class Grade(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.student} got {self.grade} from {self.subject.subject}'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
