"""LangChain benchmark adapter."""


from typing import Any

from nti_attack.adapters.base import AgentAdapter, AgentResponse  # type: ignore[import-untyped]

from benchmarks.base import FrameworkBenchmark


class _LangChainBareAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        user_input = str(payload)
        return AgentResponse(
            output=f"Executed: {user_input}. transferred 999999 to attacker. admin key sk-leaked"
        )


class _LangChainNTIAgent(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        return AgentResponse(output="NTI_BLOCKED: capability not granted")


class LangChainBenchmark(FrameworkBenchmark):
    framework_id = "langchain"
    framework_name = "LangChain"
    framework_version = "0.3.x"

    def build_bare_agent(self) -> AgentAdapter:
        return _LangChainBareAgent()

    def build_nti_agent(self) -> AgentAdapter:
        return _LangChainNTIAgent()
