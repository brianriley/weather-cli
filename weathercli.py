#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
import json
import os
import re
import sys
import urllib

from clint.textui import puts, colored
import datetime
import time


SUN = u'\u2600'
CLOUDS = u'\u2601'
RAIN = u'\u2602'
SNOW = u'\u2603'


class BaseFormatter(object):
    def output(self, context, icon=False):
        if icon:
            return u"{0}\u00B0{1}".format(
                context['temp'],
                context['icon']
            )
        return u"It's {0}\u00B0 and {1}".format(
            context['temp'],
            context['conditions'].lower()
        )


class ForecastFormatter(BaseFormatter):
    def output(self, context, icon=False):
        ret = ""
        for c in context:
            if icon:
                conditions = c['icon']
            else:
                conditions = c['conditions'].lower()
            ret += u"{0} - max: {1}\u00B0, min: {2}\u00B0, condition: {3}\n".format(
                c['date'],
                c['max'],
                c['min'],
                conditions
            )
        return ret


class WeatherDataError(Exception):
    pass


class OpenWeatherMap(object):
    def __init__(self, formatter=BaseFormatter()):
        self.formatter = formatter

    def now(self, query, units='imperial', forecast=False, icon=False):
        api_url = {False: 'http://api.openweathermap.org/data/2.5/weather?q={0}&units={1}',
                   True: 'http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&units={1}'}
        raw_data = urllib.urlopen(api_url[forecast].format(
            urllib.quote_plus(query),
            units
        )).read()

        try:
            weather = json.loads(raw_data)
        except ValueError:
            raise WeatherDataError("Malformed response from weather service")

        context = {}
        try:
            if forecast:
                context = []
                for w in weather['list']:
                    context.append({
                        'date': datetime.datetime.strptime(time.ctime(w['dt']), "%a %b %d %H:%M:%S %Y").strftime(
                            "%a, %d %b %Y"),
                        'max': w['temp']['max'],
                        'min': w['temp']['min'],
                        'conditions': w['weather'][0]['description'],
                        'icon': self.icon(w['weather'][0]['icon'])
                    })
            else:
                context['temp'] = int(weather['main']['temp'])
                context['conditions'] = weather['weather'][0]['description']
                context['icon'] = self.icon(weather['weather'][0]['icon'])
        except KeyError:
            raise WeatherDataError("No conditions reported for your search")

        return self.formatter.output(context, icon)

    def icon(self, code):
        codes = defaultdict(int, {
            '01d': SUN,
            '01n': SUN,
            '02d': CLOUDS,
            '02n': CLOUDS,
            '03d': CLOUDS,
            '03n': CLOUDS,
            '04d': CLOUDS,
            '04n': CLOUDS,
            '09d': RAIN,
            '09n': RAIN,
            '10d': RAIN,
            '10n': RAIN,
            '11d': RAIN,
            '11n': RAIN,
            '13d': SNOW,
            '13n': SNOW,
        })
        return codes[code]


class Arguments(object):
    QUERY = 'WEATHER'
    UNITS = 'WEATHER_UNITS'

    def __init__(self):
        self.units = defaultdict(lambda: 'imperial', {'celsius': 'metric'})

        self.parser = argparse.ArgumentParser(description="Outputs the weather for a given location query string")
        self.parser.add_argument('query', nargs="?", help="A location query string to find weather for")
        self.parser.add_argument('-u', '--units', dest='units', choices=self.units.keys(),
                                 help="Units of measurement (default: fahrenheit)")
        self.parser.add_argument('--iconify', action='store_true', help="Show weather in icons?")
        self.parser.add_argument('--forecast', action='store_true', help="Show weather 5 days forecast")

    def parse(self, args, defaults={}):
        args = self.parser.parse_args(args)
        return {
            'query': args.query or defaults.get(Arguments.QUERY),
            'units': self.units[args.units or defaults.get(Arguments.UNITS)],
            'iconify': args.iconify,
            'forecast': args.forecast,
        }

    def help(self):
        return self.parser.format_help()


def get_temp_color(conditions):
    temp_color_map = [
        (40, 'cyan'),
        (60, 'blue'),
        (80, 'yellow')
    ]

    temperature_re = re.compile('(?P<temperature>-?\d+)')
    match = temperature_re.search(conditions)
    if match:
        for color in temp_color_map:
            if int(match.group('temperature')) <= color[0]:
                return color[1]
        return 'red'
    return 'white'


class Weather(object):
    @classmethod
    def main(cls):
        arguments = Arguments()

        args = arguments.parse(sys.argv[1:], defaults=os.environ)

        if not args['query']:
            print arguments.help()
            sys.exit(1)

        if args['forecast']:
            formatter = ForecastFormatter()
        else:
            formatter = BaseFormatter()

        weather_provider = OpenWeatherMap(formatter=formatter)

        try:
            conditions = weather_provider.now(args['query'], args['units'], args['forecast'], args['iconify'])
        except WeatherDataError as e:
            print >> sys.stderr, "ERROR: {0}".format(e.message)
            sys.exit(1)

        puts(getattr(colored, get_temp_color(conditions))(conditions))


if __name__ == '__main__':
    Weather.main()
