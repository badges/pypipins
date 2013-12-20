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
from PIL import Image, ImageDraw, ImageFont


URL = "https://pypi.python.org/pypi/%s/json"
FONT = os.path.join(os.path.dirname(__file__), "fonts/OpenSans-Regular.ttf")
DOWNLOADS = os.path.join(os.path.dirname(__file__), "badges/downloads.png")
VERSION = os.path.join(os.path.dirname(__file__), "badges/version.png")


def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


intword_converters = (
    (3, lambda number: format_number('%(value).1fK', number)),
    (6, lambda number: format_number('%(value).1fM', number)),
    (9, lambda number: format_number('%(value).1fB', number)),
)


class BadgeHandler(tornado.web.RequestHandler):

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
        return j['info']['downloads']['last_{}'.format(period)]

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
        url = URL % package
        downloads = self.intword(self.get_downloads(url, period))
        img = self.generate_badge(downloads)
        imgbuff = BytesIO()
        img.save(imgbuff, "PNG")
        imgbuff.seek(0)
        self.write(imgbuff.read())


class LatestHandler(tornado.web.RequestHandler):

    def get_version(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return "error"
        j = json.loads(r.content)
        return j['info']['version']

    def generate_badge(self, version):
        bg = Image.open(VERSION)
        bg = self.add_text_to_image(bg, version)
        return bg

    def add_text_to_image(self, bg, version):
        font = ImageFont.truetype(FONT, 9)
        font = ImageFont.truetype(FONT, 9)
        draw = ImageDraw.Draw(bg)
        draw.text((71, 4), version,
                  (0, 0, 0), font=font)
        draw.text((71, 3), version,
                  (255, 255, 255), font=font)
        return bg

    def get(self, package):
        self.set_header("Content-Type", "image/png")
        version = self.get_argument('version', None)
        url = URL % package
        version = self.get_version(url)
        img = self.generate_badge(version)
        imgbuff = BytesIO()
        img.save(imgbuff, "PNG")
        imgbuff.seek(0)
        self.write(imgbuff.read())


application = tornado.web.Application([
    (r"^/d/(.*?)/badge.png", BadgeHandler),
    (r"^/v/(.*?)/badge.png", LatestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    print("Starting tornado server on port 8888...")
    tornado.ioloop.IOLoop.instance().start()
