import os
import markdown
import os
import frontmatter
from datetime import datetime
import config
import re

def get_markdown_posts():
    posts = []
    files = [f for f in os.listdir(config.POSTS_DIR) if os.path.isfile(os.path.join(config.POSTS_DIR, f))]

    for file in files:
        if not file.endswith(".md"):
            continue

        post = frontmatter.load(os.path.join(config.POSTS_DIR, file))

        date = datetime.strptime(post["date"], "%Y-%m-%d")
        formatted_date = date.strftime("%B %d, %Y").lower()

        posts.append({
            "title": post["title"],
            "description": post["description"],
            "date": date,
            "formatted_date": formatted_date,
            "path": file
        })

    posts.sort(key=lambda post: post["date"], reverse=True)

    return posts


def generate_html_from_markdown(posts):
    for post in posts:
        html = open(os.path.join(config.POSTS_DIR, post["path"])).read()
        html = re.sub(r"^---\s*\n.*?\n---\s*\n", "", html, count=1, flags=re.DOTALL)

        md_html = markdown.markdown(html)

        temp = open(config.POST_TEMPLATE_PATH, "r").read()

        temp = temp.replace("<TITLE>", post['title'])
        temp = temp.replace("<DATE>", post["formatted_date"])
        temp = temp.replace("<!--CONTENT-->", md_html)

        open(os.path.join(config.OUT_POST_PATH, post["path"].replace(".md", ".html")), "w+").write(temp)