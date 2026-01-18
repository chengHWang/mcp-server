# mng/server.py
import json
from urllib import request

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from .handlers import handle_list_tools, handle_async_call_tool

app = FastAPI(title="MCP Server")

@app.post("/")
async def root(request: Request):
    body = await request.json()
    method = body.get("method")

    if method == "list_tools":
        result = await handle_list_tools()
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": body.get("id"),
        }
    else:
        raise HTTPException(status_code=404, detail=f"Illegal method '{method}' requested in route path '/'.")


@app.post("/sse")
async def sse_mcp(request: Request):
    body = await request.json()
    method = body.get("method")

    if method != "call_tool":
        raise HTTPException(
            status_code=404,
            detail=f"Illegal method '{method}' requested in route path '/sse'",
        )

    session_id = request.headers.get("x-mcp-sessionid")
    async def sse_generator():
        try:
            async for response in handle_async_call_tool(body, session_id):
                yield {
                    "data": json.dumps(response, ensure_ascii=False),
                }
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "error": {"code": 500, "message": str(e)},
                "id": body.get("id"),
            }
            yield {"data": json.dumps(err_resp, ensure_ascii=False)}

    return EventSourceResponse(sse_generator())


@app.post("/streamable_http")
async def streamable_http_mcp(request: Request):
    body = await request.json()
    method = body.get("method")

    if method != "call_tool":
        raise HTTPException(
            status_code=404,
            detail=f"Illegal method '{method}' requested in route path '/streamable_http'",
        )

    session_id = request.headers.get("x-mcp-sessionid")

    async def streamable_http_generator():
        try:
            async for response in handle_async_call_tool(body, session_id):
                yield json.dumps(response, ensure_ascii=False) + "\n"
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "error": {"code": 500, "message": str(e)},
                "id": body.get("id"),
            }
            yield json.dumps(err_resp, ensure_ascii=False) + "\n"

    return StreamingResponse(streamable_http_generator(), media_type="application/x-ndjson")
