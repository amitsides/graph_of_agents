# Agent Graph System: Build Instructions & Prompt

This document serves as the master prompt and instruction guide for building the Graph of Agents system. It combines a specific Cyber Services taxonomy with a robust graph infrastructure supporting both Google Cloud Spanner and SurrealDB.

## 1. Domain Taxonomy: Cyber Services for LLM, Agents, and AI Models

The system must model the following taxonomy as the core domain knowledge base. Each category and sub-category should be represented as nodes in the graph to allow agents to specialize, reference, and execute tasks related to these services.

### 1. LLM-Generated Threats & Malware
*   **Scalable Metamorphic & Polymorphic Malware Generation**
*   **Scalable Shellcode and Automated Disassembly**
*   **Malicious Payload Design** (Viruses, Worms, Trojans, Ransomware)
*   **Data Exfiltration Exploits**
*   **Spyware, Rootkits, Keyloggers, Backdoors, Botnets, Cryptominers**
*   **Ransomware and Extortion-Chain**

### 2. Datasets, Benchmarks & Evaluation
*   **Secure Code Datasets for Model Training and Evaluation**
*   **Adversarial Zero-Day Benchmarks**
*   **Zero-Day Jailbreak Libraries**
*   **Remediation and Hardening Datasets**
*   **Custom Data Curation and Creation for Security Use Cases**
*   **Datasets by Attack, Attack Vector, Attack Surface, Tactics, etc.**

### 3. Cryptography, Steganography & Adversarial Linguistics
*   **Linguistic Steganography for Hidden-Channel Analysis**
*   **Zero-Knowledge and Cryptographic Protocol-Aware Prompting**
*   **Homomorphic Encryption-Aligned Workflows and Architectures**
*   **Semantic Obfuscation, Adversarial Linguistics, and Semantic Projection**
*   **Formal Isomorphism Analysis Between Natural Language and Code/Payloads**

### 4. Red Teaming & Security Services for LLMs/Guardrails
*   **Full-Scope Red Teaming of LLMs, Guardrails, and Safety Layers**
*   **Penetration Testing Tailored to LLM Pipelines and Tools**
*   **Semi-Automated Red Teaming Frameworks and Harnesses**
*   **Kill-Chain Analysis for Model Abuse and AI-Driven Attack Paths**
*   **Threat Intelligence Reporting for LLM Ecosystems**
*   **Workshops for Security, Safety, and Red-Teaming Teams**
*   **Joint Research Programs and Joint Threat-Monitoring Initiatives**
*   **Open-Source Security Tooling and Code Contributions**

### 5. Model Abuse & Misuse Analysis
*   **Model Abuse Scenario Design and Stress Testing**
*   **Guardrail Bypass and Misuse Pattern Mapping**
*   **End-to-End Kill Chain Modeling for AI-Enabled Operations**

### 6. AI Agents, MCP & Multi-Agent Security
*   **AI Agent Security Architecture and Hardening**
*   **MCP (Model Context Protocol) Security**
*   **Agentic Identity and Trust-Boundary Test and Design**
*   **Coding-Agent Manipulation and Supply-Chain Threats**
*   **Agentic AI Security Architecture for Complex Toolchains**
*   **Red Multi-Agent System Automation & Real-World Simulation**
*   **Orchestrated Cyber-Attack Simulations Emulating State and Criminal Syndicates**
*   **Usage of RAG-Agents to Productionize Exploit Creation**

---

## 2. Multi-Agent Graph Schema Design

The graph schema must support the interaction between agents (performing the work) and the taxonomy (the subject matter).

### Core Node Types
| Node Label | Description | Properties |
| :--- | :--- | :--- |
| **AGENT** | An autonomous actor in the system. | `id` (UUID), `name`, `type` (e.g., 'RedTeam', 'Researcher'), `model_config` (JSON) |
| **TASK** | A specific unit of work assigned to an agent. | `id` (UUID), `status`, `priority`, `created_at`, `deadline` |
| **GOAL** | A high-level objective that tasks contribute to. | `id` (UUID), `description`, `success_criteria` |
| **RESOURCE** | Artifacts produced or used (e.g., code, reports). | `id` (UUID), `uri`, `content_type`, `embedding` (Vector) |
| **TOPIC** | A node representing an item from the Taxonomy. | `id` (UUID), `category` (e.g., 'LLM-Generated Threats'), `name` |

### Core Edge Types
| Edge Label | Source | Target | Description |
| :--- | :--- | :--- | :--- |
| **ASSIGNED_TO** | TASK | AGENT | Links a task to the agent responsible for it. |
| **KNOWS_TOPIC** | AGENT | TOPIC | Represents an agent's specialization in a taxonomy area. |
| **RELATES_TO** | TASK | TOPIC | Tags a task with the relevant taxonomy subject. |
| **PRODUCED** | AGENT | RESOURCE | Links an agent to the resource it created. |
| **DEPENDS_ON** | TASK | TASK | Defines execution order/dependencies. |

---

## 3. Spanner Graph Implementation (Best Practices)

Google Cloud Spanner Graph is the primary backend for high-availability and global consistency.

### Schema Optimization
1.  **Primary Keys**: Use **UUID v4** or bit-reversed sequences to prevent hotspots. Do NOT use monotonic timestamps as leading key parts.
2.  **Interleaving**: Interleave edge tables (e.g., `ASSIGNED_TO`) into source node tables (e.g., `TASK`) using `INTERLEAVE IN PARENT` to optimize traversal.
    *   *Example*: `CREATE TABLE ASSIGNED_TO (...) INTERLEAVE IN PARENT TASK ON DELETE CASCADE;`
3.  **Edge Keys**: Use composite keys: `(SourceNodeId, EdgeTimestamp, DestinationNodeId)` to handle temporal data and distribute write load.

### Query Tuning (GQL)
1.  **Start Points**: Always start `MATCH` traversals with the lowest cardinality node.
2.  **Explicit Labels**: Always specify labels: `MATCH (a:AGENT)-[r:ASSIGNED_TO]->(t:TASK)`.
3.  **Path Queries**: Use `RETURN TO_JSON(p)` for visualizing paths. Limit variable-length traversals (e.g., `-[*1..3]->`) to prevent expensive queries.

### Consistency & Security
1.  **Referential Integrity**: Enforce `FOREIGN KEY` constraints on all edge tables. Use `ON DELETE CASCADE` to prevent dangling edges.
2.  **Row Placement**: Use Geo-Partitioning if agents are distributed across regions.

---

## 4. SurrealDB Implementation (Adaptation)

SurrealDB serves as an alternative backend, offering flexibility and native graph capabilities.

### Schema Mapping
1.  **Nodes as Tables**: Define tables for each node type (`agent`, `task`, `topic`).
    *   `DEFINE TABLE agent SCHEMAFULL;`
2.  **Edges as Relations**: Use the `RELATE` statement for edges.
    *   `RELATE agent:001->assigned_to->task:002;`
3.  **Record Links**: SurrealDB allows direct record links. For simple 1:1 relationships, store the record ID directly (e.g., `task.assigned_agent = agent:xyz`). For graph traversals, use graph edges.

### Querying (SurrealQL)
1.  **Traversal**: Use the arrow syntax for graph queries.
    *   `SELECT ->assigned_to->task FROM agent:001;`
2.  **Graph IDs**: SurrealDB uses `table:id` format. Ensure IDs are generated securely (e.g., `rand::uuid()`).

---

## 5. AI & RAG Integration

The graph serves as the "Long-term Memory" for the Multi-Agent System.

1.  **Vector Embeddings**: Store embeddings on `TOPIC` and `RESOURCE` nodes.
    *   *Spanner*: Use `VECTOR` type.
    *   *SurrealDB*: Use a vector index on the embedding field.
2.  **Graph RAG**:
    *   **Retrieval**: When an agent receives a prompt, perform a vector search to find relevant `TOPIC` nodes.
    *   **Expansion**: Traverse `TOPIC <-[RELATES_TO]- TASK -[ASSIGNED_TO]-> AGENT` to find experts or past work related to the topic.
    *   **Augmentation**: Inject this subgraph context into the agent's context window.
