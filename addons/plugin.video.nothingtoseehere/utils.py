import xbmc
import sys
from urllib.parse import urlencode
import urllib.request
import json

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


def post_html(url, data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://somesite.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://somesite.com/somepage/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }

    try:
        data = urllib.parse.urlencode(data)
        xbmc.log(f"URL posting to is {url} with data {data}", xbmc.LOGINFO)
        data = data.encode("utf-8")

        request = urllib.request.Request(url, headers=headers, data=data)
        with urllib.request.urlopen(request) as response:
            # if response.info().get("Content-Encoding") == "br":
            # response_data = brotli.decompress(response.read()).decode("utf-8", errors="replace")
            # else:
            response_data = response.read().decode("utf-8", errors="replace")
            xbmc.log(f"Post response data = {response_data}", xbmc.LOGINFO)
            return response_data
    except urllib.error.HTTPError as e:
        xbmc.log(
            f"HTTPError occurred during POST request: {e.code} - {e.reason}",
            xbmc.LOGERROR,
        )
        return None
    except Exception as e:
        xbmc.log(f"Exception occurred during POST request: {e}", xbmc.LOGERROR)
        return None
