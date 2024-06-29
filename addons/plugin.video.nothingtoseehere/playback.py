from bs4 import BeautifulSoup
from sites import SITES
import xbmc
import xbmcplugin
import xbmcgui
import sys
import resolveurl
from utils import fetch_html, post_html
from stored_state import set_stored_search_state
import os

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


def play_video(path, search_phrase, site_name, page=1):
    try:
        # Set the stored search state before playing the video
        set_stored_search_state(search_phrase, site_name, page)

        # Attempt to resolve the URL using resolveurl
        hmf = resolveurl.HostedMediaFile(path)
        if hmf:
            resolved_url = hmf.resolve()
            xbmc.log(f"URL was resolved with resolveurl: {resolved_url}", xbmc.LOGINFO)
        else:
            resolved_url = path
            xbmc.log(
                f"URL was resolved without resolveurl: {resolved_url}", xbmc.LOGINFO
            )

        # Check if the resolved URL is a .rar file
        if resolved_url.endswith(".rar"):
            xbmc.log(f"Playing video from .rar archive: {resolved_url}", xbmc.LOGINFO)
            # Format the URL for VFS RAR support
            resolved_url = f"rar://{resolved_url}/"

        xbmc.log(f"Final URL to play: {resolved_url}", xbmc.LOGINFO)
        # Create a playable item with the resolved URL
        play_item = xbmcgui.ListItem(path=resolved_url)
        xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)
    except Exception as e:
        # Handle and log any exceptions that occur
        xbmcgui.Dialog().notification(
            "Error", f"Exception: {str(e)}", xbmcgui.NOTIFICATION_ERROR
        )
        xbmc.log(f"Error resolving URL {path}: {str(e)}", xbmc.LOGERROR)


def play_nested(detail_link, search_phrase, site_name, page):
    # Fetch the detail page and extract the video URL from there
    xbmc.log("in play_nested function", xbmc.LOGINFO)
    site = next(site for site in SITES if site["name"] == site_name)
    detail_page_content = fetch_html(detail_link)
    xbmc.log(f"Found html page here: {detail_page_content}", xbmc.LOGINFO)
    detail_soup = BeautifulSoup(detail_page_content, "html.parser")

    if site.get("requires_post", False):
        # Handle the special case for sites requiring POST
        xbmc.log("Site requires post, so fetching via post", xbmc.LOGINFO)
        video_url = fetch_video_url_with_post(detail_soup, site)
    else:
        xbmc.log(
            "Site does not require post, so fetching via normal route", xbmc.LOGINFO
        )
        # Use the normal method to fetch the video URL
        video_url = fetch_video_url(detail_soup, site)

    # Play the video
    play_video(video_url, search_phrase, site_name, page)


def fetch_video_url(detail_soup, site):
    # This is the normal method for sites not requiring POST

    # Use the appropriate selector for the video URL on the detail page
    url = ""
    url_element = detail_soup.select_one(site["url_pattern"])
    if url_element:
        url = url_element["href"]
    else:
        xbmc.log(f"Cannot find nested video link", xbmc.LOGERROR)
    # Play the video
    return url


def fetch_video_url_with_post(detail_soup, site):
    # This is for sites requiring POST

    ids = detail_soup.select("div.getblock span[data-fo='streamtape.com']")
    xbmc.log(f"Found ids: {ids}", xbmc.LOGINFO)
    # for id in ids:
    #     data_id = id["data-id"]
    #     xbmc.log(f"Found data_id: {data_id}", xbmc.LOGINFO)

    #     # Extract the necessary data from the detail page
    #     data = {
    #         "type": "link",
    #         "id": id["data-id"],
    #         "fo": "streamtape.com",
    #     }

    #     # Send a POST request to the third location
    #     response = post_html(site["post_url"], data)

    #     # Parse the response to get the video URL
    #     post_response_soup = BeautifulSoup(response, "html.parser")

    #     url = post_response_soup.select_one(site["post_response_pattern"])

    #     if url:
    #         xbmc.log(f"URL found in post is {url}", xbmc.LOGINFO)
    #         return url

    # Extract the necessary data from the detail page
    data = {
        "type": "link",
        "id": "466875231696",
        "fo": "streamtape.com",
    }

    xbmc.log(f"data sending is {data}", xbmc.LOGINFO)
    # Send a POST request to the third location
    response = post_html(site["post_url"], data)

    xbmc.log(f"Response = {response}", xbmc.LOGINFO)

    # Parse the response to get the video URL
    post_response_soup = BeautifulSoup(response, "html.parser")

    url = post_response_soup.select_one(site["post_response_pattern"])

    if url:
        xbmc.log(f"URL found in post is {url}", xbmc.LOGINFO)
        return url

    xbmc.log(f"No valid URL found in post responses", xbmc.LOGINFO)
    return None
