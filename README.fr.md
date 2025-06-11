# 📚 Dictionnaire littéraire pour Kindle

[![Traduction : Anglais](https://img.shields.io/badge/translation-en-blue.svg)](README.md)
[![Traduction : Espagnol](https://img.shields.io/badge/translation-es-red.svg)](README.es.md)
[![Traduction : Italien](https://img.shields.io/badge/translation-it-green.svg)](README.it.md)
[![Traduction : Français](https://img.shields.io/badge/translation-fr-darkblue.svg)](README.fr.md)

**Votre compagnon de lecture ultime.**
Vous vous perdez dans le dédale des noms de Cent ans de solitude ? Vous ne vous souvenez plus si cet objet magique appartenait à Frodon ou à Harry ? Ce **dictionnaire littéraire** open source vous aide à suivre les personnages, les lieux et les concepts des livres et sagas emblématiques, directement depuis votre Kindle.

Le dictionnaire est actuellement disponible dans les langues suivantes :

- 🇬🇧 Anglais — [Télécharger](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Diccionario.Literario.EN.v1.0.0.mobi)
- 🇪🇸 Espagnol — [Télécharger](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Diccionario.Literario.ES.v1.0.0.mobi)
- 🇮🇹 Italien — Bientôt disponible !
- 🇫🇷 Français — Bientôt disponible !

## 🛠️ Installation

L'installation du dictionnaire littéraire pour Kindle est rapide et facile :

1. Téléchargez le fichier `.mobi` dans la langue de votre choix à partir des liens ci-dessus.
1. Connectez votre Kindle à votre ordinateur via USB.
1. Copiez le fichier `.mobi` dans le dossier `documents/dictionaries` de votre Kindle. Si ce dossier n'existe pas, vous pouvez le créer manuellement.
1. Éjectez votre Kindle en toute sécurité et déconnectez-le de votre ordinateur.

## 🧭 Comment l'utiliser

Kindle ne vous permet pas de choisir un nouveau dictionnaire dans les paramètres généraux des dictionnaires personnalisés. À la place :

1. Ouvrez un livre.
1. Sélectionnez un mot en appuyant dessus et en le maintenant enfoncé.
1. Lorsque la définition apparaît, appuyez sur le nom du dictionnaire en bas de la fenêtre.
1. Choisissez le **Dictionnaire littéraire** dans la liste.

Votre Kindle mémorisera désormais ce choix pour les futures recherches dans les livres de cette langue.

## ✨ Caractéristiques

Le **Dictionnaire littéraire pour Kindle** est conçu pour rendre votre expérience de lecture plus immersive et moins confuse. Il est accessible directement depuis le dictionnaire intégré à votre appareil.

### ✅ Caractéristiques principales

- **Prend en charge les mots isolés et les expressions composées de plusieurs mots**  
- **Fonctionne avec des livres dans toutes les langues**
- **Entièrement compatible avec le système de dictionnaire natif de Kindle**
- **Références croisées entre les personnages, les lieux et les concepts à travers les univers littéraires**
- **Renvoie plusieurs définitions lorsqu'un nom a plus d'une entrée (par exemple, les noms de famille)**
- **Entrées claires et concises, optimisées pour une recherche rapide**
- **Léger, facile à installer et sans distraction**

### 📸 Captures d'écran

| Recherche d'un seul mot | Expression à plusieurs mots | Prise en charge de plusieurs définitions | Entrées de références croisées |
|:--------------------:|:-------------------:|:---------------------------:|:---------:|
|<img src="./screenshots/en/01_definition.png" height="200px">|<img src=". /screenshots/en/02_definition_group_of_words.png" height="200px">|<img src="./screenshots/en/03_multiple_definitions.png" height="200px">|<img src="./screenshots/en/04_dict.png" height="200px">|
| **Guide des abréviations** | **Index des entrées par section** | **Section auteurs** | **Section sagas** |
|<img src="./screenshots/en/05_abbr_guide.png" height="200px">|<img src="./screenshots/en/06_entry_index. png" height="200px">|<img src="./screenshots/en/07_authors.png" height="200px">|<img src="./screenshots/en/08_sagas.png" height="200px">|

---

## 🛠️ Comment contribuer

Vous aimez les livres et la technologie ? Rejoignez la mission !

- Suggérez de nouveaux livres à inclure
- Améliorez les scripts Python
- Signalez les bugs ou demandez des fonctionnalités
- Partagez votre univers littéraire préféré !

Vous pouvez également :
- ☕ [M'offrir un café](https://buymeacoffee.com/cdmoro)
- 🧉 [M'inviter à prendre un cafecito](http://cafecito.app/cdmoro)
- 🎁 [Me soutenir sur Patreon](https://patreon.com/cdmoro)

---

## 🧪 Configuration de développement

Pour compiler et tester le dictionnaire localement :

```bash
git clone https://github.com/cdmoro/literary-dictionary.git
cd literary-dictionary
pip install -r requirements.txt
python ./main.py
```

Cela générera plusieurs dictionnaires par langue dans le dossier « output ».

Ensuite :

1. Ouvrez Kindle Previewer 3.
1. Chargez l'EPUB généré ou « dictionary_files_en/content.opf ».
1. Exportez vers MOBI.
1. Copiez dans le dossier « documents/dictionaries » de votre Kindle.

Vous êtes prêt ! 🔍📖

## 🙋‍♂️ À propos de moi

Bonjour ! Je m'appelle Carlos, je suis passionné de lecture, codeur et hacker Kindle.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Donnez vie à la littérature, une recherche à la fois.

## Licence

![CC BY-NC-SA](assets/cc_banner.png)

Ce contenu est sous licence [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). Vous êtes autorisé à copier, redistribuer et modifier le contenu à condition d'en citer la source et de ne pas l'utiliser à des fins commerciales.