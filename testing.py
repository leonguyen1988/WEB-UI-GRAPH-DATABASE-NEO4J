from py2neo import Graph,Node,Relationship,NodeMatcher
import json

graph = Graph(auth=("neo4j","banbethin1"))

links = []
nodes = {'name':[]}
layer = []
# try:
#     data = request.form["data"]
#     nodes = request.form["nodes"]
#     links = request.form["links"]
# except:
#     return json.dumps('There is error for requesting data')
name ='Java'
try:
    RelationDataIsSourceLine1 = """ 
            MATCH (n)-[r]->(m) WHERE n.name = '{0}'
                RETURN n.name as source,m.name as target 
            UNION 
            MATCH (n)<-[r]-(m) WHERE n.name = '{0}' 
                RETURN m.name as source,n.name as target ;
    """.format(name) 
    Relation_data = graph.run(RelationDataIsSourceLine1).data()
except:
    print("Error")
for data in Relation_data:
    link={}
    if((data['source'] in nodes['name']) == False):
        nodes['name'].append(data['source'])
    if((data['target']  in nodes['name']) == False):
        nodes['name'].append(data['target'])
    link['source'] = data['source']
    link['target'] = data['target']
    if( link['source'] == name):
        links.append(link)
    if( link['source'] != name):
        found = False
        for singleData in links:
            if(link['source'] == singleData['target']):
                found = True
        if(found == False):
            links.append(link)
layer =[nodes,links]
print(json.dumps(layer[1]))