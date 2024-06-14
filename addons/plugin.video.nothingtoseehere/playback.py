import xbmc
import xbmcplugin
import xbmcgui
import sys
import resolveurl
from utils import fetch_html
from stored_state import set_stored_search_state


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
            xbmc.log(f"URL was resolved with resolveurl", xbmc.LOGINFO)
        else:
            resolved_url = path
            xbmc.log(f"URL was resolved without resolveurl", xbmc.LOGINFO)

        xbmc.log(f"URL is {resolved_url}", xbmc.LOGINFO)
        # Create a playable item with the resolved URL
        play_item = xbmcgui.ListItem(path=resolved_url)
        xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)
        # xbmc.log(f'Just finished playing video, going back to search results page...', xbmc.LOGINFO)
        # xbmc.log(f'site_name={site_name}, search_phrase={search_phrase}, page={page}', xbmc.LOGINFO)
    except Exception as e:
        # Handle and log any exceptions that occur
        xbmcgui.Dialog().notification(
            "Error", f"Exception: {str(e)}", xbmcgui.NOTIFICATION_ERROR
        )
        xbmc.log(f"Error resolving URL {path}: {str(e)}", xbmc.LOGERROR)


def play_nested(detail_link, search_phrase, site_name, page):
    # Fetch the detail page and extract the video URL from there
    site = next(site for site in SITES if site["name"] == site_name)
    detail_page_content = fetch_html(detail_link)
    xbmc.log(f"Found html page here: {detail_page_content}", xbmc.LOGINFO)
    detail_soup = BeautifulSoup(detail_page_content, "html.parser")
    # Use the appropriate selector for the video URL on the detail page
    url = ""
    # for url_pattern in site['url_patterns']:
    url_element = detail_soup.select_one(site["url_pattern"])
    if url_element:
        url = url_element["href"]
        # break
    else:
        xbmc.log(f"Cannot find nested video link", xbmc.LOGERROR)
    # Play the video
    play_video(url, search_phrase, site_name, page)
