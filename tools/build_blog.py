"""Build the TSC blog: blog/<slug>.html, blog/index.html, home cards, sitemap.
Run from the repo root: python3 tools/build_blog.py"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from articles import ARTICLES

SITE = "https://tscacademyofficial.com"
BOOK = "https://calendar.app.google/6BSYJUSxb34AEXQz6"
ARTS = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="TSC Academy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{schema}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>
<nav class="nav"><div class="container">
<a class="logo" href="/">TSC<span>Academy</span></a>
<div class="nav-links"><a href="/#how">How it works</a><a href="/#pricing">Pricing</a><a href="/#team">Team</a><a href="/blog/">Blog</a></div>
<a class="btn" data-book href="{book}" target="_blank" rel="noopener">Book the Assessment</a>
</div></nav>
"""

FOOT = """<footer><div class="container">
<div>© TSC Academy · Part of The Sport Class · Prices in USD</div>
<div class="links"><a href="/">Home</a><a href="/blog/">Blog</a><a href="/toolkit.html">Free toolkit</a><a href="https://www.instagram.com/tscacademyofficial/" target="_blank" rel="noopener">Instagram</a><a href="/privacy.html">Privacy</a></div>
</div></footer>
<div class="sticky"><a class="btn" data-book href="{book}" target="_blank" rel="noopener">Book the Assessment · $125</a></div>
</body>
</html>
"""

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

def md(body):
    out, lst = [], None
    def close():
        nonlocal lst
        if lst: out.append(f"</{lst}>"); lst = None
    for line in body.strip().split("\n"):
        s = line.strip()
        if not s: close(); continue
        if s.startswith("### "): close(); out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "): close(); out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("> "): close(); out.append(f'<div class="callout">{inline(s[2:])}</div>')
        elif s.startswith("- "):
            if lst != "ul": close(); out.append("<ul>"); lst = "ul"
            out.append(f"<li>{inline(s[2:])}</li>")
        elif re.match(r"\d+\. ", s):
            if lst != "ol": close(); out.append("<ol>"); lst = "ol"
            out.append(f"<li>{inline(re.sub(r'^\\d+\\. ', '', s))}</li>")
        else: close(); out.append(f"<p>{inline(s)}</p>")
    close()
    return "\n".join(out)

def words(a): return len(re.findall(r"\w+", a["body"]))
def nice_date(d):
    import datetime
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")

def card(a):
    return (f'<a class="post" href="/blog/{a["slug"]}.html" data-cat="{a["cat"]}">'
            f'<span class="cat">{a["cat"]}</span><h3>{html.escape(a["title"])}</h3>'
            f'<p>{html.escape(a["desc"])}</p><span class="more">Read · {max(1, round(words(a)/220))} min →</span></a>')

os.makedirs("blog", exist_ok=True)
for a in ARTS:
    url = f"{SITE}/blog/{a['slug']}.html"
    schema = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"],
        "author": {"@type": "Organization", "name": "TSC Academy"},
        "publisher": {"@type": "Organization", "name": "TSC Academy", "logo": {"@type": "ImageObject", "url": f"{SITE}/favicon-512.png"}},
        "mainEntityOfPage": url, "keywords": a["kw"], "image": f"{SITE}/images/og-image.png"}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]}
    sch = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>\n' for x in (schema, crumbs))
    related = [r for r in ARTS if r["slug"] != a["slug"] and r["cat"] == a["cat"]][:2]
    related += [r for r in ARTS if r["slug"] != a["slug"] and r not in related][: 3 - len(related)]
    page = HEAD.format(title=html.escape(a["title"]) + " | TSC Academy", desc=html.escape(a["desc"]), url=url,
                       ogtype="article", schema=sch, site=SITE, book=BOOK)
    page += f"""<header class="article-hero"><div class="container narrow">
<div class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {a['cat']}</div>
<h1>{html.escape(a['title'])}</h1>
<p>{html.escape(a['desc'])}</p>
<div class="meta">TSC Academy coaching team · {nice_date(a['date'])} · {max(1, round(words(a)/220))} min read</div>
</div></header>
<main class="container narrow prose">
{md(a['body'])}
<div class="cta-box">
<h3>Want a plan built for your athlete?</h3>
<p>The TSC Athlete Assessment looks at body and mind in one video session. You get a written roadmap in 72 hours. $125, credited in full if you continue.</p>
<div class="row"><a class="btn" data-book href="{BOOK}" target="_blank" rel="noopener">Book the Assessment</a><a class="btn ghost" href="/toolkit.html">Free Parent Toolkit</a></div>
</div>
<p class="disclaimer">This article is general information for parents and coaches. It is not medical or psychological advice. For pain, injury or mental health concerns, talk to a qualified professional.</p>
</main>
<section style="padding-top:20px"><div class="container"><div class="head"><div class="eyebrow">Keep reading</div></div>
<div class="posts">{''.join(card(r) for r in related)}</div></div></section>
"""
    page += FOOT.format(book=BOOK)
    open(f"blog/{a['slug']}.html", "w").write(page)

# blog index
cats = ["All"] + sorted({a["cat"] for a in ARTS})
listing = {"@context": "https://schema.org", "@type": "Blog", "name": "TSC Academy Blog", "url": SITE + "/blog/",
           "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": f"{SITE}/blog/{a['slug']}.html", "datePublished": a["date"]} for a in ARTS]}
page = HEAD.format(title="Blog: Mental & Physical Performance for Young Athletes | TSC Academy",
                   desc="Practical guides for parents of young athletes 8–18: nerves, confidence, motivation, growth spurts, strength, sleep and recovery.",
                   url=SITE + "/blog/", ogtype="website", site=SITE, book=BOOK,
                   schema=f'<script type="application/ld+json">{json.dumps(listing)}</script>')
page += f"""<header class="article-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / Blog</div>
<h1>The TSC Blog</h1>
<p>Practical guides on the mental and physical side of youth sport, for parents of athletes 8–18.</p>
</div></header>
<section style="padding-top:50px"><div class="container">
<div class="filter" role="group" aria-label="Filter by topic">{''.join(f'<button type="button" aria-pressed="{str(c=="All").lower()}" data-f="{c}">{c}</button>' for c in cats)}</div>
<div class="posts">{''.join(card(a) for a in ARTS)}</div>
</div></section>
<script>
document.querySelectorAll('[data-f]').forEach(function(b){{b.addEventListener('click',function(){{
 document.querySelectorAll('[data-f]').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});
 document.querySelectorAll('.post').forEach(function(p){{p.style.display=(b.dataset.f==='All'||p.dataset.cat===b.dataset.f)?'':'none'}});
}})}});
</script>
"""
page += FOOT.format(book=BOOK)
open("blog/index.html", "w").write(page)

# home cards (latest 3)
h = open("index.html").read()
block = "<!--POSTS-->" + "".join(card(a) for a in ARTS[:3]) + "<!--/POSTS-->"
if "<!--/POSTS-->" in h:
    h = re.sub(r"<!--POSTS-->.*?<!--/POSTS-->", block, h, flags=re.S)
else:
    h = h.replace("<!--POSTS-->", block)
open("index.html", "w").write(h)

# sitemap
urls = [("/", "1.0"), ("/blog/", "0.8"), ("/toolkit.html", "0.7"), ("/warmup.html", "0.6")] + [(f"/blog/{a['slug']}.html", "0.7") for a in ARTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}{u}</loc><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
open("sitemap.xml", "w").write(sm)
print(f"built {len(ARTS)} articles")
