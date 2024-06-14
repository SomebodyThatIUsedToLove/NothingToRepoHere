import xbmc
import xbmcplugin
import xbmcgui
import sys
import urllib
from utils import get_url, fetch_html
from stored_state import get_stored_search_state, clear_stored_search_state
from sites import SITES
from bs4 import BeautifulSoup

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


def search(site_name):
    # Check if there is a stored search state
    xbmc.log(f"search page for {site_name}", xbmc.LOGINFO)
    stored_state = get_stored_search_state()
    xbmc.log(f"stored_state {stored_state}", xbmc.LOGINFO)
    if stored_state:
        # Clear the stored state
        clear_stored_search_state()
        # Directly call search_results with the stored state
        search_results(
            stored_state["site_name"],
            stored_state["search_phrase"],
            stored_state["page"],
        )
    else:
        # No stored state, prompt the user to enter a search term
        keyboard = xbmc.Keyboard("", "Enter search phrase")
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_phrase = keyboard.getText()
            if search_phrase:
                # Continue with the search as usual
                search_results(site_name, search_phrase, 1)


def search_results(site_name, search_phrase, page=1):
    xbmc.log(
        f"search_results called for {site_name}, {search_phrase}, {page}", xbmc.LOGINFO
    )
    site = next(site for site in SITES if site["name"] == site_name)

    if search_phrase:
        target_url = site["base_url"] + site["search_and_page_url"].format(
            query=urllib.parse.quote(search_phrase), page=page
        )
    else:
        target_url = site["base_url"] + site["page_url"].format(page=page)

    html_content = fetch_html(target_url)
    soup = BeautifulSoup(html_content, "html.parser")

    results = []
    xbmc.log(f'Site Result Pattern = {site["result_pattern"]}', xbmc.LOGINFO)
    xbmc.log(f'Site Name Pattern = {site["name_pattern"]}', xbmc.LOGINFO)
    xbmc.log(f'Site URL Pattern = {site["url_pattern"]}', xbmc.LOGINFO)
    xbmc.log(f'Site Description Pattern = {site["description_pattern"]}', xbmc.LOGINFO)
    xbmc.log(f'Site Thumb Pattern = {site["thumb_pattern"]}', xbmc.LOGINFO)
    xbmc.log(f'Total pages pattern = {site["total_pages_pattern"]}', xbmc.LOGINFO)

    for result in soup.select(site["result_pattern"]):
        xbmc.log(f"Found a result: {result}", xbmc.LOGINFO)
        name = result.select_one(site["name_pattern"]).text
        xbmc.log(f"Name is {name}", xbmc.LOGINFO)

        thumb = result.select_one(site["thumb_pattern"])
        if thumb:
            thumb = thumb["src"]
        else:
            thumb = ""
        xbmc.log(f"thumb is {thumb}", xbmc.LOGINFO)

        try:
            description = result.select_one(site["description_pattern"]).text
        except AttributeError:
            description = ""

        xbmc.log(f"description is {description}", xbmc.LOGINFO)

        # Check if we need to follow a detail link to get the video URL
        if site.get("level_to_link", 1) > 1:
            detail_link_element = result.select_one(site["detail_link_pattern"])
            if detail_link_element:
                detail_link = detail_link_element["href"]
                results.append(
                    {
                        "name": name,
                        "thumb": thumb,
                        "description": description,
                        "detail_link": detail_link,
                    }
                )
                xbmc.log(
                    f"Found result: Name: {name}, detail_link: {detail_link}, Thumb: {thumb}, Description: {description}",
                    xbmc.LOGINFO,
                )
        else:
            # Look for the URL pattern
            url_elements = result.select(site["url_pattern"])
            xbmc.log(f"Found URL Elements: {url_elements}", xbmc.LOGINFO)
            if url_elements:
                xbmc.log(
                    f"Successfully inside if/then block for Found URL Elements: {url_elements}",
                    xbmc.LOGINFO,
                )

                for url_element in url_elements:
                    xbmc.log(
                        f"Looping through url_elements: {url_element}", xbmc.LOGINFO
                    )
                    url = url_element["href"]
                    xbmc.log(f"Looping through url: {url}", xbmc.LOGINFO)

                    appended_result = {
                        "name": (
                            name if len(url_elements) == 1 else name + url_element.text
                        ),
                        "thumb": thumb,
                        "description": description,
                        "url": url,
                    }
                    results.append(appended_result)
                    xbmc.log(
                        f"Result appended: {appended_result}",
                        xbmc.LOGINFO,
                    )
            else:
                xbmc.log(f"Could not find URL!!!", xbmc.LOGERROR)

    xbmc.log(f"site = {site}", xbmc.LOGINFO)
    xbmc.log(
        f"Searching for total pages by pattern {site['total_pages_pattern']}",
        xbmc.LOGINFO,
    )

    all = soup.select(site["total_pages_pattern"])
    xbmc.log(f"Total Pages = {all}", xbmc.LOGINFO)
    total_pages = None
    if all:
        xbmc.log(f"Running manipulator because we found pages", xbmc.LOGINFO)
        pages_before_manipulator = soup.select(site["total_pages_pattern"])
        total_pages = site["total_pages_manipulator"](pages_before_manipulator)
    else:
        xbmc.log(
            f"NOT running manipulator because we found no pages other than the current one",
            xbmc.LOGINFO,
        )

    if total_pages:
        xbmc.log(f"total_pages found as {total_pages}", xbmc.LOGINFO)
    else:
        xbmc.log(f"total_pages NOT found - setting to  {page}", xbmc.LOGINFO)
        total_pages = page

    xbmc.log(f"total_pages {total_pages}", xbmc.LOGINFO)

    if search_phrase:
        xbmcplugin.setPluginCategory(
            _HANDLE,
            f'{site["name"]}  | "{search_phrase}" ({page}/{total_pages})',
        )
    else:
        xbmcplugin.setPluginCategory(
            _HANDLE, f"Browsing {site['name']} ({page}/{total_pages})"
        )
    xbmcplugin.setContent(_HANDLE, "videos")

    for result in results:
        list_item = xbmcgui.ListItem(label=result["name"])
        list_item.setArt({"thumb": result["thumb"]})
        list_item.setProperty("IsPlayable", "true")
        list_item.setInfo(
            "video", {"title": result["name"], "plot": result["description"]}
        )
        list_item.setProperty(
            "Description", result["description"]
        )  # Set the Description property
        list_item.setProperty("Title", result["name"])  # Set the Title property
        if "url" in result:
            url = get_url(
                action="play",
                video=result["url"],
                search_phrase=search_phrase,
                site_name=site_name,
                page=page,
            )
        else:
            url = get_url(
                action="play_nested",
                detail_link=result["detail_link"],
                search_phrase=search_phrase,
                site_name=site_name,
                page=page,
            )
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, False)

    # Check if there is a next page and add a "Next" button if so
    next_page = soup.select_one(site["next_pattern"])
    if next_page:
        list_item = xbmcgui.ListItem(label="Next")
        if search_phrase:
            action = "search_results"
        else:
            action = "browse"
        url = get_url(
            action=action, site=site_name, search_phrase=search_phrase, page=page + 1
        )
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, True)

    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_HANDLE)
