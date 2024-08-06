from flask import Flask, request, render_template
import pickle
import pandas as pd
from flask_cors import CORS, cross_origin
import json
import numpy as np
import time

app=Flask(__name__)
CORS(app)

@app.route("/results", methods=["POST","GET"])
def dumpResults():
    data = request.get_json()
    data = json.loads(data)
    # image = np.asarray(data["data"])
    
    print(data)
    res="Result dumped to csv"
    res={"data":res}
    return json.dumps(res)


app.run(debug=True)


#virtualenv venv
#.\\venv\Scripts\activate

#python server.py


# {
#     "Variant" : "OriginalGWO",
#     "CEC" : "F1_2017",
#     "dimensions": f"{10,20,30,40}",
#     "data": "1020.3124123"
# }