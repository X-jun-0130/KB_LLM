import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"
import chromadb
from chromadb.config import Settings

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('Model_TH/text2vec-base-chinese/')

def Search_Query(query):
    emb = model.encode(query)
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./kb_data/",
        anonymized_telemetry=False  
        ))

    collection = client.get_collection('drug_kb', embedding_function=False)

    results = collection.query(
        query_embeddings=[emb],
        # query_texts=query,
        n_results=1,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
        )['documents']
    return results

# print(Search_Query('疏风散热胶囊适应证是什么'))
