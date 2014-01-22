#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import weathercli as weather


class FakeURLOpen(object):
    def __init__(self, *args):
        pass


class BeverlyHillsResponse(FakeURLOpen):
    def read(self):
        return '{"coord":{"lon":-118.41,"lat":34.1},"sys":{"message":0.1914,"country":"United States of America","sunrise":1390402573,"sunset":1390439679},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"base":"gdps stations","main":{"temp":65.16,"humidity":30,"pressure":1018,"temp_min":53.6,"temp_max":72},"wind":{"speed":1.75,"deg":24.5007},"clouds":{"all":76},"dt":1390361961,"id":5328041,"name":"Beverly Hills","cod":200}'


class ChelseaResponse(FakeURLOpen):
    def read(self):
        return '{"coord":{"lon":3.96,"lat":49.57},"sys":{"message":0.0964,"country":"France","sunrise":1390375685,"sunset":1390407819},"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"02n"}],"base":"gdps stations","main":{"temp":35.56,"temp_min":35.56,"temp_max":35.56,"pressure":1007.62,"sea_level":1023.84,"grnd_level":1007.62,"humidity":96},"wind":{"speed":9.31,"deg":162.001},"clouds":{"all":8},"dt":1390362722,"id":3007477,"name":"Sissonne","cod":200}'


class BadResponse(FakeURLOpen):
    def read(self):
        return '['


class LocationNotFoundResponse(FakeURLOpen):
    def read(self):
        return '{"message":"Error: Not found city","cod":"404"}'


class PostalCodeTestCase(unittest.TestCase):

    def setUp(self):
        self.weather = weather.Weather()

    def test_postal_code_90210(self):
        weather.urllib.urlopen = BeverlyHillsResponse
        self.assertEquals(self.weather.now('90210'), u"It's 65\u00B0 and broken clouds")

    def test_postal_code_02150(self):
        weather.urllib.urlopen = ChelseaResponse
        self.assertEquals(self.weather.now('02150'), u"It's 35\u00B0 and sky is clear")


class MalformedResponseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.weather = weather.Weather()

    def test_bad_xml_response(self):
        weather.urllib.urlopen = BadResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, 'foobar')


class ElementsNotFoundTestCase(unittest.TestCase):
    
    def setUp(self):
        self.weather = weather.Weather()

    def test_missing_current_conditions(self):
        weather.urllib.urlopen = LocationNotFoundResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, 'there is no here here')


class GetTempColorTestCase(unittest.TestCase):
    
    def test_temp_is_blue(self):
        self.assertEquals(weather.get_temp_color("It's 45 degrees and snowing"), 'blue')

    def test_temp_is_yellow(self):
        self.assertEquals(weather.get_temp_color("It's 70 degrees and sunny"), 'yellow')

    def test_temp_is_magenta(self):
        self.assertEquals(weather.get_temp_color("It's 100 degrees and sunny"), 'red')

    def test_minus_10(self):
        self.assertEquals(weather.get_temp_color("It's -10 degrees and snowing"), 'cyan')


if __name__ == '__main__':
    unittest.main()
