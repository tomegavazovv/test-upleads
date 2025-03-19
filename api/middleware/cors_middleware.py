from fastapi import Request

async def add_cors_headers(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Origin header: {request.headers.get('origin')}")
    
    response = await call_next(request)
    
    origin = request.headers.get('origin')
    if origin in ["http://localhost:3000", "https://upleads-prod.web.app", "https://lancer.app"]:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    print("Response headers:", response.headers)
    return response

async def preflight_handler():
    return {
        "status": "ok",
        "headers": {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
    } 