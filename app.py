from flask import Flask, render_template,json,request
from py2neo import Graph,Node,Relationship,NodeMatcher
import json


app=Flask(__name__)

#
#  This is connection tool to connect neo4j database
# 

graph = Graph(auth=("neo4j","banbethin1"))

#
# Running index file
# #

@app.route("/")
def index():
    raw_data= CovertToJson()
    return render_template('index.html',data=raw_data)

#
# #

@app.route("/raw_data",methods=["POST"])
def raw_data():
    json_data = CovertToJson()
    return json.dumps({"nodes":json_data})

@app.route("/movieNodes",methods=['POST'])
def getRelation():
    data = request.form["data"]
    Movie_Query ="""MATCH (person:Person)-[:ACTED_IN]->(movies:Movie) WHERE person.name = """+data+"""
     RETURN movies.title as name;"""   
    Relation_data=graph.run(Movie_Query).data()
    return json.dumps(Relation_data)


@app.route("/personPerMovie", methods=['POST'])
def getNodes():
    try:
        data = request.form["data"]
    except:
        return json.dumps('There is error for requesting data')
    try :
    
    Relation_Query = """
                        MATCH (n:Person)-[:ACTED_IN]->(m:Movie) WHERE m.title = """+data+"""
                            RETURN n,m; 
                    """
    Relation_data = graph.run(Relation_Query).data()
    print(Relation_data)
    return json.dumps(Relation_data)

# Convert data from Neo4j to Json type for using AlchemyJS library
# Note: Before run quey in app, should run the query in neo4j browser to check the valideate
# The Neo4j database name must be exact uppercase and lowercase character
# #
def CovertToJson():
    """
      CREATE DUMP DATA
    """
    json_data = graph.run(""" 
                            MATCH (nodes:Person) 
                                RETURN nodes.name as name, nodes.born as born limit 10
                            """).data()
    return json_data


if __name__ == "__main__":
    app.run()