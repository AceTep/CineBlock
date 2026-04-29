"""
Klijent za komunikaciju s Amazon Lex V2 Runtime API-jem.
Salje korisnicki tekst i vraca strukturirane podatke (intent + slots + confidence).
"""

import os
import uuid
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
LEX_BOT_ID = os.getenv("LEX_BOT_ID")
LEX_BOT_ALIAS_ID = os.getenv("LEX_BOT_ALIAS_ID")
LEX_LOCALE_ID = os.getenv("LEX_LOCALE_ID", "en_US")

# Globalni Lex klijent (jedna instanca po procesu)
_lex_client = None

# Globalni session ID - dijeli se kroz cijeli razgovor
# (u produkciji bi bilo per-user, sad imamo jednog korisnika u demo-u)
_session_id = str(uuid.uuid4())


def get_client():
    """Lazy-init Lex klijenta."""
    global _lex_client
    if _lex_client is None:
        _lex_client = boto3.client("lexv2-runtime", region_name=AWS_REGION)
    return _lex_client


def reset_session():
    """Resetira sessionId - novi razgovor s clean state-om."""
    global _session_id
    _session_id = str(uuid.uuid4())


def parse_message(text):
    """
    Salje tekst Lex-u i vraca strukturirane podatke.

    Returns:
        dict s kljucevima:
            - intent: str (naziv intencije)
            - intent_confidence: float
            - entities: dict (slot_name -> value)
            - lex_messages: list (poruke koje je Lex sam pripremio)
            - dialog_state: str (stanje razgovora: ElicitSlot, Fulfilled, ...)
            - error: str (ako je doslo do greske)
    """
    if not LEX_BOT_ID or not LEX_BOT_ALIAS_ID:
        return {
            "intent": None,
            "intent_confidence": 0.0,
            "entities": {},
            "lex_messages": [],
            "dialog_state": None,
            "error": "LEX_BOT_ID ili LEX_BOT_ALIAS_ID nisu postavljeni u .env"
        }

    try:
        client = get_client()
        response = client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId=LEX_LOCALE_ID,
            sessionId=_session_id,
            text=text
        )
    except (BotoCoreError, ClientError) as e:
        return {
            "intent": None,
            "intent_confidence": 0.0,
            "entities": {},
            "lex_messages": [],
            "dialog_state": None,
            "error": f"AWS Lex greska: {str(e)}"
        }

    # Izvuci intent + confidence iz interpretations
    interpretations = response.get("interpretations", [])
    intent_name = None
    intent_confidence = 0.0
    entities = {}

    if interpretations:
        # Prva interpretation je najvjerojatnija
        top = interpretations[0]
        intent_obj = top.get("intent", {})
        intent_name = intent_obj.get("name")
        # Confidence je u zasebnom polju
        nlu_conf = top.get("nluConfidence", {})
        if isinstance(nlu_conf, dict):
            intent_confidence = nlu_conf.get("score", 0.0)

        # Izvuci slotove (Lex slots = nasi entiteti)
        slots = intent_obj.get("slots") or {}
        for slot_name, slot_data in slots.items():
            if slot_data is None:
                continue
            slot_value = slot_data.get("value", {})
            # interpretedValue = ono sto je korisnik rekao
            # resolvedValues = lista mogucih kanonskih vrijednosti (zbog synonym-a)
            resolved = slot_value.get("resolvedValues") or []
            interpreted = slot_value.get("interpretedValue")
            # Preferiramo resolved (kanonska vrijednost iz slot type-a)
            if resolved:
                entities[slot_name] = resolved[0]
            elif interpreted:
                entities[slot_name] = interpreted

    # Lex moze sam vratiti poruke (closing response, slot prompts, ...)
    lex_messages = []
    for msg in response.get("messages", []):
        content = msg.get("content")
        if content:
            lex_messages.append(content)

    # Dialog state - korisno za debugging
    session_state = response.get("sessionState", {})
    dialog_action = session_state.get("dialogAction", {})
    dialog_state = dialog_action.get("type")  # ElicitSlot, Close, ...

    return {
        "intent": intent_name,
        "intent_confidence": intent_confidence,
        "entities": entities,
        "lex_messages": lex_messages,
        "dialog_state": dialog_state,
    }


if __name__ == "__main__":
    # Brzi test - pokreni: python lex_client.py
    test_messages = [
        "Hello",
        "Recommend me a sci-fi movie",
        "Tell me about Inception",
        "Show me Nolan movies",
        "What movies has Tom Hanks been in",
        "How good is The Matrix",
    ]
    for msg in test_messages:
        print(f"\n>>> {msg}")
        result = parse_message(msg)
        if result.get("error"):
            print(f"ERROR: {result['error']}")
            continue
        print(f"Intent: {result['intent']} (confidence: {result['intent_confidence']:.2f})")
        print(f"Entities: {result['entities']}")
        print(f"Dialog state: {result['dialog_state']}")
        if result['lex_messages']:
            print(f"Lex messages: {result['lex_messages']}")
