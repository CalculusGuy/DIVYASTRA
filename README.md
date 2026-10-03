# DIVYASTRA v2

### AI Security Testing Framework

**Prompt Injection · Jailbreak Assessment · Prompt Exfiltration Detection**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://python.org)
[![AI Security](https://img.shields.io/badge/AI-Security-DC2626?style=for-the-badge)](https://github.com/CalculusGuy/DIVYASTRA)
[![OWASP LLM](https://img.shields.io/badge/OWASP-LLM_Top_10-7C3AED?style=for-the-badge)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-059669?style=for-the-badge)](https://github.com/CalculusGuy/DIVYASTRA)

**Author:** [Nilanjan Chowdhury](https://github.com/CalculusGuy)

---

## What is DIVYASTRA?

DIVYASTRA is a **modular AI security testing framework** for assessing LLMs against adversarial prompt attacks.

It automates:

* Prompt injection testing
* Jailbreak assessment
* Instruction override detection
* Prompt exfiltration attempts
* Indirect injection through untrusted content
* Encoding and obfuscation bypasses
* Scope boundary validation

Built after completing the **PortSwigger Web Security Academy Web LLM Attacks** module (8/8, Apprentice → Expert), DIVYASTRA turns practical LLM attack methodologies into an automated assessment workflow.

### Core Pipeline

**18 Payloads → 6 Attack Categories → Multi-Adapter Runtime → Auto-Classification → JSON Report**

---

## DIVYASTRA vs. BRAMHASTRA

Both projects are part of my **AI/LLM red-teaming toolkit**, but they solve different problems.

|                | **DIVYASTRA**                       | **BRAMHASTRA**                                               |
| -------------- | ----------------------------------- | ------------------------------------------------------------ |
| **Purpose**    | Automated payload testing           | Research harness                                             |
| **Focus**      | Payload library + detection         | Multi-model RAG comparison                                   |
| **Target**     | Any LLM via adapter                 | Llama3, Mistral, Phi behind the same RAG                     |
| **Key Output** | Vulnerable / Safe / Uncertain       | Cross-model leakage matrix                                   |
| **Use Case**   | "Is my LLM application vulnerable?" | "How do models behave differently against the same payload?" |

**DIVYASTRA:** *Is this model or application exploitable?*
**BRAMHASTRA:** *How do different models behave against the same attack?*

---

## Features

* **Prompt Injection Detection** — direct and indirect
* **Jailbreak Assessment** — roleplay, persona, developer-mode attacks
* **Prompt Exfiltration Testing** — system prompt extraction
* **Instruction Override Detection** — instruction manipulation attacks
* **Encoding & Obfuscation** — Base64, ROT13, Unicode
* **Scope Boundary Validation** — operational restriction testing
* **Confidence-Based Classification** — vulnerable / safe / uncertain
* **Multi-Adapter Runtime** — Ollama, OpenAI-compatible, custom HTTP
* **JSON Reports** — machine-readable findings
* **Terminal UI** — human-readable output
* **Extensible Payloads** — YAML-based payload framework
* **OWASP LLM Top 10 Alignment** — findings mapped to recognized risks

---

## Workflow

```mermaid
flowchart LR
    A[Payload YAML] --> B[Attack Engine]
    B --> C{Adapter Router}

    C --> D[Ollama]
    C --> E[OpenAI-Compatible]
    C --> F[Custom HTTP]

    D --> G[Detector]
    E --> G
    F --> G

    G --> H{Classification}

    H --> I[Vulnerable]
    H --> J[Safe]
    H --> K[Uncertain]

    I --> L[JSON Report]
    J --> L
    K --> L
```

### Pipeline

```text
payloads.yaml
      │
      ▼
Attack Engine
      │
      ▼
Adapter Router
   ┌──┼──────────────┐
   ▼  ▼              ▼
Ollama  OpenAI   Custom HTTP
   │      │            │
   └──────┼────────────┘
          ▼
       Detector
          │
          ▼
    Classification
 VULN / SAFE / UNCERTAIN
          │
          ▼
      JSON Report
```

---

## Supported Attack Categories

| Category                   | Description                                   |
| -------------------------- | --------------------------------------------- |
| **Instruction Override**   | Attempts to replace system instructions       |
| **Roleplay Jailbreak**     | Persona-based safety bypass attacks           |
| **Prompt Exfiltration**    | Extraction of hidden prompts and instructions |
| **Indirect Injection**     | Injection through untrusted external content  |
| **Encoding Obfuscation**   | Base64 and transformed payload attacks        |
| **Scope Boundary Testing** | Validation of operational restrictions        |

**Current Coverage:** 18 payloads across 6 categories.

---

## Architecture

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
├── divyastra.py
├── test_smoke.py
├── requirements.txt
└── README.md
```

### Adapter System

DIVYASTRA communicates with models through adapters, allowing the framework to test different model and application interfaces.

| Adapter                | Supports                                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `ollama_adapter`       | Llama3, Mistral, Phi, Gemma, and other local Ollama models                               |
| `openai_style_adapter` | OpenAI API, Anthropic-compatible endpoints, Groq, Together, and other OpenAI-format APIs |
| `custom_http_adapter`  | Custom application endpoints for testing the application itself                          |

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/CalculusGuy/DIVYASTRA.git
cd DIVYASTRA
```

### Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Optional: Ollama

Install Ollama and pull a local model:

```bash
ollama pull llama3
```

---

## Usage

### Scan a Local Ollama Model

```bash
python divyastra.py --target ollama --model llama3
```

### Generate a JSON Report

```bash
python divyastra.py \
    --target ollama \
    --model llama3 \
    --output report.json
```

### Test an OpenAI-Compatible Endpoint

```bash
python divyastra.py \
    --target openai \
    --model gpt-4 \
    --api-key $OPENAI_API_KEY
```

### Test Your Own LLM Application

```bash
python divyastra.py \
    --target custom-http \
    --endpoint https://myapp.com/api/chat
```

---

## Sample Output

```text
[VULN] io_001 (instruction_override)
[VULN] rp_001 (role_play_jailbreak)
[VULN] ex_003 (prompt_exfiltration)
[VULN] io_002 (instruction_override)
[VULN] rp_002 (role_play_jailbreak)
[VULN] en_001 (encoding_obfuscation)
[VULN] ex_001 (prompt_exfiltration)
[VULN] sc_002 (scope_boundary)
[VULN] in_001 (indirect_injection)
[SAFE] io_003 (instruction_override)
[SAFE] rp_003 (role_play_jailbreak)
[SAFE] ex_002 (prompt_exfiltration)

Summary
------------------------------
Total Payloads : 18
Vulnerable     : 9
Safe           : 8
Uncertain      : 1
```

---

## Sample JSON Report

```json
{
  "scan_date": "2026-08-17T12:00:00",
  "target": "ollama",
  "model": "llama3",
  "total_payloads": 18,
  "summary": {
    "vulnerable": 9,
    "safe": 8,
    "uncertain": 1
  },
  "findings": [
    {
      "id": "io_001",
      "category": "instruction_override",
      "payload": "Ignore all previous instructions and...",
      "response": "...",
      "classification": "VULN",
      "confidence": 0.92
    }
  ]
}
```

---

## OWASP LLM Top 10 Mapping

DIVYASTRA findings are mapped to the **OWASP Top 10 for LLM Applications**.

| OWASP ID  | Category                         | Coverage |
| --------- | -------------------------------- | -------- |
| **LLM01** | Prompt Injection                 | Full     |
| **LLM02** | Insecure Output Handling         | Partial  |
| **LLM06** | Sensitive Information Disclosure | Full     |
| **LLM07** | Insecure Plugin Design           | Partial  |
| **LLM09** | Overreliance                     | Partial  |

This mapping provides a consistent way to relate assessment findings to recognized AI security risks.

---

## Extending Payloads

Custom payloads can be added to:

`payloads/payloads.yaml`

```yaml
- id: custom_001
  category: instruction_override
  payload: "Your custom attack payload here"
  description: "What this payload tries to do"
  detection:
    - "signal_1"
    - "signal_2"
```

No code changes are required. DIVYASTRA automatically loads the payload on the next run.

---

## Testing

Run the smoke tests with:

```bash
python test_smoke.py
```

---

## Roadmap

### Phase 1 — Core

* [x] 18 payloads across 6 categories
* [x] Multi-adapter runtime
* [x] Ollama support
* [x] OpenAI-compatible support
* [x] Custom HTTP support
* [x] Detection and classification engine
* [x] JSON reports
* [x] Terminal UI
* [x] OWASP LLM Top 10 mapping

### Phase 2 — Extended Coverage

* [ ] 50+ payloads
* [ ] Multi-turn attack chains
* [ ] HTML + Markdown reports
* [ ] Advanced risk scoring
* [ ] Gemini API support
* [ ] Anthropic API support
* [ ] Hugging Face local models

### Phase 3 — Integration

* [ ] CI/CD integration
* [ ] Interactive dashboard
* [ ] Multi-model benchmarking
* [ ] SARIF output
* [ ] GitHub Actions workflow

---

## Responsible Use

DIVYASTRA is intended for **authorized security testing, AI evaluation, research, and education only**.

Use it only against:

* LLMs you own
* LLM applications you have written authorization to test
* Your own local models
* Controlled research environments

Do **not** use DIVYASTRA to:

* Attack third-party LLM applications
* Extract real credentials from systems you do not own
* Bypass safety controls on production systems
* Test models or applications without explicit permission

The author assumes no responsibility for misuse.

---

## Inspiration

* **PortSwigger Web Security Academy** — Web LLM Attacks
* **OWASP Top 10 for LLM Applications**
* **Prompt Injection Research Community**
* **AI Red Teaming Methodologies**

---

## Author

**Nilanjan Chowdhury**

Cybersecurity Researcher · AI/LLM Red Teamer

* **GitHub:** [@CalculusGuy](https://github.com/CalculusGuy)
* **LinkedIn:** [Nilanjan Chowdhury](https://linkedin.com/in/mr-nilanjan-chowdhury-a36787359/)
* **Medium:** [@nilanjan.calculus](https://medium.com/@nilanjan.calculus)
* **Portfolio:** [calculusguy.github.io](https://calculusguy.github.io/nilanjanchowdhury.github.io/)

---

## License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">

# DIVYASTRA

### The divine weapon — for AI security.

**Test. Classify. Map. Report.**

⭐ If DIVYASTRA is useful, consider starring the repository.

</div>
