import os
import time

cwd = "api.hamen.io/lexihub"

print("--- PROGRAM STARTED ---\n\n")

def writeDefinitions(content: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.post("https://www.api.hamen.io/lexihub/writeDefinitions.php", {
            "content": content,
            "password": "///"
        }, headers=headers)
    except:
        pass

def log(message: str, mode = "APPEND") -> None:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.post("https://www.api.hamen.io/lexihub/update.php", {
            "message": message + "\n",
            "password": "///",
            "mode": mode
        }, headers=headers)
    except:
        pass

    print("LOG: ", message)

def avg(data: list) -> float:
    return sum(data) / len(data)

log("IMPORT MODULES : Begin", mode="WRITE")

from wiktionaryparser import WiktionaryParser
import re
from pprint import pprint
import json
import requests
import ftplib
from bs4 import BeautifulSoup
from typing import Literal
from bs4.element import Tag
import nltk
import os
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown
from nltk.probability import FreqDist
from nltk.corpus.reader.wordnet import Synset

log("IMPORT MODULES : Completed")

def downloadNLTK(package: str) -> None:
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download(package)

class PluralForm:
    def __init__(self, baseWord: str, pluralForm: str, isIrregular: bool, locale: str = None):
        self.baseWord: str = baseWord
        self.pluralForm: str = pluralForm
        self.isIrregular: bool = isIrregular
        self.locale: str = locale
    
    def toObj(self) -> dict:
        return {
            "pluralForm": self.pluralForm,
            "isIrregular": self.isIrregular,
            "locale": self.locale
        }

class Pronunciations:
    def __init__(self, word: str, IPA: str | list[str], locale: str | list[str], audio: str = None):
        self.baseWord: str = word
        self.IPA: list[str] = IPA if type(IPA) is list else [IPA]
        self.locale: list[str] = locale if type(locale) is list else [locale]
        self.audio: str | None = audio

    def __str__(self) -> str:
        return f"({', '.join(self.locale)}): {', '.join(self.IPA)}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def toObj(self) -> dict:
        return {
            "IPA": self.IPA,
            "locale": self.locale,
            "audio": self.audio
        }

class WordRelationships:
    def __init__(
            self,
            word: str,
            *,
            hyponyms: list[str] = [],
            synonyms: list[str] = [],
            holonyms: list[str] = [],
            antonyms: list[str] = [],
            meronyms: list[str] = [],
            hypernyms: list[str] = []
        ):
        self.baseWord: str = word
        self.hyponyms: list[str] = hyponyms
        self.synonyms: list[str] = synonyms
        self.holonyms: list[str] = holonyms
        self.antonyms: list[str] = antonyms
        self.meronyms: list[str] = meronyms
        self.hypernyms: list[str] = hypernyms

    def asDict(self) -> dict:
        return dict({
            "hyponym": self.hyponyms,
            "synonym": self.synonyms,
            "holonym": self.holonyms,
            "antonym": self.antonyms,
            "meronym": self.meronyms,
            "hypernym": self.hypernyms
        })

    def asJSON(self) -> str:
        return json.dumps(self.asDict())

class PartOfSpeech:
    def __init__(self, classification: str, subClassification: str = None):
        self.classification: str = classification
        self.subClassification: str = subClassification or ""
    
    def toObj(self) -> dict:
        return {
            "partOfSpeech": self.classification,
            "classification": self.subClassification
        }

class Translation:
    def __init__(
            self,
            language: str = None,
            translation: str = None,
            *,
            qualifier: Literal["general", "literally", "formally", "colloquially"] = None,
            languageCode: str = None,
            transliteration: str = None,
        ):
        self.translationLanguage: str = language or ""
        self.translationLanguageCode: str = languageCode
        self.translationText: str = translation or ""
        self.translationQualifier: Literal["general", "literally", "formally", "colloquially"] = qualifier or "general"
        self.translationTextTransliteration: str = transliteration

class Translations:
    def __init__(self, word: str, *translations: Translation):
        self.baseWord = word
        self._translations: list[Translation] = list(translations)

class Entry:
    def __init__(self, word: str):
        self.word = word
        self.wordLemma: str = ""
        self.wordPronunciations: list[Pronunciations] = []
        self.wordPartOfSpeech: PartOfSpeech = None
        self.wordEtymology: str = ""
        self.wordDefinitions: list[str] = []
        self.wordPlurals: list[PluralForm] = []
        self.wordRelationships: WordRelationships = None
        self.wordExamples: list[str] = []
        self.wordFirstKnownUse: str = ""
        self.wordQuotes: list[str] = []
        self.wordTranslations: dict = dict()
        self.wordAlternativeSpellings: list[str] = []
        self.wordRhymeIPA: str = ""
        self.wordRhymes: list[str] = []
        self.wordFrequency: dict = dict()
        self.wordConjugations: dict = dict()
        self.wordFacts: list[str] = []

    def toDict(self) -> dict:
        return {
            "baseWord": self.word,
            "wordLemma": self.wordLemma,
            "wordPronunciations": [x.toObj() for x in self.wordPronunciations],
            "wordPartOfSpeech": self.wordPartOfSpeech,
            "wordEtymology": self.wordEtymology,
            "wordDefinitions": self.wordDefinitions,
            "wordPlurals": [x.toObj() for x in self.wordPlurals],
            "wordRelationships": self.wordRelationships.asDict(),
            "wordExamples": self.wordExamples,
            "wordFirstKnownUse": self.wordFirstKnownUse,
            "wordQuotes": self.wordQuotes,
            "wordTranslations": self.wordTranslations,
            "wordAlternativeSpellings": self.wordAlternativeSpellings,
            "wordRhymeIPA": self.wordRhymeIPA,
            "wordRhymes": self.wordRhymes,
            "wordFrequency": self.wordFrequency,
            "wordConjugations": self.wordConjugations,
            "wordFacts": self.wordFacts
        }

class Word:
    def __init__(self, word: str):
        self.word = word.lower()

        self._wordList = []
        sort_word = lambda word: "".join(sorted(word.lower()))
        with open(os.path.join(os.path.dirname(__file__), "words.txt")) as file:
            self._wordList = file.read().split("\n")
        sorted_target = sort_word(self.word)

        self.lemmatizer = WordNetLemmatizer()

        self.wiktionaryParser = WiktionaryParser()
        self.wiktionaryWord = self.wiktionaryParser.fetch(self.word.lower())
        self.wiktionaryWord = self.wiktionaryWord

        self.wordAnagrams = [word for word in self._wordList if sort_word(word) == sorted_target and word.strip().lower() != self.word.lower()]
    
    def _wordFrequency(self, word: str) -> int:
        start = 1650
        end = 2019
        params = {
            "content": word,
            "year_start": str(start),
            "year_end": str(end)
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
        }

        data = requests.get("https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30).text
        data = json.loads(data)
        data = data[0]["timeseries"]

        return {i+start: v for i,v in enumerate(data)}

    def _wordTranslations(self, word: str) -> dict:
        languages = dict({
            "spanish": "https://www.wordreference.com/es/translation.asp?tranword=%s",
            "italian": "https://www.wordreference.com/enit/%s",
            "german": "https://www.wordreference.com/ende/%s",
            "french": "https://www.wordreference.com/enfr/%s",
            "dutch": "https://www.wordreference.com/ennl/%s"
        })

        languages = {k: v % word for k,v in languages.items()}

        translations = dict()
        for language,url in languages.items():
            translations[language] = []
            data = requests.get(url)
            data = BeautifulSoup(data.text, "lxml")
            words = data.find(id="articleWRD")
            words = words.find("table")
            if not words:
                continue
            rows = words.find_all("tr", attrs={"class": ["odd", "even"]})
            for row in rows:
                if not row.find(class_="ToWrd") or type(row) is not Tag: continue
                row: Tag
                translations[language].extend([y for y in [x.text.split(",") for x in row.find_all(class_="ToWrd")]])

        return translations

    @property
    def wordEntries(self) -> list[Entry]:
        entries = []
        for entry in self.wiktionaryWord:
            etymology = entry.get("etymology")
            _pronunciations = entry.get("pronunciations")

            # Get lemma form:
            lemma = self.lemmatizer.lemmatize(self.word)

            # Get pronunciations and rhyme:
            pronunciations = []
            rhymeIPA = ""
            for pro in _pronunciations.get("text") or []:
                pro: str
                if "Rhymes" in pro:
                    rhymeIPA = pro.split(":")[-1].strip()
                    continue

                locale = "General"
                IPAs = pro
                if ":" in pro:
                    locale,IPAs = [x.strip() for x in pro.split(":", 1)]
                    locale = re.findall(r"\(.*?\)", locale)
                    if locale:
                        locale = locale[0][1:-1]
                        locale = [x.strip() for x in locale.split(",")]

                IPAs = [x.strip() for x in IPAs.split(",")]
                pronunciations.append(Pronunciations(self.word, IPAs, locale, ""))

            for definition in entry["definitions"]:
                pos = definition["partOfSpeech"]
                examples = definition["examples"]
                _rel = definition["relatedWords"]
                rel = dict({r.get("relationshipType"): r.get("words") for r in _rel})
                definitions = definition["text"]
                
                _entry = Entry(self.word)
                _entry.wordLemma = lemma
                _entry.wordPronunciations = pronunciations
                _entry.wordRhymeIPA = rhymeIPA
                _entry.wordEtymology = etymology
                _entry.wordExamples = examples
                _entry.wordPartOfSpeech = pos
                _entry.wordDefinitions = definitions
                _entry.wordRelationships = WordRelationships(
                    self.word,
                    hyponyms=rel.get("hyponyms"),
                    synonyms=rel.get("synonyms"),
                    holonyms=rel.get("holonyms"),
                    antonyms=rel.get("antonyms"),
                    meronyms=rel.get("meronyms"),
                    hypernyms=rel.get("hypernyms"),
                )
                _entry.wordFrequency = self._wordFrequency(self.word)
                _entry.wordAlternativeSpellings
                _entry.wordConjugations
                _entry.wordFacts
                _entry.wordFirstKnownUse
                _entry.wordPlurals
                _entry.wordQuotes
                _entry.wordRhymes
                _entry.wordTranslations = self._wordTranslations(self.word)

                entries.append(_entry)

        return entries

log("OPEN WORDLIST : Begin")

wordList = dict()
failed = 0
success = 0
with open(r"api.hamen.io/lexihub/words.txt", "r") as file:
    words = file.read().split("\n")
    log("OPEN WORDLIST : Completed")
    times = []
    for i,word in enumerate(words):
        fail = False
        if i % 10 == 0: os.system("clear")
        start = time.time()
        try:
            w = Word(word.lower())
            if w.wordEntries:
                wordList[word.lower()] = [x.toDict() for x in w.wordEntries]
                with open(r"api.hamen.io/lexihub/definitions.json", "w+") as definitions:
                    definitions.write(json.dumps(wordList))
                    writeDefinitions(json.dumps(wordList))
            else:
                fail = True

        except:
            fail = True
        
        _time = round(round(time.time() - start, 2) * len(words), 2)
        times.append(_time)
        if fail:
            failed += 1
        else:
            success += 1
        log(f"\rStatus: {str(round(i / len(words), 2) * 100).zfill(5)}%; Failed: {str(failed).zfill(len(str(len(words))))} && Success: {str(success).zfill(len(str(len(words))))} && Est. Time: {str(_time).zfill(12)} / {str(round(_time/3600, 2)).zfill(12)} [ Avg. {str(round(avg(times), 2)).zfill(12)} / {str(round(avg(times)/3600, 2)).zfill(12)} ] hours / days && Checked Word: \"{word}\"")

with open(r"api.hamen.io/lexihub/definitions.json", "w+") as definitions:
    definitions.write(json.dumps(wordList))
    writeDefinitions(json.dumps(wordList))

print("\n\n--- PROGRAM ENDED ---")