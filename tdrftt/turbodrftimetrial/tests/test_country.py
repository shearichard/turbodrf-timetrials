import pprint
#
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
#
from assidu.models import Country, City 
from assidu.forms import CountryForm 

# models test
class CountryTest(TestCase):

    def create_country(self, cntry_iso_cde="DEU", popultn=100, areasqkm=101):
        return Country.objects.create(country_iso_code=cntry_iso_cde, population=popultn, area_sq_km=areasqkm)

    # Test model
    def test_city_creation(self):
        c = self.create_country()
        self.assertTrue(isinstance(c, Country))
        self.assertEqual(c.__str__(), c.country_iso_code)

    # Test views
    def test_country_list_view(self, cntry_iso_cde="DEU", popultn=100, areasqkm=101):
        url = reverse("country-list")
        #
        c = Country.objects.create(country_iso_code=cntry_iso_cde, population=popultn, area_sq_km=areasqkm)
        resp = self.client.get(url)
        #
        self.assertEqual(resp.status_code, 200)
        #
        self.assertIn(c.country_iso_code.encode('latin1'), resp.content)
        self.assertIn(str(c.population).encode('latin1'), resp.content)
        self.assertIn(str(c.area_sq_km).encode('latin1'), resp.content)
        self.assertNotIn(b"FRA", resp.content)
        #
        c = Country.objects.create(country_iso_code="FRA", population=200, area_sq_km=201)
        resp = self.client.get(url)
        #
        self.assertEqual(resp.status_code, 200)
        #
        self.assertIn(c.country_iso_code.encode('latin1'), resp.content)
        self.assertIn(str(c.population).encode('latin1'), resp.content)
        self.assertIn(str(c.area_sq_km).encode('latin1'), resp.content)
        self.assertIn(b"FRA", resp.content)

    # Test forms
    def test_valid_form(self):
        c = Country.objects.create(country_iso_code="USA", population=200, area_sq_km=201)
        data = { "country_iso_code": c.country_iso_code, "population": c.population , "area_sq_km": c.area_sq_km }
        form = CountryForm(data)
        #
        if form.is_valid():
            pass
        else:
            pprint.pprint(form.errors)
        #
        self.assertTrue(form.is_valid())


    def test_invalid_form_1(self):
        #
        data = { "country_iso_code": "AUS", "population": None , "area_sq_km": None }
        #
        form = CountryForm(data)
        #
        if form.is_valid():
            pass
        else:
            pprint.pprint(form.errors)
        #
        self.assertFalse(form.is_valid())


    def test_invalid_form_2(self):
        #
        data = { "country_iso_code": "AUS", "population": None , "area_sq_km": 100}
        #
        form = CountryForm(data)
        #
        self.assertEqual(
            list(form.errors["population"]), ["This field is required."]
        )


    def test_invalid_form_3(self):
        #
        data = { "country_iso_code": "AUS", "population": 100, "area_sq_km": None}
        #
        form = CountryForm(data)
        #
        self.assertEqual(
            list(form.errors["area_sq_km"]), ["This field is required."]
        )

