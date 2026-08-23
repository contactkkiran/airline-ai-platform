from anthropic import Anthropic

from src.config.settings import ANTHROPIC_API_KEY
from src.tools.flight_status import (
    flight_status_lookup,
    flight_status_tool_schema,
)

# ============================================================
# SETUP
# ============================================================

client = Anthropic(api_key=ANTHROPIC_API_KEY)

user_question = "Is flight AI202 delayed?"


# ============================================================
# FLOW 1 — USER → CLAUDE
# ============================================================
#
# We send the user's question to Claude.
#
# At the same time, we provide the TOOL SCHEMA.
#
# Claude now knows:
#
#   Tool name: flight_status_lookup
#   Input: flight_number
#
# IMPORTANT:
# The Python function is NOT executed here.
#
# ============================================================

print("\n========================================")
print("FLOW 1 — USER → CLAUDE")
print("========================================")


response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[flight_status_tool_schema],
    messages=[
        {
            "role": "user",
            "content": user_question,
        }
    ],
)


print("\nClaude response:", response)

for block in response.content:
    print(block)


# ============================================================
# FLOW 2 — CLAUDE → TOOL REQUEST
# ============================================================
#
# Claude may decide that it needs the flight-status tool.
#
# Claude then returns a "tool_use" block.
#
# Example:
#
#   name:
#       flight_status_lookup
#
#   input:
#       {
#           "flight_number": "AI202"
#       }
#
# Claude is NOT executing our Python function.
#
# Claude is REQUESTING that our application execute it.
#
# ============================================================

if response.stop_reason == "tool_use":

    print("\n========================================")
    print("FLOW 2 — CLAUDE → TOOL REQUEST")
    print("========================================")

    tool_use_block = next(
        block for block in response.content if block.type == "tool_use"
    )

    print("\nTool requested by Claude:")
    print(f"Tool name: {tool_use_block.name}")
    print(f"Tool input: {tool_use_block.input}")

    # ========================================================
    # FLOW 3 — EXTRACT TOOL INPUT
    # ========================================================
    #
    # Claude generated:
    #
    # {
    #     "flight_number": "AI202"
    # }
    #
    # We extract the flight number.
    #
    # str() is intentional because Anthropic's SDK types
    # tool input as a generic object.
    #
    # ========================================================

    print("\n========================================")
    print("FLOW 3 — EXTRACT TOOL INPUT")
    print("========================================")

    flight_number: str = str(tool_use_block.input["flight_number"])

    print(f"Flight number received from Claude: " f"{flight_number}")

    # ========================================================
    # FLOW 4 — PYTHON EXECUTES THE TOOL
    # ========================================================
    #
    # THIS is where the actual function is called.
    #
    # Claude requested the tool.
    # Python executes the tool.
    #
    # ========================================================

    print("\n========================================")
    print("FLOW 4 — PYTHON EXECUTES TOOL")
    print("========================================")

    tool_result = flight_status_lookup(flight_number)

    print("\nLocal tool result:")
    print(tool_result)

    # ========================================================
    # FLOW 5 — TOOL RESULT → CLAUDE
    # ========================================================
    #
    # Python has executed the tool and received:
    #
    # {
    #     "status": "Delayed",
    #     "delay_minutes": 45,
    #     "gate": "B12"
    # }
    #
    # We now send that result back to Claude.
    #
    # ========================================================

    print("\n========================================")
    print("FLOW 5 — TOOL RESULT → CLAUDE")
    print("========================================")

    final_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=[flight_status_tool_schema],
        messages=[
            {
                "role": "user",
                "content": user_question,
            },
            {
                "role": "assistant",
                "content": response.content,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": str(tool_result),
                    }
                ],
            },
        ],
    )

    # ========================================================
    # FLOW 6 — CLAUDE → FINAL ANSWER
    # ========================================================
    #
    # Claude now has the tool result.
    #
    # It converts the structured result into a
    # natural-language response.
    #
    # ========================================================

    print("\n========================================")
    print("FLOW 6 — CLAUDE → FINAL ANSWER")
    print("========================================")

    for block in final_response.content:

        if block.type == "text":
            print(block.text)


else:

    print("\nClaude answered directly " "without using the tool.")
