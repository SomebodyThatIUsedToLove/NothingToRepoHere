import xbmc
import xbmcaddon


def get_addon_id():
    addon_id = xbmcaddon.Addon().getAddonInfo("id")
    xbmc.log(f"Fetched Addon ID: {addon_id}", xbmc.LOGINFO)
    return addon_id


def get_stored_search_state():
    xbmc.log("get_stored_search_state", xbmc.LOGINFO)
    addon_id = get_addon_id()
    addon = xbmcaddon.Addon(addon_id)
    search_phrase = addon.getSetting("search_phrase")
    site_name = addon.getSetting("site_name")
    page = addon.getSetting("page")
    xbmc.log(
        f'state: "search_phrase": {search_phrase}, "site_name": {site_name}, "page": {page}',
        xbmc.LOGINFO,
    )
    if search_phrase and site_name and page:
        return {
            "search_phrase": search_phrase,
            "site_name": site_name,
            "page": int(page),
        }
    return None


def set_stored_search_state(search_phrase, site_name, page):
    xbmc.log(
        f"set_stored_search_state called with search_phrase: {search_phrase}, site_name: {site_name}, page: {page}",
        xbmc.LOGINFO,
    )

    try:
        addon_id = get_addon_id()
        addon = xbmcaddon.Addon(addon_id)

        addon.setSetting("search_phrase", search_phrase)
        addon.setSetting("site_name", site_name)
        addon.setSetting("page", str(page))

        new_search_phrase = addon.getSetting("search_phrase")
        new_site_name = addon.getSetting("site_name")
        new_page = addon.getSetting("page")

        xbmc.log(
            f"State just set to: search_phrase: {new_search_phrase}, site_name: {new_site_name}, page: {new_page}",
            xbmc.LOGINFO,
        )

        # Check if settings were set correctly
        if (
            new_search_phrase == search_phrase
            and new_site_name == site_name
            and new_page == str(page)
        ):
            xbmc.log("Settings were successfully saved.", xbmc.LOGINFO)
        else:
            xbmc.log("Settings were NOT saved correctly.", xbmc.LOGERROR)
    except Exception as e:
        xbmc.log(f"Exception in set_stored_search_state: {str(e)}", xbmc.LOGERROR)


def clear_stored_search_state():
    xbmc.log("clear_stored_search_state", xbmc.LOGINFO)
    addon_id = get_addon_id()
    addon = xbmcaddon.Addon(addon_id)
    addon.setSetting("search_phrase", "")
    addon.setSetting("site_name", "")
    addon.setSetting("page", "")
