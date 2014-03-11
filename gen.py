# -*- coding: utf-8 -*-

import argparse
import requests
import misaka

DEFAULT_URL = 'https://github.com/'
REPO_API_URL = 'https://api.github.com/repos/'
RAW_README_URL = 'https://raw.github.com/'

TEMPLATE = """
<!DOCTYPE HTML>
<html>
<head>
    <title>{project_title} Project</title>
  <meta charset="utf-8" />
<link rel="alternate" type="application/atom+xml" title="Recent Entries" href="/feed.xml">
<link rel="icon" href="/images/icons/avatar.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/style/css/bootstrap.css" type="text/css" media="screen">
<script type="text/javascript" src="/style/jquery-1.7.1.min.js"></script>
<link rel="stylesheet" href="/style/style.css" type="text/css">
<meta content="{project_description}" name="description"/>
<meta content="{project_keywords}" name="keywords"/>
<script>
 $(document).ready(function(){
    $('.nav a').hover(
        function(){
            $(this).animate({opacity: 0.3}, 400)
        },
        function(){
            $(this).animate({opacity: 1}, 400)
        });
 });
 function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
 }
</script>
<style>
    .content img {
        width: auto;
    }
</style>
</head>

<body>

<div class="container">
<div class="banner">
 <ul class="nav nav-pills">
  <li><a href="/">Blog</a></li>
  <li><a href="{project_url}">Github</a></li>
 </ul>
</div>

<div class="main clearfix">


<div class="posts">
    <div class="title">{project_title}</div>
<div class="content">
    {project_readme}
</div>

<div class="footer">

© Copryright by<a href="http://guojing.me/" target="_blank">GuoJing</a> 2012-2014 using <a href="http://www.github.com/" target="_blank">GitHub</a> and <a href="http://guojing.me/duidui" target="_blank">duidui</a>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-42721249-1', 'guojing.me');
  ga('send', 'pageview');

</script>
</div>

</div>
</body>
</html>
"""


def parse(name):
    url = REPO_API_URL + name
    r = requests.get(url)
    r = r.json()
    return r


def get_readme(name):
    url = RAW_README_URL + name + '/master/README.md'
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gen Github Pages for myself')
    parser.add_argument('name', nargs='?')
    r = parser.parse_args()
    if not r.name:
        parser.print_help()
    else:
        print(r.name)
        j = parse(r.name)
        if j:
            project_title = r.name
            print('Get description of %s' % r.name)
            project_description = j.get('description', '')
            project_keywords = ''
            project_url = j.get('html_url')
            print('Get readme of %s' % r.name)
            project_readme = misaka.html(get_readme(r.name))
            print('Render template')
            TEMPLATE = TEMPLATE.decode('utf-8')
            html = TEMPLATE.replace('{project_description}', project_description)
            html = html.replace('{project_title}', r.name)
            html = html.replace('{project_keywords}', project_keywords or r.name)
            html = html.replace('{project_url}', project_url)
            html = html.replace('{project_readme}', project_readme)
            html = html.encode('utf-8')
            with open('index.html', 'w') as f:
                f.write(html)
