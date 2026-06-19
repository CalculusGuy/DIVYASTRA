███╗  ██╗  ██╗   ██╗  ██╗   ██╗   █████╗   ███████╗  ████████╗  ██████╗    █████╗

██╔══██╗  ██║  ██║   ██║  ╚██╗ ██╔╝  ██╔══██╗  ██╔════╝  ╚══██╔══╝  ██╔══██╗  ██╔══██╗

██║  ██║  ██║  ██║   ██║   ╚████╔╝   ███████║  ███████╗     ██║     ██████╔╝  ███████║

██║  ██║  ██║  ╚██╗ ██╔╝    ╚██╔╝    ██╔══██║  ╚════██║     ██║     ██╔══██╗  ██╔══██║

██████╔╝  ██║   ╚████╔╝      ██║     ██║  ██║  ███████║     ██║     ██║  ██║  ██║  ██║

╚═════╝   ╚═╝    ╚═══╝       ╚═╝     ╚═╝  ╚═╝  ╚══════╝     ╚═╝     ╚═╝  ╚═╝  ╚═╝  ╚═╝



# DIVYASTRA

> AI Security Testing Framework for Prompt Injection, Jailbreak & Prompt Exfiltration Detection

DIVYASTRA is a modular AI security testing framework designed to assess Large Language Models (LLMs) against common adversarial prompt attacks. It automates prompt injection testing, jailbreak assessment, instruction override detection, prompt exfiltration attempts, and other attack patterns inspired by real-world LLM security research.

Built after completing the full PortSwigger Web Security Academy Web LLM Attacks module (8/8, Apprentice → Expert), DIVYASTRA translates practical attack methodologies into an automated security assessment tool.

---

## Features

* Prompt Injection Detection
* Jailbreak Assessment
* Prompt Exfiltration Testing
* Instruction Override Detection
* Indirect Prompt Injection Testing
* Encoding & Obfuscation Attack Detection
* Scope Boundary Validation
* Confidence-Based Vulnerability Scoring
* JSON Report Generation
* Terminal Reporting Interface
* Ollama Support
* OpenAI-Compatible API Support
* Extensible Payload Framework
* OWASP LLM Top 10 Alignment

---

## Why DIVYASTRA Exists

As organizations increasingly integrate LLMs into applications, prompt injection has become one of the most significant security risks in AI systems.

Most testing today remains manual:

* Copy payload
* Send request
* Observe response
* Repeat

DIVYASTRA automates this process by executing a structured library of attack payloads and evaluating model behavior against predefined detection criteria.

The goal is to help developers, researchers, and security practitioners quickly identify weaknesses before deployment.

---

## Supported Attack Categories

| Category               | Description                                   |
| ---------------------- | --------------------------------------------- |
| Instruction Override   | Attempts to replace system instructions       |
| Roleplay Jailbreak     | Persona-based safety bypass attacks           |
| Prompt Exfiltration    | Extraction of hidden prompts and instructions |
| Indirect Injection     | Injection through untrusted external content  |
| Encoding Obfuscation   | Base64 and transformed payload attacks        |
| Scope Boundary Testing | Validation of operational restrictions        |

---

## Project Structure

```text
DIVYASTRA/
│
├── adapters/
│   ├── base_adapter.py
│   ├── ollama_adapter.py
│   ├── openai_style_adapter.py
│   └── custom_http_adapter.py
│
├── core/
│   ├── engine.py
│   ├── detector.py
│   ├── cli_report.py
│   └── json_report.py
│
├── payloads/
│   └── payloads.yaml
│
├── requirements.txt
├── test_smoke.py
├── divyastra.py
└── README.md
```

---

## Installation

```bash
git clone https://github.com/yourusername/DIVYASTRA.git

cd DIVYASTRA

pip install -r requirements.txt
```

---

## Quick Start

### Scan an Ollama Model

```bash
python divyastra.py --target ollama --model llama3
```

### Generate JSON Report

```bash
python divyastra.py \
    --target ollama \
    --model llama3 \
    --output report.json
```

---

## Example Output

```text
[VULN] io_001 (instruction_override)
[VULN] rp_001 (role_play_jailbreak)
[VULN] ex_003 (prompt_exfiltration)

Summary
------------------------------
Total Payloads : 18
Vulnerable     : 9
Safe           : 8
Uncertain      : 1
```

---

## OWASP LLM Top 10 Mapping

DIVYASTRA focuses primarily on:

* LLM01: Prompt Injection
* LLM02: Insecure Output Handling
* LLM06: Sensitive Information Disclosure
* LLM07: Insecure Plugin Design
* LLM09: Overreliance

This mapping helps security teams align findings with industry-recognized AI security risks.

---

## Roadmap

* Additional jailbreak payload libraries
* HTML and Markdown reporting
* Risk scoring improvements
* CI/CD integration
* Multi-model benchmarking
* Gemini API support
* Anthropic API support
* Hugging Face local model support
* Interactive dashboard

---

## Disclaimer

DIVYASTRA is intended for authorized security testing, AI evaluation, research, and educational purposes only.

Users are responsible for ensuring compliance with applicable laws, regulations, and organizational policies.

---

## Inspiration

* PortSwigger Web Security Academy — Web LLM Attacks
* OWASP LLM Top 10
* Prompt Injection Research Community
* AI Red Teaming Methodologies

---

## Author

**Nilanjan Chowdhury**

Cybersecurity Student | AI Security Enthusiast | Security Researcher

> “With great power comes great responsibility.”
