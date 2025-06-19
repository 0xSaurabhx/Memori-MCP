from fastmcp import FastMCP
from memory import add_memory, search_memory, get_all_memories, delete_memory, update_memory
from typing import List, Dict
import logging
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import humanize
from datetime import datetime
import socket
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except socket.error:
            return True

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    port = start_port
    while port < start_port + max_attempts:
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"No available ports found between {start_port} and {start_port + max_attempts - 1}")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

mcp = FastMCP(name="Memori")

# Web interface routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/memories')
def get_memories():
    memories = get_all_memories()
    return jsonify(memories)

@app.route('/api/memories/create', methods=['POST'])
def create_memory():
    try:
        data = request.json
        if not data or 'text' not in data or 'id' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        text = data['text']
        id = data['id']
        metadata = data.get('metadata', {})
        
        result = add_memory(text, metadata)
        return jsonify({'status': 'success', 'id': result['id']})
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/memories/search')
def search_memories_api():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    
    # Pass both query and category to search_memory
    results = search_memory(query, k=10, category=category if category else None)
    memories = []
    
    if results:
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
        
        for doc, meta, id in zip(documents, metadatas, ids):
            meta['id'] = id  # Ensure ID is in metadata
            memories.append({
                "text": doc,
                "metadata": meta,
                "id": id
            })
    
    return jsonify(memories)

@app.route('/api/memories/<string:memory_id>', methods=['DELETE'])
def delete_memory_api(memory_id):
    try:
        result = delete_memory(memory_id)
        return jsonify({'status': 'success', 'id': result['id']})
    except Exception as e:
        logger.error(f"Error deleting memory: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/memories/<string:memory_id>', methods=['PUT'])
def update_memory_api(memory_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No update data provided'}), 400
            
        text = data.get('text')
        metadata = data.get('metadata')
        
        if not text and not metadata:
            return jsonify({'error': 'No update data provided'}), 400
            
        result = update_memory(memory_id, text, metadata)
        return jsonify({'status': 'success', 'id': result['id']})
    except Exception as e:
        logger.error(f"Error updating memory: {e}")
        return jsonify({'error': str(e)}), 500

# MCP tools
@mcp.tool()
def store_memory(text: str, id: str, metadata: Dict = {}) -> str:
    """Store a memory with given text, id, and optional metadata."""
    try:
        logger.info(f"Storing memory with ID: {id}")
        
        if not text or not text.strip():
            return "Error: Text cannot be empty"
        
        if not id or not id.strip():
            return "Error: ID cannot be empty"
        
        # Add timestamp and default category if not present
        metadata["id"] = id
        metadata["timestamp"] = datetime.now().isoformat()
        if "category" not in metadata:
            metadata["category"] = "General"
        
        result = add_memory(text, metadata)
        success_msg = f"Memory [{result['id']}] stored successfully."
        logger.info(success_msg)
        return success_msg
    except Exception as e:
        error_msg = f"Error storing memory: {str(e)}"
        logger.error(error_msg)
        return error_msg  

@mcp.tool()
def recall(query: str, k: int = 3) -> str:
    """Recall memories based on a query string."""
    try:
        logger.info(f"Recalling memories for query: {query}")
        
        if not query or not query.strip():
            return json.dumps([{"text": "Error: Query cannot be empty", "score": 0.0}])
         
        if k <= 0:
            k = 3
            
        results = search_memory(query, k)

        # Handle empty result structure safely
        documents = results.get("documents", [[]])[0] if results.get("documents") else []
        scores = results.get("scores", [[]])[0] if results.get("scores") else []

        if not documents:
            return json.dumps([{"text": "No memory found.", "score": 0.0}])

        # Ensure we have matching lengths
        min_length = min(len(documents), len(scores))
        result_list = [{"text": documents[i], "score": float(scores[i])} for i in range(min_length)]
        logger.info(f"Found {len(result_list)} memories")
        return json.dumps(result_list)
    
    except Exception as e:
        error_msg = f"Error during recall: {str(e)}"
        logger.error(error_msg)
        return json.dumps([{"text": error_msg, "score": 0.0}])

if __name__ == "__main__":
    try:
        # Find available ports for both servers
        mcp_port = find_available_port(4444)
        flask_port = find_available_port(5555)
        
        logger.info(f"Starting Memori server...")
        logger.info(f"MCP server will run on port {mcp_port}")
        logger.info(f"Web interface will run on port {flask_port}")
        
        import threading
        
        def run_mcp():
            try:
                mcp.run(transport="streamable-http", host="0.0.0.0", port=mcp_port, path="/mcp")
            except Exception as e:
                logger.error(f"Error in MCP server: {e}")
                sys.exit(1)
        
        # Start MCP server in a separate thread
        mcp_thread = threading.Thread(target=run_mcp)
        mcp_thread.daemon = True
        mcp_thread.start()
        
        # Run Flask app
        app.run(host="0.0.0.0", port=flask_port, debug=True)
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

