# 📚 Dicionário Literário para Kindle

[![Tradução: Inglês](https://img.shields.io/badge/tradução-en-blue.svg)](README.md)
[![Tradução: Espanhol](https://img.shields.io/badge/tradução-es-red.svg)](README.es.md)
[![Tradução: Italiano](https://img.shields.io/badge/tradução-it-green.svg)](README.it.md)
[![Tradução: Francês](https://img.shields.io/badge/tradução-fr-darkblue.svg)](README.fr.md)
[![Tradução: Português](https://img.shields.io/badge/tradução-pt-yellow.svg)](README.pt.md)

**Seu melhor companheiro de leitura.**  
Perdeu-se no labirinto de nomes de _Cem Anos de Solidão_? Não consegue lembrar se aquele objeto mágico pertencia a Frodo ou Harry? Este **Dicionário Literário** de código aberto ajuda você a acompanhar personagens, lugares e conceitos de livros e sagas icônicos — diretamente do seu Kindle.

O dicionário está disponível atualmente nos seguintes idiomas:

- 🇬🇧 Inglês — [Baixar](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Diccionario.Literario.EN.v1.0.0.mobi)
- 🇪🇸 Espanhol — [Baixar](https://github.com/cdmoro/literary-dictionary/releases/download/v1.0.0/Bonadeo.Carlos.-.Diccionario.Literario.ES.v1.0.0.mobi)
- 🇮🇹 Italiano — Em breve!
- 🇫🇷 Francês — Em breve!
- 🇧🇷 Português — Em breve!

## 🛠️ Instalação

Instalar o Dicionário Literário para Kindle é rápido e fácil:

1. Baixe o arquivo .mobi no idioma desejado usando os links acima.
1. Conecte seu Kindle ao computador via cabo USB.
1. Copie o arquivo .mobi para a pasta documents/dictionaries/ do seu Kindle. Se essa pasta não existir, você pode criá-la manualmente.
1. Ejetar com segurança e desconectar o Kindle.

## 🧭 Como usar

O Kindle não permite escolher dicionários personalizados nas configurações gerais. Em vez disso:

1. Abra um livro.
1. Selecione uma palavra tocando e segurando sobre ela.
1. Quando a definição aparecer, toque o nome do dicionário no topo da janela.
1. Escolha o Dicionário Literário da lista.

O Kindle vai lembrar essa escolha nas próximas leituras nesse idioma.

## ✨ Recursos

O **Dicionário Literário para Kindle** foi criado para tornar sua experiência de leitura mais imersiva e menos confusa — acessível diretamente do dicionário integrado ao seu dispositivo.

### ✅ Principais recursos

- **Suporta palavras únicas e expressões com várias palavras**
- **Funciona com livros em qualquer idioma**
- **Totalmente compatível com o sistema de dicionário nativo do Kindle**
- **Faz referências cruzadas entre personagens, lugares e conceitos em universos literários**
- **Retorna várias definições quando um nome tem mais de uma entrada (por exemplo, sobrenomes de família)**
- **Entradas limpas e concisas, otimizadas para pesquisa rápida**
- **Leve, fácil de instalar e sem distrações**

### 📸 Capturas de tela

| Pesquisa de palavra única | Frase com várias palavras | Suporte a múltiplas definições | Entradas de referência cruzada |
|:--------------------:|:-------------------:|:---------------------------:|:---------:|
|<img src="./screenshots/pt/01_definition.png" height="200px">|<img src="./screenshots/pt/02_definition_group_of_words.png" height="200px">|<img src="./screenshots/pt/03_multiple_definitions.png" height="200px">|<img src="./screenshots/pt/04_dict.png" height="200px">|
| **Guia de abreviações** | **Índice de entradas por seção** | **Seção de autores** | **Seção de sagas** |
|<img src="./screenshots/pt/05_abbr_guide.png" height="200px">|<img src="./screenshots/pt/06_entry_index.png" height="200px">|<img src="./screenshots/pt/07_authors.png" height="200px">|<img src="./screenshots/pt/08_sagas.png" height="200px">|

---

## 🛠️ Como contribuir

Adora livros e tecnologia? Junte-se à missão!

- Sugira novos livros para incluir
- Melhore os scripts Python
- Relate bugs ou solicite recursos
- Compartilhe seu universo literário favorito!

Você também pode:
- ☕ [Me pagar um café](https://buymeacoffee.com/cdmoro)
- 🧉 [Me convidar para um cafecito](http://cafecito.app/cdmoro)
- 🎁 [Apoiar no Patreon](https://patreon.com/cdmoro)

---

## 🧪 Configuração de desenvolvimento

Para compilar e testar o dicionário localmente:

```bash
git clone https://github.com/cdmoro/literary-dictionary.git
cd literary-dictionary
pip install -r requirements.txt
python ./main.py
```

Isso irá gerar vários dicionários por idioma na pasta `output`.

Em seguida:

1. Abra o Kindle Previewer 3
1. Carregue o EPUB gerado ou `dictionary_files_en/content.opf`
1. Exporte para MOBI
1. Copie para a pasta `documents/dictionaries` do seu Kindle

Você está pronto para começar! 🔍📖

## 🙋‍♂️ Sobre mim

Olá! Sou Carlos — amante de livros, programador e hacker do Kindle.

- 🐦 [Twitter](https://twitter.com/CarlosBonadeo)
- 💼 [LinkedIn](https://www.linkedin.com/in/cdbonadeo/)

Vamos dar vida à literatura, uma pesquisa de cada vez.

## Licença

![CC BY-NC-SA](assets/cc_banner.png)

Este conteúdo está licenciado sob uma licença [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). Você tem permissão para copiar, redistribuir e modificar o conteúdo, desde que o crédito adequado seja dado e ele não seja usado para fins comerciais.