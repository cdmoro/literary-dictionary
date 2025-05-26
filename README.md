# 📚 Literary Dictionary for Kindle

**Your ultimate reading companion.**  
Lost in the maze of names from _One Hundred Years of Solitude_? Can’t remember if that magical object belonged to Frodo or Harry? This open-source **Literary Dictionary** helps you keep track of characters, places, and concepts from iconic books and sagas—right from your Kindle.

The dictionary is currently available in English and Spanish. Additional languages are planned for future releases. Each version is designed independently to ensure smooth reading and navigation on Kindle and other e-reader devices.

🎯 [Download the dictionary here](https://github.com/cdmoro/literary-dictionary/releases/latest)

## 🚀 What It Is

A Kindle-optimized literary dictionary designed to enrich your reading experience. Simply download it, install it, and start looking up unfamiliar names or phrases without ever leaving the page.

- Works with **single words** and **multi-word expressions**
- Supports books in **any language**
- Fully functional with **Kindle’s built-in dictionary system**

|Single Word|Multi-word Phrase|Foreign Language Support|
|---|---|---|
|﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿![image](https://github.com/user-attachments/assets/43fe84ab-9879-4b0f-a888-9b71d4f11e88)|![image](https://github.com/user-attachments/assets/826923f0-74ec-4d70-b62f-1fe823747b08)|![image](https://github.com/user-attachments/assets/8491310c-d80a-490f-a90a-2963b9d1badf)|

---

## ✍️ How It Works

Entries are neatly organized in YAML files by author. Each file can cover a single book, an entire saga, or just the broader universe.

### ✅ Entry Structure

Each entry includes:
- `entry`: Main term
- `alias` (optional): Alternative names
- `description`: Short explanation

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
