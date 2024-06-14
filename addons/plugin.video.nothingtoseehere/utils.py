import xbmc
import sys
from urllib.parse import urlencode
import urllib.request

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    xbmc.log(f"get_url: {kwargs}", xbmc.LOGINFO)
    return "{}?{}".format(_URL, urlencode(kwargs))


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    xbmc.log(f"URL requesting is {url}", xbmc.LOGINFO)
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        return response.read()
