Voici un fichier `README.md` bien structuré basé sur les informations fournies dans le fichier texte. Ce fichier résume les commandes nécessaires pour configurer et exécuter votre projet Django, tout en incluant des explications supplémentaires pour résoudre les erreurs courantes.

---

# README

Ce dépôt contient un projet Django avec une application appelée `documents`. Voici les étapes à suivre pour configurer et exécuter ce projet.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :
- **Python 3.11** : [Télécharger Python](https://www.python.org/downloads/)
- **pip** (gestionnaire de paquets Python) - inclus avec Python
- **Git** (facultatif) : [Télécharger Git](https://git-scm.com/downloads)

## Installation

### 1. Cloner le dépôt (si applicable)
Si vous avez accès au dépôt Git, clonez-le avec la commande suivante :

```bash
git clone https://github.com/bouiz05/CGI.git
cd cgi_project
```


### Environnement virtuel (optionnel)

#### Créer un environnement virtuel

Il faut s'assurer d'utiliser la bonne version de python (3.11.7)

> Windows

```cmd
python3 -m venv venv
```

> Mac/linux

```bash
python -m venv venv
```


- **Windows (PowerShell)** :
  
  ```powershell
  .\venv\Scripts\Activate
  ```
  Si vous rencontrez une erreur, essayez d'exécuter PowerShell en mode administrateur ou configurez votre stratégie d'exécution avec :
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **macOS/Linux** :
  ```bash
  source venv/bin/activate
  ```

#### Installer les requirements

Ainsi pour installer l'ensemble des packages il suffit d'exécuter:

```bash
pip install -r requirements.txt
```

### Appliquer les migrations
Exécutez les migrations pour configurer la base de données:

```bash
cd cgi_project
python manage.py migrate
python manage.py makemigrations
```
## Exécution

### 1. Démarrer le serveur de développement
Lancez le serveur de développement avec la commande suivante :

```bash
python manage.py runserver
```

Le serveur sera accessible à l'adresse suivante : [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 2. Accéder à l'API
Si vous utilisez Django REST Framework, l'API sera disponible à l'adresse suivante : [http://127.0.0.1:8000/myapp/test/](http://127.0.0.1:8000/myapp/test/).

## Manipulation avec Postman

Pour manipuler l’application, une vidéo de démonstration est disponible, déposé sur le Team de l’équipe 3, dans la section Fichiers.

Voici les 2 requêtes à utiliser sur Postman :
-	POST: http://localhost:8000/documents/
-	GET: http://localhost:8000/documents/DOCUMENT_ID_ICI_À_METTRE/extract-names/
- Pour tester un CV, plusieurs sont disponible dans la section pdf du repo : CGI\cgi_project\documents\pdf


## Résolution des erreurs courantes

### 1. `ModuleNotFoundError`
Si vous rencontrez une erreur comme `ModuleNotFoundError: No module named 'pdfminer.high_level'`, installez les dépendances manquantes :

```bash
pip install pdfminer.six
```

### 2. Problèmes d'activation de l'environnement virtuel
Si l'activation de l'environnement virtuel échoue sous Windows, vérifiez que votre stratégie d'exécution PowerShell est correctement configurée :

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Migrations non appliquées
Si vous voyez un message indiquant des migrations non appliquées, exécutez :

```bash
python manage.py migrate
```

## Tests

Pour exécuter les tests unitaires :

```bash
python manage.py test
```

## Contributions

Les contributions sont les bienvenues ! Voici comment contribuer :
1. Forkez ce dépôt.
2. Créez une nouvelle branche (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Committez vos changements (`git commit -am 'Ajout d\'une nouvelle fonctionnalité'`).
4. Poussez la branche (`git push origin feature/nouvelle-fonctionnalite`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

### Remarques supplémentaires

- Assurez-vous que toutes les dépendances sont installées avant d'exécuter le projet.
- Si vous travaillez avec des fichiers PDF ou des analyses de texte, vérifiez que les bibliothèques `spacy` et `pdfminer.six` sont correctement configurées.
- Pour mettre à jour `pip`, utilisez la commande suivante :
  ```bash
  python -m pip install --upgrade pip
  ```
- Contactez-nous sur la Canal Team, équipe 3, pour tout autre problème!
