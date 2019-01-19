from flask import Flask, render_template,json,request,redirect,url_for
from py2neo import Graph,Node,Relationship,NodeMatcher
from flask_restful import Resource,Api  
import json


app = Flask(__name__)

api = Api(app)


#
#  This is connection tool to connect neo4j database
# 

graph = Graph(auth=("neo4j","banbethin1"))

#
# Running index file
# #

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    raw_data= CovertToJson()
    for data in raw_data:
        data['name'] = data['name'][0]
    return render_template('index.html',data = raw_data)

#
# #

@app.route("/raw_data",methods=["POST"])
def raw_data():
    json_data = CovertToJson()
    return json.dumps({"nodes":json_data})

@app.route("/subLayerOfRootConcept",methods=['POST'])
def getRelation():
    label = request.form["data"]
    label =json.loads(label)
    Movie_Query =' MATCH (n:'+label+') Return n.name as name,n.descr as description limit 20; '   
    Relation_data=graph.run(Movie_Query).data()
    return json.dumps(Relation_data)


@app.route("/sublayersOfLayer", methods=['POST'])
def getNodes():
    links = []
    nodes = {'name':[]}
    layer = {}

    try:
        RequestedNode = json.loads(request.form["data"])
        # nodes = request.form["nodes"]
        # links = request.form["links"]
    except:
        return json.dumps('There is error for requesting data')
    try:
        RelationDataIsSourceLine1 = """ 
                MATCH (n)-[r]->(m) WHERE n.name = '{0}'
                    RETURN n.name as source,m.name as target limit 10
                UNION 
                MATCH (n)<-[r]-(m) WHERE n.name = '{0}' 
                    RETURN m.name as source,n.name as target limit 10;
        """.format(RequestedNode) 

        Relation_data = graph.run(RelationDataIsSourceLine1).data()
    
    except:
        return print("Error")
    for data in Relation_data:
        link={}
        found = False
        if((data['source'] in nodes['name']) == False):
            nodes['name'].append(data['source'])
        if((data['target']  in nodes['name']) == False):
            nodes['name'].append(data['target'])
        link['source'] = data['source']
        link['target'] = data['target']
        if(link['source'] != RequestedNode):
            for singleData in links:
                if(link['source'] == singleData['target']):
                    found = True
                    break
        else:
            if(link['source'] == RequestedNode and link['target'] == RequestedNode):
                found = True
        if(found == False):
            links.append(link)
    layer['nodes'] = nodes
    layer['links'] = links
    return json.dumps(layer)

# Convert data from Neo4j to Json type for using AlchemyJS library
# Note: Before run quey in app, should run the query in neo4j browser to check the valideate
# The Neo4j database data name must be exact uppercase and lowercase character
# #
def CovertToJson():
    """
      Get All Labels
    """
    json_data = graph.run(""" 
                            MATCH (nodes) 
                                RETURN distinct labels(nodes) as name;
                            """).data()
    return json_data


if __name__ == "__main__":
    app.run(port = 5002)