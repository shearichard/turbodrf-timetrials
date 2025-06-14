import pytest

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from ..models import Country, City 


@pytest.fixture(scope="session")
def valid_country():
    cntry_alb = Country.objects.create(country_iso_code='ALB', population=1000000, area_sq_km=50000)


@pytest.fixture(scope="module")
def create_country_as_a_func(title="only a test", body="yes, this is only a test"):
    x = Country.objects.create(country_iso_code='USA', population=1000000, area_sq_km=50000)
    print(type(x))
    #import pdb;pdb.set_trace()
    return x

@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_a(create_country):
    assert create_country.__str__() ==  create_country.country_iso_code


@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_b(create_country):
    assert create_country.population == 100


@pytest.mark.django_db
def test_country_creation_as_a_function_new_style_fixtures_c(create_country):
    assert create_country.area_sq_km== 101


@pytest.mark.parametrize('username', ['directly-overridden-username'])
def test_username(username):
	#Temporary only https://docs.pytest.org/en/latest/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization
    assert username == 'directly-overridden-username'

@pytest.mark.parametrize('username', ['directly-overridden-username-other'])
def test_username_other(other_username):
	#Temporary only https://docs.pytest.org/en/latest/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization
    assert other_username == 'other-directly-overridden-username-other'

