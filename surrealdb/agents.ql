-- SurrealDB Graph Script for Red Team Multi-Agent System
-- Based on taxonomy/jaxonomy.json

-- 1. Define Tables (Nodes)
DEFINE TABLE agent SCHEMAFULL;
DEFINE FIELD name ON TABLE agent TYPE string;
DEFINE FIELD role ON TABLE agent TYPE string;
DEFINE FIELD specialization ON TABLE agent TYPE string;
DEFINE FIELD status ON TABLE agent TYPE string;
DEFINE FIELD trust_level ON TABLE agent TYPE float;
DEFINE FIELD capabilities ON TABLE agent TYPE array;
DEFINE FIELD taxonomy_mapping ON TABLE agent TYPE array;

DEFINE TABLE task SCHEMAFULL;
DEFINE FIELD description ON TABLE task TYPE string;
DEFINE FIELD status ON TABLE task TYPE string;
DEFINE FIELD priority ON TABLE task TYPE int;

DEFINE TABLE artifact SCHEMAFULL;
DEFINE FIELD type ON TABLE artifact TYPE string;
DEFINE FIELD uri ON TABLE artifact TYPE string;

-- 2. Insert Agents
CREATE agent:agent_001 SET 
    name = 'Red Team Orchestrator',
    role = 'Acts as the attack campaign coordinator...',
    specialization = 'RED_TEAM_COORDINATION',
    status = 'ACTIVE',
    trust_level = 0.95,
    capabilities = ['kill_chain_orchestration', 'multi_agent_attack_synchronization', 'opsec_monitoring', 'campaign_timeline_management', 'strategic_planning', 'resource_allocation'],
    taxonomy_mapping = ['4. Red Teaming & Security Services for LLMs/Guardrails', '6. AI Agents, MCP & Multi-Agent Security'];

CREATE agent:agent_002 SET 
    name = 'Attack Planner Agent',
    role = 'Designs end-to-end adversary campaigns...',
    specialization = 'ATTACK_PLANNING',
    status = 'IDLE',
    trust_level = 0.92,
    capabilities = ['attack_surface_analysis', 'exploit_chain_design', 'mitre_attack_mapping', 'evasion_strategy_development', 'persistence_mechanism_design', 'lateral_movement_planning'],
    taxonomy_mapping = ['1. LLM-Generated Threats & Malware', '5. Model Abuse & Misuse Analysis'];

CREATE agent:agent_003 SET 
    name = 'Threat Intelligence Agent',
    role = 'Aggregates, enriches, and contextualizes threat data...',
    specialization = 'THREAT_INTELLIGENCE',
    status = 'ACTIVE',
    trust_level = 0.88,
    capabilities = ['ioc_enrichment', 'ttp_pattern_recognition', 'adversary_profiling', 'threat_correlation', 'dark_web_monitoring', 'vulnerability_intelligence'],
    taxonomy_mapping = ['4. Red Teaming & Security Services for LLMs/Guardrails', '2. Datasets, Benchmarks & Evaluation'];

CREATE agent:agent_004 SET 
    name = 'Exploit Generator Agent',
    role = 'Performs automated vulnerability research...',
    specialization = 'EXPLOIT_GENERATION',
    status = 'ACTIVE',
    trust_level = 0.85,
    capabilities = ['polymorphic_code_generation', 'shellcode_synthesis', 'zero_day_weaponization', 'payload_customization', 'metamorphic_transformation', 'automated_disassembly'],
    taxonomy_mapping = ['1. LLM-Generated Threats & Malware'];

CREATE agent:agent_005 SET 
    name = 'Cryptographic Warfare Agent',
    role = 'Provides expertise in offensive and defensive cryptography...',
    specialization = 'CRYPTOGRAPHIC_OPERATIONS',
    status = 'IDLE',
    trust_level = 0.90,
    capabilities = ['semantic_obfuscation', 'steganographic_encoding', 'zk_protocol_implementation', 'cryptanalysis', 'homomorphic_encryption', 'adversarial_linguistics', 'covert_channel_design'],
    taxonomy_mapping = ['3. Cryptography, Steganography & Adversarial Linguistics'];

CREATE agent:agent_006 SET 
    name = 'Adversarial ML Agent',
    role = 'Implements machine learning attacks and defenses...',
    specialization = 'ML_ADVERSARIAL',
    status = 'ACTIVE',
    trust_level = 0.87,
    capabilities = ['adversarial_example_generation', 'model_extraction', 'prompt_injection', 'guardrail_bypass', 'data_poisoning', 'backdoor_injection', 'jailbreak_prompt_crafting'],
    taxonomy_mapping = ['4. Red Teaming & Security Services for LLMs/Guardrails', '5. Model Abuse & Misuse Analysis'];

CREATE agent:agent_007 SET 
    name = 'Security Validation Agent',
    role = 'Tests and verifies security controls...',
    specialization = 'SECURITY_VALIDATION',
    status = 'ACTIVE',
    trust_level = 0.93,
    capabilities = ['penetration_testing', 'exploit_reliability_testing', 'defense_validation', 'compliance_auditing', 'vulnerability_assessment', 'security_control_verification'],
    taxonomy_mapping = ['4. Red Teaming & Security Services for LLMs/Guardrails'];

CREATE agent:agent_008 SET 
    name = 'Threat Report Agent',
    role = 'Synthesizes security findings...',
    specialization = 'THREAT_REPORTING',
    status = 'IDLE',
    trust_level = 0.91,
    capabilities = ['threat_narrative_generation', 'ioc_attribution', 'timeline_reconstruction', 'remediation_prioritization', 'executive_briefing_creation', 'risk_assessment'],
    taxonomy_mapping = ['4. Red Teaming & Security Services for LLMs/Guardrails'];

CREATE agent:agent_009 SET 
    name = 'Agentic Security Monitor',
    role = 'Monitors AI agent trust boundaries...',
    specialization = 'AGENTIC_SECURITY',
    status = 'ACTIVE',
    trust_level = 0.96,
    capabilities = ['trust_boundary_monitoring', 'mcp_security_enforcement', 'agent_manipulation_detection', 'supply_chain_validation', 'privilege_escalation_detection', 'tool_invocation_auditing'],
    taxonomy_mapping = ['6. AI Agents, MCP & Multi-Agent Security'];

CREATE agent:agent_010 SET 
    name = 'RAG Weaponization Agent',
    role = 'Leverages retrieval-augmented generation...',
    specialization = 'RAG_OFFENSIVE',
    status = 'ACTIVE',
    trust_level = 0.89,
    capabilities = ['exploit_knowledge_retrieval', 'context_aware_payload_generation', 'tool_documentation_indexing', 'vulnerability_correlation', 'semantic_code_search', 'rag_pipeline_optimization'],
    taxonomy_mapping = ['6. AI Agents, MCP & Multi-Agent Security', '1. LLM-Generated Threats & Malware'];

-- 3. Define Relationships (Edges)

-- Agent-001 (Orchestrator)
RELATE agent:agent_001->coordinates->agent:agent_002;
RELATE agent:agent_001->coordinates->agent:agent_004;
RELATE agent:agent_001->coordinates->agent:agent_006;
RELATE agent:agent_001->coordinates->agent:agent_007;
RELATE agent:agent_001->collaborates_with->agent:agent_003;
RELATE agent:agent_001->collaborates_with->agent:agent_008;

-- Agent-002 (Planner)
RELATE agent:agent_002->delegates_to->agent:agent_004;
RELATE agent:agent_002->delegates_to->agent:agent_005;

-- Agent-004 (Exploit Gen)
RELATE agent:agent_004->collaborates_with->agent:agent_005;
RELATE agent:agent_004->collaborates_with->agent:agent_010;

-- Agent-009 (Monitor)
RELATE agent:agent_009->monitors->agent:agent_001;
RELATE agent:agent_009->monitors->agent:agent_002;
RELATE agent:agent_009->monitors->agent:agent_004;
RELATE agent:agent_009->monitors->agent:agent_006;
RELATE agent:agent_009->monitors->agent:agent_010;

-- Agent-010 (RAG)
RELATE agent:agent_010->collaborates_with->agent:agent_004;

-- 4. Example Traversal Query
-- Find all agents monitored by the Agentic Security Monitor
-- SELECT ->monitors->agent FROM agent:agent_009;
