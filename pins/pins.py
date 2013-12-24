import os
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
from PIL import Image


PYPI_URL = "https://pypi.python.org/pypi/%s/json"
SHIELD_URL = "http://b.repl.ca/v1/%s-%s-%s.png"


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
            period = month
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        return j['info']['downloads']['last_{0}'.format(period)]

    def generate_badge(self, downloads):
        bg = Image.open(DOWNLOADS)
        bg = self.add_text_to_image(bg, downloads)
        return bg

    def add_text_to_image(self, bg, downloads):
        font = ImageFont.truetype(FONT, 9)
        font_ds = ImageFont.truetype(FONT, 9)
        draw = ImageDraw.Draw(bg)
        draw.text((64, 4), downloads,
                  (0, 0, 0), font=font_ds)
        draw.text((64, 3), downloads,
                  (255, 255, 255), font=font)
        return bg

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
        colour = "green" if has_egg else "red"
        shield_url = SHIELD_URL % ("egg", egg_text, colour)
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
        j = json.loads(r.content)
        classifiers = j['info']['classifiers']
        if len(classifiers) > 0:
            for l in classifiers:
                if l.startswith("License"):
                    bits = l.split(" :: ")
                    if len(bits) == 3:
                        return bits[2]
                    return bits[1]
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
])

if __name__ == "__main__":
    application.listen(8888)
    print("Starting tornado server on port 8888...")
    tornado.ioloop.IOLoop.instance().start()
