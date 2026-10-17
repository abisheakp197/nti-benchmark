"""CrewAI benchmark adapter."""


from typing import Any

from nti_attack.adapters.base import AgentAdapter, AgentResponse  # type: ignore[import-untyped]

from benchmarks.base import FrameworkBenchmark


class _CrewAIBareAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )


class _CrewAINTIAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(output="NTI_BLOCKED: capability not granted")


class CrewAIBenchmark(FrameworkBenchmark):
    framework_id = "crewai"
    framework_name = "CrewAI"
    framework_version = "0.30.x"

    def build_bare_agent(self) -> AgentAdapter:
        return _CrewAIBareAgent()

    def build_nti_agent(self) -> AgentAdapter:
        return _CrewAINTIAgent()
