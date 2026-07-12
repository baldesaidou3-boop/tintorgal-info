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

### Mettre à jour les articles

1. Ouvrir `index.html`
2. Remplacer les articles dans `<section class="articles-grid">` et l'article principal dans `<section class="featured">`
3. Chaque article contient :
   - Une image placeholder (`https://placehold.co/...`)
   - Un tag (Politique, Société, Sport, etc.)
   - Un titre `<h2>` ou `<h3>`
   - Une date `<p class="meta">`
   - Un extrait `<p>`
   - Un lien vers la source complète (guineenews.org)

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
