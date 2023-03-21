from flask import Flask, render_template, request, session, json
from flask_session import Session
import base64

from matplotlib.figure import Figure
from io import BytesIO
# import requi9red module
import sys
 
# append the path of the
# parent directory
sys.path.append("..")
 
# import method from sibling
# module
from trueskill import Rating, rate
 
#TODO: Refactor with new data structure
#TODO: Finish swap, swapall and remove functions

app = Flask(__name__)
app.secret_key = 'any random string'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    
    session.update({
       'teamWin' : {},
       'teamLose' : {}
    })

    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template('main.html')


@app.route('/add_to_list', methods = ['POST', 'GET'])
def add_to_list():
   if request.method == 'POST':
    formitem = request.form
    print('got from form: ', formitem)
    
    
    

    s=dict(session.items())
    team = formitem['team']
    playerName = formitem['playerName']
    s[team][playerName] = {'mu' : '', 'sigma' : ''}
    
    
    s[team][playerName]['mu'] = formitem['mu']
    s[team][playerName]['sigma'] = formitem['sigma']

        

   return render_template('main.html')

@app.route('/manage', methods = [])
def manage():
    return render_template('manage.html')

@app.route('/calculate', methods = ['POST'])
def calculate():
    s = dict(session.items())
    print('CALCULATING: ' , s)
    win_ratings = []
    lose_ratings = []
    
    
    for keys, values in s['teamWin'].items(): 
        
        win_ratings.append(Rating(mu=float(values['mu']), sigma=float(values['sigma'])))

    for keys, values in s['teamLose'].items():
         
        lose_ratings.append(Rating(mu=float(values['mu']), sigma=float(values['sigma'])))

    print(win_ratings, lose_ratings)
    rated = rate([tuple(win_ratings), tuple(lose_ratings)])
    print(rated)

    i = 0
    for keys, values in s['teamWin'].items():
         
        values['mu'] = rated[0][i].mu
        values['sigma'] = rated[0][i].sigma
        i+=1
    i = 0
    for keys, values in s['teamLose'].items():
        
        
        values['mu'] = rated[1][i].mu
        values['sigma'] = rated[1][i].sigma
        i+=1

    return render_template('main.html')

@app.route('/remove', methods = ['POST'])
def remove():
    s = dict(session.items())
    
    #form = dict(request.form)['playerName'].split('\'')[1] #unholy, find a better solution
    
    s['teamWin'].pop(request.form['playerName'], '') 
    s['teamLose'].pop(request.form['playerName'], '')
    
   
    print(s)
    return render_template('main.html')

if __name__ == '__main__':
    app.run()

@app.route('/swap', methods = ['POST'])
def swap():
    s = dict(session.items())
    print(request.form['playerName'])
    
    return render_template('main.html')

"""
new data structure todo
session:
{
    "teams" : {
        "team1" : {
            "playerName" : 
                {
                "sigma" : "",
                "mu" : "",
                "experience" : "",
                "isInSquad" : "",
                etc.
            },

        },

        "team2" : {},
        etc.
    }

}
player:

"playerName" : {
    "sigma" : "",
    "mu" : "",
    "experience" : "",
    "isInSquad" : "",
    etc.
}

"""