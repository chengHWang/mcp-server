# mng/handlers.py
from typing import Optional, Dict, Any
from tool.registry import get_tool, list_tools_metadata

async def handle_list_tools():
    return {"tools": list_tools_metadata()}

async def handle_async_call_tool(
        request: Dict[str, Any], session_id: Optional[str] = None
    ):
    try:
        tool_name = request["params"]["name"]
        arguments = request["params"]["arguments"]
        tool = get_tool(tool_name)

        async for chunk in tool(arguments, session_id=session_id):
            yield {
                "jsonrpc": "2.0",
                "result": chunk,
                "id": request["id"]
            }
    except KeyError as e:
        yield {
            "jsonrpc": "2.0",
            "error": {"code": 400, "message": f"Missing key: '{str(e)}'"},
            "id": request.get("id")
        }
    except Exception as e:
        yield {
            "jsonrpc": "2.0",
            "error": {"code": 401, "message": f"Tool Error: '{str(e)}'"},
            "id": request.get("id")
        }