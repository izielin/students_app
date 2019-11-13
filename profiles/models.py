from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


YEARS = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
)


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    birthdate = models.DateField(null=True, blank=True)
    picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    website = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    year = models.IntegerField(choices=YEARS, default=1)

    def get_website(self):
        if self.website[0:4] != 'http':
            return 'http://' + self.website
        else:
            return self.website

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Student' + ' ' + str(self.user)