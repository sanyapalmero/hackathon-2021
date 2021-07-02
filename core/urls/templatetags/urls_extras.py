from urllib.parse import parse_qs, urlencode, urlparse

from django.template import Library

register = Library()


@register.simple_tag
def set_url_param(full_path, param, value):
    if '?' not in full_path:
        full_path += "{}{}={}".format('?', param, value)
        return full_path

    base = full_path.split('?')[0]
    parsed_url = urlparse(full_path)
    url_params = parse_qs(parsed_url.query)

    if param in url_params:
        url_params[param][0] = value
    else:
        url_params[param] = [value]

    return base + '?' + urlencode(url_params, doseq=True)
