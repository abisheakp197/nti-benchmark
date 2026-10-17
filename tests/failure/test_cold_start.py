"""Cold start: all modules import cleanly."""


def test_all_modules_import() -> None:
    import benchmarks
    import benchmarks.autogen_bench
    import benchmarks.base
    import benchmarks.crewai_bench
    import benchmarks.langchain_bench
    import benchmarks.maf_bench
    import cli
    import cli.main
    import runner
    import runner.attestation
    import runner.run_benchmark
    assert benchmarks is not None
    assert runner is not None
    assert cli is not None
