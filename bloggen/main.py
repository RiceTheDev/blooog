#
# bloggen - tool for generating html posts from md and generating the main page with posts
# i made this in like 10 minutes please dont judge my code help me
#

import md
import homepage
import config

def main():
    md_posts = md.get_markdown_posts()
    print(f"found {len(md_posts)} post(s) in {config.POSTS_DIR}")

    homepage.generate_homepage_from_posts(md_posts)
    md.generate_html_from_markdown(md_posts)
    md.generate_sitemap(md_posts)
    md.generate_rss(md_posts)

if __name__ == "__main__":
    main()
