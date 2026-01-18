# mng/server.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .handlers import handle_list_tools, handle_call_tool

app = FastAPI(title="MCP Server")


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    body = await request.json()
    method = body.get("method")

    if method == "list_tools":
        data = await handle_list_tools()
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": data,
            "id": body.get("id")
        })

    elif method == "call_tool":
        response = await handle_call_tool(body)
        return JSONResponse(response)

    else:
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": body.get("id")
        }, status_code=400)