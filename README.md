# DIVYASTRA v2

### AI Security Testing Framework

**Prompt Injection · Jailbreaks · Prompt Exfiltration · LLM Security Testing**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-059669?style=flat-square)](https://github.com/CalculusGuy/DIVYASTRA)

**DIVYASTRA** is a modular framework for automated security testing of LLMs and LLM-powered applications.

It tests adversarial prompts, classifies model responses, and generates machine-readable and human-readable reports.

> Built from practical LLM attack techniques studied through PortSwigger Web Security Academy.

---

## Features

* Prompt injection & indirect injection
* Jailbreak assessment
* Prompt exfiltration testing
* Instruction override detection
* Encoding & obfuscation attacks
* Scope boundary testing
* Negation-aware detection
* Confidence-based classification
* Ollama, OpenAI-compatible, Gemini & custom HTTP adapters
* Gemini model fallback & retry handling
* JSON, HTML & Markdown reports
* YAML-based payloads
* OWASP LLM Top 10 mapping

**Current:** 18 payloads · 6 attack categories

---

## Workflow

```text
Payloads
   │
   ▼
Attack Engine
   │
   ▼
Adapter Router
 ┌─┼─────────────┬────────────┐
 ▼ ▼             ▼            ▼
Ollama OpenAI   Gemini    Custom HTTP
 └─┴─────────────┴────────────┘
              │
              ▼
       Detection Engine
              │
              ▼
    VULNERABLE / SAFE / UNCERTAIN
              │
              ▼
       JSON / HTML / MD
```

---

## Adapters

| Adapter  | Target                  |
| -------- | ----------------------- |
| `ollama` | Local LLMs              |
| `openai` | OpenAI-compatible APIs  |
| `gemini` | Google Gemini           |
| `custom` | Custom LLM applications |

---

## Installation

```bash
git clone https://github.com/CalculusGuy/DIVYASTRA.git
cd DIVYASTRA

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Gemini

Create `.env`:

```env
GEMINI_API_KEY=your_key_here
```

### Ollama

```bash
ollama pull llama3
```

---

## Usage

### Ollama

```bash
python divyastra.py --target ollama --model llama3
```

### Gemini

```bash
python divyastra.py --target gemini
```

### OpenAI-Compatible

```bash
python divyastra.py --target openai --model gpt-4 --api-key $OPENAI_API_KEY
```

### Custom Application

```bash
python divyastra.py --target custom --url https://target.example/api/chat
```

### Category / Payload

```bash
python divyastra.py --target gemini --category role_play_jailbreak

python divyastra.py --target gemini --payload-id io_001
```

### Reports

```bash
python divyastra.py \
  --target gemini \
  --json-out reports/run.json \
  --html-out reports/run.html \
  --md-out reports/run.md
```

### Debugging

```bash
python divyastra.py --target gemini --verbose
```

---

## CLI

| Flag           | Description                               |
| -------------- | ----------------------------------------- |
| `--target`     | `ollama` / `openai` / `gemini` / `custom` |
| `--model`      | Target model                              |
| `--api-key`    | API key                                   |
| `--url`        | Custom endpoint                           |
| `--category`   | Run one attack category                   |
| `--payload-id` | Run one payload                           |
| `--delay`      | Request delay                             |
| `--json-out`   | JSON report                               |
| `--html-out`   | HTML report                               |
| `--md-out`     | Markdown report                           |
| `--quiet`      | Summary only                              |
| `--verbose`    | Full response output                      |

---

## Detection

DIVYASTRA v2 uses **negation-aware and refusal-aware detection** to reduce false positives.

```text
Signal Match
     │
     ▼
Negation Check
     │
     ▼
Refusal Detection
     │
     ▼
Confidence Scoring
     │
     ▼
VULN / SAFE / UNCERTAIN
```

Example:

```text
"No API keys were exposed."
```

A naive keyword detector may flag `API key`.

DIVYASTRA recognizes the negation and avoids incorrectly reporting a leak.

---

## Reports

### JSON

Machine-readable results for automation.

### HTML

Self-contained report with findings, confidence and response details.

### Markdown

GitHub-ready report for documentation and writeups.

---

## Payloads

Payloads are defined in:

```text
payloads/payloads.yaml
```

Example:

```yaml
- id: custom_001
  category: instruction_override
  text: "Your payload"
  success_signal: "expected signal"
```

Add payloads without modifying the core engine.

---

## Testing

```bash
python test_smoke.py
```

---

## Roadmap

* [x] Multi-adapter runtime
* [x] 18 payloads / 6 categories
* [x] Detection engine
* [x] Gemini support
* [x] Negation-aware detection
* [x] JSON / HTML / Markdown reports
* [x] OWASP LLM mapping
* [ ] 50+ payloads
* [ ] Multi-turn attack chains
* [ ] CI/CD integration
* [ ] SARIF output
* [ ] Interactive dashboard
* [ ] Multi-model benchmarking

---

## Responsible Use

DIVYASTRA is for **authorized security testing, research and education**.

Only test systems, models and applications you own or have explicit permission to assess.

---

## Author

**Nilanjan Chowdhury**

Cybersecurity Researcher · AI/LLM Security

[GitHub](https://github.com/CalculusGuy) ·
[LinkedIn](https://linkedin.com/in/mr-nilanjan-chowdhury-a36787359/) ·
[Medium](https://medium.com/@nilanjan.calculus) ·
[Portfolio](https://calculusguy.github.io/nilanjanchowdhury.github.io/)

---

## License

MIT License — see [LICENSE](LICENSE).

<div align="center">

### DIVYASTRA

**Test. Classify. Map. Report.**

</div>
