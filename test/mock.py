from fastapi import FastAPI, Request
from fastapi.responses import Response
import json
import os

app = FastAPI()

RESPONSE_FILE = "mock_response.json"


def load_mock_response():
    if not os.path.exists(RESPONSE_FILE):
        return json.dumps({"error": "mock_response.json no existe"})

    try:
        with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            json.loads(content)  # Validamos JSON
            return content
    except json.JSONDecodeError as e:
        return json.dumps({
            "error": "JSON inválido en mock_response.json",
            "detalle": str(e)
        })


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):

    print("\n================== REQUEST RECIBIDA ==================")

    # Línea de llamada
    print(">>> LLAMADA")
    print(f"{request.method} /{full_path}")
    print(f"Query Params: {dict(request.query_params)}")

    # Headers
    print("\n>>> HEADERS")
    for key, value in request.headers.items():
        print(f"{key}: {value}")

    # Body
    print("\n>>> BODY")
    body_bytes = await request.body()
    if body_bytes:
        try:
            body_json = json.loads(body_bytes)
            print(json.dumps(body_json, indent=4))
        except:
            print(body_bytes.decode("utf-8"))
    else:
        print("Sin body")

    print("======================================================\n")

    response_body = load_mock_response()

    return Response(
        content=response_body,
        status_code=200,
        media_type="application/json"
    )