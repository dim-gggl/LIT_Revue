# <div align="center">🇬🇧 lit review

**lit review** is a web application designed to bring readers together. Key features include:
	•	Request a review (book, article, journal, etc.)
	•	Post reviews
	•	Follow other users
	•	Comment on reviews

⸻

## 🚀 Quick Start
1.	Clone the repository
```bash
git clone https://github.com/dim-gggl/LIT_Revue.git
cd LIT_Revue
```


2.	Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate         # macOS/Linux
env\Scripts\activate            # Windows
```

3.	Install dependencies

```bash
pip install -r requirements.txt
```

4.	Run the server

```bash
python manage.py runserver
```


Open your browser and go to: http://127.0.0.1:8000

⸻

### 👥 Test Accounts

| Username |	Password |
|---|---|
| reader	| azerty123 |
| critique |	azerty123 |
| library |	azerty123 |

Use these accounts to explore a pre-populated interface with posts, reviews, follows, and comments.

⸻

### 📁 Project Structure


`authentication/`:  user account management

`main_feed/`: posts, reviews, comments, follows
`templates/`: HTML templates
`static/`: CSS and other static files

⸻

🛠️ Key Files
	•	requirements.txt : Python dependencies
	•	manage.py        : Django CLI tool

⸻

### 📝 License

This code is distributed under the MIT License. See the LICENSE file for details.

---
---

# <div align="center">🇫🇷 lit review

**lit review** est une application web pensée pour rassembler la communauté des lecteurs, permettant à ses utilisateurs de :
- Demander une critique (de livre, d'article, de revue, etc.)
- De poster des critiques
- De suivre d'autres utilisateurs
- Et de commenter les critiques

---

## 🚀 Installation rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/dim-gggl/LIT_Revue.git
cd LIT_Revue
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv env
source env/bin/activate         # macOS/Linux
env\Scripts\activate            # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```


### 4. Lancer le serveur
```bash
python manage.py runserver
```
Accédez à l'application sur : http://127.0.0.1:8000

---

## 👥 Comptes de test

| Identifiant         | Mot de passe |
|---------------------|---------------|
| **reader**    | azerty123     |
| **critique**    | azerty123     |
| **library** | azerty123  |

Ces comptes permettent d’explorer une interface déjà peuplée de billets, critiques, abonnements et commentaires.

---

## 📁 Structure du projet

- `authentication/` : gestion des comptes utilisateurs
- `main_feed/` : billets, critiques, commentaires, suivis
- `templates/` : templates HTML
- `static/` : fichiers CSS

---

## 🛠️ Fichiers importants

- `requirements.txt` : dépendances Python
- `manage.py` : outil CLI de Django

## 📝 Licence

Code distribué sous licence MIT. Voir `LICENSE` pour plus d'infos.
