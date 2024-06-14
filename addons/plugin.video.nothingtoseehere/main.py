# Module: main
# Author: SomebodyThatIUsedToLove
# Created on: 2024-06-01
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib.parse import parse_qsl
import xbmc

from navigation import list_sites, list_site_options
from search import search, search_results
from playback import play_video, play_nested
from settings import open_settings, open_resolveurl_settings


def router(paramstring):
    xbmc.log(f"Router hit with {paramstring}", xbmc.LOGINFO)
    params = dict(parse_qsl(paramstring))
    if params:
        xbmc.log(f"router paramstring: {paramstring}", xbmc.LOGINFO)
        if params["action"] == "site":
            xbmc.log(f"Action = site", xbmc.LOGINFO)
            list_site_options(params["site"])
        elif params["action"] == "search":
            xbmc.log(f"Action = search", xbmc.LOGINFO)
            search(params["site"])
        elif params["action"] == "search_results":
            xbmc.log(f"Action = search_results", xbmc.LOGINFO)
            search_results(
                params["site"], params["search_phrase"], int(params.get("page", 1))
            )
        elif params["action"] == "browse":
            xbmc.log(f"Action = browse", xbmc.LOGINFO)
            search_results(params["site"], "", int(params.get("page", 1)))
        elif params["action"] == "play":
            xbmc.log(f"Action = play", xbmc.LOGINFO)
            play_video(
                params["video"],
                params.get("search_phrase", ""),
                params["site_name"],
                int(params.get("page", 1)),
            )
        elif params["action"] == "play_nested":
            xbmc.log(f"Action = play_nested", xbmc.LOGINFO)
            play_nested(
                params["detail_link"],
                params.get("search_phrase", ""),
                params["site_name"],
                int(params["page"]),
            )
        elif params["action"] == "settings":
            xbmc.log(f"Action = settings", xbmc.LOGINFO)
            open_settings()
        elif params["action"] == "configure_resolveurl":
            xbmc.log(f"Action = open_resolveurl_settings", xbmc.LOGINFO)
            open_resolveurl_settings()
        else:
            xbmc.log(f"Action = other", xbmc.LOGINFO)
            raise ValueError("Invalid paramstring: {}!".format(paramstring))
    else:
        list_sites()


if __name__ == "__main__":
    router(sys.argv[2][1:])
