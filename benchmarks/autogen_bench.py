"""AutoGen benchmark adapter."""


from typing import Any

from nti_attack.adapters.base import AgentAdapter, AgentResponse  # type: ignore[import-untyped]

from benchmarks.base import FrameworkBenchmark


class _AutoGenBareAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )


class _AutoGenNTIAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(output="NTI_BLOCKED: capability not granted")


class AutoGenBenchmark(FrameworkBenchmark):
    framework_id = "autogen"
    framework_name = "AutoGen"
    framework_version = "0.2.x"

    def build_bare_agent(self) -> AgentAdapter:
        return _AutoGenBareAgent()

    def build_nti_agent(self) -> AgentAdapter:
        return _AutoGenNTIAgent()
