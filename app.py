from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import base64
import os

app = FastAPI()


# Retrieve GitHub repository information from environment variables
ORG = os.getenv('GITHUB_ORG')
REPO_NAME = os.getenv('GITHUB_REPO')
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

if None in (ORG, REPO_NAME, ACCESS_TOKEN):
    raise ValueError("GitHub credentials not provided")



# Define folders for different file types in the GitHub repository
SERVICE_GRAPH_FOLDER = 'service_graphs'
NETWORK_FUNCTION_FOLDER = 'network_functions'

# Create folders if they don't exist
if not os.path.exists(SERVICE_GRAPH_FOLDER):
    os.makedirs(SERVICE_GRAPH_FOLDER)
if not os.path.exists(NETWORK_FUNCTION_FOLDER):
    os.makedirs(NETWORK_FUNCTION_FOLDER)

def check_file_existence(file_name, folder):
    url = f'https://api.github.com/repos/{ORG}/{REPO_NAME}/contents/{folder}'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = [file['name'] for file in response.json() if file['type'] == 'file']
    return file_name in files

def upload_file_to_github(file_content, file_name, folder):
    # Construct the file path including the folder
    file_path = os.path.join(folder, file_name)
    url = f'https://api.github.com/repos/{ORG}/{REPO_NAME}/contents/{file_path}'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': f'{folder}: Add {file_name}',
        'content': base64.b64encode(file_content).decode()  # Encode content as base64
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    if file.filename.endswith('.sg.yaml'):
        folder = SERVICE_GRAPH_FOLDER
    elif file.filename.endswith('.nf.yaml'):
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    if check_file_existence(file.filename, folder):
        raise HTTPException(status_code=400, detail="File already exists")
    
    upload_file_to_github(file_content, file.filename, folder)
    return {"message": f"File '{file.filename}' uploaded successfully to GitHub"}


def download_file_from_github(file_path):
    url = f'https://raw.githubusercontent.com/{ORG}/{REPO_NAME}/master/{file_path}'
    response = requests.get(url)
    response.raise_for_status()
    return response.content

@app.get("/file/{file_type}/{file_name}")
async def download_file(file_type: str, file_name: str):
    if file_type == 'service_graph':
        file_path = os.path.join(SERVICE_GRAPH_FOLDER, file_name)
    elif file_type == 'network_function':
        file_path = os.path.join(NETWORK_FUNCTION_FOLDER, file_name)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_content = download_file_from_github(file_path)
    return {"file_content": file_content.decode()}  # Return file content as string

@app.get("/list_files/{file_type}")
async def list_files(file_type: str):
    if file_type == 'service_graph':
        folder = SERVICE_GRAPH_FOLDER
    elif file_type == 'network_function':
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    files = os.listdir(folder)
    return {"files": files}

@app.get("/list_files_github/{file_type}")
async def list_files_github(file_type: str):
    if file_type == 'service_graph':
        folder = SERVICE_GRAPH_FOLDER
    elif file_type == 'network_function':
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")

    url = f'https://api.github.com/repos/{ORG}/{REPO_NAME}/contents/{folder}'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = [file['name'] for file in response.json() if file['type'] == 'file']
    return {"files": files}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
