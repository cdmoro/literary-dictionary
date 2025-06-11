# 📚 Dizionario Letterario per Kindle

[![Traduzione: Inglese](https://img.shields.io/badge/traduzione-en-blue.svg)](README.md)
[![Traduzione: Spagnolo](https://img.shields.io/badge/traduzione-es-red.svg)](README.es.md)
[![Traduzione: Italiano](https://img.shields.io/badge/traduzione-it-green.svg)](README.it.md)
[![Traduzione: Francese](https://img.shields.io/badge/traduzione-fr-darkblue.svg)](README.fr.md)

**Il tuo compagno di lettura definitivo.**
Perso nel labirinto di nomi de _Cent'anni di solitudine_? Non ricordi se quell'oggetto magico appartenesse a Frodo o a Harry? Questo **Dizionario Letterario** open-source ti aiuta a tenere traccia di personaggi, luoghi e concetti di libri e saghe iconiche—direttamente dal tuo Kindle.

Il dizionario è attualmente disponibile nelle seguenti lingue:

- 🇬🇧 Inglese — [Scarica](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Literary.Dictionary.EN.v1.0.0.mobi)
- 🇪🇸 Spagnolo — [Scarica](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Diccionario.Literario.ES.v1.0.0.mobi)
- 🇮🇹 Italiano — Prossimamente!
- 🇫🇷 Francese — Prossimamente!

## 🛠️ Installazione

Installare il Dizionario Letterario per Kindle è semplice e veloce:

1. Scarica il file `.mobi` nella lingua desiderata dai link sopra.
1. Collega il Kindle al computer tramite cavo USB.
1. Copia il file `.mobi` nella cartella `documents/dictionaries` del tuo Kindle. Se la cartella non esiste, puoi crearla manualmente.
1. Espelli in sicurezza il Kindle e scollegalo dal computer.

## 🧭 Come si usa

Il Kindle non consente di selezionare dizionari personalizzati dalle impostazioni generali. Invece:

1. Apri un libro.
1. Seleziona una parola tenendo premuto su di essa.
1. Quando compare la definizione, tocca il nome del dizionario nella parte inferiore della finestra.
1. Scegli il **Dizionario Letterario** dall'elenco.

Il Kindle ricorderà questa scelta per le prossime letture in quella lingua.

## ✨ Caratteristiche

Il **Dizionario Letterario per Kindle** è costruito per rendere la tua esperienza di lettura più immersiva e meno confusa—accessibile direttamente dal dizionario integrato del tuo dispositivo.

### ✅ Funzionalità principali

- **Supporta sia parole singole che espressioni multi-parola**
- **Funziona con libri in qualsiasi lingua**
- **Pienamente compatibile con il sistema di dizionario nativo di Kindle**
- **Collega personaggi, luoghi e concetti tra universi letterari**
- **Restituisce più definizioni quando un nome ha più voci (es. cognomi di famiglia)**
- **Voci pulite e concise, ottimizzate per una consultazione rapida**
- **Leggero, facile da installare e senza distrazioni**

### 📸 Screenshot

| Ricerca di parola singola | Frase multi-parola | Supporto a definizioni multiple | Voci con riferimenti incrociati |
|:--------------------------:|:------------------:|:------------------------------:|:------------------------------:|
|<img src="./screenshots/it/01_definition.png" height="200px">|<img src="./screenshots/it/02_definition_group_of_words.png" height="200px">|<img src="./screenshots/it/03_multiple_definitions.png" height="200px">|<img src="./screenshots/it/04_dict.png" height="200px">|
| **Guida alle abbreviazioni** | **Indice delle voci per sezione** | **Sezione Autori** | **Sezione Saghe** |
|<img src="./screenshots/it/05_abbr_guide.png" height="200px">|<img src="./screenshots/it/06_entry_index.png" height="200px">|<img src="./screenshots/it/07_authors.png" height="200px">|<img src="./screenshots/it/08_sagas.png" height="200px">|

---

## 🛠️ Come contribuire

Ami i libri e la tecnologia? Unisciti alla missione!

- Suggerisci nuovi libri da includere
- Migliora gli script Python
- Segnala bug o richiedi funzionalità
- Condividi il tuo universo letterario preferito!

Puoi anche:
- ☕ [Offrimi un caffè](https://buymeacoffee.com/cdmoro)
- 🧉 [Invitami un cafecito](http://cafecito.app/cdmoro)
- 🎁 [Supportami su Patreon](https://patreon.com/cdmoro)

---

## 🧪 Setup per sviluppatori

Per costruire e testare il dizionario localmente:

```bash
git clone https://github.com/cdmoro/literary-dictionary.git
cd literary-dictionary
pip install -r requirements.txt
python ./main.py
```

Genererà un dizionario per ogni lingua nella cartella `output`.

Poi:

1. Apri Kindle Previewer
2. Carica l'EPUB generato o `dictionary_files_it/content.opf`
3. Esporta in formato MOBI
4. Copialo nella cartella `dictionaries` del tuo Kindle

Sei pronto per iniziare! 🔍📖

## 🙋‍♂️ Su di me

Ciao! Sono Carlos — appassionato di libri, programmatore e hacker Kindle.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Portiamo la letteratura alla vita, una ricerca alla volta.

## Licenza

![CC BY-NC-SA](assets/cc_banner.png)

Questo contenuto è concesso in licenza con una <a href="https://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribuzione-Non Commerciale 4.0 Internazionale (CC BY-NC 4.0)</a>. È permesso copiare, ridistribuire e modificare il contenuto purché venga riconosciuto il merito all'autore e non sia usato per scopi commerciali.
