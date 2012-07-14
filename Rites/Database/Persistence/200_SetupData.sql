INSERT INTO graphs(graphName) VALUES('GraphName1');

INSERT INTO works(graphName, workName) VALUES('GraphName1', 'WorkName1_1');
INSERT INTO works(graphName, workName) VALUES('GraphName1', 'WorkName1_2');

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName1_2', 'WorkName1_1');

INSERT INTO graphs(graphName) VALUES('GraphName2');

INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_1');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_2');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_3');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_4');

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_2', 'WorkName2_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_3', 'WorkName2_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_4', 'WorkName2_1');

INSERT INTO graphs(graphName) VALUES('GraphName3');

INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_1');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_2');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_3');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_4');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_5');

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_2', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_3', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_4', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_2');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_3');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_4');

INSERT INTO graphs(graphName) VALUES('GraphName4');

INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_1');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_2');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_3');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_4');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_5');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_6');

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_2', 'WorkName4_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_3', 'WorkName4_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_4', 'WorkName4_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_5', 'WorkName4_2');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_5', 'WorkName4_3');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_5', 'WorkName4_4');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_6', 'WorkName4_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_6', 'WorkName4_2');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_6', 'WorkName4_3');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName4_6', 'WorkName4_4');
