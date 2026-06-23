import asyncio


class DummyToolExecutionPort:
    async def execute(self, step):
        # simulate async tool execution delay
        await asyncio.sleep(0.1)

        return {
            "step_id": step.step_id,
            "type": step.type,
            "input": step.input,
            "output": f"result_of_{step.step_id}"
        }