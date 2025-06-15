from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F
from turbodrf.mixins import TurboDRFMixin


from .model_static_data import COUNTRY_ISO_CODES, HIGHEST_POINT_ON_LAND, LOWEST_POINT_ON_LAND
from .models_utils import validate_not_divisible_by_seven, validate_even
 

class Country(models.Model, TurboDRFMixin):
    '''
    Represents a Country.
    '''

    COUNTRIES = COUNTRY_ISO_CODES

    country_iso_code = models.CharField(max_length=3, choices = COUNTRIES)
    population = models.IntegerField()
    area_sq_km = models.IntegerField()


    class Meta:
        verbose_name_plural = "Countries"


    def __str__(self):
        return self.country_iso_code

    @classmethod
    def turbodrf(cls):
        return {
            'fields': ['country_iso_code', 'population', 'area_sq_km']
        }


class CityManager(models.Manager):
    def get_queryset(self):
        # Annotate the queryset with the country_iso_code from the related Country model
        return super().get_queryset().annotate(
            country_iso_code=F('country__country_iso_code')
        )


class City(models.Model, TurboDRFMixin):
    '''
    Represents a City.
    '''
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    mayor_name = models.CharField(max_length=255)
    date_of_last_mayoral_election = models.DateField(null=True, blank=True)
    population = models.IntegerField()
    area_sq_km = models.IntegerField(null=True, blank=True, validators=[validate_not_divisible_by_seven, validate_even])
    elevation_metres = models.IntegerField(null=True, blank=True)
    some_number = models.IntegerField(blank=True, null=True)

    objects = CityManager()


    class Meta:
        verbose_name_plural = "Cities"

    @classmethod
    def turbodrf(cls):
        return {
            'fields': {
                'list': ['country', 'city_name', 'mayor_name', 'date_of_last_mayoral_election', 'population', 'area_sq_km', 'elevation_metres', 'some_number' ]
            }
        }

    def clean(self):

        if (self.elevation_metres is not None):
            if (self.elevation_metres > HIGHEST_POINT_ON_LAND):
                raise ValidationError("Elevation is higher than any point on earth.")

        if (self.elevation_metres is not None):
            if (self.elevation_metres < LOWEST_POINT_ON_LAND):
                raise ValidationError("Elevation is lower than any point on earth.")

        today = date.today()

        if (self.date_of_last_mayoral_election is not None):
            if (self.date_of_last_mayoral_election > today):
                raise ValidationError("Date of Last Mayoral Election is after today. If provided, it must be today, or earlier")


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city_name} ({self.country.country_iso_code})"
        #return f"{self.city_name}"

