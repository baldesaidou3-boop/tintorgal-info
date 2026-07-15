# Tintorgal Info

Site d'actualité guinéenne statique. Informations en continu.

## Stack

- **HTML / CSS / JS** — Site statique vanilla
- **Hébergement** — Netlify (`tintorgal-info.netlify.app`)
- **Source** — GitHub (`baldesaidou3-boop/tintorgal-info`)
- **CI/CD** — Netlify (auto-deploy depuis GitHub)

## Structure

```
tintorgal-info/
├── index.html            # Page d'accueil (articles + navigation)
├── assets/
│   ├── css/
│   │   └── style.css     # Styles du site
│   ├── js/
│   │   └── script.js     # Scripts (navigation active)
│   ├── images/           # Dossier images (vide, utilise placeholders)
│   ├── Tintorgal_Logo_Vectorise.svg   # Logo principal
│   └── baobab_tintorgal.svg           # Logo baobab (non utilisé actuellement)
└── README.md
```

## Mécanisme de mise à jour

Le site est entièrement statique. Les articles sont écrits directement dans `index.html`.

### Règle d'or — Couvrir TOUTES les catégories

Chaque mise à jour doit impérativement contenir **au moins un article par catégorie** :
- Politique
- Économie
- Sport
- Société
- Faits Divers
- Culture
- International / Monde

**Il ne faut jamais publier une mise à jour incomplète.** Si une catégorie n'a pas d'article récent, chercher plus loin ou sur une autre source.

### Mode de fonctionnement actuel

Chaque mise à jour est faite manuellement via l'assistant IA (opencode) :
1. L'assistant recherche les dernières infos sur les sites d'actualité guinéenne
2. Il sélectionne **au moins un article par catégorie**
3. Il met à jour le fichier `index.html`
4. Il commit et push sur GitHub
5. Netlify déploie automatiquement

**L'assistant IA est le seul à faire les recherches, les mises à jour et les pushs.**

### Catégories

Chaque catégorie a sa propre section sur la page d'accueil :

| Section      | Tag utilisé      |
|--------------|------------------|
| **À la une** | Article principal|
| Politique    | `Politique`      |
| Économie     | `Économie`       |
| Sport        | `Sport`          |
| Société      | `Société`        |
| Faits Divers | `Faits Divers`   |
| Culture      | `Culture`        |
| International| `Monde`          |

### Mettre à jour les articles

1. Ouvrir `index.html`
2. Pour chaque catégorie, remplacer les articles dans sa `<section class="articles-grid">`. Mettre à jour aussi l'article principal dans `<section class="featured">`
3. Chaque article contient :
   - Une image placeholder (`https://placehold.co/...`)
   - Un tag correspondant à la catégorie
   - Un titre `<h2>` ou `<h3>`
   - Une date `<p class="meta">`
   - Un extrait `<p>`
   - Un lien vers la source complète (guineenews.org)
4. Toujours vérifier qu'on a au moins **1 article par catégorie**

### Source par catégorie

Aller sur https://guineenews.org et filtrer par catégorie via le menu, ou utiliser les URLs directes :
- **Politique** : https://guineenews.org/category/news/politique/
- **Économie** : https://guineenews.org/category/news/economie/
- **Sport** : https://guineenews.org/category/sport/
- **Société** : chercher dans les articles récents
- **Faits Divers** : https://guineenews.org/category/news/faitsdivers/
- **Culture** : https://guineenews.org/category/news/artculture/
- **Monde** : https://guineenews.org/category/lemonde/

## Dernière mise à jour (15 juillet 2026)

| Section       | Titre |
|---------------|-------|
| **À la une**  | Simbaya : quatre personnes périssent dans un violent incendie |
| **Politique** | Kamsar : le DG de la CBG reçoit le nouveau maire |
| **Politique** | Guinée : la HAC désigne des superviseurs bénévoles |
| **Économie**  | Santé : l'Inde promet de renforcer son soutien à la Guinée |
| **Économie**  | Quand le retard de l'État redore le blason des semences locales |
| **Sport**     | NBA : Le Guinéen Alpha Diallo s'engage avec les Denver Nuggets |
| **Sport**     | Mondial 2026 : le rêve africain s'arrête en quarts |
| **Société**   | BEPC 2026 : taux de réussite national de 58,90% |
| **Société**   | Guinée : risque d'inondations extrêmes les 15 et 16 juillet |
| **Société**   | Kindia : les fruits hors de portée des consommateurs |
| **Faits Divers** | Sanoyah : un homme en uniforme tue un DJ dans une boîte de nuit |
| **Faits Divers** | Prison centrale : un garde pénitentiaire écope de 6 mois ferme |
| **Culture**   | Entretien exclusif avec Kabiné Kouyaté "Kaabi" |
| **Culture**   | Patrimoine culturel : vaste programme de recensement |
| **International** | Sénégal : un député alerte sur des menaces visant des Guinéens |
| **International** | UE : restrictions de visas temporaires pour les Guinéens |
| **International** | Drame en Côte d'Ivoire : famille guinéenne décimée |

### Déploiement (CI/CD)

1. `git add .`
2. `git commit -m "message"`
3. `git push`

Netlify détecte automatiquement le push sur `main` et redéploie le site en ~1-2 minutes.

### URLs

- **Site** : https://tintorgal-info.netlify.app
- **GitHub** : https://github.com/baldesaidou3-boop/tintorgal-info
- **Source des articles** : https://guineenews.org

## Commandes utiles

```bash
# Voir l'état
git status

# Préparer les fichiers
git add index.html

# Valider
git commit -m "Mise à jour des articles"

# Publier
git push
```

## Automatisation (GitHub Actions)

Le site se met à jour **automatiquement tous les jours à 8h00 UTC** (9h00 Conakry) via GitHub Actions.

### Fonctionnement

1. **Le script** `scripts/update_news.py` scrape les 3 sources (guineenews.org, africaguinee.com, guinee360.com)
2. Il collecte les articles par catégorie (Politique, Économie, Sport, Société, Faits Divers, Culture, Monde)
3. Il déduplique, classe par fraîcheur et génère le `index.html`
4. Si des modifications sont détectées, il commit et push automatiquement
5. Netlify redéploie le site

### Déclenchement manuel

Tu peux aussi lancer la mise à jour manuellement depuis GitHub :
1. Va sur https://github.com/baldesaidou3-boop/tintorgal-info/actions
2. Clique sur "Mise à jour quotidienne des articles"
3. Clique sur "Run workflow"

### Ajouter une source

Pour ajouter une source, édite `scripts/update_news.py` :
1. Ajoute une entrée dans la liste `SOURCES` (nom + URLs par catégorie)
2. Crée une fonction `parse_nom()` 
3. Ajoute-la dans le dictionnaire `parsers` de la fonction `collect_articles()`

## Notes

- Les images utilisent des placeholders placehold.co (pas de stockage local)
- Les articles pointent vers guineenews.org comme source
- Pas de base de données ni backend — site 100% statique
- Le fichier `baobab_tintorgal.svg` est un logo alternatif non utilisé
