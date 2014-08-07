try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from BytesIO import BytesIO

import gc
import hashlib
import json
import mimetypes
import os
import re
import time

from klein import Klein
from redis import Redis
import requests


PYPI_URL = "https://pypi.python.org/pypi/%s/json"
SHIELD_URL = "http://img.shields.io/badge/%s-%s-%s.%s"
# SHIELD_URL = "http://localhost:9000/badge/%s-%s-%s.%s"  # pypip.in uses a local version of img.shields.io
FILE_CACHE = "/tmp/shields.py/"
CACHE_TIME = (60 * 60) * 24  # 24 hours
REDIS_EXPIRE = 60 * 10  # 10 minutes

app = Klein()
redis = Redis()


def format_number(singular, number):
    value = singular % {'value': number}
    # Get rid of the .0 but keep the other decimals
    return value.replace('.0', '')


intword_converters = (
    (3, lambda number: format_number('%(value).1fk', number)),
    (6, lambda number: format_number('%(value).1fM', number)),
    (9, lambda number: format_number('%(value).1fB', number)),
)


class PypiHandler(object):
    '''Get the pypi json data for the package, and process.'''
    shield_subject = None
    request = None
    format = 'svg'
    cacheable = False

    def get(self, request, package, format, *args, **kwargs):
        self.request = request
        self.format = format
        url = PYPI_URL % package
        r_data = redis.get(package)
        if r_data:
            data = json.loads(r_data)
            return self.handle_package_data(data)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.shield_subject = 'error'
            return self.write_shield('error', 'red')
        else:
            redis.set(package, response.content)
            redis.expire(package, REDIS_EXPIRE)
            data = json.loads(response.content)
            return self.handle_package_data(data)

    def handle_package_data(self, json_data):
        '''Look at the pypi data and decide what text goes on the badge.'''
        raise NotImplementedError

    def hash(self, url):
        return hashlib.md5(url).hexdigest()

    def write_shield(self, status, colour='brightgreen'):
        '''Obtain and write the shield to the response.'''
        shield_url = SHIELD_URL % (
            self.shield_subject,
            status,
            colour,
            self.format,
        )
        style = self.request.args.get('style', None)
        if style is not None and style[0] in ['flat', ]:
            shield_url += "?style={0}".format(style[0])

        ihash = self.hash(shield_url)
        cache = os.path.join(FILE_CACHE, ihash)
        if os.path.exists(cache) and self.cacheable:
            mtime = os.stat(cache).st_mtime + CACHE_TIME
            if mtime > time.time():
                return open(cache).read()

        shield_response = requests.get(shield_url, stream=True)
        img = BytesIO()
        for chunk in shield_response.iter_content(1024):
            if not chunk:
                break
            img.write(chunk)
        if self.cacheable:
            with open(cache, 'w') as ifile:
                img.seek(0)
                ifile.write(img.read())
        img.seek(0)
        return img.read()


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
        period = self.request.args.get('period', 'month')
        if isinstance(period, list):
            period = period[0]
        if period not in ('day', 'week', 'month'):
            period = 'month'
        downloads = data['info']['downloads']['last_{0}'.format(period)]
        downloads = self.intword(downloads)
        period = "%s" % period if period in ('week', 'month') else "today"
        pperiod = "%s/%s" % (downloads, period)
        return self.write_shield(pperiod)


class VersionHandler(PypiHandler):
    shield_subject = 'pypi'

    def handle_package_data(self, data):
        text = self.request.args.get('text', 'pypi')
        if text[0] in ('pypi', 'version'):
            self.shield_subject = text[0]
        return self.write_shield(data['info']['version'].replace('-', '--'))


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
    cacheable = True

    def handle_package_data(self, data):
        has_wheel = has_package(data, 'bdist_wheel')
        wheel_text = "yes" if has_wheel else "no"
        colour = "brightgreen" if has_wheel else "red"
        return self.write_shield(wheel_text, colour)


class EggHandler(PypiHandler):
    shield_subject = 'egg'
    cacheable = True

    def handle_package_data(self, data):
        has_egg = has_package(data, 'bdist_egg')
        egg_text = "yes" if has_egg else "no"
        colour = "red" if has_egg else "brightgreen"
        return self.write_shield(egg_text, colour)


class FormatHandler(PypiHandler):
    shield_subject = 'format'
    cacheable = True

    def handle_package_data(self, data):
        has_egg = has_package(data, 'bdist_egg')
        colour = "yellow"
        text = "source"
        text = "egg" if has_egg else text
        colour = "red" if has_egg else colour
        has_wheel = has_package(data, 'bdist_wheel')
        text = "wheel" if has_wheel else text
        colour = "brightgreen" if has_wheel else colour
        return self.write_shield(text, colour)


class LicenseHandler(PypiHandler):
    shield_subject = 'license'
    cacheable = True

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
        colour = "blue" if license != "unknown" else "red"
        return self.write_shield(license, colour)


class PythonVersionsHandler(PypiHandler):
    shield_subject = 'python'
    cacheable = True

    def get_versions(self, data):
        """"
        Get supported Python versions
        """
        classifiers = data['info']['classifiers']
        if not isinstance(classifiers, list):
            return "none found"
        cs = []
        version_re = re.compile(r"Programming Language \:\: Python \:\: \d\.\d")
        for classifier in classifiers:
            if version_re.match(classifier):
                cs.append(classifier[-3:])
        if not len(cs) > 0:
            # assume 2.7
            return "2.7"
        return cs

    def handle_package_data(self, data):
        versions = self.get_versions(data)
        if not isinstance(versions, list):
            return self.write_shield(versions, 'blue')
        return self.write_shield(", ".join(versions), 'blue')


class ImplementationHandler(PypiHandler):
    shield_subject = 'implementation'
    cacheable = True

    def get_implementations(self, data):
        """"
        Get supported Python implementations
        """
        classifiers = data['info']['classifiers']
        if not isinstance(classifiers, list):
            return "none found"
        cs = []
        if "Programming Language :: Python :: Implementation :: CPython" in classifiers:
            cs.append('cpython')
        if "Programming Language :: Python :: Implementation :: IronPython" in classifiers:
            cs.append('iron')
        if "Programming Language :: Python :: Implementation :: Jython" in classifiers:
            cs.append('jython')
        if "Programming Language :: Python :: Implementation :: PyPy" in classifiers:
            cs.append('pypy')
        if "Programming Language :: Python :: Implementation :: Stackless" in classifiers:
            cs.append('stackless')
        if not len(cs) > 0:
            # assume CPython
            return 'cpython'
        return cs

    def handle_package_data(self, data):
        versions = self.get_implementations(data)
        if not isinstance(versions, list):
            return self.write_shield(versions, 'blue')
        return self.write_shield(", ".join(versions), 'blue')


class StatusHandler(PypiHandler):
    shield_subject = 'status'
    cacheable = True

    def get_implementations(self, data):
        """"
        Get supported Python implementations
        """
        classifiers = data['info']['classifiers']
        if not isinstance(classifiers, list):
            return "none found"
        for classifier in classifiers:
            if classifier.startswith("Development Status"):
                bits = classifier.split(' :: ')
                return bits[1].split(' - ')
        return "1", "unknown"

    def handle_package_data(self, data):
        statuses = {'1': 'red', '2': 'red', '3': 'red', '4': 'yellow',
                    '5': 'brightgreen', '6': 'brightgreen', '7': 'red'}
        code, status = self.get_implementations(data)
        status = status.lower().replace('-', '--')
        status = "stable" if status == "production/stable" else status
        return self.write_shield(status, statuses[code])


generators = {
    'd': DownloadHandler,
    'download': DownloadHandler,
    'v': VersionHandler,
    'version': VersionHandler,
    'wheel': WheelHandler,
    'egg': EggHandler,
    'license': LicenseHandler,
    'format': FormatHandler,
    'py_versions': PythonVersionsHandler,
    'implementation': ImplementationHandler,
    'status': StatusHandler,
}


@app.route('/<string:generator>/<string:package>/badge.<string:extension>')
def shield(request, generator, package, extension):
    gc.collect()
    ext = mimetypes.types_map[".{0}".format(extension)]
    request.headers.update({'content-type': ext})
    klass = generators[generator]()
    img = klass.get(request, package, extension)
    return img


if __name__ == '__main__':
    if not os.path.exists(FILE_CACHE):
        os.mkdir(FILE_CACHE)
    if '.svg' not in mimetypes.types_map:
        mimetypes.add_type("image/svg+xml", ".svg")
    app.run("localhost", 8888)
