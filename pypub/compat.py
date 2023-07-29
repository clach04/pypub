"""Python 2 and 3 compat for pypub
"""

try:
    basestring
except NameError:
    try:
        basestring = (str, unicode)
    except NameError:
        basestring = str


try:
    unicode
except NameError:
    def unicode(x, encoding=None):
        if encoding is None:
            return str(x)
        return x.decode(encoding)
