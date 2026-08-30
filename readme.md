# my blog

my little personal blog!

its a static blog generated from markdown files using python. no javascript, no framework shit

## how it works?

posts are written in markdown with yaml frontmatter:

```yaml
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
```

python then generates the homepage based on the posts, and the posts themselves are converted to html using [templates](https://github.com/RiceTheDev/blooog/blob/master/templates).

all of that gets done by [bloggen](https://github.com/RiceTheDev/blooog/tree/master/bloggen), which is configurable through [`bloggen/config.py`](https://github.com/RiceTheDev/blooog/blob/master/bloggen/config.py)

## building

you can create your post using markdown and put on the posts/md/ folder, then run bloggen, it will automatically find and generate html based on your markdown

instructions are in [`bloggen/readme.md`](https://github.com/RiceTheDev/blooog/blob/master/bloggen/readme.md).

## why?

because a normal blog framework is boring and I want some space to speak more freely.

i talk a bit more on why i made it on the [hello, world!](raice.lol/posts/hello-world.html) post in the blog.

---

made by raice!
