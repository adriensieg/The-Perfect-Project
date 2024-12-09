import os
from google.cloud import firestore
import uuid

class FirestoreDB:
    def __init__(self):
        self.client = firestore.Client()
        self.collection_name = "history_data"

    def create_entry(self, original, processed):
        entry_id = str(uuid.uuid4())
        data = {
            "id": entry_id,
            "original": original,
            "processed": processed,
        }
        self.client.collection(self.collection_name).document(entry_id).set(data)
        return data

    def read_all_entries(self):
        docs = self.client.collection(self.collection_name).stream()
        return [doc.to_dict() for doc in docs]

    def update_entry(self, entry_id, original, processed):
        data = {"original": original, "processed": processed}
        self.client.collection(self.collection_name).document(entry_id).update(data)
        return self.client.collection(self.collection_name).document(entry_id).get().to_dict()

    def delete_entry(self, entry_id):
        self.client.collection(self.collection_name).document(entry_id).delete()
