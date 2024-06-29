SITES = [
    {
        "name": "1. PornRapidgator",
        "base_url": "https://pornrapidgator.com",
        "page_url": "/page/{page}",
        "search_and_page_url": "/search/{query}/page/{page}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",
        "url_pattern": "a.rglink[href],a.primaryLinkS3[href],a.rg-link[href]",
        "description_pattern": "div.theDescription:not(:first-child)",
        "thumb_pattern": "div.thumbnail img",
        "next_pattern": "a.next",
        "total_pages_pattern": "li:nth-last-child(2)",
        "total_pages_manipulator": lambda elem: elem[0].text,
        "level_to_link": 1,
    },
    {
        "name": "1. Pornbly",
        "base_url": "http://pornbly.com",
        "page_url": "/page/{page}",
        "search_and_page_url": "/search/{query}/page/{page}",
        "result_pattern": "article.post",
        "name_pattern": "h1.entry-title a",
        "url_pattern": "a.rglink[href],a.primaryLinkS3[href],a.rg-link[href]",
        "description_pattern": "div.theDescription:not(:first-child)",
        "thumb_pattern": "div.thumbnail img",
        "next_pattern": "a.next",
        "total_pages_pattern": "div.pagination a.page-numbers:nth-last-child(2)",
        "total_pages_manipulator": lambda elem: elem[0].text,
        "level_to_link": 1,
    },
    {
        "name": "1. ErotikDream",
        "base_url": "https://erotikdream.com/",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "div.theDescription:not(:first-child)",
        "thumb_pattern": "a.entry-thumbnail img",
        "level_to_link": 2,
        "next_pattern": "a.nextpostslink",
        "total_pages_pattern": "div.wp-pagenavi a:last-child",
        "detail_link_pattern": "h2.entry-title a[href]",
        "total_pages_manipulator": lambda elem: elem[0].text,
    },
    {
        "name": "1. PornChil",
        "base_url": "https://pornchil.com",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "h2 em strong span",
        "thumb_pattern": "div.inside-article > div.entry-content > p > a > img",
        "level_to_link": 2,
        "next_pattern": "a.next",
        "total_pages_pattern": "div.nav-links a.page-numbers:not(.next):not(.prev)",
        "total_pages_manipulator": lambda pages: (
            pages[-1].text.split("Page")[-1].strip() if pages else None
        ),
        "detail_link_pattern": "h2.entry-title a[href]",
    },
    {
        "name": "2. RapidgatorKink",
        "base_url": "https://rapidgatorkink.com",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "h2 em strong span",
        "thumb_pattern": "div.inside-article > div.entry-content > p > a > img",
        "level_to_link": 2,
        "next_pattern": "a.next",
        "total_pages_pattern": "div.nav-links a.page-numbers:not(.next):not(.prev):last-child",
        "total_pages_manipulator": lambda pages: (
            # pages[-1].text.split("Page")[-1].strip() if pages else None
            pages[0].text
        ),
        "detail_link_pattern": "h2.entry-title a[href]",
    },
    {
        "name": "2. Rapid Porn Gator",
        "base_url": "https://rapidporngator.com",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h1.entry-title a",  # streamtape
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "header.entry-header div.entry-meta span.cat-links a",
        "thumb_pattern": "a.entry-thumbnail img",
        "level_to_link": 2,
        "requires_post": True,
        "post_url": "https://rapidporngator.com/wp-content/themes/twentyfourteen/ajax.php",
        "post_response_pattern": "a[href]",
        "next_pattern": "a.next",
        "total_pages_pattern": "div.loop-pagination a.page-numbers:not(.next):not(.prev)",
        "total_pages_manipulator": lambda pages: (pages[-1].text),
        "detail_link_pattern": "h1.entry-title a[href]",
    },
    {
        "name": "2. Porn BB",
        "base_url": "https://www.pornbb.org/",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",  # streamtape
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "div.theDescription:not(:first-child)",
        "thumb_pattern": "a.entry-thumbnail img",
        "level_to_link": 2,
        "next_pattern": "a.next",
        "total_pages_pattern": "li:nth-last-child(2)",
        "total_pages_manipulator": lambda elem: elem[0].text,
        "detail_link_pattern": "h2.entry-title a[href]",
    },
    {
        "name": "1. Free Porn Site Rips",
        "base_url": "https://freepornsiterips.com/",
        "page_url": "/page/{page}",
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",  # streamtape
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "div.entry-summary p:has(strong)",
        "thumb_pattern": "div.entry-summary img",
        "level_to_link": 1,
        "next_pattern": "a.next",
        "total_pages_pattern": "nav.navigation a.page-numbers:not(.next):not(.prev)",
        "total_pages_manipulator": lambda elem: elem[-1].text,
    },
    {
        "name": "08. Sexuria",
        "base_url": "https://sexuria.net",
        "page_url": "/page/{page}",  # post for search, not get
        "search_and_page_url": "/page/{page}/?s={query}",
        "result_pattern": "article.post",
        "name_pattern": "h2.entry-title a",  # streamtape
        "url_pattern": 'a[href*="rapidgator.net"], a[href*="rg.to"]',
        "description_pattern": "div.theDescription:not(:first-child)",
        "thumb_pattern": "a.entry-thumbnail img",
        "level_to_link": 2,
        "next_pattern": "a.next",
        "total_pages_pattern": "li:nth-last-child(2)",
        "total_pages_manipulator": lambda elem: elem[0].text,
        "detail_link_pattern": "h2.entry-title a[href]",
    },
    # Add more sites as needed
    # https://www.forumophilia.com/
    # https://rgporn.org/
    # http://xxt5.com/
    # https://vipergirls.to/forum.php
    # https://v1.intporn.com/forums/
    # https://www.phun.org/
    # http://www.planetsuzy.org/index.php
    # https://porncoven.com/forum.php
    # https://pornsavant.com/forum.php
    # https://myslavegirl.org/
    # https://kitty-kats.net/
    # https://porn4k.to/
]
