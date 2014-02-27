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
SHIELD_URL = "http://localhost:9000/v1/%s-%s-%s.png"


def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


intword_converters = (
    (3, lambda number: format_number('%(value).1fK', number)),
    (6, lambda number: format_number('%(value).1fM', number)),
    (9, lambda number: format_number('%(value).1fB', number)),
)


class DownloadHandler(tornado.web.RequestHandler):

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

    def get_downloads(self, url, period):
        if period not in ('day', 'week', 'month'):
            period = 'month'
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        return j['info']['downloads']['last_{0}'.format(period)]

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        period = self.get_argument('period', 'month')
        url = PYPI_URL % package
        downloads = self.intword(self.get_downloads(url, period))
        period = "this_%s" % period if period in ('week', 'month') else "today"
        pperiod = "%s_%s" % (downloads, period)
        shield_url = SHIELD_URL % ("downloads", pperiod, 'brightgreen')
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


class LatestHandler(tornado.web.RequestHandler):

    def get_version(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        return j['info']['version']

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        version = self.get_version(url)
        shield_url = SHIELD_URL % ("version", version, 'brightgreen')
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


class WheelHandler(tornado.web.RequestHandler):

    def get_wheel(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        urls = j['urls']
        if len(urls) > 0:
            for u in urls:
                if u['packagetype'] == 'bdist_wheel':
                    return True
        return False

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        has_wheel = self.get_wheel(url)
        wheel_text = "yes" if has_wheel else "no"
        colour = "green" if has_wheel else "red"
        shield_url = SHIELD_URL % ("wheel", wheel_text, colour)
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


class EggHandler(tornado.web.RequestHandler):

    def get_egg(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        urls = j['urls']
        if len(urls) > 0:
            for u in urls:
                if u['packagetype'] == 'bdist_egg':
                    return True
        return False

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        has_egg = self.get_egg(url)
        egg_text = "yes" if has_egg else "no"
        colour = "red" if has_egg else "brightgreen"
        shield_url = SHIELD_URL % ("egg", egg_text, colour)
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


class FormatHandler(tornado.web.RequestHandler):

    def get_wheel(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        urls = j['urls']
        if len(urls) > 0:
            for u in urls:
                if u['packagetype'] == 'bdist_wheel':
                    return True
        return False

    def get_egg(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        urls = j['urls']
        if len(urls) > 0:
            for u in urls:
                if u['packagetype'] == 'bdist_egg':
                    return True
        return False

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        has_egg = self.get_egg(url)
        colour = "yellow"
        text = "source"
        text = "egg" if has_egg else text
        colour = "red" if has_egg else colour
        has_wheel = self.get_wheel(url)
        text = "wheel" if has_wheel else text
        colour = "brightgreen" if has_wheel else colour
        shield_url = SHIELD_URL % ("format", text, colour)
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


class LicenseHandler(tornado.web.RequestHandler):

    def get_license(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        info = json.loads(r.content)['info']
        license = info.get('license')
        # Use the license unless someone blobbed the whole license text in
        # this field. In this case fallback on classifers.
        if license and '\n' not in license and license.upper() != 'UNKNOWN':
            return license
        for classifier in info['classifiers']:
            if classifier.startswith("License"):
                return classifier.split(" :: ")[-1]
        return "unknown"

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        url = PYPI_URL % package
        license = self.get_license(url)
        license = license.replace(' ', '_')
        shield_url = SHIELD_URL % ("license", license, "blue")
        shield = requests.get(shield_url).content
        img = BytesIO(shield)
        img.seek(0)
        self.write(img.read())


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
