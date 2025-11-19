-- Example inserts into relational tables to mirror graph nodes/edges (for relational queries)
INSERT INTO Agents (AgentId, Name, Role, Instructions, AgentType, Metadata) VALUES
('perception','Perception','sensor_agent','Ingest inputs and produce structured observations.','sensor', NULL),
('sensory_buffer','Sensory Buffer','memory','Immutable recent events window.','memory', NULL),
('working_memory','Working Memory','stm','Active reasoning slots and ToT root.','memory', NULL),
('ltm_index','LTM Index','memory','Semantic/procedural long-term store.','memory', NULL),
('reduction_engine','Reduction Engine','transform','Reduce problems into canonical subproblems.','service', NULL),
('planner','Planner','planner_agent','Generate hierarchical plans and ToT seeds.','LLM', NULL),
('tot_manager','ToT Manager','tree_of_thoughts','Expand/prune thought trees.','service', NULL),
('proposer_agents','Proposers','ensemble_agents','Neural + symbolic proposers.','ensemble', NULL),
('executor','Executor','executor_agent','Execute or simulate proposed actions.','simulator', NULL),
('verifier','Verifier','critic_agent','Formal and learned verification.','LLM', NULL),
('reflector','Reflector','analysis','Analyze results; produce training signals.','service', NULL),
('learner','Learner','learner_agent','Update models and heuristics.','service', NULL),
('archivist','Archivist','memory_manager','Store episodic and semantic traces.','service', NULL),
('meta_controller','Meta Controller','meta_agent','Adapt heuristics and allocate attention.','meta', NULL),
('arbiter','Arbiter','scheduler','Manage scheduling and resources.','service', NULL),
('monitor','Monitor','observability','Collect telemetry and metrics.','observability', NULL),
('root','Root','session_root','Root entry for sessions.','system', NULL);

-- Insert edges (AgentRelationships)
INSERT INTO AgentRelationships (ParentAgentId, ChildAgentId, RelationshipType, ExecutionOrder, Properties) VALUES
('root','perception','SEQUENTIAL',0,NULL),
('perception','sensory_buffer','SEQUENTIAL',1,NULL),
('sensory_buffer','working_memory','SEQUENTIAL',2,NULL),
('working_memory','reduction_engine','SEQUENTIAL',3,NULL),
('reduction_engine','planner','SEQUENTIAL',4,NULL),
('planner','tot_manager','PARALLEL',5,NULL),
('planner','proposer_agents','PARALLEL',5,NULL),
('tot_manager','proposer_agents','SEQUENTIAL',6,NULL),
('proposer_agents','executor','PARALLEL',7,NULL),
('executor','verifier','SEQUENTIAL',8,NULL),
('verifier','executor','ITERATIVE_LOOP',9,NULL),
('verifier','reflector','ITERATIVE_EXIT',10,NULL),
('reflector','learner','SEQUENTIAL',11,NULL),
('reflector','archivist','SEQUENTIAL',11,NULL),
('reflector','meta_controller','SEQUENTIAL',12,NULL),
('meta_controller','arbiter','SEQUENTIAL',13,NULL),
('monitor','meta_controller','SEQUENTIAL',14,NULL);
