from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from my_user.models import Profile

class Item(models.Model):
    kind = models.CharField(max_length = 200, default = 'Lost',
            choices = [('Lost', 'Lost'), ('Found', 'Found')],
            verbose_name = 'Lost/Found')
    location = models.CharField(max_length = 200)

    date = models.DateField(default = now, verbose_name = 'Lost on')
    created = models.DateTimeField(default = now)

    category = models.CharField(max_length = 200, verbose_name='Category')
    desc = models.TextField(verbose_name = 'Description of the Item')
    image = models.ImageField(upload_to='static/lnf/pics', blank = True, null = True)
    claimed = models.BooleanField(default = False)

    submitter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created', '-date']

    def __str__(self):
        return f"{self.kind} {self.category} at {self.location} on {self.date.strftime('%a, %d %b %Y')}"
        # return (self.kind + '. ' + str(self.category) + '. ' + self.location + '. ' + self.date.strftime("%a, %d %b %Y")) + '.'
    def name(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('main:item', kwargs={'pk': self.pk})
