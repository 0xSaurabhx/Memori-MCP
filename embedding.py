import requests
import time

def get_embedding(text: str) -> list[float]:
    """Get embedding for text using Ollama API with retry logic."""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": text},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "embedding" not in result:
                raise ValueError("No embedding in response")
                
            return result["embedding"]
            
        except requests.exceptions.RequestException as e:
            print(f"Embedding request attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise e
        except Exception as e:
            print(f"Embedding error: {e}")
            raise e
