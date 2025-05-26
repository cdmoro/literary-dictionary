# 📚 Literary Dictionary for Kindle

**Your ultimate reading companion.**  
Lost in the maze of names from _One Hundred Years of Solitude_? Can’t remember if that magical object belonged to Frodo or Harry? This open-source **Literary Dictionary** helps you keep track of characters, places, and concepts from iconic books and sagas—right from your Kindle.

The dictionary is currently available in English and Spanish. Additional languages are planned for future releases. Each version is designed independently to ensure smooth reading and navigation on Kindle and other e-reader devices.

🎯 Download the latests version of the dictionary [here](https://github.com/cdmoro/literary-dictionary/releases/latest)

## ✨ Features

The **Literary Dictionary for Kindle** is designed to make your reading more immersive and less confusing—right from your device’s built-in dictionary tool.

### ✅ Key Features

- **Works with both single words and multi-word expressions**  
- **Supports books in any language**
- **Fully compatible with Kindle’s native dictionary system**
- **Cross-references characters, places, and concepts across literary universes**
- **Returns multiple definitions when a name matches more than one entry (e.g., family surnames)**
- **Clean and concise entries, optimized for fast lookup**
- **Lightweight, easy to install, and distraction-free**

### 📸 Screenshots

| Single Word Lookup | Multi-word Phrase | Foreign Language Support |
|--------------------|-------------------|---------------------------|
| ![Single Word Screenshot](./screenshots/single-word.png) | ![Multi-word Screenshot](./screenshots/multi-word.png) | ![Foreign Language Screenshot](./screenshots/foreign-language.png) |

| Cross-referenced Entry | Multiple Definitions | Abbreviation Guide |
|------------------------|------------------------|------------------------|
| ![Cross-reference Screenshot](./screenshots/cross-reference.png) | ![Multiple Definitions Screenshot](./screenshots/multiple-definitions.png) | ![Abbreviation Guide Screenshot](./screenshots/abbreviation-guide.png) |


---

## ✍️ How It Works

Entries are neatly organized in YAML files by author. Each file can cover a single book, an entire saga, or just the broader universe.

### ✅ Entry Structure

Each entry includes:
- `entry`: Main term
- `displayValue` (optional): Visual term
- `alias` (optional): Alternative names
- `description`: Definition

You can further categorize entries with:
- `characters`, `places`, `objects`, `concepts`, `events`, `creatures`, `institutions`, `spells`, `languages`, `quotes`

Everything you need, from Elvish languages to famous literary quotes.  
All stored in `dictionary/**/*.yaml`.

---

## 🛠️ How to Contribute

Love books and tech? Join the mission!

- Add new entries (in YAML format)
- Improve the Python scripts
- Report issues or suggest features
- Share your favorite literary universe!

You can also:
- ☕ [Buy me a coffee](https://buymeacoffee.com/cdmoro)
- 🧉 [Invite me a cafecito](http://cafecito.app/cdmoro)
- 🎁 [Support on Patreon](https://patreon.com/cdmoro)

---

## 🧪 Dev Setup

To build and test the dictionary locally:

```bash
git clone https://github.com/cdmoro/diccionario-literario.git
cd diccionario-literario
pip install -r requirements.txt
python scripts/build.py
```

It will generate several one dictionary per language in `output` folder.

Then:

1. Open Kindle Previewer
1. Load the generated EPUB or `dictionary_files_en/Dictionary.opf`
1. Export to MOBI
1. Copy to your Kindle’s dictionaries/ folder

You’re ready to go! 🔍📖

## 🙋‍♂️ About Me

Hi! I’m Carlos — book lover, coder, and Kindle hacker.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Let’s bring literature to life, one lookup at a time.
