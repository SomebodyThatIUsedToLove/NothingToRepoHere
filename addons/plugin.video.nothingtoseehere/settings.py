import xbmc
import xbmcaddon
import sys

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


def open_settings():
    addon_id = xbmcaddon.Addon().getAddonInfo("id")
    xbmcaddon.Addon(addon_id).openSettings()


def open_resolveurl_settings():
    # Close the current settings window
    xbmc.log(f"Closing the dialog settings", xbmc.LOGINFO)

    # Close the current settings window by trying to force close dialogs
    xbmc.executebuiltin("Dialog.Close(all, true)")

    xbmc.log(f"Closed the dialog settings", xbmc.LOGINFO)

    # find the resolver
    resolve_addon = xbmcaddon.Addon("script.module.resolveurl")
    xbmc.log(f"resolve_addon: {resolve_addon}", xbmc.LOGINFO)

    # open the settings
    resolve_addon.openSettings()
    xbmc.log(f"Just opened the settings for ResolveURL", xbmc.LOGINFO)
