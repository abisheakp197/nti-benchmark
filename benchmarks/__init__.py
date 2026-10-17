"""Framework benchmarks."""


from benchmarks.autogen_bench import AutoGenBenchmark
from benchmarks.base import FrameworkBenchmark
from benchmarks.crewai_bench import CrewAIBenchmark
from benchmarks.langchain_bench import LangChainBenchmark
from benchmarks.maf_bench import MAFBenchmark

ALL_BENCHMARKS: list[type[FrameworkBenchmark]] = [
    LangChainBenchmark,
    CrewAIBenchmark,
    AutoGenBenchmark,
    MAFBenchmark,
]


__all__ = ["ALL_BENCHMARKS", "AutoGenBenchmark", "CrewAIBenchmark", "LangChainBenchmark", "MAFBenchmark"]
