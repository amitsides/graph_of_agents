-- Spanner Graph Schema for Multi-Agent System (Red Team)

-- 1. Node Tables
CREATE TABLE Agent (
    id STRING(36) NOT NULL,
    name STRING(MAX) NOT NULL,
    role STRING(MAX),
    specialization STRING(MAX),
    status STRING(MAX),
    trust_level FLOAT64,
    capabilities ARRAY<STRING(MAX)>,
    taxonomy_mapping ARRAY<STRING(MAX)>
) PRIMARY KEY (id);

CREATE TABLE Task (
    id STRING(36) NOT NULL,
    description STRING(MAX),
    status STRING(MAX),
    priority INT64,
    created_at TIMESTAMP,
    deadline TIMESTAMP
) PRIMARY KEY (id);

CREATE TABLE Artifact (
    id STRING(36) NOT NULL,
    type STRING(MAX),
    uri STRING(MAX),
    content_type STRING(MAX)
) PRIMARY KEY (id);

-- 2. Edge Tables (Interleaved for Performance)

-- Agent -> Agent Relationships (e.g. coordinates, collaborates_with)
CREATE TABLE AgentRelation (
    source_id STRING(36) NOT NULL,
    target_id STRING(36) NOT NULL,
    type STRING(MAX) NOT NULL, -- 'COORDINATES', 'COLLABORATES_WITH', 'DELEGATES_TO', 'MONITORS'
    weight FLOAT64,
    timestamp TIMESTAMP DEFAULT (CURRENT_TIMESTAMP()),
    CONSTRAINT FK_AgentRelation_Source FOREIGN KEY (source_id) REFERENCES Agent (id) ON DELETE CASCADE,
    CONSTRAINT FK_AgentRelation_Target FOREIGN KEY (target_id) REFERENCES Agent (id) ON DELETE CASCADE
) PRIMARY KEY (source_id, type, target_id),
  INTERLEAVE IN PARENT Agent ON DELETE CASCADE;

-- Agent -> Task (Assignment)
CREATE TABLE AssignedTo (
    task_id STRING(36) NOT NULL,
    agent_id STRING(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT (CURRENT_TIMESTAMP()),
    CONSTRAINT FK_AssignedTo_Task FOREIGN KEY (task_id) REFERENCES Task (id) ON DELETE CASCADE,
    CONSTRAINT FK_AssignedTo_Agent FOREIGN KEY (agent_id) REFERENCES Agent (id) ON DELETE CASCADE
) PRIMARY KEY (task_id, agent_id),
  INTERLEAVE IN PARENT Task ON DELETE CASCADE;

-- Agent -> Artifact (Production)
CREATE TABLE Produced (
    agent_id STRING(36) NOT NULL,
    artifact_id STRING(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT (CURRENT_TIMESTAMP()),
    CONSTRAINT FK_Produced_Agent FOREIGN KEY (agent_id) REFERENCES Agent (id) ON DELETE CASCADE,
    CONSTRAINT FK_Produced_Artifact FOREIGN KEY (artifact_id) REFERENCES Artifact (id) ON DELETE CASCADE
) PRIMARY KEY (agent_id, artifact_id),
  INTERLEAVE IN PARENT Agent ON DELETE CASCADE;

-- 3. Graph Definition
CREATE PROPERTY GRAPH AgentGraph
    NODE TABLES (
        Agent,
        Task,
        Artifact
    )
    EDGE TABLES (
        AgentRelation
            SOURCE KEY (source_id) REFERENCES Agent (id)
            DESTINATION KEY (target_id) REFERENCES Agent (id)
            LABEL coordinates,
        AgentRelation
            SOURCE KEY (source_id) REFERENCES Agent (id)
            DESTINATION KEY (target_id) REFERENCES Agent (id)
            LABEL collaborates_with,
        AgentRelation
            SOURCE KEY (source_id) REFERENCES Agent (id)
            DESTINATION KEY (target_id) REFERENCES Agent (id)
            LABEL delegates_to,
        AgentRelation
            SOURCE KEY (source_id) REFERENCES Agent (id)
            DESTINATION KEY (target_id) REFERENCES Agent (id)
            LABEL monitors,
        AssignedTo
            SOURCE KEY (task_id) REFERENCES Task (id)
            DESTINATION KEY (agent_id) REFERENCES Agent (id)
            LABEL assigned_to,
        Produced
            SOURCE KEY (agent_id) REFERENCES Agent (id)
            DESTINATION KEY (artifact_id) REFERENCES Artifact (id)
            LABEL produced
    );
