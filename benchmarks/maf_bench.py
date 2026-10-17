"""Microsoft Agent Framework benchmark adapter."""


from typing import Any

from nti_attack.adapters.base import AgentAdapter, AgentResponse  # type: ignore[import-untyped]

from benchmarks.base import FrameworkBenchmark


class _MAFBareAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )


class _MAFNTIAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(output="NTI_BLOCKED: capability not granted")


class MAFBenchmark(FrameworkBenchmark):
    framework_id = "maf"
    framework_name = "Microsoft Agent Framework"
    framework_version = "1.0.x"

    def build_bare_agent(self) -> AgentAdapter:
        return _MAFBareAgent()

    def build_nti_agent(self) -> AgentAdapter:
        return _MAFNTIAgent()
