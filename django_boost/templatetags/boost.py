from django.template import Library

register = Library()


@register.filter(name="abs")
def _abs(x):
    return abs(x)


@register.filter(name="all")
def _all(iterable):
    return all(iterable)


@register.filter(name="any")
def _any(iterable):
    return any(iterable)


@register.filter(name="ascii")
def _ascii(obj):
    return ascii(obj)


@register.filter(name="bin")
def _bin(number):
    return bin(number)


@register.filter(name="bool")
def _bool(x):
    return bool(x)


@register.filter(name="callable")
def _callable(obj):
    return callable(obj)


@register.filter(name="chr")
def _chr(i):
    return chr(i)


@register.filter(name="complex")
def _complex(real, imag=None):
    if imag is None:
        return complex(real)
    return complex(real, imag)


@register.simple_tag(name="delattr")
def _delattr(obj, name):
    return delattr(obj, name)


@register.filter(name="dir")
def _dir(obj):
    return dir(obj)


@register.filter(name="divmod")
def _divmod(a, b):
    return divmod(a, b)


@register.filter(name="enumerate")
def _enumerate(iterable, start=0):
    return enumerate(iterable, start)


@register.filter(name="filter")
def _filter(iterable):
    return filter(None, iterable)


@register.filter(name="float")
def _float(x):
    return float(x)


@register.filter(name="format")
def _format(value, format_spec=None):
    if format_spec is None:
        return format(value)
    return format(value, format_spec)


@register.filter(name="getattr")
def _getattr(obj, name):
    return getattr(obj, name)


@register.filter(name="hasattr")
def _hasattr(obj, name):
    return hasattr(obj, name)


@register.filter(name="hash")
def _hash(obj):
    return hash(obj)


@register.filter(name="hex")
def _hex(x):
    return hex(x)


@register.filter(name="id")
def _id(obj):
    return id(obj)


@register.filter(name="isiterable")
def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


@register.filter(name="int")
def _int(value, base=10):
    return int(value, base)


@register.filter(name="len")
def _len(s):
    return len(s)


@register.filter(name="max")
def _max(iterable):
    return max(iterable)


@register.filter(name="min")
def _min(iterable):
    return min(iterable)


@register.filter(name="next")
def _next(iterable, default=None):
    if default is None:
        return iterable(iterable)
    return next(iterable, default)


@register.filter(name="oct")
def _oct(x):
    return oct(x)


@register.filter(name="ord")
def _ord(c):
    return ord(c)


@register.filter(name="pow")
def _pow(x, y):
    return pow(x, y)


@register.filter(name="range")
def _range(start, stop=None):
    if stop is None:
        return range(start)
    return range(start, stop)


@register.filter(name="repr")
def _repr(obj):
    return repr(obj)


@register.filter(name="reversed")
def _reversed(seq):
    return reversed(seq)


@register.filter(name="round")
def _round(number, ndigits=None):
    if ndigits is None:
        return round(number)
    return round(number, ndigits)


@register.simple_tag(name="setattr")
def _setattr(obj, name, value):
    return setattr(obj, name, value)


@register.filter(name="sorted")
def _sorted(iterable):
    return sorted(iterable)


@register.filter(name="str")
def _str(obj):
    return str(obj)


@register.filter(name="sum")
def _sum(iterable):
    return sum(iterable)


@register.filter(name="type")
def _type(obj):
    return type(obj)


@register.filter(name="vars")
def _vars(obj):
    return vars(obj)


@register.filter(name="zip")
def _zip(*objs):
    return zip(*objs)
