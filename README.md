# FastAPI GitHub File Server

This FastAPI server allows you to upload YAML files to a GitHub repository and retrieve them on demand. It supports two types of YAML files: service graphs and network functions.

## Features

- **Upload Files**: You can upload service graph (`*.sg.yaml`) and network function (`*.nf.yaml`) YAML files to the server. Upon upload, the files are stored in a GitHub repository.
- **Download Files**: You can retrieve the contents of uploaded YAML files by their filenames. The server fetches the files from the GitHub repository and returns their contents.
- **List Files**: You can list all available files stored in the server's local storage.

## Usage

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/your_repository.git

2. Install dependencies:
```bash
pip install -r requirements.txt
```
### Running the Server
Run the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The server will start running on http://localhost:8000 by default.

## Endpoints
- Upload File: `POST /upload/`

  - Upload a YAML file to the server. The filename should have either .sg.yaml or .nf.yaml extension.
  - Example:
```bash
curl -X POST -F "file=@/path/to/your/service_graph.sg.yaml" http://localhost:8000/upload/
```

- Download File: `GET /file/{file_name}`

  - Retrieve the contents of a YAML file by its filename.
  - Example:
```bash
curl http://localhost:8000/file/example_file.yaml
```

- List Files: `GET /list_files`

  - List all available files stored in the server's local storage.
  - Example:
```bash
curl http://localhost:8000/list_files
```

### GitHub Integration

- GitHub Repository: We use a local (org) repository. The access token specified belongs to a member of this org.

### Dependencies
- FastAPI: Web framework for building APIs with Python
- Uvicorn: ASGI server for running FastAPI applications
- Requests: HTTP library for sending requests
