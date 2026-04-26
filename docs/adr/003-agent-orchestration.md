# ADR 003: Agent Orchestration with LangGraph

## Date
2026-04-26

## Status
Accepted

## Context
The AROGYA system handles complex, multimodal medical research queries. Resolving these queries requires multiple steps of reasoning, including classifying the user's intent, optionally retrieving grounded evidence, verifying that evidence against hallucinations, and finally generating a comprehensive, cited report. 

Using basic LLM chains or standard `AgentExecutor` implementations proved inadequate. They are often "black-boxes," making it difficult to guarantee deterministic control flow (e.g., strictly enforcing that a verification step happens after retrieval and before reporting). We needed an orchestration framework that allows us to explicitly define the state of the conversation and control the routing between specialized agents.

## Decision
We decided to implement the multi-agent workflow using **LangGraph**. 

Specifically:
- We define a strongly typed `AgentState` using Python's `TypedDict` to pass context between agents.
- Each agent (Triage, RAG, Verifier, Report) is implemented as a modular node function.
- We construct a `StateGraph` to explicitly define the execution sequence.
- We use conditional edges (e.g., after the Triage node, routing directly to the Report node for general queries or to the RAG node for specific medical questions requiring evidence).

## Consequences

### Positive
- **Determinism:** The flow of data is explicitly wired. We know exactly which agents run and in what order.
- **Observability:** We can inspect the `AgentState` at any point in the graph, making debugging and logging significantly easier.
- **Extensibility:** Adding new agents (e.g., a Vision agent or a Guardrail agent) is as simple as adding a node and an edge to the graph.
- **Robustness:** Resolves IDE type warnings and improves the testability of individual agent functions.

### Negative
- **Complexity:** Requires more boilerplate (explicit state definition, node signatures, graph compilation) compared to a simple sequential chain.
- **Learning Curve:** Developers need to understand LangGraph's graph-based execution model and state management.
