"""Broken adapters must not crash the benchmark runner."""


from typing import Any

from nti_attack.adapters.base import AgentAdapter, AgentResponse  # type: ignore[import-untyped]

from benchmarks.base import FrameworkBenchmark


class _Crash(AgentAdapter):  # type: ignore[misc]
    def invoke(self, payload: Any) -> AgentResponse:
        raise RuntimeError("boom")


class _Break(FrameworkBenchmark):
    framework_id = "broken"
    framework_name = "Broken"
    framework_version = "0.0.1"

    def build_bare_agent(self) -> AgentAdapter:
        return _Crash()

    def build_nti_agent(self) -> AgentAdapter:
        return _Crash()


def test_broken_adapter_does_not_crash_run() -> None:
    b = _Break()
    result = b.run()
    assert "bare" in result
    assert "with_nti" in result
