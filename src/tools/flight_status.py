from anthropic.types import ToolParam

flight_status_tool_schema: ToolParam = {
    "name": "flight_status_lookup",
    "description": "Get the current status of a flight by its flight number.",
    "input_schema": {
        "type": "object",
        "properties": {
            "flight_number": {
                "type": "string",
                "query": "The flight number, e.g. AI102",
            }
        },
        "required": ["flight_number"],
    },
}


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
