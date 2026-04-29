# 🎬 CineBot (Amazon Lex V2)

Filmski chatbot powered by Amazon Lex V2, Flask i Pythonom.

## 🚀 Pokretanje

### 1. Stvori `.env` datoteku

```bash
cp .env.example .env
```

Otvori `.env` i popuni:

```
AWS_ACCESS_KEY_ID=AKIA...                    # od cinebot-api-user IAM korisnika
AWS_SECRET_ACCESS_KEY=tvoj_secret_key
AWS_REGION=eu-central-1
LEX_BOT_ID=EOIM8UTEVE
LEX_BOT_ALIAS_ID=PBYQXJU4W6
LEX_LOCALE_ID=en_US
FLASK_DEBUG=True
```

### 2. Instaliraj dependencies

```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Test Lex konekcije (PRIJE Flask-a)

```bash
python lex_client.py
```

Trebao bi vidjeti **6 test rečenica** s ispravno prepoznatim intencijama i slotovima.

### 4. Pokreni Flask aplikaciju

```bash
python app.py
```

Otvori u browseru: **http://localhost:5000**

## 📁 Struktura

| Datoteka | Što radi |
|---|---|
| `app.py` | Flask server (rute `/`, `/chat`, `/reset`) |
| `lex_client.py` | Komunikacija s Amazon Lex V2 Runtime API |
| `conversation.py` | Logika razgovora, handleri za 6 intencija |
| `movies.py` | Baza od 15 filmova |
| `templates/index.html` | Chat sučelje |

## 🎯 Što bot zna

- **6 intencija**: `RecommendMovie`, `MovieInfo`, `MoviesByActor`, `MoviesByDirector`, `MovieRating`, `Greeting`
- **4 slot type-a**: `MovieGenre`, `MovieTitle`, `Actor`, `Director`
- **Multi-turn razgovor**: Lex pamti session — ako kažeš "I want to watch a movie", bot pita "What genre?", a ti odgovoriš "horror" → bot zna da je to genre za prethodni intent
- **Synonym matching**: "Nolan" → `Christopher Nolan`, "DiCaprio" → `Leonardo DiCaprio`, itd.

## 💡 Primjeri pitanja

- "Recommend me a sci-fi movie"
- "Tell me about Inception"
- "What movies has Tom Hanks been in?"
- "Show me Nolan movies"
- "How good is The Matrix?"
- "Hello"

## 🐛 Troubleshooting

**Greška: "Could not connect to the endpoint URL"**
→ Provjeri `AWS_REGION` u `.env` — bot je u eu-central-1.

**Greška: "ResourceNotFoundException"**
→ Provjeri `LEX_BOT_ID` i `LEX_BOT_ALIAS_ID` — moraju biti točni iz Lex konzole.

**Greška: "AccessDeniedException"**
→ IAM korisnik nema `AmazonLexRunBotsOnly` policy. Vrati se u IAM i provjeri.

**Bot ne prepoznaje intencije**
→ Provjeri da je bot **buildan** i da alias pokazuje na **publishanu verziju** (ne Draft).
