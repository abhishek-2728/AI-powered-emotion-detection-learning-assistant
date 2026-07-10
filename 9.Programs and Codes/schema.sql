-- schema.sql
-- Implements the Entity Relationship Diagram for the
-- Emotion Detection & Learning Support Engine.
--
-- Users (1) ----< Emotion_Records (N)
--
-- This schema is provided for the optional database-backed deployment path
-- (e.g. multi-user hosted version). The current reference implementation
-- (app.py) persists interactions to CSV per Epic 3/4 for simplicity; this
-- schema is the natural next step described in the Scalability & Future
-- Plan document (08_Project_Demonstration/).

CREATE TABLE IF NOT EXISTS Users (
    UserID       INTEGER PRIMARY KEY AUTOINCREMENT,
    Name         TEXT NOT NULL,
    Email        TEXT NOT NULL UNIQUE,
    Password     TEXT NOT NULL,          -- store a salted hash, never plaintext
    Role         TEXT NOT NULL DEFAULT 'student',  -- student | educator | admin
    Login_Count  INTEGER NOT NULL DEFAULT 0,
    Created_At   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Emotion_Records (
    RecordID           INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID             INTEGER NOT NULL,
    Email              TEXT NOT NULL,
    Field              TEXT NOT NULL,
    Input_Text         TEXT NOT NULL,
    Predicted_Emotion  TEXT NOT NULL,
    Secondary_Emotion  TEXT,
    Confidence_Score   REAL NOT NULL,
    Model_Used         TEXT NOT NULL,        -- BiLSTM | BERT | RuleBasedFallback
    AI_Response        TEXT,
    Response_Type      TEXT NOT NULL DEFAULT 'template',  -- gemini | template
    Emotion_Scores     TEXT,                  -- JSON-encoded {emotion: score, ...}
    Timestamp          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CSV_Logged         BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (UserID) REFERENCES Users (UserID) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_emotion_records_userid ON Emotion_Records (UserID);
CREATE INDEX IF NOT EXISTS idx_emotion_records_emotion ON Emotion_Records (Predicted_Emotion);
CREATE INDEX IF NOT EXISTS idx_emotion_records_timestamp ON Emotion_Records (Timestamp);
