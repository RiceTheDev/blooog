import config

def generate_homepage_from_posts(posts):
    html_posts = []

    html = open(config.HOME_TEMPLATE_PATH, "r").read()

    for post in posts:
        print(f"post \"{post['title']}\" added")
        temp = config.POST_TEMPLATE
        temp = temp.replace("<PATH>", f"posts/{post['path'].replace(".md", ".html")}")
        temp = temp.replace("<TITLE>", f"{post['title']}")
        temp = temp.replace("<DATE>", f"{post['formatted_date']}")
        temp = temp.replace("<DESCRIPTION>", f"{post['description']}")
        html_posts.append(temp)

    html = html.replace("<!--POSTS-->", "".join(html_posts))

    open(config.OUT_HOME_PATH, "w+").write(html)

    print(f"{len(html_posts)} post(s) added sucessfully!")