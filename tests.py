#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

import mock

import weathercli

weather = weathercli.Weather()


class WeatherTestCase(unittest.TestCase):

    def test_it_passes_query_to_url(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 1
                },
                'weather': [
                    {
                        'description': 'abc'
                    },
                ],
            })

            weather.now('chelsea,ma')

            mock_urlopen.assert_called_with('http://api.openweathermap.org/data/2.5/weather?q=chelsea%2Cma&units=imperial')

    def test_it_passes_units_along_to_query(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 1
                },
                'weather': [
                    {
                        'description': 'abc'
                    },
                ],
            })

            weather.now('chelsea,ma', units='metric')

            mock_urlopen.assert_called_with('http://api.openweathermap.org/data/2.5/weather?q=chelsea%2Cma&units=metric')

    def test_it_raises_an_error_when_given_a_bad_response(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{'

            with self.assertRaises(weathercli.WeatherDataError) as cm:
                weather.now('chelsea,ma')

            self.assertEquals(cm.exception.message, "Malformed response from weather service")

    def test_it_raises_an_error_when_elements_arent_found(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{}'

            with self.assertRaises(weathercli.WeatherDataError) as cm:
                weather.now('chelsea,ma')

            self.assertEquals(cm.exception.message, "No conditions reported for your search")

    def test_it_returns_the_weather_conditions(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 35
                },
                'weather': [
                    {
                        'description': 'sky is clear'
                    },
                ],
            })

            self.assertEquals(weather.now('chelsea,ma'), u"It's 35\u00B0 and sky is clear")


class GetTempColorTestCase(unittest.TestCase):
    
    def test_temp_is_blue(self):
        self.assertEquals(weathercli.get_temp_color("It's 45 degrees and snowing"), 'blue')

    def test_temp_is_yellow(self):
        self.assertEquals(weathercli.get_temp_color("It's 70 degrees and sunny"), 'yellow')

    def test_temp_is_magenta(self):
        self.assertEquals(weathercli.get_temp_color("It's 100 degrees and sunny"), 'red')

    def test_minus_10(self):
        self.assertEquals(weathercli.get_temp_color("It's -10 degrees and snowing"), 'cyan')


if __name__ == '__main__':
    unittest.main()
