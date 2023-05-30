import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"
import json
import chromadb
from chromadb.config import Settings

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('/Model_TH/text2vec-base-chinese/')

client = chromadb.Client()

def create_kb(kb_directory, kb_name, json_file):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=kb_directory,
        anonymized_telemetry=False 
        ))
    
    #创建数据库，并使用自定义embedding
    #client.delete_collection(kb_name) #删除原表
    collection = client.create_collection(name=kb_name, embedding_function=False)

    query_list = []
    metas_list = []
    ids_list = []
    embedding_list = []

    json_medical = json.load(open(json_file, 'r', encoding='utf-8'))
    for i, key in enumerate(json_medical[:9733]):
        name = key.split('\n')[0]
        query_list.append(key)
        embedding_list.append(model.encode(name))
        metas_list.append({'source':name})
        ids_list.append('m'+str(i+1))


    collection.add(
        documents=query_list, 
        embeddings=embedding_list,
        metadatas=metas_list, # filter on these!
        ids=ids_list, # unique for each doc
        )
    
    client.persist()


create_kb('./kb_data',  'drug_kb', './data/drug_disease_json.json')



# 使用自定义向量
# collection.add(
#    文章内容：documents=["doc1", "doc2", "doc3", ...],   
#    向量内容：embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
#    原始数据：metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
#    ID：ids=["id1", "id2", "id3", ...]
# )

