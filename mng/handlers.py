# mng/handlers.py
from fastapi import Header, HTTPException
from typing import Optional
from tool.registry import get_tool, list_tools_metadata


async def handle_list_tools():
    return {"tools": list_tools_metadata()}


async def handle_call_tool(request: dict, x_mcp_sessionid: Optional[str] = Header(None)):
    try:
        tool_name = request["params"]["name"]
        arguments = request["params"]["arguments"]
        tool = get_tool(tool_name)

        # 调用工具（目前是非流式，一次性返回）
        async for chunk in tool(arguments, session_id=x_mcp_sessionid):
            return {
                "jsonrpc": "2.0",
                "result": chunk,
                "id": request["id"]
            }
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool error: {str(e)}")