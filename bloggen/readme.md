# bloggen

bloggen is a tool for generating the main website page with posts and generate posts via markdown.

```bash
pip install -r requirements.txt
```

```bash
cd .. # you need to be in the repo's root directory!!1!11
python bloggen/main.py
```

## front matter

posts are written in markdown with yaml frontmatter:

```yaml
---
title: "my post"
description: "this is a post"
author: "raice"
date: "YYYY-MM-DD"
tags:
  - "tag one"
  - "tag two"
keywords:
  - "seo keyword"
  - "another keyword"
og_image: "/assets/posts/my-post.png"
---
```

required fields: `title`, `date`  
optional fields: `description`, `author`, `tags`, `keywords`, `og_image`

if `description` is missing, the site description is used.  
if `keywords` is missing, `tags` are used as keywords.  
if `og_image` is missing, the default site image is used.

## seo stuff

bloggen now generates a few extra things to help with search engines and feeds:

- `<meta name="description">`, `<meta name="keywords">`, `<meta name="author">` on every page
- open graph tags (`og:title`, `og:description`, `og:image`, etc.)
- twitter card tags
- canonical urls
- ~~json-ld article schema on post pages~~ (couldnt get it to work)
- a `sitemap.xml`
- an `rss.xml` feed

you can edit site-wide info in [`bloggen/config.py`](config.py).
