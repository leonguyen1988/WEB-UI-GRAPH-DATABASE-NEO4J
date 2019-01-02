from flask import Flask, render_template,json
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

@app.route("/raw_data")
def raw_data():
    json_data = CovertToJson()
    return json.dumps({"nodes":json_data})

# Convert data from Neo4j to Json type for using AlchemyJS library
# Note: Before run quey in app, should run the query in neo4j browser to check the valideate
# The Neo4j database name must be exact uppercase and lowercase character
# #
def CovertToJson():
    json_data = graph.run(" MATCH (nodes:Person) RETURN nodes.name as name, nodes.born as born limit 10").data()
    return json_data


if __name__ == "__main__":
    app.run()