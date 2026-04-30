from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
print("Client type:", type(client))
print(dir(client))
