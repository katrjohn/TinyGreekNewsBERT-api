from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer
import torch


app = FastAPI()

try:
    model = AutoModel.from_pretrained("katrjohn/TinyGreekNewsBERT", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/bert-base-greek-uncased-v1")
except Exception as e:
    raise RunTimeError(f"Model failded to load: {e}")


# Classification label dictionary (reverse)
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
    "B-PRODUCT", "I-PRODUCT", "B-FAC", "I-FAC", "B-QUANTITY", "I-QUANTITY"
]
tag2idx = {t:i for i,t in enumerate(ner_label_set)}
idx2tag = {i:t for t,i in tag2idx.items()}


class PredictRequest(BaseModel):
    sentence : str = Field(min_length = 1, description="Greek text to classify and tag")

@app.post("/predict")
def predict(request : PredictRequest):
    try:
        ner_preds_dict = {}
        cls_preds = []
        inputs = tokenizer(request.sentence, return_tensors="pt")
        with torch.no_grad():
            cls_logits,ner_logits = model(**inputs)
        cls_probs = torch.softmax(cls_logits, dim=-1)
        topk_results = torch.topk(cls_probs,k=2)
        cls_pred  = topk_results[1]
        cls_preds_probs = topk_results[0]

        for pred,prob in zip(cls_pred.flatten().tolist(), cls_preds_probs.flatten().tolist()):
            cls_preds.append(
                {
                "label" : classification_label_dict_reverse.get(pred, "Unknown"),
                "confidence" : round(prob,4)
                }
            )
        ner_predictions = torch.argmax(ner_logits, dim=-1).squeeze().tolist()
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze())
        for token, pred_idx in zip(tokens, ner_predictions):
            tag = idx2tag.get(pred_idx, "O")
            if token in ["[CLS]", "[SEP]"]:
                tag = "O"
            ner_preds_dict.update({token : tag})
        
        return {
                "classification labels" : cls_preds,
                "Named Entity Recognition Labels" : ner_preds_dict 
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
    
    
@app.get("/health")
def health():
    return {"status": "ok"}
    