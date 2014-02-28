try:
    # Python 2
    from StringIO import StringIO as BytesIO
except ImportError:
    # Python 3
    from io import BytesIO

import simplejson as json
import tornado.ioloop
import tornado.web
import requests


PYPI_URL = "https://pypi.python.org/pypi/%s/json"
SHIELD_URL = "http://img.shields.io/badge/%s-%s-%s.png"

def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


intword_converters = (
    (3, lambda number: format_number('%(value).1fK', number)),
    (6, lambda number: format_number('%(value).1fM', number)),
    (9, lambda number: format_number('%(value).1fB', number)),
)


class PypiHandler(tornado.web.RequestHandler):
    '''Get the pypi json data for the package, and process.'''
    shield_subject = None

    def get(self, package, *args, **kwargs):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return self.write_shield('error', 'red')
        else:
            data = json.loads(response.content)
            self.handle_package_data(data)

    def handle_package_data(self, json_data):
        '''Look at the pypi data and decide what text goes on the badge.'''
        raise NotImplementedError

    def write_shield(self, status, colour='brightgreen'):
        '''Obtain and write the shield to the response.'''
        shield_url = SHIELD_URL % (self.shield_subject, status, colour)
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())

class DownloadHandler(PypiHandler):
    shield_subject = 'downloads'

    # Pretty much taken straight from Django
    def intword(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            return value

        if value < 1000:
            return str(value)

        for exponent, converters in intword_converters:
            large_number = 10 ** exponent
            if value < large_number * 1000:
                new_value = value / float(large_number)
                return converters(new_value)

    def handle_package_data(self, data):
        period = self.get_argument('period', 'month')
        if period not in ('day', 'week', 'month'):
            period = 'month'
        downloads = data['info']['downloads']['last_{0}'.format(period)]
        downloads = self.intword(downloads)
        period = "this_%s" % period if period in ('week', 'month') else "today"
        pperiod = "%s_%s" % (downloads, period)
        self.write_shield(pperiod)


class LatestHandler(PypiHandler):
    shield_subject = 'version'

    def handle_package_data(self, data):
        self.write_shield(data['info']['version'])


def has_package(data, package_type):
    '''Does the package have a download of the right type?'''
    urls = data['urls']
    if len(urls) > 0:
        for u in urls:
            if u['packagetype'] == package_type:
                return True
    return False


class WheelHandler(PypiHandler):
    shield_subject = 'wheel'

    def handle_package_data(self, data):
        has_wheel = has_package(data, 'bdist_wheel')
        wheel_text = "yes" if has_wheel else "no"
        colour = "green" if has_wheel else "red"
        self.write_shield(wheel_text, colour)


class EggHandler(PypiHandler):
    shield_subject = 'egg'

    def handle_package_data(self, data):
        has_egg = has_package(data, 'bdist_egg')
        egg_text = "yes" if has_egg else "no"
        colour = "red" if has_egg else "brightgreen"
        self.write_shield(egg_text, colour)


class FormatHandler(PypiHandler):
    shield_subject = 'format'

    def handle_package_data(self, data):
        has_egg = has_package(data, 'bdist_egg')
        colour = "yellow"
        text = "source"
        text = "egg" if has_egg else text
        colour = "red" if has_egg else colour
        has_wheel = has_package(data, 'bdist_wheel')
        text = "wheel" if has_wheel else text
        colour = "brightgreen" if has_wheel else colour
        self.write_shield(text, colour)


class LicenseHandler(PypiHandler):
    shield_subject = 'license'

    def get_license(self, data):
        '''Get the package license.'''
        info = data['info']
        license = info.get('license')
        # Use the license unless someone blobbed the whole license text in
        # this field. In this case fallback on classifers.
        if license and '\n' not in license and license.upper() != 'UNKNOWN':
            return license
        for classifier in info['classifiers']:
            if classifier.startswith("License"):
                return classifier.split(" :: ")[-1]
        return "unknown"

    def handle_package_data(self, data):
        license = self.get_license(data)
        license = license.replace(' ', '_')
        self.write_shield(license, 'blue')


application = tornado.web.Application([
    (r"^/d/(.*?)/badge.png", DownloadHandler),
    (r"^/v/(.*?)/badge.png", LatestHandler),
    (r"^/wheel/(.*?)/badge.png", WheelHandler),
    (r"^/egg/(.*?)/badge.png", EggHandler),
    (r"^/license/(.*?)/badge.png", LicenseHandler),
    (r"^/format/(.*?)/badge.png", FormatHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    print("Starting tornado server on port 8888...")
    tornado.ioloop.IOLoop.instance().start()
