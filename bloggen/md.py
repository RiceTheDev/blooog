import os
import markdown
import frontmatter
from datetime import datetime
import config
import html

def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).split(",") if v.strip()]

def _iso_date(date):
    return date.strftime("%Y-%m-%d")

def _rfc822_date(date):
    return date.strftime("%a, %d %b %Y %H:%M:%S GMT")

def _post_url(post):
    filename = post["path"].replace(".md", ".html")
    return f"{config.SITE_URL}/posts/{filename}"

def _post_og_image(post):
    image = post.get("og_image") or config.DEFAULT_OG_IMAGE
    if image.startswith("http://") or image.startswith("https://"):
        return image
    return config.SITE_URL + image

def get_markdown_posts():
    posts = []
    files = [f for f in os.listdir(config.POSTS_DIR) if os.path.isfile(os.path.join(config.POSTS_DIR, f))]

    for file in files:
        if not file.endswith(".md"):
            continue

        post = frontmatter.load(os.path.join(config.POSTS_DIR, file))

        date = datetime.strptime(post["date"], "%Y-%m-%d")
        formatted_date = date.strftime("%B %d, %Y").lower()

        tags = _as_list(post.get("tags"))
        keywords = _as_list(post.get("keywords")) or tags

        posts.append({
            "title": post["title"],
            "description": post.get("description") or config.SITE_DESCRIPTION,
            "author": post.get("author") or config.DEFAULT_AUTHOR,
            "tags": tags,
            "keywords": keywords,
            "og_image": post.get("og_image") or config.DEFAULT_OG_IMAGE,
            "date": date,
            "formatted_date": formatted_date,
            "iso_date": _iso_date(date),
            "rfc822_date": _rfc822_date(date),
            "path": file,
            "content": post.content
        })

    posts.sort(key=lambda post: post["date"], reverse=True)

    return posts


def generate_html_from_markdown(posts):
    for post in posts:
        md_html = markdown.markdown(post["content"])

        temp = open(config.POST_TEMPLATE_PATH, "r").read()

        # basic shit
        temp = temp.replace("<SITE_NAME>", html.escape(config.SITE_NAME))
        temp = temp.replace("<TITLE>", html.escape(post['title']))
        temp = temp.replace("<DATE>", post["formatted_date"])
        temp = temp.replace("<TIME_DATETIME>", post["iso_date"])
        temp = temp.replace("<!--CONTENT-->", md_html)

        # seo (i suck at this)
        temp = temp.replace("<META_DESCRIPTION>", html.escape(post["description"]))
        temp = temp.replace("<META_KEYWORDS>", html.escape(", ".join(post["keywords"])))
        temp = temp.replace("<META_AUTHOR>", html.escape(post["author"]))
        temp = temp.replace("<CANONICAL_URL>", html.escape(_post_url(post)))

        # opengraph
        temp = temp.replace("<OG_TITLE>", html.escape(post["title"]))
        temp = temp.replace("<OG_DESCRIPTION>", html.escape(post["description"]))
        temp = temp.replace("<OG_URL>", html.escape(_post_url(post)))
        temp = temp.replace("<OG_IMAGE>", html.escape(_post_og_image(post)))
        temp = temp.replace("<OG_SITE_NAME>", html.escape(config.SITE_NAME))
        temp = temp.replace("<TWITTER_TITLE>", html.escape(post["title"]))
        temp = temp.replace("<TWITTER_DESCRIPTION>", html.escape(post["description"]))
        temp = temp.replace("<TWITTER_IMAGE>", html.escape(_post_og_image(post)))
        temp = temp.replace("<RSS_URL>", html.escape(config.SITE_URL + "/" + config.RSS_PATH.replace("./", "")))

        # article meta
        temp = temp.replace("<ARTICLE_PUBLISHED_TIME>", post["iso_date"])
        temp = temp.replace("<ARTICLE_MODIFIED_TIME>", post["iso_date"])
        temp = temp.replace("<ARTICLE_AUTHOR>", html.escape(post["author"]))
        article_tags = "".join(
            f'    <meta property="article:tag" content="{html.escape(tag)}">\n'
            for tag in post["tags"]
        )
        temp = temp.replace("<!--ARTICLE_TAGS-->", article_tags.rstrip())



        open(os.path.join(config.OUT_POST_PATH, post["path"].replace(".md", ".html")), "w+").write(temp)


def generate_sitemap(posts):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    urls = [
        f"    <url>\n"
        f"        <loc>{html.escape(config.SITE_URL + '/')}</loc>\n"
        f"        <lastmod>{today}</lastmod>\n"
        f"        <changefreq>weekly</changefreq>\n"
        f"        <priority>1.0</priority>\n"
        f"    </url>"
    ]

    for post in posts:
        urls.append(
            f"    <url>\n"
            f"        <loc>{html.escape(_post_url(post))}</loc>\n"
            f"        <lastmod>{post['iso_date']}</lastmod>\n"
            f"        <changefreq>monthly</changefreq>\n"
            f"        <priority>0.8</priority>\n"
            f"    </url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n"
        '</urlset>\n'
    )

    open(config.SITEMAP_PATH, "w+").write(sitemap)
    print(f"sitemap generated at {config.SITEMAP_PATH}")


def generate_rss(posts):
    now = datetime.utcnow()
    build_date = _rfc822_date(now)

    items = []
    for post in posts:
        description = html.escape(post["description"])
        items.append(
            f"    <item>\n"
            f"        <title>{html.escape(post['title'])}</title>\n"
            f"        <link>{html.escape(_post_url(post))}</link>\n"
            f"        <description>{description}</description>\n"
            f"        <pubDate>{post['rfc822_date']}</pubDate>\n"
            f"        <guid isPermaLink=\"true\">{html.escape(_post_url(post))}</guid>\n"
            f"        {''.join(f'<category>{html.escape(tag)}</category>' for tag in post['tags'])}\n"
            f"    </item>"
        )

    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        '    <channel>\n'
        f"        <title>{html.escape(config.SITE_NAME)}</title>\n"
        f"        <link>{html.escape(config.SITE_URL + '/')}</link>\n"
        f"        <description>{html.escape(config.SITE_DESCRIPTION)}</description>\n"
        "        <language>en</language>\n"
        f"        <lastBuildDate>{build_date}</lastBuildDate>\n"
        + "\n".join(items) + "\n"
        '    </channel>\n'
        '</rss>\n'
    )

    # holy fuck i hate rss, too boring omfg

    open(config.RSS_PATH, "w+").write(rss)
    print(f"rss feed generated at {config.RSS_PATH}")
