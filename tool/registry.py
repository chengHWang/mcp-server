# tool/registry.py
from typing import Dict
from .base import BaseTool
from .add import AddTool
from .count_down import CountdownTool

TOOL_REGISTRY: Dict[str, BaseTool] = {
    "add": AddTool(),
    "count_down": CountdownTool(),
}

def get_tool(name: str):
    if name not in TOOL_REGISTRY:
        raise KeyError(f"Tool '{name}' not found")
    return TOOL_REGISTRY[name]

def list_tools_metadata():
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
        for tool in TOOL_REGISTRY.values()
    ]