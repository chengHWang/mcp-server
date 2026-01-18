# tool/add.py
from typing import Dict, Any, AsyncGenerator
from .base import BaseTool


class AddTool(BaseTool):
    name = "add"
    description = "Add two numbers together."
    parameters = {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }

    async def __call__(self, arguments: Dict[str, Any], session_id: str = None) -> AsyncGenerator[Dict, None]:
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        yield {"final": result}


if __name__ == "__main__":
    import asyncio

    async def test_add_tool():
        tool = AddTool()
        test_cases = [
            {"a": 1, "b": 2},
            {"a": -5, "b": 3.5},
            {"a": 0, "b": 0},
            {"a": 1.1, "b": 2.2}
        ]

        for i, args in enumerate(test_cases, 1):
            print(f"Test case {i}: {args}")
            async for output in tool(args):
                print(f"Result: {output['final']}")
            print("-" * 30)

    asyncio.run(test_add_tool())