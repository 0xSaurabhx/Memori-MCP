import chromadb

client = chromadb.PersistentClient(path="./db")  # New API
collection = client.get_or_create_collection("memory")

def add_memory(text: str, metadata: dict = {}):
    try:
        from embedding import get_embedding
        emb = get_embedding(text)
        print("Embedding length:", len(emb))
        
        # Get existing IDs to generate a new unique ID
        existing_data = collection.get()
        id_value = metadata.get("id", str(len(existing_data.get('ids', []))))
        
        collection.add(
            documents=[text],
            embeddings=[emb],
            metadatas=[metadata],
            ids=[id_value]
        )
        return {"status": "added", "id": id_value}
    except Exception as e:
        print(f"Error in add_memory: {e}")
        raise e

def search_memory(query: str, k: int = 3, category: str = None):
    try:
        # If there's no query but there's a category, return all memories for that category
        if not query.strip() and category:
            results = collection.get(
                where={"category": category} if category else None
            )
            return {
                "documents": [results.get("documents", [])],
                "metadatas": [results.get("metadatas", [])],
                "ids": [results.get("ids", [])],
                "distances": [[1.0] * len(results.get("documents", []))]
            }

        from embedding import get_embedding
        query_embedding = get_embedding(query)

        # Perform the search with category filter if specified
        where_clause = {"category": category} if category else None
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_clause
        )
        
        return {
            "documents": results.get("documents", [[]]),
            "metadatas": results.get("metadatas", [[]]),
            "ids": results.get("ids", [[]]),
            "scores": results.get("distances", [[]])
        }
    except Exception as e:
        print("Chroma query error:", e)
        return {
            "documents": [[]],
            "scores": [[]]
        }

def get_all_memories():
    try:
        results = collection.get()
        memories = []
        
        if results and results.get('documents'):
            for doc, meta, id in zip(results['documents'], results['metadatas'], results['ids']):
                # Include both the ID in metadata and as a top-level field
                meta['id'] = id  # Ensure ID is in metadata
                memories.append({
                    "text": doc,
                    "metadata": meta,
                    "id": id  # Add ID as a top-level field
                })
                
        return memories
    except Exception as e:
        print(f"Error getting all memories: {e}")
        return []

def delete_memory(id: str):
    try:
        collection.delete(ids=[id])
        return {"status": "deleted", "id": id}
    except Exception as e:
        print(f"Error in delete_memory: {e}")
        raise e

def update_memory(id: str, text: str = None, metadata: dict = None):
    try:
        # Get the existing memory
        results = collection.get(ids=[id])
        if not results or not results['ids']:
            raise ValueError(f"Memory with ID {id} not found")
        
        # Get the existing embedding or generate new one if text changed
        if text:
            from embedding import get_embedding
            embedding = get_embedding(text)
        else:
            # Keep existing embedding if text hasn't changed
            text = results['documents'][0]
            embedding = results['embeddings'][0]
        
        # Merge existing metadata with updates
        if metadata:
            existing_metadata = results['metadatas'][0]
            existing_metadata.update(metadata)
            metadata = existing_metadata
        else:
            metadata = results['metadatas'][0]
        
        # Delete old entry
        collection.delete(ids=[id])
        
        # Add updated entry with same ID
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[id]
        )
        
        return {"status": "updated", "id": id}
    except Exception as e:
        print(f"Error in update_memory: {e}")
        raise e
