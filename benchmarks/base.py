"""Base benchmark harness. Every framework adapter subclasses this."""


from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from nti_attack.adapters.base import AgentAdapter  # type: ignore[import-untyped]
from nti_attack.attestation import build_report  # type: ignore[import-untyped]
from nti_attack.runner import load_all_attacks, run_attacks  # type: ignore[import-untyped]


class FrameworkBenchmark(ABC):
    """Base class. Each framework provides a factory for a bare agent
    and an NTI-hardened agent."""


    framework_id: str = ""
    framework_name: str = ""
    framework_version: str = ""


    @abstractmethod
    def build_bare_agent(self) -> AgentAdapter:
        """Return an adapter with NO NTI protection."""
        raise NotImplementedError


    @abstractmethod
    def build_nti_agent(self) -> AgentAdapter:
        """Return an adapter WITH NTI protection."""
        raise NotImplementedError


    def run(self) -> dict[str, Any]:
        attacks = load_all_attacks()


        bare_results = run_attacks(attacks, self.build_bare_agent())
        nti_results = run_attacks(attacks, self.build_nti_agent())


        bare_report = build_report(
            agent_id=f"{self.framework_id}-bare",
            commit_sha=self.framework_version,
            results=bare_results,
        )
        nti_report = build_report(
            agent_id=f"{self.framework_id}-nti",
            commit_sha=self.framework_version,
            results=nti_results,
        )


        return {
            "framework_id": self.framework_id,
            "framework_name": self.framework_name,
            "framework_version": self.framework_version,
            "run_at": datetime.now(UTC).isoformat(),
            "bare": {
                "score": bare_report["resistance_score"],
                "attacks_run": bare_report["attacks_run"],
                "attacks_passed": bare_report["attacks_passed"],
                "attacks_failed": bare_report["attacks_failed"],
                "results": [r.to_dict() for r in bare_results],
            },
            "with_nti": {
                "score": nti_report["resistance_score"],
                "attacks_run": nti_report["attacks_run"],
                "attacks_passed": nti_report["attacks_passed"],
                "attacks_failed": nti_report["attacks_failed"],
                "results": [r.to_dict() for r in nti_results],
            },
            "delta": nti_report["resistance_score"] - bare_report["resistance_score"],
            "attack_count": len(attacks),
        }
