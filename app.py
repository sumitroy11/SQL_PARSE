
from flask import Flask, request, render_template
import re
from sql_metadata import Parser
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse',methods=['POST'])
def parse():
    '''
    For rendering results on HTML GUI
    '''
    sql = request.form.get("SQL")
    newquery = re.sub("- .+","",sql)
    newquery = re.sub("--.*","",newquery)
    newquery = re.sub("-"," ",newquery)
    newquery = newquery.replace("\r"," ")
    newquery = newquery.replace("\n"," ")
    newquery = newquery.replace("TEMPORARY TABLE","TABLE")
    newquery = newquery.upper()
    splitted = newquery.split(";")
    queries = []
    for query in splitted:
        query = query.strip()
        if re.search("(SELECT|FROM)",query):
            queries.append(query)
        else:
            pass
    table = []
    for query in queries:
        for tbl in Parser(query).tables:
            table.append(tbl)
    prd_table = []
    for tbl in table:
        if re.match("(^PRD|^WRK)",tbl):
            prd_table.append(tbl) 
    
    df = pd.DataFrame(prd_table)
    df.rename(columns = {0:'Table Name'}, inplace=True)
    return render_template('output.html', tables=[df.to_html(classes='data')], titles=df.columns.values)



if __name__ == "__main__":
    app.run(debug=True)
