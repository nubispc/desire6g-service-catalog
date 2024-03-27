# DESIRE6G Service Catalog

This is the initial implementation for the D6G Service Catalog.

## Requirements

- Python 3.x
- FastAPI
- PyYAML

## Installation

1. Clone this repository:

`git clone https://github.com/nubispc/desire6g-service-catalog`

2. Install dependencies:

`pip install -r requirements.txt`

## Usage

1. Start the server:

`uvicorn server:app --reload`

2. Use the following endpoints:

- `POST /store`: Store a YAML graph. Provide JSON data with `name` and `data` fields.
- `GET /retrieve/{graph_name}`: Retrieve a YAML graph by its name.

## Example

### Storing a YAML Graph

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "graph1", "data": {"nodes": ["A", "B", "C"], "edges": [["A", "B"], ["B", "C"]]}}' http://localhost:8000/store
```

### Retrieving a YAML Graph
```bash
curl http://localhost:8000/retrieve/graph1
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
