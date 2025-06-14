from django.db import models

# Create your models here.

class Country(models.Model):
    '''
    Represents a Country.

    NB: This model will only exist for a short time while
    some aspects of pytest are sorted out
    '''

    COUNTRIES = COUNTRY_ISO_CODES

    country_iso_code = models.CharField(max_length=3, choices = COUNTRIES)
    population = models.IntegerField()
    area_sq_km = models.IntegerField()


    class Meta:
        verbose_name_plural = "Countries"


    def __str__(self):
        return self.country_iso_code


def validate_not_divisible_by_seven(value):
    if (value is not None):
        if value % 7 == 0:
            raise ValidationError(
                "%(value)s is divisible by seven",
                params={"value": value},
                )


def validate_even(value):
    if (value is not None):
        if value % 2 != 0:
            raise ValidationError(
                "%(value)s is not an even number",
                params={"value": value},
                )


class CityManager(models.Manager):
    def get_queryset(self):
        # Annotate the queryset with the country_iso_code from the related Country model
        return super().get_queryset().annotate(
            country_iso_code=F('country__country_iso_code')
        )


class City(models.Model):
    '''
    Represents a City.

    NB: This model will only exist for a short time while
    some aspects of pytest are sorted out
    '''
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    mayor_name = models.CharField(max_length=255)
    date_of_last_mayoral_election = models.DateField(null=True, blank=True)
    population = models.IntegerField()
    area_sq_km = models.IntegerField(null=True, blank=True, validators=[validate_not_divisible_by_seven, validate_even])
    elevation_metres = models.IntegerField(null=True, blank=True)
    some_number = models.IntegerField(blank=True, null=True)
    '''
    @property
    def country_iso_code(self):
        return self.country.country_iso_code if self.country else None
    '''

    objects = CityManager()


    class Meta:
        verbose_name_plural = "Cities"


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

