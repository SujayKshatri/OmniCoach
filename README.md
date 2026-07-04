# Sports Coaching CV — Universal Multi-Agent System

A multi-agent AI pipeline that generates personalised coaching reports for
**any sport** by analysing biomechanical data and benchmarking against elite
athletes.

Built on the [Google Antigravity SDK](https://pypi.org/project/google-antigravity/).

## Supported Sports (out of the box)

| Sport | Elite Benchmarks |
|-------|-----------------|
| Football | Messi, Ronaldo |
| Basketball | LeBron James, Stephen Curry |
| Tennis | Djokovic, Nadal |
| Cricket | Kohli, Bumrah |
| Athletics | Usain Bolt, Mondo Duplantis |

> Any sport name works — the agents adapt their analysis to the discipline.
> The benchmark database covers the sports above; for others, the coach agent
> still produces a full report based on the raw biomechanical data.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Coordinator Agent (sport-aware)             │
│   Orchestrates the 3-stage pipeline + synthesises CV     │
│                                                         │
│  ┌─────────────────┐ ┌──────────────────┐ ┌───────────┐│
│  │ BiometricsAnalyst│→│ EliteComparison  │→│ Personal  ││
│  │ (Sub-Agent 1)    │ │ (Sub-Agent 2)    │ │ Coach     ││
│  │                  │ │                  │ │ (Sub-Agt3)││
│  │ Tool: extract_   │ │ Data: Multi-sport│ │ Output:   ││
│  │ mediapipe_       │ │ elite athlete    │ │ 7-day     ││
│  │ telemetry()      │ │ benchmark DB     │ │ training  ││
│  └─────────────────┘ └──────────────────┘ │ plan      ││
│                                           └───────────┘│
└─────────────────────────────────────────────────────────┘
         │
         ▼
  Inspect Hooks → Structured Audit Log
  [TIMESTAMP] - [AGENT_NAME] - [ACTION/THOUGHT]
```

## Quick Start

```bash
# 1. Install the SDK
pip install -r requirements.txt

# 2. Set your Gemini API key
export GEMINI_API_KEY="your_key_here"          # macOS/Linux
set GEMINI_API_KEY=your_key_here               # Windows CMD
$env:GEMINI_API_KEY = "your_key_here"          # PowerShell

# 3. Run for any sport
python app.py                                    # default: football
python app.py --sport basketball                 # basketball, mock data
python app.py --sport tennis path/to/serve.mp4   # tennis + real video
python app.py --sport cricket                    # cricket
python app.py --sport athletics                  # track & field
python app.py --sport swimming                   # works too — no benchmarks,
                                                 # but agents still analyse
```

## Project Structure

```
football-coaching-cv/
├── app.py                  # Main entry point — full pipeline
├── elite_benchmarks.json   # Multi-sport elite athlete benchmark database
├── requirements.txt        # Python dependencies
└── README.md               # You are here
```

## What Each Agent Does

| Agent              | Role                                                | Tools/Data                     |
|--------------------|-----------------------------------------------------|--------------------------------|
| BiometricsAnalyst  | Parses raw coordinate data from video               | `extract_mediapipe_telemetry()`|
| EliteComparison    | Benchmarks user data vs sport-specific elite athletes| `elite_benchmarks.json`       |
| PersonalCoach      | Generates actionable 7-day training plan            | None (pure LLM reasoning)      |

All three agents receive the `--sport` flag value and adapt their analysis
to the specified discipline.

## Audit Logging

Every internal decision is captured via Antigravity Inspect hooks:

```
[2026-07-04T00:30:12+0530] - [COORDINATOR] - [PRE_TURN — New turn starting]
[2026-07-04T00:30:13+0530] - [AGENT] - [PRE_TOOL — Calling 'extract_mediapipe_telemetry' | args={'video_path': '...'}]
[2026-07-04T00:30:13+0530] - [BIOMETRICS_ANALYST] - [TOOL_EXEC — Extracting telemetry from: ...]
[2026-07-04T00:30:14+0530] - [AGENT] - [POST_TOOL — 'extract_mediapipe_telemetry' returned: {...}]
[2026-07-04T00:30:15+0530] - [COORDINATOR] - [PRE_TOOL — Delegating to sub-agent: EliteComparison]
```

## Requirements

- Python >= 3.10
- `google-antigravity >= 0.1.5`
- A valid `GEMINI_API_KEY` environment variable
