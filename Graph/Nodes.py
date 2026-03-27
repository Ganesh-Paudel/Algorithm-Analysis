import csv

class Node:
    def __init__(self, id, x, y):
        self.id = id;
        self.x = x;
        self.y = y;
        self.edges = []

    def addEdges(self):
        pass

    def getPosition(self):
        return self.x, self.y;

class Edges:

    def __init__(self, sourceId, targetId, weight, oneway = False):
        self.source = sourceId;
        self.target = targetId;
        self.weight = float(weight);
        self.oneway = oneway
        

import xml.etree.ElementTree as eT

class ExtractNodeAndEdges:

    def __init__(self, graphMLFile):
        self.graphMLFile = graphMLFile;
        self.tree = eT.parse(self.graphMLFile)
        self.root = self.tree.getroot();
        self.ns = {'g':'http://graphml.graphdrawing.org/xmlns'}
        self.nodeRepository = {}

    def getNodes(self):

        for node in self.root.findall('.//g:node',self.ns):
            nodeId = node.get('id');
            lat = node.find("./g:data[@key='d4']", self.ns).text
            lon = node.find("./g:data[@key='d5']", self.ns).text
            self.nodes_registry[n_id] = Node(nodeId, lon, lat)

    def getEdges(self):
        for edge in root.findall('.//g:edge', self.ns):
            u = edge.get('source')
            v = edge.get('target')

            weight = edge.find("./g:data[@key='d16']", self.ns).text
            oneway_val = edge.find("./g:data[@key='d14']", self.ns).text
            is_oneway = True if oneway_val == 'true' else False
            
            new_edge = Edge(u, v, weight, is_oneway)
            
            self.nodes_registry[u].edges.append(new_edge)

            if not is_oneway:
                self.nodes_registry[v].edges.append(Edge(v, u, weight, is_oneway))

    def saveToCSV(self):

        with open('data/nodes.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['node_id', 'x', 'y'])
            for node in self.root.findall('.//g:node', self.ns):
                n_id = node.get('id')
                y = node.find("./g:data[@key='d4']", self.ns).text
                x = node.find("./g:data[@key='d5']", self.ns).text
                writer.writerow([n_id, x, y])

        with open('data/edges.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['source', 'target', 'weight', 'oneway'])
            for edge in self.root.findall('.//g:edge', self.ns):
                u = edge.get('source')
                v = edge.get('target')
                weight = edge.find("./g:data[@key='d16']", self.ns).text
                oneway = edge.find("./g:data[@key='d14']", self.ns).text
                writer.writerow([u, v, weight, oneway])

