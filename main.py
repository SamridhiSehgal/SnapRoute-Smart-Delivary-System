from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from algorithms import dijkstra, k_shortest_paths
from graph_loader import get_graph
from schemas import PathRequest, DijkstraResponse, KPathsResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow your frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/dijkstra", response_model=DijkstraResponse)
def get_dijkstra_path(req: PathRequest):
    try:
        graph, _ = get_graph()
        cost, path = dijkstra(graph, req.start, req.end)
        if not path:
            raise HTTPException(status_code=404, detail="Path not found")
        return {"cost": cost, "path": path}
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/k-shortest", response_model=KPathsResponse)
def get_k_paths(req: PathRequest):
    try:
        graph, _ = get_graph()
        paths = k_shortest_paths(graph, req.start, req.end, req.k)
        if not paths:
            raise HTTPException(status_code=404, detail="No paths found")
        return {"paths": [{"cost": cost, "path": path} for cost, path in paths]}
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/graph")
def get_full_graph():
    try:
        graph, coordinates = get_graph()
        edges = []

        for node, neighbors in graph.items():
            for neighbor, weight in neighbors:
                edges.append({
                    "from": node,
                    "to": neighbor,
                    "weight": weight
                })

        return JSONResponse(content={
            "nodes": [
                {"id": node, "lat": lat, "lng": lng}
                for node, (lat, lng) in coordinates.items()
            ],
            "edges": edges
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
