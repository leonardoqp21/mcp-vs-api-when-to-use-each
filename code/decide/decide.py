"""MCP, an API, or both? A small explainable decision helper.

Answer yes/no questions about who will use the capability and how. It returns one or more
recommendations and the reasons. It is a thinking aid, not an oracle.

    python decide.py                          # interactive
    python decide.py --json '{"...": true}'

Standard library only. Python 3.9 or newer.
"""
from __future__ import annotations

import argparse
import json

QUESTIONS = {
    "ai_client_is_the_caller": "Will an AI assistant or agent (Claude, ChatGPT, Cursor) decide at run time what to call?",
    "code_is_the_caller": "Will your own code call it on a fixed path (a backend, a script, a pipeline)?",
    "needs_discovery": "Must the caller discover what is available and how to use it, without hard-coding it?",
    "must_be_deterministic": "Must the same input always give the same call and the same result?",
    "high_volume_or_latency_sensitive": "Is it high volume, or sensitive to cost per call and delay?",
    "acts_as_the_signed_in_person": "Must it act with the permissions of the person who is using it, with their own sign in?",
    "exploratory_or_ad_hoc": "Is the use exploratory or ad hoc (a person asking questions, trying things)?",
    "an_api_already_exists": "Does a stable API for this already exist?",
    "event_driven": "Is it event-driven (react when something happens, push data to a system)?",
}


def decide(a: dict) -> list[dict]:
    missing = [k for k in QUESTIONS if k not in a]
    if missing:
        raise ValueError(f"missing answers: {', '.join(missing)}")
    picks: list[dict] = []

    def add(option: str, why: str):
        if option not in {p["option"] for p in picks}:
            picks.append({"option": option, "why": why})

    if a["event_driven"]:
        add("webhook_or_workflow", "The need is to react to events. Use webhooks or a workflow. Neither MCP nor a request-response API is the main tool.")

    if a["code_is_the_caller"] and a["must_be_deterministic"]:
        add("api", "Your code calls a fixed path and needs the same call every time. Use the API (or its SDK) directly.")
    elif a["code_is_the_caller"] and a["high_volume_or_latency_sensitive"]:
        add("api", "High volume or latency sensitivity favors a direct API call with no tool-description overhead.")

    if a["ai_client_is_the_caller"] and (a["needs_discovery"] or a["exploratory_or_ad_hoc"]):
        add("mcp", "An AI client must find and use capabilities at run time. MCP gives it a standard list of tools with descriptions and schemas.")
    if a["ai_client_is_the_caller"] and a["acts_as_the_signed_in_person"]:
        add("mcp", "A remote MCP server can sign the person in (OAuth) so the assistant acts with their permissions, not a shared key.")

    if a["ai_client_is_the_caller"] and a["an_api_already_exists"]:
        add("mcp_wrapping_the_api", "Keep the API as the source of truth. Put a small, well-scoped MCP server in front of it for AI clients.")
    if a["ai_client_is_the_caller"] and a["code_is_the_caller"]:
        add("both", "Both kinds of caller exist. Serve code through the API and AI clients through MCP, backed by the same logic and permissions.")

    if not picks:
        if a["an_api_already_exists"]:
            add("api", "No AI client is involved. The existing API is enough.")
        else:
            add("api", "Start with a plain API. Add MCP only when AI clients need to use it.")
    return picks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json")
    args = parser.parse_args()
    if args.json:
        answers = json.loads(args.json)
    else:
        answers = {}
        for key, text in QUESTIONS.items():
            while True:
                raw = input(f"{text} [y/n] ").strip().lower()
                if raw in {"y", "n"}:
                    answers[key] = raw == "y"
                    break
    for p in decide(answers):
        print(f"- {p['option']}: {p['why']}")


if __name__ == "__main__":
    main()
