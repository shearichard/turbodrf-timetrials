import pprint
#
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
import pytest
#
from assidu.models import Country, City 
from assidu.forms import CityForm 

# models test
class CityTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.AUS = Country.objects.create(country_iso_code="AUS", population=500, area_sq_km=1000)
        cls.NZL = Country.objects.create(country_iso_code="NZL", population=500, area_sq_km=1000)
        cls.USA = Country.objects.create(country_iso_code="USA", population=500, area_sq_km=1000)


    def create_country(self, 
            cntry_iso_cde="DEU", 
            popultn=100, 
            areasqkm=102):
        #
        c = Country.objects.create(country_iso_code=cntry_iso_cde, population=popultn, area_sq_km=areasqkm)
        return c


    def create_city(self, 
            cntry_parent = None, 
            cntry_iso_cde = "", 
            city_nme = "", 
            myr_nme = "", 
            dt_of_lst_myr_elect = "", 
            pop = "", 
            areasqkm = "", 
            elev_m = "", 
            sm_nmbr = ""):
        #
        if cntry_parent is None:
            cntry_parent = self.create_country(cntry_iso_cde=cntry_iso_cde, popultn = pop)
        #
        return City.objects.create(
            country = cntry_parent,
            city_name = city_nme,
            mayor_name = myr_nme, 
            date_of_last_mayoral_election = dt_of_lst_myr_elect, 
            population = pop, 
            area_sq_km = areasqkm, 
            elevation_metres = elev_m, 
            some_number = sm_nmbr)


    # Test model
    def test_city_creation(self):
        #
        cntry_parent = self.create_country(cntry_iso_cde="FRA", popultn = 101)
        #
        c = self.create_city(
            cntry_parent = cntry_parent, 
            cntry_iso_cde = "FRA",
            city_nme = "Paris", 
            myr_nme = "Pierre Smith", 
            dt_of_lst_myr_elect = None, 
            pop = "1", 
            areasqkm = "10", 
            elev_m = "10", 
            sm_nmbr = "42")
        #
        city_descriptor = f"{c.city_name} ({cntry_parent.country_iso_code})"
        self.assertTrue(isinstance(c, City))
        self.assertEqual(c.__str__(), city_descriptor)

    # Test views
    def test_city_list_view_setuptestdata_check(self):
        lst_country = Country.objects.all()
        print("test_city_list_view_stripped_down A")
        print(lst_country)
        print("test_city_list_view_stripped_down B")
        #
        self.assertEqual(len(lst_country), 3)

    def test_city_list_view_stripped_down(self):
        url = reverse("city-list")
        resp = self.client.get(url)
        #
        self.assertEqual(resp.status_code, 200)

    def test_city_list_view(self):
        #
        if False:
            cntry_parent = self.create_country(cntry_iso_cde="USA", popultn = 102)

        #
        c = self.create_city(
            cntry_parent = self.USA, 
            cntry_iso_cde = "USA",
            city_nme = "New York", 
            myr_nme = "Jane Jones", 
            dt_of_lst_myr_elect = None, 
            pop = "1", 
            areasqkm = "12", 
            elev_m = "10", 
            sm_nmbr = "42")
        #
        lst_city = City.objects.all()
        print("test_city_list_view A")
        print(len(lst_city))
        print("test_city_list_view B")
        #
        url = reverse("city-list")
        resp = self.client.get(url)
        #
        self.assertEqual(resp.status_code, 200)
        #
        self.assertIn(c.city_name.encode('latin1'), resp.content)
        self.assertIn(str(c.population).encode('latin1'), resp.content)
        self.assertIn(str(c.area_sq_km).encode('latin1'), resp.content)
        self.assertNotIn(b"Moscow", resp.content)
        #
        c = self.create_city(
            cntry_parent = self.USA, 
            cntry_iso_cde = "USA",
            city_nme = "Dallas", 
            myr_nme = "Mahesh Patel", 
            dt_of_lst_myr_elect = None, 
            pop = "1", 
            areasqkm = "2", 
            elev_m = "10", 
            sm_nmbr = "42")
        #
        resp = self.client.get(url)
        #
        self.assertEqual(resp.status_code, 200)
        #
        self.assertIn(str(c.population).encode('latin1'), resp.content)
        self.assertIn(str(c.area_sq_km).encode('latin1'), resp.content)
        self.assertIn(b"Dallas", resp.content)

    # Test forms
    @pytest.mark.skip
    def test_valid_form(self):
        c = City.objects.create(country_iso_code="USA", population=200, area_sq_km=201)
        data = { "country_iso_code": c.country_iso_code, "population": c.population , "area_sq_km": c.area_sq_km }
        #data = { "country": self.USA, "population": c.population , "area_sq_km": 10 }
        form = CityForm(data)
        #
        if form.is_valid():
            pass
        else:
            pprint.pprint(form.errors)
        #
        self.assertTrue(form.is_valid())


    @pytest.mark.skip
    def test_invalid_form_1(self):
        #
        data = { "country_iso_code": "AUS", "population": None , "area_sq_km": None }
        #
        form = CityForm(data)
        #
        if form.is_valid():
            pass
        else:
            pprint.pprint(form.errors)
        #
        self.assertFalse(form.is_valid())


    @pytest.mark.skip
    def test_invalid_form_2(self):
        #
        data = { "country_iso_code": "AUS", "population": None , "area_sq_km": 100}
        #
        form = CityForm(data)
        #
        self.assertEqual(
            list(form.errors["population"]), ["This field is required."]
        )


    @pytest.mark.skip
    def test_invalid_form_3(self):
        #
        data = { "country_iso_code": "AUS", "population": 100, "area_sq_km": None}
        #
        form = CityForm(data)
        #
        self.assertEqual(
            list(form.errors["area_sq_km"]), ["This field is required."]
        )

