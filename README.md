# Airline AI Platform

An early-stage platform that uses Claude's tool-use (function calling) to answer
airline questions — e.g. flight status — by letting Claude call real backend
functions instead of guessing.

## How it works

Claude is offered a **tool schema** describing a Python function it can request.
When it decides the question needs live data, it returns a `tool_use` block
instead of an answer; the app runs the real function locally, sends the result
back, and Claude uses it to write the final answer.

`test_connection.py` walks through this as six explicit, printed flows:

```mermaid
sequenceDiagram
    participant U as User
    participant App as test_connection.py
    participant C as Claude API
    participant T as flight_status_lookup()

    Note over App,C: FLOW 1 — USER → CLAUDE
    U->>App: "Is flight AI202 delayed?"
    App->>C: messages.create(tools=[flight_status_tool_schema])

    Note over App,C: FLOW 2 — CLAUDE → TOOL REQUEST
    C-->>App: stop_reason = tool_use<br/>name: flight_status_lookup

    Note over App: FLOW 3 — EXTRACT TOOL INPUT
    App->>App: flight_number = tool_use_block.input["flight_number"]

    Note over App,T: FLOW 4 — PYTHON EXECUTES THE TOOL
    App->>T: flight_status_lookup("AI202")
    T-->>App: {status: Delayed, delay_minutes: 45, gate: B12}

    Note over App,C: FLOW 5 — TOOL RESULT → CLAUDE
    App->>C: messages.create(tool_result)

    Note over App,C: FLOW 6 — CLAUDE → FINAL ANSWER
    C-->>App: final text answer
    App-->>U: "AI202 is delayed 45 min, gate B12"
```

If Claude decides it doesn't need the tool, it skips straight to a direct
text answer and flows 2–6 never run.

## Project structure

```mermaid
flowchart TD
    subgraph root[" "]
        TC[test_connection.py]
    end

    subgraph src/config
        SET["settings.py<br/><i>loads ANTHROPIC_API_KEY</i>"]
    end

    subgraph src/tools["src/tools (basic, working)"]
        FS["flight_status.py<br/><i>flight_status_lookup&#40;&#41;<br/>flight_status_tool_schema: ToolParam</i>"]
    end

    subgraph src/integrations["src/integrations (new, scaffold only)"]
        subgraph amadeus["amadeus/"]
            INIT["__init__.py"]
            CLIENT["client.py<br/><i>empty — Amadeus API client, planned</i>"]
            subgraph amadeustools["tools/"]
                FSEARCH["flight_search.py<br/><i>empty — real flight search, planned</i>"]
            end
        end
    end

    subgraph src/agents["src/agents (planned)"]
        AG[" "]
    end

    subgraph src/orchestration["src/orchestration (planned)"]
        OR[" "]
    end

    TC -->|reads API key| SET
    TC -->|imports tool + schema| FS
    TC -.->|not yet wired up| FSEARCH
    FSEARCH -.->|will call| CLIENT
    TC -.->|future| AG
    TC -.->|future| OR
```

- **`src/config/settings.py`** — loads `ANTHROPIC_API_KEY` from `.env`.
- **`src/tools/flight_status.py`** — a mock flight-status lookup and its
  Anthropic `ToolParam` schema. This is the only tool actually wired into
  `test_connection.py` today.
- **`src/integrations/amadeus/`** — scaffolding for a real flight-search
  provider (Amadeus). `client.py` and `tools/flight_search.py` exist but are
  currently empty; nothing here is called yet. The idea is to keep
  Claude-facing tools (`src/tools/`) separate from third-party API
  integrations (`src/integrations/`), so other providers (e.g. Sabre) could
  be added the same way later.
- **`src/agents/`, `src/orchestration/`** — scaffolding for future multi-agent
  orchestration; currently empty.
- **`test_connection.py`** — end-to-end smoke test: sends a question, lets
  Claude call the flight-status tool, and prints each of the six flows above.

## Roadmap

Planned direction, once the Amadeus integration is implemented:

```mermaid
flowchart LR
    C[Claude]
    C -->|tool_use: flight_status_lookup| BT[flight_status tool]
    C -->|tool_use: flight_search| AT[flight_search tool]
    BT --> LOCAL[Local mock data]
    AT --> CLIENT[integrations/amadeus/client.py]
    CLIENT --> API[(Amadeus API)]
```

`src/tools/flight_status.py` and `test_connection.py` stay untouched while
this is built out separately under `src/integrations/`.

## Setup

1. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```
2. Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Run

```bash
python3 test_connection.py
```
