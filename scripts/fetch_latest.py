import requests, re, sys, os, json
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
TIMEOUT = 12

URLS = {
    'Politique': 'https://guineenews.org/category/news/politique/',
    'Économie': 'https://guineenews.org/category/news/economie/',
    'Sport': 'https://guineenews.org/category/sport/',
    'Société': 'https://guineenews.org/',
    'Faits Divers': 'https://guineenews.org/category/news/faitsdivers/',
    'Culture': 'https://guineenews.org/category/news/artculture/',
    'Monde': 'https://guineenews.org/category/lemonde/',
}

def extract_date(text):
    months = {'janvier':'01','février':'02','mars':'03','avril':'04','mai':'05','juin':'06',
              'juillet':'07','août':'08','septembre':'09','octobre':'10','novembre':'11','décembre':'12'}
    m = re.search(r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})', text, re.IGNORECASE)
    if m:
        return f"{m.group(3)}-{months[m.group(2).lower()]}-{m.group(1).zfill(2)}"
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ''

results = {}
for cat, url in URLS.items():
    results[cat] = []
    try:
        r = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        seen = set()
        for tag in soup.find_all(['h2', 'h3', 'h4']):
            a = tag.find('a')
            if not a or not a.get('href'): continue
            href = a['href']
            if not href.startswith('http'): href = 'https://guineenews.org' + href
            title = a.get_text(strip=True)
            if len(title) < 10 or href in seen: continue
            seen.add(href)
            date_text = ''
            for time_tag in tag.find_all_previous('time')[:1]:
                date_text = time_tag.get('datetime','') or time_tag.get_text(strip=True)
            if not date_text:
                for time_tag in tag.find_all_next('time')[:1]:
                    date_text = time_tag.get('datetime','') or time_tag.get_text(strip=True)
            if not date_text:
                parent = tag.find_parent(['article','div','li'])
                if parent:
                    t = parent.find('time')
                    if t: date_text = t.get('datetime','') or t.get_text(strip=True)
            date = extract_date(date_text)
            excerpt = ''
            p = tag.find_next('p')
            if p: excerpt = p.get_text(strip=True)[:200]
            results[cat].append({'title': title, 'url': href, 'date': date, 'excerpt': excerpt or title, 'category': cat})
        print(f'{cat}: {len(results[cat])} articles')
    except Exception as e:
        print(f'{cat}: ERROR - {e}')

print('\n--- RESULTATS ---')
print(json.dumps(results, ensure_ascii=False, indent=2))
