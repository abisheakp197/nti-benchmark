[![NTI Verified](https://img.shields.io/badge/NTI_Score-85%2F100-brightgreen)](https://nti-registry.vercel.app)

# NTI Benchmark


**Verifiable security benchmark for AI agent frameworks.**


[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## What It Does


Runs the full NTI Attack Library against four leading AI agent frameworks — LangChain, CrewAI, AutoGen, and Microsoft Agent Framework — with and without NTI protection. Produces a signed, offline-verifiable report.


## Results Shape


    NTI Benchmark Results
    ┌─────────────────────────────┬───────────┬───────────┬───────┐
    │ Framework                   │ Bare      │ With NTI  │ Delta │
    ├─────────────────────────────┼───────────┼───────────┼───────┤
    │ LangChain                   │ 32/100    │ 98/100    │ +66   │
    │ CrewAI                      │ 28/100    │ 97/100    │ +69   │
    │ AutoGen                     │ 30/100    │ 98/100    │ +68   │
    │ Microsoft Agent Framework   │ 31/100    │ 98/100    │ +67   │
    └─────────────────────────────┴───────────┴───────────┴───────┘


## Why It Matters


Every framework claims to be secure. This benchmark proves or disproves it. Every result is signed and verifiable offline by anyone.


## Install


    pip install nti-benchmark


## Run


    nti-benchmark run


Output written to results/ with a Dilithium5 signature.


## Verify Any Report Offline


    nti-benchmark verify ./results/benchmark-2026-01-15T10-00-00.json


No network. No servers. Just math.


## Submit a Framework


See docs/SUBMITTING.md.


## License


Apache License 2.0. See LICENSE.


## Links


- NTI-1 Spec: https://abisheakp197.github.io/nti-spec/
- nti-attack: https://pypi.org/project/nti-attack/
- nti-scanner: https://pypi.org/project/nti-scanner/
- nti-badge: https://nti-badge-svs1.vercel.app


## Architecture

```mermaid
graph TD
    subgraph BE["Benchmark Engine"]
        CLI["CLI (cli/main.py)"]
        Runner["Runner (runner/run_benchmark.py)"]
        Config["Config Loader (benchmarks/__init__.py)"]
    end

    subgraph FA["Framework Adapters"]
        Base["FrameworkBenchmark Base Class"]
        LC["LangChain Benchmark"]
        CR["CrewAI Benchmark"]
        AG["AutoGen Benchmark"]
        MAF["MAF Benchmark"]
    end

    subgraph AI["Attack Injection"]
        NAL["nti-attack-library"]
        LoadAttacks["load_all_attacks()"]
        RunAttacks["run_attacks()"]
        BareVsNTI["Bare vs. NTI-Secured Execution"]
    end

    subgraph AG_SUB["Attestation Generation"]
        PQC["ube-foundation (PqcKeyPair)"]
        Hash["SHA-256 Payload Hashing (cert_hash)"]
        Sign["Dilithium5 Post-Quantum Signature"]
        Report["Signed Verifiable Report (.json)"]
    end

    CLI -->|"1. Trigger Benchmark"| Runner
    Runner -->|"2. Load Frameworks"| Config
    Config --> LC & CR & AG & MAF

    LC & CR & AG & MAF -->|"Inherit Harness"| Base
    Base -->|"3. Import Library"| NAL
    NAL --> LoadAttacks
    LoadAttacks --> RunAttacks
    RunAttacks -->|"4. Run Baseline vs Secured"| BareVsNTI

    BareVsNTI -->|"5. Compute Delta & Score"| Runner
    Runner -->|"6. Pass Results Payload"| PQC
    PQC --> Hash
    Hash --> Sign
    Sign -->|"7. Output Artifact"| Report
```
