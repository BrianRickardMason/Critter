DROP TABLE IF EXISTS elections CASCADE;
CREATE TABLE elections
(
    critthash CHAR(64) PRIMARY KEY NOT NULL CHECK(critthash <> ''),
    crittnick VARCHAR(88) NOT NULL CHECK (crittnick <> '')
);

DROP TABLE IF EXISTS graphs CASCADE;
CREATE TABLE graphs
(
    graphName VARCHAR(88) PRIMARY KEY NOT NULL CHECK(graphName <> '')
);

DROP TABLE IF EXISTS graphCycles CASCADE;
CREATE TABLE graphCycles
(
    graphName VARCHAR(88) REFERENCES graphs(graphName) ON DELETE CASCADE,
    cycleSeq  INTEGER NOT NULL CHECK(cycleSeq > 0),

    UNIQUE(graphName, cycleSeq)
);

DROP TABLE IF EXISTS graphDetails CASCADE;
CREATE TABLE graphDetails
(
    graphName VARCHAR(88) REFERENCES graphs(graphName) ON DELETE CASCADE,

    softTimeout INTEGER NOT NULL CHECK(softTimeout >= 0),
    hardTimeout INTEGER NOT NULL CHECK(hardTimeout >= softTimeout)
);

DROP TABLE IF EXISTS works CASCADE;
CREATE TABLE works
(
    graphName VARCHAR(88) REFERENCES graphs(graphName) ON DELETE CASCADE,
    workName  VARCHAR(88) PRIMARY KEY NOT NULL CHECK(workName <> '')
);

DROP TABLE IF EXISTS workCycles CASCADE;
CREATE TABLE workCycles
(
    workName VARCHAR(88) REFERENCES works(workName) ON DELETE CASCADE,
    cycle    INTEGER NOT NULL CHECK(cycle > 0),

    UNIQUE(workName, cycle)
);

DROP TABLE IF EXISTS workDetails CASCADE;
CREATE TABLE workDetails
(
    workName VARCHAR(88) REFERENCES works(workName) ON DELETE CASCADE,

    softTimeout INTEGER NOT NULL CHECK(softTimeout >= 0),
    hardTimeout INTEGER NOT NULL CHECK(hardTimeout >= softTimeout),
    dummy       INTEGER NOT NULL CHECK(dummy > 0)
);

DROP TABLE IF EXISTS workPredecessors CASCADE;
CREATE TABLE workPredecessors
(
    workName            VARCHAR(88) REFERENCES works(workName) ON DELETE CASCADE,
    predecessorWorkName VARCHAR(88) REFERENCES works(workName) ON DELETE CASCADE,

    UNIQUE(workName, predecessorWorkName),

    CHECK(workName <> predecessorWorkName)

    -- TODO: Check if both works have the same graphName.
);

GRANT ALL ON elections, graphs, graphCycles, graphDetails, works, workCycles, workDetails, workPredecessors TO crittuser;
