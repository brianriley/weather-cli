#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import mock
import pytest

import weathercli


class DescribeOpenWeatherMap:

    def setup(self):
        self.weather = weathercli.OpenWeatherMap()

    def it_passes_query_to_url(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 1
                },
                'weather': [
                    {
                        'description': 'abc',
                        'icon': '123',
                    },
                ],
            })

            self.weather.now('chelsea,ma')

            mock_urlopen.assert_called_with('http://api.openweathermap.org/data/2.5/weather?q=chelsea%2Cma&units=imperial')

    def it_passes_units_along_to_query(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 1
                },
                'weather': [
                    {
                        'description': 'abc',
                        'icon': '123',
                    },
                ],
            })

            self.weather.now('chelsea,ma', units='metric')

            mock_urlopen.assert_called_with('http://api.openweathermap.org/data/2.5/weather?q=chelsea%2Cma&units=metric')

    def it_raises_an_error_when_given_a_bad_response(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{'

            with pytest.raises(weathercli.WeatherDataError) as cm:
                self.weather.now('chelsea,ma')

            assert cm.value.message == "Malformed response from weather service"

    def it_raises_an_error_when_elements_arent_found(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = '{}'

            with pytest.raises(weathercli.WeatherDataError) as cm:
                self.weather.now('chelsea,ma')

            assert cm.value.message == "No conditions reported for your search"

    def it_calls_the_formatter_with_correct_parameters(self):
        with mock.patch('weathercli.urllib.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps({
                'main': {
                    'temp': 35
                },
                'weather': [
                    {
                        'description': 'sky is clear',
                        'icon': '01d',
                    },
                ],
            })
            formatter = mock.Mock()
            weather = weathercli.OpenWeatherMap(formatter=formatter)

            weather.now('chelsea,ma')

            formatter.output.assert_called_with({'temp': 35, 'conditions': 'sky is clear', 'icon': u'\u2600'})

    def it_converts_sunny_icon_code_to_our_code(self):
        assert self.weather.icon('01d') == weathercli.SUN
        assert self.weather.icon('01n') == weathercli.SUN

    def it_converts_few_clouds_icon_code_to_our_code(self):
        assert self.weather.icon('02d') == weathercli.CLOUDS
        assert self.weather.icon('02n') == weathercli.CLOUDS

    def it_converts_scattered_clouds_icon_code_to_our_code(self):
        assert self.weather.icon('03d') == weathercli.CLOUDS
        assert self.weather.icon('03n') == weathercli.CLOUDS

    def it_converts_broken_clouds_icon_code_to_our_code(self):
        assert self.weather.icon('04d') == weathercli.CLOUDS
        assert self.weather.icon('04n') == weathercli.CLOUDS

    def it_converts_shower_rain_icon_code_to_our_code(self):
        assert self.weather.icon('09d') == weathercli.RAIN
        assert self.weather.icon('09n') == weathercli.RAIN

    def it_converts_rain_icon_code_to_our_code(self):
        assert self.weather.icon('10d') == weathercli.RAIN
        assert self.weather.icon('10n') == weathercli.RAIN

    def it_converts_thunderstorm_icon_code_to_our_code(self):
        assert self.weather.icon('11d') == weathercli.RAIN
        assert self.weather.icon('11n') == weathercli.RAIN

    def it_converts_snow_icon_code_to_our_code(self):
        assert self.weather.icon('13d') == weathercli.SNOW
        assert self.weather.icon('13n') == weathercli.SNOW

    def it_converts_all_other_icon_codes_to_0(self):
        assert self.weather.icon('aslfj') == 0


class DescribeGetTempColor:
    
    def it_is_blue_when_cold(self):
        assert weathercli.get_temp_color("It's 45 degrees and snowing") == 'blue'

    def it_is_yellow_when_warm(self):
        assert weathercli.get_temp_color("It's 70 degrees and sunny") == 'yellow'

    def it_is_magenta_when_hot(self):
        assert weathercli.get_temp_color("It's 100 degrees and sunny") == 'red'

    def it_is_cyan_when_very_cold(self):
        assert weathercli.get_temp_color("It's -10 degrees and snowing") == 'cyan'


class DescribeArguments:

    def it_returns_None_if_no_query_given(self):
        args = weathercli.Arguments().parse([])

        assert args['query'] == None

    def it_returns_a_query_passed_in(self):
        args = weathercli.Arguments().parse(['foo'])

        assert args['query'] == 'foo'

    def it_gets_query_from_the_defaults(self):
        args = weathercli.Arguments().parse([], defaults={weathercli.Arguments.QUERY: 'foo'})

        assert args['query'] == 'foo'

    def it_defaults_units_to_imperial(self):
        args = weathercli.Arguments().parse([])

        assert args['units'] == 'imperial'

    def it_returns_the_units_passed_in(self):
        args = weathercli.Arguments().parse(['-u', 'celsius'])

        assert args['units'] == 'metric'

    def it_gets_units_from_the_defaults(self):
        args = weathercli.Arguments().parse([], defaults={weathercli.Arguments.UNITS: 'celsius'})

        assert args['units'] == 'metric'

    def it_defaults_unknown_units_to_imperial(self):
        args = weathercli.Arguments().parse([], defaults={weathercli.Arguments.UNITS: 'foo'})

        assert args['units'] == 'imperial'

    def it_can_output_its_help(self):
        args = weathercli.Arguments()

        assert args.help().startswith('usage')

    def it_defaults_iconify_to_false(self):
        args = weathercli.Arguments().parse([])

        assert args['iconify'] == False

    def it_sets_iconify_to_true_when_passed_as_an_arg(self):
        args = weathercli.Arguments().parse(['--iconify'])

        assert args['iconify'] == True


class DescribeVerboseFormatter:

    def it_returns_the_weather_written_out(self):
        formatter = weathercli.VerboseFormatter()

        assert formatter.output({'temp': 10, 'conditions': 'cloudy'}) == u"It's 10\u00B0 and cloudy"


class DescribeIconifyFormatter:

    def setup(self):
        self.formatter = weathercli.IconifyFormatter()

    def it_returns_the_weather_in_icon_format(self):
        assert self.formatter.output({'temp': 10, 'icon': u'\u2600'}) == u"10\u00B0\u2600"
