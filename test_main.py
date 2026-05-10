from main import app
import fixture
from fastapi.testclient import TestClient
import pytest

classification_label_dict_reverse = {
    0: "Αυτοκίνητο", 1: "Επιχειρήσεις και βιομηχανία", 2: "Έγκλημα και δικαιοσύνη",
    3: "Ειδήσεις για καταστροφές και έκτακτες ανάγκες", 4: "Οικονομικά και χρηματοοικονομικά", 5: "Εκπαίδευση",
    6: "Ψυχαγωγία και πολιτισμός", 7: "Περιβάλλον και κλίμα", 8: "Οικογένεια και σχέσεις",
    9: "Μόδα", 10: "Τρόφιμα και ποτά", 11: "Υγεία και ιατρική", 12: "Μεταφορές και υποδομές",
    13: "Ψυχική υγεία και ευεξία", 14: "Πολιτική και κυβέρνηση", 15: "Θρησκεία",
    16: "Αθλητισμός", 17: "Ταξίδια και αναψυχή", 18: "Τεχνολογία και επιστήμη"
}

ner_label_set = ["PAD", "O",
    "B-ORG", "I-ORG", "B-PERSON", "I-PERSON", "B-CARDINAL", "I-CARDINAL",
    "B-GPE", "I-GPE", "B-DATE", "I-DATE", "B-ORDINAL", "I-ORDINAL",
    "B-PERCENT", "I-PERCENT", "B-LOC", "I-LOC", "B-NORP", "I-NORP",
    "B-MONEY", "I-MONEY", "B-TIME", "I-TIME", "B-EVENT", "I-EVENT",
    "B-PRODUCT", "I-PRODUCT", "B-FAC", "I-FAC", "B-QUANTITY", "I-QUANTITY","[CLS]","[SEP]"
]
@pytest.fixture
def client():
    # Αυτή η συνάρτηση "γεννάει" τον client
    return TestClient(app)


def test_model(client):
    payload = {"sentence" : "Οι μετάλικα έκαναν θρίαμβο στο ΟΑΚΑ το βράδυ του Σαββάτου."}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    for dict1 in data["classification labels"]:
        assert dict1["label"] in classification_label_dict_reverse.values()
    for item in list(data["Named Entity Recognition Labels"].values()):
        
        assert item in ner_label_set

def test_health(client):  # pytest sees "client" parameter, finds the fixture, runs it, passes the result in
    response = client.get("/health")
    assert response.status_code == 200

def test_pydantic(client):
    payload = {"sentence" : "Ο"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    for dict1 in data["classification labels"]:
        assert dict1["label"] in classification_label_dict_reverse.values()
    for item in list(data["Named Entity Recognition Labels"].values()):
        
        assert item in ner_label_set
        
def test_pydantic2(client):
    payload = {"sentence" : ""}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_pydantic3(client):
    payload = {"sentence" : "Οι μετάλικα έκαναν θρίαμβο στο ΟΑΚΑ το βράδυ του Σαββάτου." * 100}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
