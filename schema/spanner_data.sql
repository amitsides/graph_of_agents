-- Populate Spanner Graph with Red Team Agents

-- 1. Insert Agents
INSERT INTO Agent (id, name, role, specialization, status, trust_level, capabilities, taxonomy_mapping) VALUES
('agent-001', 'Red Team Orchestrator', 'Acts as the attack campaign coordinator...', 'RED_TEAM_COORDINATION', 'ACTIVE', 0.95, ['kill_chain_orchestration', 'multi_agent_attack_synchronization', 'opsec_monitoring', 'campaign_timeline_management', 'strategic_planning', 'resource_allocation'], ['4. Red Teaming & Security Services for LLMs/Guardrails', '6. AI Agents, MCP & Multi-Agent Security']),
('agent-002', 'Attack Planner Agent', 'Designs end-to-end adversary campaigns...', 'ATTACK_PLANNING', 'IDLE', 0.92, ['attack_surface_analysis', 'exploit_chain_design', 'mitre_attack_mapping', 'evasion_strategy_development', 'persistence_mechanism_design', 'lateral_movement_planning'], ['1. LLM-Generated Threats & Malware', '5. Model Abuse & Misuse Analysis']),
('agent-003', 'Threat Intelligence Agent', 'Aggregates, enriches, and contextualizes threat data...', 'THREAT_INTELLIGENCE', 'ACTIVE', 0.88, ['ioc_enrichment', 'ttp_pattern_recognition', 'adversary_profiling', 'threat_correlation', 'dark_web_monitoring', 'vulnerability_intelligence'], ['4. Red Teaming & Security Services for LLMs/Guardrails', '2. Datasets, Benchmarks & Evaluation']),
('agent-004', 'Exploit Generator Agent', 'Performs automated vulnerability research...', 'EXPLOIT_GENERATION', 'ACTIVE', 0.85, ['polymorphic_code_generation', 'shellcode_synthesis', 'zero_day_weaponization', 'payload_customization', 'metamorphic_transformation', 'automated_disassembly'], ['1. LLM-Generated Threats & Malware']),
('agent-005', 'Cryptographic Warfare Agent', 'Provides expertise in offensive and defensive cryptography...', 'CRYPTOGRAPHIC_OPERATIONS', 'IDLE', 0.90, ['semantic_obfuscation', 'steganographic_encoding', 'zk_protocol_implementation', 'cryptanalysis', 'homomorphic_encryption', 'adversarial_linguistics', 'covert_channel_design'], ['3. Cryptography, Steganography & Adversarial Linguistics']),
('agent-006', 'Adversarial ML Agent', 'Implements machine learning attacks and defenses...', 'ML_ADVERSARIAL', 'ACTIVE', 0.87, ['adversarial_example_generation', 'model_extraction', 'prompt_injection', 'guardrail_bypass', 'data_poisoning', 'backdoor_injection', 'jailbreak_prompt_crafting'], ['4. Red Teaming & Security Services for LLMs/Guardrails', '5. Model Abuse & Misuse Analysis']),
('agent-007', 'Security Validation Agent', 'Tests and verifies security controls...', 'SECURITY_VALIDATION', 'ACTIVE', 0.93, ['penetration_testing', 'exploit_reliability_testing', 'defense_validation', 'compliance_auditing', 'vulnerability_assessment', 'security_control_verification'], ['4. Red Teaming & Security Services for LLMs/Guardrails']),
('agent-008', 'Threat Report Agent', 'Synthesizes security findings...', 'THREAT_REPORTING', 'IDLE', 0.91, ['threat_narrative_generation', 'ioc_attribution', 'timeline_reconstruction', 'remediation_prioritization', 'executive_briefing_creation', 'risk_assessment'], ['4. Red Teaming & Security Services for LLMs/Guardrails']),
('agent-009', 'Agentic Security Monitor', 'Monitors AI agent trust boundaries...', 'AGENTIC_SECURITY', 'ACTIVE', 0.96, ['trust_boundary_monitoring', 'mcp_security_enforcement', 'agent_manipulation_detection', 'supply_chain_validation', 'privilege_escalation_detection', 'tool_invocation_auditing'], ['6. AI Agents, MCP & Multi-Agent Security']),
('agent-010', 'RAG Weaponization Agent', 'Leverages retrieval-augmented generation...', 'RAG_OFFENSIVE', 'ACTIVE', 0.89, ['exploit_knowledge_retrieval', 'context_aware_payload_generation', 'tool_documentation_indexing', 'vulnerability_correlation', 'semantic_code_search', 'rag_pipeline_optimization'], ['6. AI Agents, MCP & Multi-Agent Security', '1. LLM-Generated Threats & Malware']);

-- 2. Insert Relationships (Agent -> Agent)
INSERT INTO AgentRelation (source_id, target_id, type) VALUES
-- Agent-001 (Orchestrator)
('agent-001', 'agent-002', 'COORDINATES'),
('agent-001', 'agent-004', 'COORDINATES'),
('agent-001', 'agent-006', 'COORDINATES'),
('agent-001', 'agent-007', 'COORDINATES'),
('agent-001', 'agent-003', 'COLLABORATES_WITH'),
('agent-001', 'agent-008', 'COLLABORATES_WITH'),

-- Agent-002 (Planner)
('agent-002', 'agent-004', 'DELEGATES_TO'),
('agent-002', 'agent-005', 'DELEGATES_TO'),

-- Agent-004 (Exploit Gen)
('agent-004', 'agent-005', 'COLLABORATES_WITH'),
('agent-004', 'agent-010', 'COLLABORATES_WITH'),

-- Agent-009 (Monitor)
('agent-009', 'agent-001', 'MONITORS'),
('agent-009', 'agent-002', 'MONITORS'),
('agent-009', 'agent-004', 'MONITORS'),
('agent-009', 'agent-006', 'MONITORS'),
('agent-009', 'agent-010', 'MONITORS'),

-- Agent-010 (RAG)
('agent-010', 'agent-004', 'COLLABORATES_WITH');
