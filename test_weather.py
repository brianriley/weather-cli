#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import mock
import pytest

import weathercli

weather = weathercli.Weather()


class DescribeWeather:

    def it_passes_query_to_url(self):
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

    def it_passes_units_along_to_query(self):
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

    def it_raises_an_error_when_given_a_bad_response(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{'

            with pytest.raises(weathercli.WeatherDataError) as cm:
                weather.now('chelsea,ma')

            assert cm.value.message == "Malformed response from weather service"

    def it_raises_an_error_when_elements_arent_found(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{}'

            with pytest.raises(weathercli.WeatherDataError) as cm:
                weather.now('chelsea,ma')

            assert cm.value.message == "No conditions reported for your search"

    def it_returns_the_weather_conditions(self):
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

            assert weather.now('chelsea,ma') == u"It's 35\u00B0 and sky is clear"


class DescribeGetTempColor:
    
    def it_is_blue_when_cold(self):
        assert weathercli.get_temp_color("It's 45 degrees and snowing") == 'blue'

    def it_is_yellow_when_warm(self):
        assert weathercli.get_temp_color("It's 70 degrees and sunny") == 'yellow'

    def it_is_magenta_when_hot(self):
        assert weathercli.get_temp_color("It's 100 degrees and sunny") == 'red'

    def it_is_cyan_when_very_cold(self):
        assert weathercli.get_temp_color("It's -10 degrees and snowing") == 'cyan'
