import xbmcgui
import xbmcplugin
import sys
from utils import get_url
from sites import SITES

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


def list_sites():
    xbmcplugin.setPluginCategory(_HANDLE, "Video Sites")
    xbmcplugin.setContent(_HANDLE, "videos")
    for site in SITES:
        list_item = xbmcgui.ListItem(label=site["name"])
        url = get_url(action="site", site=site["name"])
        is_folder = True
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)

    # Add settings menu item
    settings_item = xbmcgui.ListItem(label="Settings")
    settings_url = f"{sys.argv[0]}?action=settings"
    xbmcplugin.addDirectoryItem(_HANDLE, settings_url, settings_item, isFolder=False)

    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_HANDLE)


def list_site_options(site_name):
    xbmcplugin.setPluginCategory(_HANDLE, site_name)
    xbmcplugin.setContent(_HANDLE, "videos")

    # Search option
    list_item = xbmcgui.ListItem(label="Search")
    url = get_url(action="search", site=site_name)
    xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, True)

    # Browse option
    list_item = xbmcgui.ListItem(label="Browse")
    url = get_url(action="browse", site=site_name)
    xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, True)

    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_HANDLE)
