from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import yaml

app = FastAPI()

# Directory to store YAML files
STORE_DIR = "stored_graphs"


class Graph(BaseModel):
    name: str
    data: dict


def save_graph(graph_name, data):
    """Save a YAML graph."""
    filename = os.path.join(STORE_DIR, f"{graph_name}.yaml")
    with open(filename, "w") as file:
        yaml.dump(data, file)


def load_graph(graph_name):
    """Load a YAML graph."""
    filename = os.path.join(STORE_DIR, f"{graph_name}.yaml")
    with open(filename, "r") as file:
        return yaml.safe_load(file)


@app.post('/store')
def store_graph(graph: Graph):
    """Endpoint to store a YAML graph."""
    graph_name = graph.name
    graph_data = graph.data
    save_graph(graph_name, graph_data)
    return {"message": "Graph stored successfully"}


@app.get('/retrieve/{graph_name}')
def retrieve_graph(graph_name: str):
    """Endpoint to retrieve a YAML graph."""
    try:
        graph_data = load_graph(graph_name)
        return graph_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Graph not found")


if __name__ == '__main__':
    if not os.path.exists(STORE_DIR):
        os.makedirs(STORE_DIR)
