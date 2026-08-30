import config
import html


def _home_url():
    return config.SITE_URL + "/"


def _og_image_url():
    image = config.DEFAULT_OG_IMAGE
    if image.startswith("http://") or image.startswith("https://"):
        return image
    return config.SITE_URL + image


def generate_homepage_from_posts(posts):
    html_posts = []

    template = open(config.HOME_TEMPLATE_PATH, "r").read()

    for post in posts:
        print(f"post \"{post['title']}\" added")
        temp = config.POST_TEMPLATE
        temp = temp.replace("<PATH>", f"posts/{post['path'].replace('.md', '.html')}")
        temp = temp.replace("<TITLE>", f"{post['title']}")
        temp = temp.replace("<DATE>", f"{post['formatted_date']}")
        temp = temp.replace("<DESCRIPTION>", f"{post['description']}")
        html_posts.append(temp)

    template = template.replace("<!--POSTS-->", "".join(html_posts))

    template = template.replace("<SITE_NAME>", html.escape(config.SITE_NAME))
    template = template.replace("<META_DESCRIPTION>", html.escape(config.SITE_DESCRIPTION))
    template = template.replace("<META_KEYWORDS>", html.escape(", ".join(config.DEFAULT_KEYWORDS)))
    template = template.replace("<META_AUTHOR>", html.escape(config.DEFAULT_AUTHOR))
    template = template.replace("<CANONICAL_URL>", html.escape(_home_url()))
    template = template.replace("<OG_TITLE>", html.escape(config.SITE_NAME))
    template = template.replace("<OG_DESCRIPTION>", html.escape(config.SITE_DESCRIPTION))
    template = template.replace("<OG_URL>", html.escape(_home_url()))
    template = template.replace("<OG_IMAGE>", html.escape(_og_image_url()))
    template = template.replace("<OG_SITE_NAME>", html.escape(config.SITE_NAME))
    template = template.replace("<OG_TYPE>", "website")
    template = template.replace("<TWITTER_TITLE>", html.escape(config.SITE_NAME))
    template = template.replace("<TWITTER_DESCRIPTION>", html.escape(config.SITE_DESCRIPTION))
    template = template.replace("<TWITTER_IMAGE>", html.escape(_og_image_url()))
    template = template.replace("<RSS_URL>", html.escape(config.SITE_URL + "/" + config.RSS_PATH.replace("./", "")))

    open(config.OUT_HOME_PATH, "w+").write(template)

    print(f"{len(html_posts)} post(s) added sucessfully!")
