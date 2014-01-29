#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
import sys
import urllib

from clint.textui import puts, colored


class WeatherDataError(Exception):
    pass


class Weather(object):
    def now(self, query, units='imperial'):
        raw_data = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q={0}&units={1}'.format(
            urllib.quote_plus(query),
            units
        )).read()
        
        try:
            weather = json.loads(raw_data)
        except ValueError:
            raise WeatherDataError("Malformed response from weather service")

        try:
            temperature = int(weather['main']['temp'])
            condition = weather['weather'][0]['description']
        except KeyError:
            raise WeatherDataError("No conditions reported for your search")

        return u"It's {0}\u00B0 and {1}".format(temperature, condition.lower())


class Arguments(object):
    QUERY = 'WEATHER'

    def __init__(self):
        self.units = {
            'celsius': 'metric',
            'fahrenheit': 'imperial',
        }

        self.parser = argparse.ArgumentParser(description="Outputs the weather for a given location query string")
        self.parser.add_argument('query', nargs="?", help="A location query string to find weather for")
        self.parser.add_argument('-u', '--units', dest='units', choices=self.units.keys(), help="Units of measurement (default: fahrenheit)")

    def parse(self, args):
        args = self.parser.parse_args(args)
        return {
            'query': args.query or os.environ.get(Arguments.QUERY),
            'units': args.units and self.units[args.units] or self.units['fahrenheit'],
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
    

def main():
    arguments = Arguments()

    args = arguments.parse(sys.argv[1:])
    weather = Weather()

    if not args['query']:
        print arguments.help()
        sys.exit(1)
    
    try:
        conditions = weather.now(args['query'], args['units'])
    except WeatherDataError as e:
        print >> sys.stderr, "ERROR: {0}".format(e.message)
        sys.exit(1)

    puts(getattr(colored, get_temp_color(conditions))(conditions))


if __name__ == '__main__':
    main()
