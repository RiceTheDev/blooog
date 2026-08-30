POSTS_DIR = "./posts/md/"
POST_TEMPLATE = """
                    <article class="post">
                        <a href="<PATH>">
                            <TITLE>
                        </a>
                        <small><DATE></small>

                        <p>
                            <DESCRIPTION>
                        </p>
                    </article>
"""

HOME_TEMPLATE_PATH = "./templates/home_template.html"
OUT_HOME_PATH = "./index.html"

POST_TEMPLATE_PATH = "./templates/post_template.html"
OUT_POST_PATH = "./posts/"

SITE_URL = "https://blog.raice.lol"
SITE_NAME = "raice's space"
SITE_DESCRIPTION = "my little personal blog about programming, emulation, old hardware, low level stuff and random thoughts"
DEFAULT_AUTHOR = "raice"
DEFAULT_KEYWORDS = ["blog", "programming", "emulation", "old hardware", "low level", "cybersecurity"]
DEFAULT_OG_IMAGE = "/assets/og-image.png"

SITEMAP_PATH = "./sitemap.xml"
RSS_PATH = "./rss.xml"
