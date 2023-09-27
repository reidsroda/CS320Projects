import pandas as pd
from flask import Flask, request, jsonify
import re

#project: p4
#submitter: rgsroda
#partner: pfife
#hours: 13

#main is a marvel movie dataset showing the descripitve statistics of the top marvel movies
app = Flask(__name__)
df = pd.read_csv("main.csv").to_html()
reload = 0
ta = 0 
tb = 0

donate_visits = 0
def count_donations():
    global donate_visits
    donate_visits +=1
    print("VISITER", donate_visits)
    
@app.route('/')
def home():
    global reload
    global ta
    global tb
    if reload < 10:
        if reload % 2 == 0:
            with open("index.html") as f:
                html = f.read()
        else:
            with open("indexB.html") as f:
                html = f.read()
    else:
        if ta > tb:
            with open("index.html") as f:
                html = f.read()
        
        else:
            with open("indexB.html") as f:
                html = f.read()
    reload += 1
    return html

@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()
        
    return html + df 

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"[^@\.]*@[^@\.]*\.[^@\.]", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + '\n') # 2
        with open("emails.txt", "r") as f: 
            num_subscribed = len(f.readlines())
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify(f"please stop being so careless, this is not a valid email address") # 3

@app.route('/donate.html')
def donate():
    with open("donate.html") as f:
        html = f.read()    
    return html 


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
    
    

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.