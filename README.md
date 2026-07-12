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

## Notes

- Les images utilisent des placeholders placehold.co (pas de stockage local)
- Les articles pointent vers guineenews.org comme source
- Pas de base de données ni backend — site 100% statique
- Le fichier `baobab_tintorgal.svg` est un logo alternatif non utilisé
