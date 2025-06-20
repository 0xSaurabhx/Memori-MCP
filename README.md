# Memori - A Unified Context Hub for AI Conversations & Knowledge

Memori is an open-source context management system that provides a modern web interface for managing, searching, and organizing AI conversation memories and knowledge. It uses advanced embedding techniques for semantic search and provides a complete CRUD interface for managing memory entries.


## Demo UI
![image](https://github.com/user-attachments/assets/72bdff64-8bfe-4805-a55d-d66751ca3eaa)


## Usage Demo

<p align="center">
  <img src="https://github.com/user-attachments/assets/71190f78-4828-40a1-b586-1053567aeb83" alt="Memori Logo" width="400" />
</p>


## Features

- 🧠 **Semantic Search**: Utilizes Ollama's embedding model for intelligent, context-aware memory retrieval
- 🌐 **Modern Web Interface**: Clean, responsive UI built with Flask and Tailwind CSS
- 📝 **Full CRUD Operations**: Create, read, update, and delete memory entries
- 🔍 **Real-time Search**: Instant search with category filtering
- 💾 **Persistent Storage**: ChromaDB-based vector database for reliable storage
- 🐳 **Docker Support**: Easy deployment with Docker
- 🔄 **Real-time Updates**: Instant UI updates when memories are modified
- 🎯 **Category Management**: Organize memories with categories
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## How to use Memori MCP

```json
{
    "servers": {
        "Memori": {
            "type": "http",
            "url": "http://localhost:4444/mcp/sse",
        }
    }
}
```

<details>
<summary><b>Installing on VS Code</b></summary>


1. Create `.vscode` folder and create `mcp.json` with below content.

```json
{
    "servers": {
        "Memori": {
            "type": "http",
            "url": "http://localhost:4444/mcp/sse",
        }
    }
}
```

You can find your Smithery key in the [Smithery.ai webpage](https://smithery.ai/server/@upstash/context7-mcp).

</details>



## Prerequisites

- Python 3.11+
- Ollama with `nomic-embed-text` model installed
- Docker (optional, for containerized deployment)

## Installation

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/memori.git
   cd memori
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Ollama is running with the required model:
   ```bash
   ollama pull nomic-embed-text
   ```

5. Start the server:
   ```bash
   python server.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t memori .
   ```

2. Run with host networking (recommended for Ollama access):
   ```bash
   docker run -d --network host memori
   ```

   Or with port mapping and host.docker.internal:
   ```bash
   docker run -d -p 4444:4444 -p 5555:5555 --add-host=host.docker.internal:host-gateway memori
   ```

## Usage

1. Access the web interface at http://localhost:5555

2. Creating Memories:
   - Click the "New Memory" button
   - Fill in the memory details
   - Click "Save" to store the memory

3. Searching Memories:
   - Use the search bar for real-time semantic search
   - Filter by category using the dropdown
   - Click on memory cards to view full content

4. Editing/Deleting Memories:
   - Click the edit/delete icons on memory cards
   - Confirm actions in the modal dialogs

## API Endpoints

- `GET /api/memories`: List all memories
- `POST /api/memories/create`: Create a new memory
- `GET /api/memories/search`: Search memories
- `PUT /api/memories/<id>`: Update a memory
- `DELETE /api/memories/<id>`: Delete a memory
- `GET /`: Web interface

## Project Structure

```
memori/
├── server.py           # Main server file (Flask + FastMCP)
├── memory.py          # Memory management and database operations
├── embedding.py       # Embedding generation using Ollama
├── requirements.txt   # Python dependencies
├── Dockerfile        # Docker configuration
├── templates/        # HTML templates
│   └── index.html   # Main web interface
└── db/              # ChromaDB storage
```

## Technical Details

- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Backend**: Flask, FastMCP
- **Database**: ChromaDB (vector database)
- **Embedding**: Ollama (nomic-embed-text model)
- **Containerization**: Docker

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or recommend improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama for providing the embedding model
- ChromaDB for the vector database
- FastMCP for the MCP server implementation

