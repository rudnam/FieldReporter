from aqt import mw
from aqt import Collection
from anki.collection import OpChangesWithCount

config = mw.addonManager.getConfig(__name__)["field_to_tag"]

SOURCE_FIELD = config["source_field"]
PREFIXES = config["prefixes"]
SUFFIXES = config["suffixes"]
REPLACEMENTS = config["replacements"]

def update_config():
    config = mw.addonManager.getConfig(__name__)["field_to_tag"]

    SOURCE_FIELD = config["source_field"]
    PREFIXES = config["prefixes"]
    SUFFIXES = config["suffixes"]
    REPLACEMENTS = config["replacements"]

# Removes the first found suffix
def remove_prefixes(field: str) -> str:
    for prefix in PREFIXES:
        if field.startswith(prefix):
            return field[len(prefix):]
    
    return field

# Removes the first found suffix
def remove_suffixes(field: str) -> str:
    for suffix in SUFFIXES:
        if field.endswith(suffix):
            return field[:-len(suffix)]
    
    return field

# Replaces occurrence of substring
def apply_replacements(original: str) -> str:
    stripped = remove_suffixes(remove_prefixes(original))
    for replacement in REPLACEMENTS:
        stripped = stripped.replace(replacement,REPLACEMENTS[replacement])
        
    return stripped

# Adds tags via the source field
def add_tags(col: Collection) -> None:
    if "field_to_tag" not in mw.addonManager.getConfig(__name__):
        return
    
    update_config()

    # Get all notes with the source field not-empty
    notes = [col.get_note(note_id) for note_id in col.find_notes(f"{SOURCE_FIELD}:_*")]

    for note in notes:
        # Attempt to use replacements
        tags = apply_replacements(note[SOURCE_FIELD])

        # Add tags
        for i in tags.split(" "):
            note.add_tag(i)

        # Wipe Source Field
        note[SOURCE_FIELD] = ""

    # Apply changes
    return col.update_notes(notes)
