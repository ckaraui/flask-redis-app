# Instructions pour agents Copilot

But : fournir à un agent IA le contexte essentiel pour être productif rapidement sur ce dépôt Flask + Redis.

- **Architecture générale** : application Flask basée sur un pattern factory (`create_app()` dans [app/__init__.py](app/__init__.py)). Les extensions partagées sont déclarées dans [app/extensions.py](app/extensions.py) (`db`, `migrate`, `cache`, `jwt`). Les routes sont organisées en blueprints dans [app/routes/](app/routes/).

- **Flux de données clés** : requête → blueprint (`app/routes/*`) → modèles (`app/models.py`) → `db.session` pour persistance. Le cache (`flask_caching`) est utilisé via des décorateurs `@cache.cached` (ex. [app/routes/books.py](app/routes/books.py)).

- **Exemples concrets** :
  - Auth : [app/routes/auth.py](app/routes/auth.py) — enregistrement, login (JWT via `flask_jwt_extended`) ; token créé avec `create_access_token(identity=str(user.id))`.
  - Caching : [app/routes/cache.py](app/routes/cache.py) et [app/routes/books.py](app/routes/books.py) utilisent `@cache.cached(timeout=...)` et `cache.clear()`.

- **Configuration & variables d'environnement** : voir [app/config.py](app/config.py).
  - `SQLALCHEMY_DATABASE_URI` prend `DATABASE_URL` ou tombe sur `sqlite:///data.db`.
  - `CACHE_TYPE` est `RedisCache` et l'hôte Redis utilisé est `CACHE_REDIS_HOST` (env `REDIS_HOST` par défaut dans le code). NOTE: le `README.md` mentionne `REDIS_URL`, mais le code ne le parse pas — préférez définir `CACHE_REDIS_HOST`/`CACHE_REDIS_PORT` ou mettre à jour le code si vous voulez supporter `REDIS_URL`.

- **Déploiement & démarrage** :
  - Local : `pip install -r requirements.txt`, exporter `DATABASE_URL`, `JWT_SECRET_KEY`, `CACHE_REDIS_HOST` ou utiliser Docker Compose.
  - Dockerfile / image : le conteneur exécute `python init_db.py && gunicorn -w 2 -b 0.0.0.0:5000 run:app` (voir `Dockerfile`). `run.py` expose `app = create_app()` pour Gunicorn.
  - `docker-compose.yml` fourni dans le repo démarre `flask_app` et `nginx_app`, mais **ne contient pas** de service Redis : soit fournissez un Redis externe, soit ajoutez un service `redis` (contradiction avec l'exemple du README).

- **Migrations vs init_db** : `Flask-Migrate` est inclus (extension `migrate`) mais la commande de démarrage du conteneur exécute `init_db.py` (qui fait `db.create_all()`). Lorsque vous modifiez les modèles, notez cette divergence :
  - Pour changements simples, `init_db.py` suffit.
  - Pour changements structurés/prod, préférez ajouter une migration Alembic via `flask db migrate` / `flask db upgrade`.

- **Conventions de code observées** :
  - Pas ou peu de gestion d'erreurs centralisée : les endpoints renvoient JSON et code HTTP directement.
  - Hachage de mot de passe avec `passlib.hash.bcrypt` dans `User.set_password` / `check_password`.
  - Identifiants JWT stockés comme `str(user.id)`.

- **Points d'attention (à vérifier avant PRs)** :
  - Alignement README ↔ code (ex. `REDIS_URL` mentionné mais non supporté).
  - Docker Compose n'inclut pas Redis — tests locaux peuvent échouer si Redis absent.
  - Si vous modifiez la config du cache, mettez à jour `app/config.py` et les variables d'env utilisées par Docker.

- **Quand et comment modifier** :
  - Modifier les modèles → mettre à jour `init_db.py` et/ou créer une migration (`Flask-Migrate`).
  - Ajouter endpoint → placer le blueprint sous `app/routes/`, utiliser `db.session` et respecter le style de réponses JSON.
  - Ajouter cache → utiliser `@cache.cached(timeout=...)`; pour invalidation utiliser `cache.clear()` ou clefs spécifiques selon besoin.

Si une section est peu claire ou si vous voulez que j'ajoute des règles supplémentaires (ex. templates de PR, style de commit, tests d'intégration), dites-moi lesquelles et j'itérerai.
