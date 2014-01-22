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
    def now(self, query):
        raw_data = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q={0}&units=imperial'.format(urllib.quote_plus(query))).read()
        
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
    parser = argparse.ArgumentParser(description="Outputs the weather for a given location query string")
    parser.add_argument('query', metavar='query', nargs="?", help="A location query string to find weather for")

    args = parser.parse_args()
    weather = Weather()

    query = args.query or os.environ.get('WEATHER')
    if not query:
        parser.print_help()
        sys.exit(1)
    
    try:
        conditions = weather.now(query)
    except WeatherDataError as e:
        print >> sys.stderr, "ERROR: {0}".format(e.message)
        sys.exit(1)

    puts(getattr(colored, get_temp_color(conditions))(conditions))


if __name__ == '__main__':
    main()
