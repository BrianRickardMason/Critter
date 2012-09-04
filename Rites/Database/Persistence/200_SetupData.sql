INSERT INTO graphs(graphName) VALUES('GraphName1');

INSERT INTO graphDetails(graphName, softTimeout, hardTimeout) VALUES('GraphName1', 60, 300);

INSERT INTO works(graphName, workName) VALUES('GraphName1', 'WorkName1_1');
INSERT INTO works(graphName, workName) VALUES('GraphName1', 'WorkName1_2');

INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName1_1', 20, 60, 11);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName1_2', 20, 60, 12);

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName1_2', 'WorkName1_1');

INSERT INTO graphs(graphName) VALUES('GraphName2');

INSERT INTO graphDetails(graphName, softTimeout, hardTimeout) VALUES('GraphName2', 60, 300);

INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_1');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_2');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_3');
INSERT INTO works(graphName, workName) VALUES('GraphName2', 'WorkName2_4');

INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName2_1', 20, 60, 21);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName2_2', 20, 60, 22);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName2_3', 20, 60, 23);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName2_4', 20, 60, 24);

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_2', 'WorkName2_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_3', 'WorkName2_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName2_4', 'WorkName2_1');

INSERT INTO graphs(graphName) VALUES('GraphName3');

INSERT INTO graphDetails(graphName, softTimeout, hardTimeout) VALUES('GraphName3', 60, 300);

INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_1');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_2');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_3');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_4');
INSERT INTO works(graphName, workName) VALUES('GraphName3', 'WorkName3_5');

INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName3_1', 20, 60, 31);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName3_2', 20, 60, 32);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName3_3', 20, 60, 33);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName3_4', 20, 60, 34);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName3_5', 20, 60, 35);

INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_2', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_3', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_4', 'WorkName3_1');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_2');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_3');
INSERT INTO workPredecessors(workName, predecessorWorkName) VALUES ('WorkName3_5', 'WorkName3_4');

INSERT INTO graphs(graphName) VALUES('GraphName4');

INSERT INTO graphDetails(graphName, softTimeout, hardTimeout) VALUES('GraphName4', 60, 300);

INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_1');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_2');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_3');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_4');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_5');
INSERT INTO works(graphName, workName) VALUES('GraphName4', 'WorkName4_6');

INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_1', 20, 60, 41);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_2', 20, 60, 42);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_3', 20, 60, 43);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_4', 20, 60, 44);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_5', 20, 60, 45);
INSERT INTO workDetails(workName, softTimeout, hardTimeout, dummy) VALUES('WorkName4_6', 20, 60, 46);

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
