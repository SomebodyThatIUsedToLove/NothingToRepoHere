import xbmc
import xbmcaddon
import xbmcvfs
import os
import json


def get_addon_id():
    addon_id = xbmcaddon.Addon().getAddonInfo("id")
    xbmc.log(f"Fetched Addon ID: {addon_id}", xbmc.LOGINFO)
    return addon_id


def get_json_path():
    xbmc.log(f"get_json_path", xbmc.LOGINFO)
    addon_data_path = xbmcvfs.translatePath(
        f"special://profile/addon_data/{get_addon_id()}"
    )
    if not os.path.exists(addon_data_path):
        os.makedirs(addon_data_path)
    return os.path.join(addon_data_path, "data.json")


def save_data(data):
    xbmc.log(f"save_data: {data}", xbmc.LOGINFO)
    json_path = get_json_path()
    with open(json_path, "w") as f:
        json.dump(data, f)


def load_data():
    xbmc.log(f"load_data", xbmc.LOGINFO)
    json_path = get_json_path()
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            loaded_json = json.load(f)
            xbmc.log(f"data loaded as {loaded_json}", xbmc.LOGINFO)
            return loaded_json
    xbmc.log(f"could not load data, so returning empty object", xbmc.LOGINFO)
    return {}


def get_stored_search_state():
    xbmc.log("get_stored_search_state", xbmc.LOGINFO)
    data = load_data()
    search_phrase = data.get("search_phrase", "")
    site_name = data.get("site_name", "")
    page = data.get("page", "")

    xbmc.log(
        f'state: "search_phrase": {search_phrase}, "site_name": {site_name}, "page": {page}',
        xbmc.LOGINFO,
    )
    if search_phrase and site_name and page:
        return {
            "search_phrase": search_phrase,
            "site_name": site_name,
            "page": page,
        }
    return None


def set_stored_search_state(search_phrase, site_name, page):
    xbmc.log(
        f"set_stored_search_state called with search_phrase: {search_phrase}, site_name: {site_name}, page: {page}",
        xbmc.LOGINFO,
    )

    try:
        data = load_data()
        data["search_phrase"] = search_phrase
        data["site_name"] = site_name
        data["page"] = page
        save_data(data)

        data = load_data()
        new_search_phrase = data["search_phrase"]
        new_site_name = data["site_name"]
        new_page = data["page"]

        xbmc.log(
            f"State just set to: search_phrase: {new_search_phrase}, site_name: {new_site_name}, page: {new_page}",
            xbmc.LOGINFO,
        )

        # Check if settings were set correctly
        if (
            new_search_phrase == search_phrase
            and new_site_name == site_name
            and str(new_page) == str(page)
        ):
            xbmc.log("Settings were successfully saved.", xbmc.LOGINFO)
        else:
            xbmc.log("Settings were NOT saved correctly.", xbmc.LOGERROR)
    except Exception as e:
        xbmc.log(f"Exception in set_stored_search_state: {str(e)}", xbmc.LOGERROR)


def clear_stored_search_state():
    xbmc.log("clear_stored_search_state", xbmc.LOGINFO)
    data = load_data()
    data["search_phrase"] = ""
    data["site_name"] = ""
    data["page"] = ""
    save_data(data)


def get_stored_setting(setting_name):
    xbmc.log(f"get_stored_setting: {setting_name}", xbmc.LOGINFO)
    addon_id = get_addon_id()
    addon = xbmcaddon.Addon(addon_id)
    setting_value = addon.getSetting(setting_name)
    xbmc.log(
        f'state: "setting name": {setting_name}, "setting value": {setting_value}',
        xbmc.LOGINFO,
    )
    if setting_value:
        return setting_value
    return None
