import asyncio
from typing import AsyncGenerator, Dict, Any

class CountdownTool:
    name = "count_down"
    description = "Count down tool"
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    async def __call__(
        self,
        arguments: Dict[str, Any],
        session_id: str = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式倒计时工具
        输入: {"start": 5}
        输出: 多次 yield {"count": N}, 最后 yield {"final": "Done!"}
        """
        start = arguments.get("start", 3)
        if not isinstance(start, int) or start < 0:
            raise ValueError("Parameter 'start' must be a non-negative integer")

        # 模拟逐步生成结果（每秒一个）
        for i in range(start, 0, -1):
            yield {"count": i}
            await asyncio.sleep(1)  # 模拟耗时操作（如 API 调用、计算）

        yield {"final": "Done!"}