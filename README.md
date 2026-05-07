# TinyGreekNewsBERT-api
REST API serving a Greek news classification and NER model built on BERT
# Greek News BERT API

REST API serving a Greek news classification and NER model built on BERT.

Built with [TinyGreekNewsBERT](https://huggingface.co/katrjohn/TinyGreekNewsBERT) — a fine-tuned BERT model for Greek news text. Given a Greek sentence, the API returns the two most likely news categories and the named entities found in the text.

---

## Features

- **News Classification** — returns top 2 predicted categories with confidence scores
- **Named Entity Recognition** — tags tokens with entity types (person, organization, location, etc.)
- **Input validation** via Pydantic
- **Health check** endpoint

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/katrjohn/TinyGreekNewsBERT-api
cd TinyGreekNewsBERT-api
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the API**
```bash
uvicorn main:app --reload
```

**4. Open the interactive docs**
```
http://localhost:8000/docs
```

---

## Endpoints

### `POST /predict`

Accepts a Greek text string and returns classification labels and NER tags.

**Request:**
```json
{
  "sentence": "Η νέα τεχνολογία της katranis softworks δημιουργεί data centers τα οποία είναι φιλικά προς το περιβάλλον και δεν δημιουργούν ρύπους"
}
```

**Response:**
```json
	
Response body{
  "classification labels": [
    {
      "label": "Περιβάλλον και κλίμα",
      "confidence": 0.826
    },
    {
      "label": "Αυτοκίνητο",
      "confidence": 0.1243
    }
  ],
  "Named Entity Recognition Labels": {
    "[CLS]": "O",
    "η": "O",
    "νεα": "O",
    "τεχνολογια": "O",
    "της": "O",
    "kat": "B-PRODUCT",
    "##ran": "I-PRODUCT",
    "##is": "I-PRODUCT",
    "soft": "I-PRODUCT",
    "##works": "I-PRODUCT",
    "δημιουργει": "O",
    "data": "O",
    "center": "O",
    "##s": "O",
    "τα": "O",
    "οποια": "O",
    "ειναι": "O",
    "φιλικα": "O",
    "προς": "O",
    "το": "O",
    "περιβαλλον": "O",
    "και": "O",
    "δεν": "O",
    "δημιουργουν": "O",
    "ρυπου": "O",
    "##ς": "O",
    "[SEP]": "O"
  }
}
```

### `GET /health`

Returns API status.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Classification Categories

| ID | Category |
|---|---|
| 0 | Αυτοκίνητο |
| 1 | Επιχειρήσεις και βιομηχανία |
| 2 | Έγκλημα και δικαιοσύνη |
| 3 | Ειδήσεις για καταστροφές και έκτακτες ανάγκες |
| 4 | Οικονομικά και χρηματοοικονομικά |
| 5 | Εκπαίδευση |
| 6 | Ψυχαγωγία και πολιτισμός |
| 7 | Περιβάλλον και κλίμα |
| 8 | Οικογένεια και σχέσεις |
| 9 | Μόδα |
| 10 | Τρόφιμα και ποτά |
| 11 | Υγεία και ιατρική |
| 12 | Μεταφορές και υποδομές |
| 13 | Ψυχική υγεία και ευεξία |
| 14 | Πολιτική και κυβέρνηση |
| 15 | Θρησκεία |
| 16 | Αθλητισμός |
| 17 | Ταξίδια και αναψυχή |
| 18 | Τεχνολογία και επιστήμη |

---
## NER Labels
 
| Label | Description |
|---|---|
| O | No entity |
| B-ORG / I-ORG | Organization |
| B-PERSON / I-PERSON | Person |
| B-CARDINAL / I-CARDINAL | Cardinal number |
| B-GPE / I-GPE | Geopolitical entity (country, city) |
| B-DATE / I-DATE | Date |
| B-ORDINAL / I-ORDINAL | Ordinal number |
| B-PERCENT / I-PERCENT | Percentage |
| B-LOC / I-LOC | Location |
| B-NORP / I-NORP | Nationality, religious or political group |
| B-MONEY / I-MONEY | Monetary value |
| B-TIME / I-TIME | Time |
| B-EVENT / I-EVENT | Event |
| B-PRODUCT / I-PRODUCT | Product |
| B-FAC / I-FAC | Facility |
| B-QUANTITY / I-QUANTITY | Quantity |
 
`B-` marks the beginning of an entity. `I-` marks continuation of the same entity.
 
---

## Model

- **Classification + NER model:** [katrjohn/TinyGreekNewsBERT](https://huggingface.co/katrjohn/TinyGreekNewsBERT)
- **Tokenizer:** [nlpaueb/bert-base-greek-uncased-v1](https://huggingface.co/nlpaueb/bert-base-greek-uncased-v1)
