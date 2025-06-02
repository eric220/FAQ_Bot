from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2 # this is how you import in Chroma 0.5.0+
ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("faq_embeddings", embedding_function=ef)

with open('data/corpus.txt') as f:
    documents = [line.strip()   for line in f.readlines() if line.strip()]

ids = [f'id{i}' for i in range(len(documents))]
collection.add(
    documents = documents,
    ids = ids
)

def get_results(query_str: str):
    results = collection.query(query_texts=[f"{query_str}"], n_results=3)
    return results
    