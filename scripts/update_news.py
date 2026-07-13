"""
Tintorgal Info - Agrégateur d'actualités multi-sources
Sources : guineenews.org, africaguinee.com, guinee360.com
Génère index.html avec articles classés par catégorie
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import sys
import html
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

CATEGORIES = ["Politique", "Économie", "Sport", "Société", "Faits Divers", "Culture", "Monde"]

ARTICLES_PER_CATEGORY = {
    "Politique": 2,
    "Économie": 2,
    "Sport": 2,
    "Société": 3,
    "Faits Divers": 2,
    "Culture": 2,
    "Monde": 3,
}

SOURCES = [
    {
        "name": "guineenews.org",
        "urls": {
            "Politique": "https://guineenews.org/category/news/politique/",
            "Économie": "https://guineenews.org/category/news/economie/",
            "Sport": "https://guineenews.org/category/sport/",
            "Société": "https://guineenews.org/",
            "Faits Divers": "https://guineenews.org/category/news/faitsdivers/",
            "Culture": "https://guineenews.org/category/news/artculture/",
            "Monde": "https://guineenews.org/category/lemonde/",
        },
    },
    {
        "name": "africaguinee.com",
        "urls": {
            "Politique": "https://www.africaguinee.com/category/guinee/politique/",
            "Économie": "https://www.africaguinee.com/category/guinee/economie/",
            "Sport": "https://www.africaguinee.com/category/sport/",
            "Société": "https://www.africaguinee.com/category/guinee/societe/",
            "Monde": "https://www.africaguinee.com/category/monde/",
        },
    },
    {
        "name": "guinee360.com",
        "urls": {
            "Politique": "https://www.guinee360.com/category/news/politique/",
            "Économie": "https://www.guinee360.com/category/news/economie/",
            "Sport": "https://www.guinee360.com/category/news/sport/",
            "Société": "https://www.guinee360.com/category/news/societe/",
            "Monde": "https://www.guinee360.com/category/news/monde/",
        },
    },
]


def fetch(url, timeout=15):
    try:
        resp = requests.get(url, timeout=timeout, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  [WARN] {url} -> {e}")
        return None


def extract_date(text):
    months = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12",
    }
    patterns = [
        r"(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})",
        r"(\d{4})-(\d{2})-(\d{2})",
        r"(\d{2})/(\d{2})/(\d{4})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            if len(m.groups()) == 3 and m.group(2).isdigit():
                return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            elif m.group(2).lower() in months:
                return f"{m.group(3)}-{months[m.group(2).lower()]}-{m.group(1).zfill(2)}"
    return ""


def parse_guineenews(html_text, category):
    soup = BeautifulSoup(html_text, "html.parser")
    articles = []
    articles_seen = set()

    for tag in soup.find_all(["h2", "h3"]):
        a = tag.find("a")
        if not a or not a.get("href"):
            continue
        url = a["href"]
        if not url.startswith("http"):
            url = "https://guineenews.org" + url
        title = a.get_text(strip=True)
        if not title or len(title) < 10:
            continue
        if url in articles_seen:
            continue
        articles_seen.add(url)

        excerpt = ""
        p = tag.find_next("p")
        if p:
            excerpt = p.get_text(strip=True)[:200]

        date_text = ""
        meta = tag.find_previous("time")
        if not meta:
            meta = tag.find_next("time")
        if meta:
            date_text = meta.get("datetime", "") or meta.get_text(strip=True)
        if not date_text:
            parent = tag.find_parent(["article", "div"])
            if parent:
                time_tag = parent.find("time")
                if time_tag:
                    date_text = time_tag.get("datetime", "") or time_tag.get_text(strip=True)
        if not date_text:
            date_text = tag.get_text()

        date = extract_date(date_text)

        articles.append({
            "title": title,
            "url": url,
            "date": date,
            "excerpt": excerpt or title,
            "category": category,
            "source": "guineenews.org",
        })

    return articles


def parse_africaguinee(html_text, category):
    soup = BeautifulSoup(html_text, "html.parser")
    articles = []
    articles_seen = set()

    for tag in soup.find_all(["h2", "h3", "h4"]):
        a = tag.find("a")
        if not a or not a.get("href"):
            continue
        url = a["href"]
        if not url.startswith("http"):
            url = "https://www.africaguinee.com" + url
        title = a.get_text(strip=True)
        if not title or len(title) < 10:
            continue
        if url in articles_seen:
            continue
        articles_seen.add(url)

        excerpt = ""
        parent = tag.find_parent(["article", "div", "li"])
        if parent:
            p = parent.find("p")
            if p:
                excerpt = p.get_text(strip=True)[:200]

        date_text = ""
        if parent:
            time_tag = parent.find("time")
            if time_tag:
                date_text = time_tag.get("datetime", "") or time_tag.get_text(strip=True)
            if not date_text:
                spans = parent.find_all("span", class_=re.compile(r"date|meta|time"))
                for sp in spans:
                    txt = sp.get_text(strip=True)
                    if re.search(r"\d{4}", txt):
                        date_text = txt
                        break

        date = extract_date(date_text)

        articles.append({
            "title": title,
            "url": url,
            "date": date,
            "excerpt": excerpt or title,
            "category": category,
            "source": "africaguinee.com",
        })

    return articles


def parse_guinee360(html_text, category):
    soup = BeautifulSoup(html_text, "html.parser")
    articles = []
    articles_seen = set()

    for tag in soup.find_all(["h2", "h3", "h4"]):
        a = tag.find("a")
        if not a or not a.get("href"):
            continue
        url = a["href"]
        if not url.startswith("http"):
            url = "https://www.guinee360.com" + url
        title = a.get_text(strip=True)
        if not title or len(title) < 10:
            continue
        if url in articles_seen:
            continue
        articles_seen.add(url)

        excerpt = ""
        parent = tag.find_parent(["article", "div", "li"])
        if parent:
            div = parent.find("div", class_=re.compile(r"excerpt|content|text"))
            if div:
                excerpt = div.get_text(strip=True)[:200]
            if not excerpt:
                p = parent.find("p")
                if p:
                    excerpt = p.get_text(strip=True)[:200]

        date_text = ""
        if parent:
            time_tag = parent.find("time")
            if time_tag:
                date_text = time_tag.get("datetime", "") or time_tag.get_text(strip=True)
            if not date_text:
                span = parent.find("span", class_=re.compile(r"date|meta|time|post"))
                if span:
                    date_text = span.get_text(strip=True)

        date = extract_date(date_text)

        articles.append({
            "title": title,
            "url": url,
            "date": date,
            "excerpt": excerpt or title,
            "category": category,
            "source": "guinee360.com",
        })

    return articles


def collect_articles():
    """Collect articles from all sources for all categories."""
    all_articles = []
    parsers = {
        "guineenews.org": parse_guineenews,
        "africaguinee.com": parse_africaguinee,
        "guinee360.com": parse_guinee360,
    }

    for source in SOURCES:
        name = source["name"]
        parser = parsers.get(name)
        if not parser:
            continue
        print(f"\n[{name}]")
        for cat, url in source["urls"].items():
            print(f"  Fetching {cat}...", end=" ")
            html = fetch(url)
            if html:
                articles = parser(html, cat)
                for a in articles:
                    a["category"] = cat
                all_articles.extend(articles)
                print(f"{len(articles)} articles")
            else:
                print("failed")

    print(f"\nTotal articles collected: {len(all_articles)}")
    return all_articles


def deduplicate_and_rank(articles):
    """Remove duplicates and rank by date freshness."""
    seen_urls = set()
    unique = []
    for a in articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique.append(a)

    def score(a):
        s = 0
        if a["date"]:
            try:
                dt = datetime.strptime(a["date"], "%Y-%m-%d")
                days_ago = (datetime.now() - dt).days
                if days_ago <= 1:
                    s += 100
                elif days_ago <= 3:
                    s += 50
                elif days_ago <= 7:
                    s += 20
            except:
                pass
        if len(a["title"]) > 30:
            s += 10
        if a["source"] == "guineenews.org":
            s += 5
        return s

    unique.sort(key=score, reverse=True)
    return unique


def pick_featured(articles_by_cat):
    """Pick the best article as featured."""
    all_flat = []
    for cat, arts in articles_by_cat.items():
        for a in arts:
            all_flat.append(a)

    def score(a):
        s = 0
        if a["date"]:
            try:
                dt = datetime.strptime(a["date"], "%Y-%m-%d")
                days_ago = (datetime.now() - dt).days
                if days_ago <= 1:
                    s += 100
                elif days_ago <= 2:
                    s += 50
            except:
                pass
        if len(a["title"]) > 40:
            s += 20
        return s

    all_flat.sort(key=score, reverse=True)
    if all_flat:
        return all_flat[0]
    return None


def slugify(text, max_len=30):
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "+", text.strip())
    return text[:max_len]


def generate_main_html(featured, articles_by_cat, today_str):
    """Generate the <main> section HTML."""

    def card_html(a, is_featured=False):
        tag = a["category"]
        title = html.escape(a["title"])
        excerpt = html.escape(a["excerpt"][:200])
        url = html.escape(a["url"])
        date = a["date"] if a["date"] else today_str

        if is_featured:
            img = f'https://placehold.co/800x400/1a365d/ffffff?text={slugify(a["title"], 50)}'
            return f"""      <article class="main-article">
        <img src="{img}" alt="{title}">
        <div class="content">
          <span class="tag">{tag}</span>
          <h2>{title}</h2>
          <p class="meta">{date}</p>
          <p>{excerpt}</p>
          <a href="{url}" target="_blank" class="read-more">Lire la suite →</a>
        </div>
      </article>"""
        else:
            short_title = slugify(a["title"], 40)
            img = f"https://placehold.co/400x250/2d3748/ffffff?text={short_title}"
            return f"""      <article class="card">
        <img src="{img}" alt="{slugify(a['title'])}">
        <div class="card-body">
          <span class="tag">{tag}</span>
          <h3>{title}</h3>
          <p class="meta">{date}</p>
          <p>{excerpt}</p>
          <a href="{url}" target="_blank" class="read-more">Lire →</a>
        </div>
      </article>"""

    lines = ['  <main class="container">']
    lines.append("    <section class=\"featured\">")
    if featured:
        lines.append(card_html(featured, is_featured=True))
    lines.append("    </section>")
    lines.append("")

    for cat in CATEGORIES:
        arts = articles_by_cat.get(cat, [])
        if not arts:
            continue
        lines.append(f"""    <section class="section-title">
      <div class="container">
        <h2 class="section-heading">{cat}</h2>
      </div>
    </section>""")
        lines.append("    <section class=\"articles-grid\">")
        for a in arts:
            lines.append(card_html(a))
        lines.append("    </section>")
        lines.append("")

    lines.append("  </main>")
    return "\n".join(lines)


def update_index_html(main_html):
    """Replace the <main> section in index.html."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    index_path = os.path.join(project_dir, "index.html")

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<main class="container">.*?</main>'
    new_content = re.sub(pattern, main_html, content, flags=re.DOTALL)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("\n[OK] index.html mis a jour")


def estimate_date(text):
    """Try to find a date string in article context."""
    months = "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"
    m = re.search(rf"(\d{{1,2}})\s+({months})\s+(\d{{4}})", text, re.IGNORECASE)
    if m:
        month_map = {"janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06",
                     "juillet":"07","août":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}
        return f"{m.group(3)}-{month_map[m.group(2).lower()]}-{m.group(1).zfill(2)}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


def main():
    print("=" * 50)
    print("Tintorgal Info - Agrégateur d'actualités")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    today = datetime.now().strftime("%Y-%m-%d")

    all_articles = collect_articles()

    if not all_articles:
        print("\n[ERREUR] Aucun article récupéré. Vérifie ta connexion.")
        sys.exit(1)

    print("\n--- Déduplication et classement ---")
    ranked = deduplicate_and_rank(all_articles)
    print(f"Articles uniques: {len(ranked)}")

    articles_by_cat = {cat: [] for cat in CATEGORIES}
    for a in ranked:
        cat = a["category"]
        if len(articles_by_cat[cat]) < ARTICLES_PER_CATEGORY.get(cat, 2):
            articles_by_cat[cat].append(a)

    print("\n--- Articles sélectionnés ---")
    for cat in CATEGORIES:
        arts = articles_by_cat.get(cat, [])
        print(f"  {cat}: {len(arts)} articles")
        for a in arts:
            print(f"    - [{a['source']}] {a['title'][:60]}...")

    featured = pick_featured(articles_by_cat)
    if featured:
        print(f"\n  À la une: [{featured['source']}] {featured['title'][:60]}...")

    main_html = generate_main_html(featured, articles_by_cat, today)
    update_index_html(main_html)
    print("\n[OK] Termine !")


if __name__ == "__main__":
    main()
