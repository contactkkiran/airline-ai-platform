from anthropic.types import ToolParam

# ============================================================
# TOOL SCHEMA
# ============================================================
#
# This describes the tool to Claude.
#
# IMPORTANT:
# This does NOT execute flight_status_lookup().
# It only tells Claude what tool is available and
# what input the tool expects.
#
# ============================================================

flight_status_tool_schema: ToolParam = {
    "name": "flight_status_lookup",
    "description": "Get the current status of a flight by its flight number.",
    "input_schema": {
        "type": "object",
        "properties": {
            "flight_number": {
                "type": "string",
                "description": "The flight number, e.g. AI202",
            }
        },
        "required": ["flight_number"],
    },
}


# ============================================================
# ACTUAL PYTHON TOOL
# ============================================================
#
# This function is executed by OUR Python application.
# Claude does NOT execute this function directly.
#
# ============================================================


def flight_status_lookup(flight_number: str) -> dict:
    fake_db = {
        "AI202": {
            "status": "Delayed",
            "delay_minutes": 45,
            "gate": "B12",
        },
        "AI305": {
            "status": "On Time",
            "delay_minutes": 0,
            "gate": "A4",
        },
    }

    return fake_db.get(
        flight_number,
        {"status": "Unknown flight number"},
    )
