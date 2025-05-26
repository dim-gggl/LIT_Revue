# <div align="center"> 📚 lit review 📖

## <div align="center">How-to

1. Authentication

Tout ce qui concerne la logique d'authentification ainsi que les relations entre utilisateurs se trouve dans l'app "authentication" du projet django.

On trouve les modèles `User` et `UserFollows` dans cette app. Définissant tous les deux les relations entre utilisateurs. Notamment pour ce qui est de la partie Abonnements de l'appli.

2. Main Feed

Tout le reste, donc le principal, est accessible via l'app Django `main_feed`. Ici, on trouve les modèles `Ticket` et `Review` par exemple, avec les formulaires et les vues leur correspondant.

Tout cette logique est accessible via, donc, les parties `forms.py`, `views.py` et `models.py` de l'app `main_feed`.
