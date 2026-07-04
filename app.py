#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#  Sports Coaching CV — Universal Multi-Agent System
#  Built on the Google Antigravity SDK (google-antigravity)
#
#  Works for ANY sport: football, basketball, tennis, cricket, athletics, etc.
#  Football is used as the default example / reference sport.
#
#  Architecture:
#    Coordinator Agent  ←──→  3 Sub-Agents
#      ├── Biometrics Analyst   (parses raw MediaPipe-style coordinate data)
#      ├── Elite Comparison     (benchmarks against elite athlete database)
#      └── Personal Coach       (generates actionable training feedback)
#
#  Run:
#    export GEMINI_API_KEY="your_key"
#    python app.py                                    # default: football
#    python app.py --sport basketball video.mp4       # any sport + video
#    python app.py --sport tennis                     # mock mode
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import asyncio
import json
import logging
import os
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import hooks

# ─────────────────────────────────────────────────────────────────────────────
#  0.  STRUCTURED AUDIT LOGGER
#      Prints: [TIMESTAMP] - [AGENT_NAME] - [ACTION / THOUGHT]
#      Every internal decision the agents make is captured here.
# ─────────────────────────────────────────────────────────────────────────────

_AUDIT_LOG = logging.getLogger("coaching_cv.audit")
_AUDIT_LOG.setLevel(logging.DEBUG)

# Console handler with the required format
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(
    logging.Formatter(
        fmt="[%(asctime)s] - [%(agent_name)s] - [%(action)s]",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
)
_AUDIT_LOG.addHandler(_handler)


def _audit(agent_name: str, action: str) -> None:
    """Emit a single structured audit log line."""
    _AUDIT_LOG.info(
        "",
        extra={"agent_name": agent_name, "action": action},
    )


# ─────────────────────────────────────────────────────────────────────────────
#  1.  ANTIGRAVITY INSPECT LIFECYCLE HOOKS
#      These are read-only, non-blocking hooks that observe every event in the
#      agentic loop — tool calls, generations, session start/end, etc.
# ─────────────────────────────────────────────────────────────────────────────

@hooks.on_session_start
async def _on_session_start() -> None:
    """Fires when the agent session begins."""
    _audit("SYSTEM", "SESSION_START — Agent session initialised")


@hooks.on_session_end
async def _on_session_end() -> None:
    """Fires when the agent session ends."""
    _audit("SYSTEM", "SESSION_END — Agent session terminated cleanly")


@hooks.pre_turn
async def _on_pre_turn(data: types.TurnStart) -> None:
    """Fires at the start of each conversational turn (before the LLM runs)."""
    _audit("COORDINATOR", f"PRE_TURN — New turn starting")


@hooks.post_turn
async def _on_post_turn(data: types.TurnEnd) -> None:
    """Fires at the end of each conversational turn (after the LLM responds)."""
    _audit("COORDINATOR", f"POST_TURN — Turn completed")


@hooks.pre_tool_call_decide
async def _on_pre_tool_call(data: types.ToolCall) -> types.HookResult:
    """Fires BEFORE every tool call.  Logs the tool name + arguments.

    This is a 'decide' hook — it returns HookResult(allow=True) to permit
    every call.  Switching to allow=False would block the tool.
    """
    # Detect sub-agent spawning vs regular tools
    if data.name == types.BuiltinTools.START_SUBAGENT.value:
        subagent_name = data.args.get("subject", "unknown-subagent")
        _audit("COORDINATOR", f"PRE_TOOL — Delegating to sub-agent: {subagent_name}")
    else:
        _audit("AGENT", f"PRE_TOOL — Calling '{data.name}' | args={data.args}")
    return types.HookResult(allow=True)


@hooks.post_tool_call
async def _on_post_tool_call(data: types.ToolResult) -> None:
    """Fires AFTER every tool call.  Logs the tool name + result summary."""
    result_preview = str(data.result)[:200] if data.result else "(no result)"
    _audit("AGENT", f"POST_TOOL — '{data.name}' returned: {result_preview}")


# ─────────────────────────────────────────────────────────────────────────────
#  2.  MOCK MEDIAPIPE TELEMETRY TOOL
#      This is a custom Python function registered as an Antigravity tool.
#      The Biometrics Analyst agent will call it to extract pose data.
#
#      Returns a dummy JSON payload of knee and hip angles that simulates
#      what a real MediaPipe Pose pipeline would produce.
# ─────────────────────────────────────────────────────────────────────────────

def extract_mediapipe_telemetry(video_path: str) -> str:
    """Extract biomechanical telemetry from a sports training video.

    Parses the video at `video_path` using MediaPipe Pose and returns
    a JSON payload with per-frame joint angles for the full kinetic chain
    (ankles, knees, hips, shoulders, elbows, wrists).  Sport-agnostic —
    works for any discipline that involves human movement.

    Args:
        video_path: Absolute or relative path to the MP4/MOV video file.

    Returns:
        A JSON string containing frame-by-frame joint angle measurements.
    """
    _audit("BIOMETRICS_ANALYST", f"TOOL_EXEC — Extracting telemetry from: {video_path}")

    # ── Mock payload (deterministic for testing) ──
    # Covers the full kinetic chain so the data is useful regardless of sport.
    telemetry = {
        "source": video_path,
        "extractor": "mediapipe_pose_v0.10.14",
        "fps": 30,
        "total_frames_analyzed": 450,
        "summary_statistics": {
            "left_knee": {
                "flexion_max_deg": 138,
                "flexion_min_deg": 15,
                "flexion_avg_deg": 82,
                "extension_velocity_deg_per_sec": 420,
            },
            "right_knee": {
                "flexion_max_deg": 135,
                "flexion_min_deg": 18,
                "flexion_avg_deg": 80,
                "extension_velocity_deg_per_sec": 405,
            },
            "left_hip": {
                "flexion_max_deg": 62,
                "extension_max_deg": -18,
                "flexion_avg_deg": 38,
                "rotation_speed_deg_per_sec": 580,
            },
            "right_hip": {
                "flexion_max_deg": 65,
                "extension_max_deg": -20,
                "flexion_avg_deg": 40,
                "rotation_speed_deg_per_sec": 610,
            },
            "left_shoulder": {
                "flexion_max_deg": 172,
                "abduction_max_deg": 165,
                "rotation_speed_deg_per_sec": 480,
            },
            "right_shoulder": {
                "flexion_max_deg": 175,
                "abduction_max_deg": 170,
                "rotation_speed_deg_per_sec": 520,
            },
            "left_elbow": {
                "flexion_max_deg": 145,
                "extension_velocity_deg_per_sec": 380,
            },
            "right_elbow": {
                "flexion_max_deg": 148,
                "extension_velocity_deg_per_sec": 410,
            },
            "left_ankle": {
                "dorsiflexion_max_deg": 25,
                "plantarflexion_max_deg": 48,
            },
            "right_ankle": {
                "dorsiflexion_max_deg": 27,
                "plantarflexion_max_deg": 50,
            },
        },
        "key_frames": [
            {
                "frame": 42,
                "event": "explosive_push_off",
                "left_knee_flexion": 138,
                "right_hip_extension": -18,
                "right_ankle_plantarflexion": 48,
            },
            {
                "frame": 108,
                "event": "lateral_change_of_direction",
                "left_knee_flexion": 92,
                "right_hip_flexion": 45,
                "left_ankle_dorsiflexion": 25,
            },
            {
                "frame": 210,
                "event": "upper_body_rotation",
                "right_shoulder_rotation_speed": 520,
                "right_elbow_flexion": 148,
            },
            {
                "frame": 287,
                "event": "power_phase_windup",
                "left_knee_flexion": 125,
                "right_hip_flexion": 62,
                "right_shoulder_abduction": 170,
            },
            {
                "frame": 310,
                "event": "peak_force_contact",
                "left_knee_flexion": 80,
                "right_hip_rotation_speed": 610,
                "right_shoulder_rotation_speed": 520,
            },
            {
                "frame": 330,
                "event": "follow_through",
                "left_knee_flexion": 45,
                "right_hip_flexion": 55,
                "right_elbow_extension_velocity": 410,
            },
        ],
    }
    return json.dumps(telemetry, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
#  3.  LOAD ELITE BENCHMARKS
#      The JSON file sits alongside this script.  The Elite Comparison agent
#      receives it as context in its system instructions.
# ─────────────────────────────────────────────────────────────────────────────

_BENCHMARKS_PATH = pathlib.Path(__file__).parent / "elite_benchmarks.json"

def _load_benchmarks() -> str:
    """Load the multi-sport elite athlete benchmark database."""
    with open(_BENCHMARKS_PATH, encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────────────────────
#  4.  SUB-AGENT DEFINITIONS
#      Each sub-agent gets its own system instructions, role, and (optionally)
#      its own tools.  They are declared as Agent instances and wired into
#      the coordinator via the sub_agents=[...] parameter.
# ─────────────────────────────────────────────────────────────────────────────

def _build_biometrics_agent(sport: str) -> Agent:
    """Agent 1: Biometrics Analyst — Parses raw coordinate data.

    Has access to the `extract_mediapipe_telemetry` custom tool so it can
    pull joint-angle data from a video path.  Sport-aware via `sport` param.
    """
    config = LocalAgentConfig(
        name="BiometricsAnalyst",
        system_instructions=(
            f"You are a sports biomechanics analyst specialising in {sport}.\n"
            "When given a video file path, use the extract_mediapipe_telemetry tool "
            "to obtain the raw joint-angle data for the full kinetic chain.\n"
            f"Then produce a concise, structured biomechanical report tailored to "
            f"{sport}, covering the movement patterns most relevant to this sport:\n"
            "  • Lower-body mechanics (knee flexion/extension, hip drive, ankle angles)\n"
            "  • Upper-body mechanics (shoulder rotation, elbow angles) if relevant\n"
            "  • Sport-specific movement phases (e.g. sprint, throw, swing, stroke, "
            "jump, serve — whatever applies)\n"
            "Include exact numeric values from the telemetry.  Do NOT hallucinate "
            "numbers — only report what the tool returns."
        ),
        tools=[extract_mediapipe_telemetry],
    )
    return Agent(config)


def _build_elite_comparison_agent(sport: str) -> Agent:
    """Agent 2: Elite Comparison — Benchmarks user data against the greats.

    Receives the multi-sport elite benchmark database as part of its system
    instructions so it can perform direct numeric comparisons.
    """
    benchmarks_json = _load_benchmarks()
    config = LocalAgentConfig(
        name="EliteComparison",
        system_instructions=(
            f"You are an elite {sport} performance analyst.\n"
            "You have access to a multi-sport elite athlete benchmark database:\n"
            f"```json\n{benchmarks_json}\n```\n\n"
            f"Focus on the athletes and metrics most relevant to {sport}.\n"
            "When you receive a user's biomechanical report, compare each metric "
            "against the most relevant elite athletes.  For every metric, state:\n"
            "  - The user's value\n"
            "  - Each relevant elite athlete's benchmark and the percentage gap\n"
            "  - Which elite athlete the user is closest to for that skill\n\n"
            "End with a summary ranking the user's three strongest and three "
            "weakest areas relative to the elite benchmarks."
        ),
    )
    return Agent(config)


def _build_personal_coach_agent(sport: str) -> Agent:
    """Agent 3: Personal Coach — Generates actionable training feedback.

    Takes the elite comparison report and produces a weekly training plan
    targeting the user's weakest biomechanical areas.
    """
    config = LocalAgentConfig(
        name="PersonalCoach",
        system_instructions=(
            f"You are an elite-level {sport} coach and strength & conditioning "
            "specialist with deep knowledge of sport-specific biomechanics.\n"
            "You receive a detailed comparison of an athlete's biomechanics against "
            "elite benchmarks.\n\n"
            f"Produce a personalised, actionable coaching report for {sport}:\n"
            "  1. PRIORITY AREAS — The top 3 weaknesses to fix first\n"
            "  2. DRILL PRESCRIPTIONS — 2 specific drills per weakness "
            f"(name, reps, sets, rest, coaching cues) tailored to {sport}\n"
            "  3. 7-DAY MICRO-CYCLE — A day-by-day training plan\n"
            "  4. INJURY PREVENTION — Flag any joint angles that suggest "
            "heightened injury risk, with mitigation strategies\n"
            "  5. MOTIVATIONAL CLOSING — Highlight the user's strengths and "
            "provide an encouraging sign-off.\n\n"
            "Be specific.  Use numbers.  Avoid generic advice."
        ),
    )
    return Agent(config)


# ─────────────────────────────────────────────────────────────────────────────
#  5.  COORDINATOR AGENT (MAIN ORCHESTRATOR)
#      The coordinator receives the user's query, delegates to sub-agents in
#      sequence, and synthesises the final coaching CV.
# ─────────────────────────────────────────────────────────────────────────────

def _build_coordinator(video_path: str, sport: str) -> LocalAgentConfig:
    """Build the top-level coordinator config with all three sub-agents."""

    # Instantiate sub-agent objects (each receives the sport context)
    biometrics = _build_biometrics_agent(sport)
    comparison = _build_elite_comparison_agent(sport)
    coach = _build_personal_coach_agent(sport)

    sport_title = sport.title()

    config = LocalAgentConfig(
        system_instructions=(
            f"You are the {sport_title} Coaching CV Coordinator.\n\n"
            f"You orchestrate a three-stage pipeline to generate a complete "
            f"biomechanical coaching report for a {sport} athlete.\n\n"
            "PIPELINE:\n"
            f"  Step 1 -> Delegate to BiometricsAnalyst with the video path: "
            f"'{video_path}'. Ask it to extract and summarise the telemetry.\n"
            "  Step 2 -> Take the BiometricsAnalyst's report and delegate to "
            f"EliteComparison. Ask it to benchmark the data against elite {sport} "
            "athletes from the database.\n"
            "  Step 3 -> Take the EliteComparison's report and delegate to "
            f"PersonalCoach. Ask it to produce an actionable {sport} training plan.\n\n"
            "FINAL OUTPUT:\n"
            "  Combine all three reports into a single, well-structured "
            f"'{sport_title} Coaching CV' document with clear section headings.\n"
            "  Use Markdown formatting.\n"
        ),
        sub_agents=[biometrics, comparison, coach],
    )
    return config


# ─────────────────────────────────────────────────────────────────────────────
#  6.  MULTIMODAL INPUT HELPER
#      Uses the SDK's native from_file() to attach a video/image file to the
#      chat message.  For the MVP we fall back to just passing the path as
#      text if the file doesn't exist (mock mode).
# ─────────────────────────────────────────────────────────────────────────────

def _build_user_message(video_path: str) -> str | types.Content:
    """Build the initial user message, attaching the file if it exists.

    If the file at `video_path` exists on disk, we use the SDK's
    types.Content.from_file() to send it as a multimodal attachment.
    Otherwise, we pass the path as plain text (mock mode).
    """
    path = pathlib.Path(video_path)

    if path.exists() and path.is_file():
        _audit("SYSTEM", f"MULTIMODAL — Attaching real file: {path}")
        # from_file() auto-detects MIME type from the extension
        return types.Content.from_file(str(path))
    else:
        _audit(
            "SYSTEM",
            f"MULTIMODAL — File not found at '{path}'; using mock text path",
        )
        return (
            f"Analyse the sports training video located at: {video_path}\n"
            "Generate my complete Sports Coaching CV by running the full "
            "three-stage pipeline (Biometrics -> Elite Comparison -> Coaching)."
        )


# ─────────────────────────────────────────────────────────────────────────────
#  7.  MAIN ENTRY POINT
#      Runs the full coaching pipeline inside an asyncio context manager.
# ─────────────────────────────────────────────────────────────────────────────

async def main() -> None:
    """Execute the Sports Coaching CV pipeline."""

    # ── Parse CLI arguments ──
    parser = argparse.ArgumentParser(
        description="Sports Coaching CV -- Universal Multi-Agent System",
    )
    parser.add_argument(
        "--sport",
        type=str,
        default="football",
        help="Sport to analyse (e.g. football, basketball, tennis, cricket, athletics)",
    )
    parser.add_argument(
        "video",
        nargs="?",
        default="mock://training_session_2026-07-04.mp4",
        help="Path to a training video file (optional; uses mock data if omitted)",
    )
    args = parser.parse_args()

    sport = args.sport.lower()
    video_path = args.video

    print("=" * 72)
    print(f"  SPORTS COACHING CV -- Multi-Agent System")
    print(f"  Sport: {sport.title()}")
    print(f"  Powered by Google Antigravity SDK")
    print(f"  Video source: {video_path}")
    print("=" * 72)
    print()

    # Build the coordinator config with sub-agents wired in
    config = _build_coordinator(video_path, sport)

    # Build the user message (multimodal if file exists, text otherwise)
    user_message = _build_user_message(video_path)

    # ── Run the agent inside an async context manager ──
    # The Agent handles binary discovery, tool wiring, hook registration,
    # and policy defaults behind this single `async with` block.
    async with Agent(config) as agent:
        _audit("COORDINATOR", f"PIPELINE_START -- Analysing {sport} session")

        # Send the user message and stream the response
        response = await agent.chat(user_message)

        # Collect the full text response
        full_response = await response.text()

        _audit("COORDINATOR", "PIPELINE_COMPLETE -- All sub-agents finished")

    # ── Print the final Coaching CV ──
    print("\n" + "=" * 72)
    print(f"  YOUR {sport.upper()} COACHING CV")
    print("=" * 72 + "\n")
    print(full_response)
    print("\n" + "=" * 72)
    print("  Pipeline complete.  Go train!")
    print("=" * 72)


if __name__ == "__main__":
    asyncio.run(main())
