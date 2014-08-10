from itertools import combinations
from collections import defaultdict
import operator
import json
from subeng.datakit import *


# @param dataA, dataB, dataJoin, a list of dictionaries
# @param attrA, attrB, strings
# @return connect, a dictionary of tuples
def countConnectivity(dataA, attrA, dataB = None, attrB=None, dataJoin=None):
    connect= defaultdict(lambda:0)
    
    if dataB==None:
        # connectivity within the same type of attributes
        for record in dataA:
            groupA = record[attrA].split("#")
            groupA  = [item for item in groupA if item]
            pairs = list(combinations(groupA, 2))
            for p in pairs:
                if (p[1],p[0]) in connect:
                    connect[(p[1],p[0])]+=1
                else:
                    connect[p] += 1
                    
    else:
        # connectivity between two types of attributes
        for k in dataJoin[0].keys():
            if k in dataA[0].keys():
                keyA = k
            # try to align key names for dataset, ideally should be like commented 
            ##elif k in dataB[0].keys():
            ##    keyB = k
            else:
                for kk in dataB[0].keys():
                    if kk.find(k)!=-1:
                        keyB, keyb = kk, k
        
        dataAGrouped, dataBGrouped = group(dataA, by(keyA)), group(dataB, by(keyB))
    
        for record in dataJoin:
            # int function is tailored for dataset, ideally should be same data type
            # if dataA.has_key(int(record[keyA]kcs = load_data('kcs/')
            if dataAGrouped.has_key(int(record[keyA])) and dataBGrouped.has_key(record[keyb]):
                groupA, groupB = [], []
                for x in dataAGrouped[int(record[keyA])]:
                    groupA+=x[attrA].split('#')
                groupA = [a for a in groupA if a!='']
                    
                for y in dataBGrouped[record[keyb]]:
                    groupB += y[attrB].split('#')
                groupB = [b for b in groupB if b!='']
               
                pairs = [ (a, b) for a in groupA for b in groupB]
                for p in pairs:
                    if (p[1],p[0]) in connect:
                        connect[(p[1],p[0])]+=1
                    else:
                        connect[(p[0],p[1])] += 1
                    
    return connect

# @param datadict, a dictionary of tuples
# @param threshold, an integer
# @return top, a list 
def topConnectivity(datadict, threshold):
    sorted_x = sorted(datadict.iteritems(), key=operator.itemgetter(1))
    top = [x for x in sorted_x if x[1]>threshold]
    
    return top
        

            
class constructGraph:
    # @param networkList, a list of lists/tuples 
    # @param graphType, a string
    def __init__(self, graphList, graphType='network'):
        self.graphType = graphType
        self.nodesA = defaultdict(lambda:0)
        self.nodesB = defaultdict(lambda:0)
        self.links = defaultdict(lambda:0)
        for item in graphList:
            self.nodesA[item[0][0]] += item[1]
            self.nodesB[item[0][1]] += item[1]
            self.links[item[0]] = item[1]
    
    # @return jsonObj, a dict of json objects      
    def convertToJson(self):
        if self.graphType=='network':
            nodes = dict(self.nodesA.items()+self.nodeB.items())
            n, l =[],[]
            idx,i = {},0
            for key in nodes:
                d={}
                d['name'], d['radius'], d['group'] = key, nodes[key], 1
                n.append(d)
                idx[key]=i
                i+=1
    
            for pair in self.links:
                d={}
                d['source'],d['target'] = idx[pair[0]], idx[pair[1]]
                d['value'] = self.links[pair]
                l.append(d)
            
            jsonObj = {}
            jsonObj['nodes'], jsonObj['links'] = n,l
            
        elif self.graphType=='adjacency':
            n, l =[],[]
            idx,i = {},0
            for key in self.nodesA:
                d={}
                d['name'], d['radius'], d['group'] = key, self.nodesA[key], 1
                n.append(d)
                idx[key]=i
                i+=1

            for key in self.nodesB:
                d={}
                d['name'], d['radius'], d['group'] = key, self.nodesB[key], 2
                n.append(d)
                idx[key]=i
                i+=1
            
            for link in self.links:
                d={}
                d['source'],d['target'] = idx[link[0]], idx[link[1]]
                d['value'] = self.links[link]
                l.append(d)
            
        else:
            print "unknown graph type"
            return
            
        jsonObj = {}
        jsonObj['nodes'], jsonObj['links'] = n,l
                    
        return jsonObj
        
