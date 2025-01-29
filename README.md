## Installer python 3.10

Recommendation: Utiliser pyenv

Installation de pyenv sur (Mac)[https://github.com/pyenv/pyenv#homebrew-in-macos]  
Installation de pyenv sur (Windows)[https://github.com/pyenv-win/pyenv-win#installation]  
Installation de pyenv sur (Linux)[https://github.com/pyenv/pyenv-installer]

Une fois pyenv installé, il faut installer la bonne version de python (peut être modifiée)

```bash
pyenv install 3.11.7
```

### Changer de version python (avec pyenv)

```bash
pyenv shell 3.11.7
```

Puis vérifier :

> Windows

```cmd
python3 --version
```

> Mac/linux

```bash
python --version
```

### Environnement virtuel

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

#### Activer l'environnement virtuel

> Windows

```cmd
venv\Scripts\activate
```

> Mac/linux

```bash
. ./venv/bin/activate
```

#### Installer les requirements

Ainsi pour installer l'ensemble des packages il suffit d'exécuter:

```bash
pip install -r requirements.txt
```
