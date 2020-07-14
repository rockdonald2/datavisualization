# api/settings.py

# opcionális MONGO változók az adatbázis eléréséhez és hitelesítéshez
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# MONGO_USERNAME = 'user'
# MONGO_PASSWORD = 'user'

URL_PREFIX  = 'api'
MONGO_DBNAME = 'nobel_prize'
DOMAIN = {'winners_cleaned_w_bios': {
    'schema': {
        'country': {'type': 'string'},
        'category': {'type': 'string'},
        'name': {'type': 'string'},
        'year': {'type': 'integer'},
        'gender': {'type': 'string'},
        'award_age': {'type': 'integer'},
        'mini_bio': {'type': 'string'},
        'bio_image': {'type': 'string'}
    },
    'url': 'winners'
    # az url key lehetővé teszi azt, hogy eltérjünk az alapértelmezett eléréstől, ami a fenti hosszú,
    # tehát a jelenlegi elérés /api/winners?where...
}}
# a schema lehetővé teszi, hogy 'felfedjük' azokat a mezőket a winners_cleaned dokumentumunkból, amelyeket elérhetővé akarunk tenni
# valamint, azt is lehetővé teszi, hogy 'data validation'-t végezzünk

X_DOMAINS = '*'
HATEOAS = False
# a HATEOAS kikapcsolja azokat a linkeket, amelyekkel a response-ban találkozhatnánk: _links,
# ez a link arra vonatkozó információkat tartalmaz, hogy milyen a különböző elért erőforrások közötti kapcsolat: self, parent, next, prev, stb.
# így úgy lennénk képesek dinamikusan frissíteni a UI-t, vagy navigálni az API-ban, hogy nem tudjuk előre annak struktúráját,
# jelen esetben tudjuk, nincs szükség ezekre
PAGINATION = False
# minden eredményt egy állományban adjon vissza, nincs szükség oldalakra szedni őket