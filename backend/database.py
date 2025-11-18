from typing import Any, Dict, List, Optional
from datetime import datetime
import os
from pymongo import MongoClient

DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "appdb")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    now = datetime.utcnow()
    doc = {**data, "created_at": now, "updated_at": now}
    result = db[collection_name].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    db = get_db()
    query = filter_dict or {}
    items = db[collection_name].find(query).limit(limit)
    out: List[Dict[str, Any]] = []
    for it in items:
        it["_id"] = str(it["_id"])  # convert ObjectId to string
        out.append(it)
    return out
