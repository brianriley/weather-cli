import unittest

from weathercli import main as weather


class FakeURLOpen(object):
    def __init__(self, *args):
        pass


class BeverlyHillsResponse(FakeURLOpen):
    def read(self):
        return '<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0" mobile_row="0" mobile_zipped="1" row="0" section="0" ><forecast_information><city data="Beverly Hills, CA"/><postal_code data="90210"/><latitude_e6 data=""/><longitude_e6 data=""/><forecast_date data="2011-12-27"/><current_date_time data="2011-12-28 05:51:00 +0000"/><unit_system data="US"/></forecast_information><current_conditions><condition data="Clear"/><temp_f data="48"/><temp_c data="9"/><humidity data="Humidity: 63%"/><icon data="/ig/images/weather/sunny.gif"/><wind_condition data="Wind: N at 0 mph"/></current_conditions><forecast_conditions><day_of_week data="Tue"/><low data="43"/><high data="68"/><icon data="/ig/images/weather/sunny.gif"/><condition data="Clear"/></forecast_conditions><forecast_conditions><day_of_week data="Wed"/><low data="50"/><high data="74"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Thu"/><low data="52"/><high data="74"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Fri"/><low data="50"/><high data="72"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions></weather></xml_api_reply>'


class ChelseaResponse(FakeURLOpen):
    def read(self):
        return '<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0" mobile_row="0" mobile_zipped="1" row="0" section="0" ><forecast_information><city data="Chelsea, MA"/><postal_code data="02150"/><latitude_e6 data=""/><longitude_e6 data=""/><forecast_date data="2011-12-28"/><current_date_time data="2011-12-28 05:54:00 +0000"/><unit_system data="US"/></forecast_information><current_conditions><condition data="Light rain"/><temp_f data="56"/><temp_c data="13"/><humidity data="Humidity: 90%"/><icon data="/ig/images/weather/mist.gif"/><wind_condition data="Wind: S at 21 mph"/></current_conditions><forecast_conditions><day_of_week data="Wed"/><low data="20"/><high data="47"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Thu"/><low data="29"/><high data="36"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Fri"/><low data="31"/><high data="47"/><icon data="/ig/images/weather/chance_of_snow.gif"/><condition data="Chance of Snow Showers"/></forecast_conditions><forecast_conditions><day_of_week data="Sat"/><low data="29"/><high data="40"/><icon data="/ig/images/weather/chance_of_rain.gif"/><condition data="Chance of Showers"/></forecast_conditions></weather></xml_api_reply>'


class BadXMLResponse(FakeURLOpen):
    def read(self):
        return 'abcdefg'


class LocationNotFoundResponse(FakeURLOpen):
    def read(self):
        return '<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0" mobile_row="0" mobile_zipped="1" row="0" section="0" ><problem_cause data=""/></weather></xml_api_reply>'


class TempFNotFoundResponse(FakeURLOpen):
    def read(self):
        return '<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0" mobile_row="0" mobile_zipped="1" row="0" section="0" ><forecast_information><city data="Chelsea, MA"/><postal_code data="02150"/><latitude_e6 data=""/><longitude_e6 data=""/><forecast_date data="2011-12-28"/><current_date_time data="2011-12-28 05:54:00 +0000"/><unit_system data="US"/></forecast_information><current_conditions><condition data="Light rain"/><temp_c data="13"/><humidity data="Humidity: 90%"/><icon data="/ig/images/weather/mist.gif"/><wind_condition data="Wind: S at 21 mph"/></current_conditions><forecast_conditions><day_of_week data="Wed"/><low data="20"/><high data="47"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Thu"/><low data="29"/><high data="36"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Fri"/><low data="31"/><high data="47"/><icon data="/ig/images/weather/chance_of_snow.gif"/><condition data="Chance of Snow Showers"/></forecast_conditions><forecast_conditions><day_of_week data="Sat"/><low data="29"/><high data="40"/><icon data="/ig/images/weather/chance_of_rain.gif"/><condition data="Chance of Showers"/></forecast_conditions></weather></xml_api_reply>'


class ConditionNotFoundResponse(FakeURLOpen):
    def read(self):
        return '<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0" mobile_row="0" mobile_zipped="1" row="0" section="0" ><forecast_information><city data="Chelsea, MA"/><postal_code data="02150"/><latitude_e6 data=""/><longitude_e6 data=""/><forecast_date data="2011-12-28"/><current_date_time data="2011-12-28 05:54:00 +0000"/><unit_system data="US"/></forecast_information><current_conditions><temp_f data="56"/><temp_c data="13"/><humidity data="Humidity: 90%"/><icon data="/ig/images/weather/mist.gif"/><wind_condition data="Wind: S at 21 mph"/></current_conditions><forecast_conditions><day_of_week data="Wed"/><low data="20"/><high data="47"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Thu"/><low data="29"/><high data="36"/><icon data="/ig/images/weather/mostly_sunny.gif"/><condition data="Mostly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Fri"/><low data="31"/><high data="47"/><icon data="/ig/images/weather/chance_of_snow.gif"/><condition data="Chance of Snow Showers"/></forecast_conditions><forecast_conditions><day_of_week data="Sat"/><low data="29"/><high data="40"/><icon data="/ig/images/weather/chance_of_rain.gif"/><condition data="Chance of Showers"/></forecast_conditions></weather></xml_api_reply>'


class PostalCodeTestCase(unittest.TestCase):

    def setUp(self):
        self.weather = weather.Weather()

    def test_postal_code_90210(self):
        weather.urllib.urlopen = BeverlyHillsResponse
        self.assertEquals(self.weather.now('90210'), "It's 48 degrees and clear")

    def test_postal_code_02150(self):
        weather.urllib.urlopen = ChelseaResponse
        self.assertEquals(self.weather.now('02150'), "It's 56 degrees and light rain")


class BadXMLTestCase(unittest.TestCase):
    
    def setUp(self):
        self.weather = weather.Weather()

    def test_bad_xml_response(self):
        weather.urllib.urlopen = BadXMLResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, 'foobar')

class ElementsNotFoundTestCase(unittest.TestCase):
    
    def setUp(self):
        self.weather = weather.Weather()

    def test_missing_current_conditions(self):
        weather.urllib.urlopen = LocationNotFoundResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, 'there is no here here')

    def test_missing_temp_f(self):
        weather.urllib.urlopen = TempFNotFoundResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, '1234')

    def test_missing_condition(self):
        weather.urllib.urlopen = ConditionNotFoundResponse
        self.assertRaises(weather.WeatherDataError, self.weather.now, '1234')


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
