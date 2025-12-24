---
layout: default
title: "espaillato.github.io"
---

# Blog

Practical notes and exact setup guides.

## Latest posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}
