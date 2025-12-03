import pytest

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from ..models import Country, City 

def create_country(self, cntry_iso_cde="DEU", popultn=100, areasqkm=101):
    return Country.objects.create(country_iso_code=cntry_iso_cde, population=popultn, area_sq_km=areasqkm)

@pytest.fixture(scope="session")
def valid_country():
    cntry_alb = Country.objects.create(country_iso_code='ALB', population=1000000, area_sq_km=50000)


@pytest.fixture
def create_country_as_a_func(db):  # Use db fixture to access the database
    # Create a test country instance
    country = Country.objects.create(
        country_iso_code="AFG",  # Use a valid country ISO code from COUNTRY_ISO_CODES
        population=100,
        area_sq_km=101
    )
    return country

@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_a(create_country_as_a_func):
    assert create_country_as_a_func.__str__() == create_country_as_a_func.country_iso_code


@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_b(create_country_as_a_func):
    assert create_country_as_a_func.population == 100


@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_c(create_country_as_a_func):
    assert create_country_as_a_func.area_sq_km == 101


@pytest.mark.parametrize('username', ['directly-overridden-username'])
def test_username(username):
	#Temporary only https://docs.pytest.org/en/latest/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization
    assert username == 'directly-overridden-username'


@pytest.mark.parametrize('username', ['directly-overridden-username-other'])
def test_username_other(username):
	#Temporary only https://docs.pytest.org/en/latest/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization
    assert username == 'directly-overridden-username-other'

