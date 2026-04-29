"""
Logika razgovora za CineBot (Lex verzija).
Mapira Lex intent + slots u smislene odgovore iz baze filmova.
"""

import re
import random
import movies as movies_db


# Globalni kontekst (u produkciji bi bilo session-based)
context = {
    "last_movie": None,
    "last_intent": None,
    "last_genre": None,
    "last_actor": None,
    "last_director": None,
}


CONFIDENCE_THRESHOLD = 0.7  # ispod ovoga -> fallback


def is_gibberish(text):
    """
    Heuristika za prepoznavanje besmislenog inputa.
    Vraca True za stvari poput 'dsadsa', 'dasdsadas', 'qwertyuiop'.
    """
    if not text:
        return True
    cleaned = text.strip().lower()
    # Prekratko
    if len(cleaned) < 2:
        return True
    # Samo specijalni znakovi/brojevi (npr. "...", "123")
    if not re.search(r"[a-z]", cleaned):
        return True
    # Predugacak niz istih znakova (npr. 'aaaaaa', 'jjjjjj')
    if re.search(r"(.)\1{4,}", cleaned):
        return True

    # Ako tekst sadrzi razmake (vise od jedne rijeci), pretpostavljamo da je validan -
    # ljudi rijetko pisu vise besmislenih rijeci s razmacima namjerno
    if " " in cleaned:
        return False

    # Za jednu rijec - dodatne provjere
    letters_only = re.sub(r"[^a-z]", "", cleaned)
    if len(letters_only) < 2:
        return True

    # Nema ni jednog samoglasnika
    if not re.search(r"[aeiou]", letters_only):
        return True

    # Provjera omjera samoglasnika/suglasnika - prirodne engleske rijeci imaju
    # cca 35-45% samoglasnika. Random gibberish cesto ima manje od 25%
    vowels = sum(1 for c in letters_only if c in "aeiou")
    vowel_ratio = vowels / len(letters_only)
    if len(letters_only) >= 5 and vowel_ratio < 0.2:
        return True

    # Detekcija ponavljanja slogova/parova slova (npr. 'dsdsds', 'abab', 'dasdas')
    # Ako se isti par slova ponavlja 3+ puta zaredom, vjerojatno je gibberish
    if re.search(r"(.{2,3})\1{2,}", letters_only):
        return True

    return False


def reset_context():
    global context
    context = {
        "last_movie": None,
        "last_intent": None,
        "last_genre": None,
        "last_actor": None,
        "last_director": None,
    }


def format_movie_short(movie):
    return f"{movie['title']} ({movie['year']}) - rated {movie['rating']}/10"


def format_movie_list(movies, max_items=5):
    if not movies:
        return "No movies found."
    items = movies[:max_items]
    lines = [f"• {format_movie_short(m)}" for m in items]
    if len(movies) > max_items:
        lines.append(f"...and {len(movies) - max_items} more.")
    return "\n".join(lines)


def get_slot(entities, *names):
    """Vrati prvu vrijednost koja postoji od navedenih imena slotova."""
    for name in names:
        if name in entities and entities[name]:
            return entities[name]
    return None


def handle_recommend_movie(entities):
    """Preporuci film na temelju zanra."""
    candidates = movies_db.get_all_movies()
    filters_applied = []

    genre = get_slot(entities, "Genre", "GenreSlot")
    if genre:
        candidates = [m for m in candidates if genre.lower() in [g.lower() for g in m["genres"]]]
        filters_applied.append(f"genre '{genre}'")
        context["last_genre"] = genre

    if not candidates:
        criteria = " and ".join(filters_applied) if filters_applied else "those criteria"
        return f"Sorry, I don't have any movies matching {criteria} in my database."

    movie = random.choice(candidates)
    context["last_movie"] = movie

    if filters_applied:
        criteria = " and ".join(filters_applied)
        return (f"How about **{movie['title']}** ({movie['year']})? "
                f"It's a great pick for {criteria}, rated {movie['rating']}/10.\n\n"
                f"_{movie['description']}_")
    else:
        return (f"I'd recommend **{movie['title']}** ({movie['year']}) - "
                f"directed by {movie['director']}, rated {movie['rating']}/10.\n\n"
                f"_{movie['description']}_")


def handle_movie_info(entities):
    """Detaljne info o filmu."""
    title = get_slot(entities, "MovieTitleSlot", "MovieTitle")
    if title:
        movie = movies_db.find_by_title(title)
    elif context["last_movie"]:
        movie = context["last_movie"]
    else:
        return "Which movie would you like to know about?"

    if not movie:
        return f"Sorry, I don't have **{title}** in my database."

    context["last_movie"] = movie
    actors_str = ", ".join(movie["actors"])
    genres_str = ", ".join(movie["genres"])
    return (f"**{movie['title']}** ({movie['year']})\n"
            f"• Director: {movie['director']}\n"
            f"• Genres: {genres_str}\n"
            f"• Starring: {actors_str}\n"
            f"• Rating: {movie['rating']}/10\n\n"
            f"_{movie['description']}_")


def handle_movies_by_actor(entities):
    """Filmovi nekog glumca."""
    actor = get_slot(entities, "ActorSlot", "Actor")
    if not actor:
        return "Which actor are you interested in?"

    found = movies_db.find_by_actor(actor)
    context["last_actor"] = actor

    if not found:
        return f"Sorry, I don't have any **{actor}** movies in my database."

    context["last_movie"] = found[0]
    return f"Movies with **{actor}**:\n{format_movie_list(found)}"


def handle_movies_by_director(entities):
    """Filmovi nekog redatelja."""
    director = get_slot(entities, "DirectorSlot", "Director")
    if not director:
        return "Which director?"

    found = movies_db.find_by_director(director)
    context["last_director"] = director

    if not found:
        return f"Sorry, I don't have any movies by **{director}** in my database."

    context["last_movie"] = found[0]
    return f"Movies directed by **{director}**:\n{format_movie_list(found)}"


def handle_movie_rating(entities):
    """Ocjena filma."""
    title = get_slot(entities, "MovieTitleSlot", "MovieTitle")
    if title:
        movie = movies_db.find_by_title(title)
    elif context["last_movie"]:
        movie = context["last_movie"]
    else:
        return "Which movie's rating do you want to know?"

    if not movie:
        return f"Sorry, I don't have **{title}** in my database."

    context["last_movie"] = movie
    rating = movie["rating"]

    # Dinamicki odgovor ovisno o ocjeni
    if rating >= 9.0:
        verdict = "an absolute masterpiece"
    elif rating >= 8.5:
        verdict = "excellent"
    elif rating >= 8.0:
        verdict = "very good"
    elif rating >= 7.5:
        verdict = "solid"
    else:
        verdict = "decent"

    return f"**{movie['title']}** is rated **{rating}/10** - I'd say it's {verdict}."


def handle_greeting(entities):
    greetings = [
        "Hi there! I'm CineBot. Ask me about movies - I can recommend something, give you info on specific films, or list movies by actor or director.",
        "Hello! Ready to talk about movies? Try asking me to recommend something, or ask about a specific film.",
        "Hey! I'm CineBot - your movie companion. What would you like to know?"
    ]
    return random.choice(greetings)


def handle_fallback():
    return ("I'm not sure I understood that. I can help you with:\n"
            "• Recommending movies (by genre)\n"
            "• Information about specific films\n"
            "• Movies by an actor or director\n"
            "• Ratings of movies\n\n"
            "Try asking 'Recommend me a sci-fi movie' or 'Tell me about Inception'.")


# Mapiranje Lex intent imena -> handler funkcija
INTENT_HANDLERS = {
    "RecommendMovie": handle_recommend_movie,
    "MovieInfo": handle_movie_info,
    "MoviesByActor": handle_movies_by_actor,
    "MoviesByDirector": handle_movies_by_director,
    "MovieRating": handle_movie_rating,
    "Greeting": handle_greeting,
}


def respond(parsed, user_text=None):
    """
    Glavni ulaz - prima parsed podatke iz Lex-a, vraca string odgovora.

    user_text: originalni tekst korisnika (opcionalno) - koristi se za gibberish detekciju.
    """
    if parsed.get("error"):
        return f"⚠️ Error: {parsed['error']}"

    intent = parsed.get("intent")
    confidence = parsed.get("intent_confidence", 0.0)
    entities = parsed.get("entities", {})
    dialog_state = parsed.get("dialog_state")

    # 1. Gibberish detekcija - presreci besmislene unose prije bilo cega drugog
    if user_text and is_gibberish(user_text):
        return handle_fallback()

    # 2. Ako Lex zeli slot prompt (ElicitSlot), prikazi ga SAMO ako je confidence
    #    dovoljno visok (inace je Lex pogadjao i ne zelimo bezveze pitati za slot)
    if dialog_state == "ElicitSlot":
        if confidence >= CONFIDENCE_THRESHOLD:
            lex_msgs = parsed.get("lex_messages", [])
            if lex_msgs:
                return lex_msgs[0]
        # Inace - tretiramo kao fallback
        return handle_fallback()

    # 3. Niska confidence ili nepoznat intent -> fallback
    if not intent or intent == "FallbackIntent":
        return handle_fallback()
    if confidence < CONFIDENCE_THRESHOLD:
        return handle_fallback()

    handler = INTENT_HANDLERS.get(intent)
    if not handler:
        return handle_fallback()

    context["last_intent"] = intent
    return handler(entities)
