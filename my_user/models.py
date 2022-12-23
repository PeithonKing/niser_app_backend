from django.db import models
from django.core.mail import mail_admins
from authtools.models import User
from django.utils import timezone


class School(models.Model):
    abbr = models.CharField(max_length = 5)  # abbreviation of the school
    name = models.CharField(max_length = 256)  # full name of the school
    appr = models.BooleanField(default=False)  # approval status of the school

    def __str__(self):
        return self.name + ' ('+ self.abbr.upper() + ')'

class Course(models.Model):
    op = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)  # person who suggested the opening of the course
    code    = models.CharField('Code', max_length=6, unique=True)  # 4-6 digit course code
    name    = models.CharField('Name', max_length=128)  # name of the course (can contain spaces)
    school  = models.ForeignKey(School, on_delete=models.CASCADE)  # school in which the course is offered
    appr = models.BooleanField(default=False)  # approval status of the course

    def __str__(self):
        return (self.code.upper() + ' - ' + self.name)

    def save(self, *args, **kwargs):
        if self.appr == False:
            mail_admins(
                subject = 'New Course Needs Approval.',
                message = f'A new course "{self}" was added by {self.op} on the NISER Archive. It is pending approval.')

        super().save(*args, **kwargs)

class Profile(models.Model):
    # PROFILE
    # 	1. A profile has a one to one relationship with a user instance.
    # 		i.e.: There is an inbuilt class User in Django which is used to store user data.
    # 		We found some of its features useful and wanted to use it. Now, it doesn't meet
    # 		all our required features (it only stores username, password, email, etc.) and
    #       we wanted to add more fields to it. So, we created a new
    # 		class Profile which has a one to one relationship with the User class (this is
    # 		how it's done). This means that every user has a profile and every profile has
    # 		a user. Whenever a person creates an account, two instances are created: one
    # 		Profile and one User and the User gets attached to the Profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #   2. Profile Picture of the user
    dp = models.ImageField(upload_to='static/profile_pictures', default="/static/profile_pictures/anonymous.png")
    # 	3. vid is a unique id for the user
    vid = models.CharField(max_length=64, null=True)
    # 	4. ip stores the IP address of the user
    ip = models.GenericIPAddressField(null=True)
    # 	5. joined stores the date and time when the user joined
    joined = models.DateTimeField(default=timezone.now)
    # 	6. IDK what data is used for or even if it's used at all
    data = models.TextField(max_length=2048, null=True, blank=True)
    # 	7. The school the user is from
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.SET_NULL)
    # 	8. The batch the user is from
    batch = models.SmallIntegerField('Batch', blank=True, null=True)
    # 	9. The program the user is in (Int. MSc/ PhD/ etc.)
    prog = models.CharField('Program', max_length=128, blank=True, default='')
    # 	10. About the user
    about = models.TextField('About', max_length=2048, blank=True, default='')
    # 	11. The karma of the user, which is not used I guess
    karma = models.IntegerField(default=0)
    #   12. The Gender of the user
    gender = models.CharField(max_length=16, choices=[("M", "Male"), ("F", "Female"), ("O", "Others"), ("---", "---")], default="---")


    # NISER CANTEEN MENU
    # ... features/fields related to canteen menu ...
    fav_foods = models.ManyToManyField("canteen_menu.FoodItem", blank=True)


    # NISER TIMETABLE
    # ... features/fields related to timetable ...
    courses = models.ManyToManyField("Course", blank=True)


    # NISER LISTINGS
    # ... features/fields related to listings ...


    # LOST AND FOUND
    # ... features/fields related to lost and found ...
    
    
    
    def __str__(self):
        return self.user.name

