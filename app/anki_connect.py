import json
import urllib.request

model_css = """.card {
    font-family: arial;
    font-size: 18px;
    text-align: center;
    color: black;
    background-color: white;
}
ul {
    padding: 0;
    list-style: none;
}

.translate .word {
    display: inline-block;
    margin: 4px;
    padding: 4px 12px;
    font-size: 18px;
    font-weight: bold;
    line-height: 1.2em;
    vertical-align: middle;
    color: rgba(25, 131, 255, 1);
    background-color: rgba(25, 131, 255, 0.05);
}

.ghost {
    font-size: 14px;
    color: rgba(0, 32, 51, 0.4);
}
"""
model_front = """<div class="note">
    <div class="main-container">
        <h1>{{Keyword}}</h1>
        <div class="example">{{Example}}</div>
    </div>
</div>
"""
model_back = """<div class="note">
    <div class="main-container">
        <h1>{{Keyword}}</h1>
        <div class="example">{{Example}}<br><span class="ghost">{{Example_translate}}</span></div>
        <hr id=answer>
        <div>{{Sound}}</div>
        <div class="translate">
            {{Translation}}
        </div>
        <div class="example">{{Examples}}</div>
    </div>
</div>
"""


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://127.0.0.1:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    # return response["result"]
    return response


def get_sync():
    """Synchronize the local Anki collections with AnkiWeb."""
    return invoke("sync")


def get_deck_names() -> list:
    """Get the complete list of deck names for the current user."""
    return invoke(action="deckNames")


def get_model_names() -> list:
    """Get the complete list of model names for the current user."""
    return invoke(action="modelNames")


def get_profiles() -> list:
    """Retrieve the list of profiles."""
    return invoke(action="getProfiles")


def load_profile(anki_profile: str) -> bool:
    """Retrieve the list of profiles."""
    return invoke("loadProfile", name=anki_profile)


def create_deck(deck_name) -> int:
    """Create a new empty deck.

    Will not overwrite a deck that exists with the same name.
    """
    return invoke(action="createDeck", deck=deck_name)


def create_model(model_name: str) -> dict:
    """Create a new model to be used in Anki."""
    return invoke(
        "createModel",
        modelName=model_name,
        inOrderFields=[
            "Keyword",
            "Example",
            "Example_translate",
            "Examples",
            "Translation",
            "Sound",
        ],
        css=model_css,
        isCloze=False,
        cardTemplates=[
            {
                "Name": "Card 1",
                "Front": model_front,
                "Back": model_back,
            }
        ],
    )


def add_note(deck: str, model: str, note: tuple) -> int:
    """Create a note using the given deck and model, with the provided
    field values and tags.

    Returns the identifier of the created note created on success, and
    null on failure.
    """
    return invoke(
        "addNote",
        note={
            "deckName": deck,
            "modelName": model,
            "fields": {
                "Keyword": note.get("keyword"),
                "Example": note.get("example"),
                "Example_translate": note.get("example_translate"),
                "Examples": note.get("examples"),
                "Translation": note.get("translation"),
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": deck,
                    "checkChildren": False,
                },
            },
            "audio": {
                "url": note.get("sound"),
                "filename": f"{note.get('keyword')}.mp3",
                "fields": [
                    "Sound",
                ],
            },
        },
    )


if __name__ == "__main__":
    anki_user_email = ""
    deck_name = "English"
    model_name = "CARDS"

    if deck_name not in get_deck_names().get("result"):
        create_deck(deck_name)
    if model_name not in get_model_names().get("result"):
        create_model(model_name)
