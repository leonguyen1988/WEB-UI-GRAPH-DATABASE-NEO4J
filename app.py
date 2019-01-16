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

@app.route("/subGraphOfLabel",methods=['POST'])
def getRelation():
    label = request.form["data"]
    label =json.loads(label)
    Movie_Query =' MATCH (n:'+label+') Return n.name as name,n.descr as description limit 10; '   
    Relation_data=graph.run(Movie_Query).data()
    return json.dumps(Relation_data)


@app.route("/personPerMovie", methods=['POST'])
def getNodes():
    try:
        data = request.form["data"]
        nodes = request.form["nodes"]
        links = request.form["links"]
    except:
        return json.dumps('There is error for requesting data')
    Relation_Query = """
                        MATCH (n:Person)-[:ACTED_IN]->(m:Movie) WHERE m.title = """+data+"""
                            RETURN n.name as name ,n.born as born; 
                    """
    Relation_data = graph.run(Relation_Query).data()
    return json.dumps(Relation_data)

# Convert data from Neo4j to Json type for using AlchemyJS library
# Note: Before run quey in app, should run the query in neo4j browser to check the valideate
# The Neo4j database name must be exact uppercase and lowercase character
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