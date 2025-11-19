-- Spanner DDL: create relational tables for agent-driven orchestration
-- Run this in your Spanner admin console or via gcloud/spanner client.

CREATE TABLE Agents (
  AgentId        STRING(64) NOT NULL,     -- primary agent id (matches graph node id)
  Name           STRING(256),
  Role           STRING(256),
  Instructions   STRING(MAX),
  AgentType      STRING(64),              -- 'LLM', 'Tool', 'Memory', etc.
  Metadata       JSON,                    -- free-form metadata
) PRIMARY KEY (AgentId);

CREATE TABLE AgentRelationships (
  ParentAgentId     STRING(64) NOT NULL,
  ChildAgentId      STRING(64) NOT NULL,
  RelationshipType  STRING(64),    -- e.g., SEQUENTIAL, PARALLEL, ITERATIVE_LOOP, ITERATIVE_EXIT
  ExecutionOrder    INT64,         -- ordering for sequential edges
  Properties        JSON,
) PRIMARY KEY (ParentAgentId, ChildAgentId);

CREATE TABLE Sessions (
  SessionId     STRING(36) NOT NULL,
  RootAgentId   STRING(64),
  Status        STRING(32),        -- CREATED, RUNNING, COMPLETED, FAILED
  CreatedAt     TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
  UpdatedAt     TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (SessionId);

CREATE TABLE Tasks (
  SessionId        STRING(36) NOT NULL,
  TaskId           STRING(36) NOT NULL,
  AssignedAgentId  STRING(64) NOT NULL,
  ParentTaskId     STRING(36),
  Status           STRING(32) NOT NULL, -- PENDING, IN_PROGRESS, COMPLETED, FAILED
  InputPayload     JSON,
  OutputResult     JSON,
  AttemptCount     INT64 DEFAULT 0,
  CreatedAt        TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
  UpdatedAt        TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (SessionId, TaskId);

CREATE TABLE SessionState (
  SessionId    STRING(36) NOT NULL,
  StateKey     STRING(256) NOT NULL,
  StateValue   JSON,
  UpdatedAt    TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (SessionId, StateKey);

-- Indexes for performance
CREATE INDEX TasksByAgent ON Tasks (AssignedAgentId, Status, CreatedAt);
CREATE INDEX RelationshipsByParent ON AgentRelationships (ParentAgentId, ExecutionOrder);
CREATE INDEX RelationshipsByChild ON AgentRelationships (ChildAgentId);
CREATE INDEX SessionsByStatus ON Sessions (Status);
