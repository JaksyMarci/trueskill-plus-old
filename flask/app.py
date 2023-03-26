from flask import Flask, render_template, request, session, json
from flask_session import Session
import base64

from matplotlib.figure import Figure
from io import BytesIO
# import requi9red module
import sys

# append the path of the
# parent directory
import logging;
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
        'teams' : {
            'team1' : {},
            'team2' : {}
        }
        
    })
    print(session)
    """
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    """

    return render_template('main.html')


@app.route('/add_player', methods = ['POST', 'GET'])
def add_to_list():
    if request.method == 'POST':
        formitem = request.form
        print('got from form: ', formitem)




        s=dict(session['teams'].items())
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
    s = dict(session['teams'].items())
    print('CALCULATING: ' , s)
   
    ratings = []
    for teamName, teamMembers in s.items(): 
        playerRating = []
        
        for member, rating in teamMembers.items():
            
            playerRating.append(Rating(mu=float(rating['mu']), sigma=float(rating['sigma'])))
        

        ratings.append(playerRating)

    

    
    rated = rate(ratings)
    
    rated_flat = [item for sublist in rated for item in sublist] #flatten

    #dict items are ordered since python 3.6!

    i = 0
    for teams, teamMembers in s.items():
        for member, rating in teamMembers.items():

            rating['mu'] = rated_flat[i].mu
            rating['sigma'] = rated_flat[i].sigma
            i+=1
       
    
    return render_template('main.html')

@app.route('/remove_player', methods = ['POST'])
def remove():
    s = dict(session['teams'])
    
    print(s)
    #form = dict(request.form)['playerName'].split('\'')[1] #unholy, find a better solution
    
    for teams, teamMembers in s.items():
        teamMembers.pop(request.form['playerName'], '') 
    
    
   
    
    return render_template('main.html')

@app.route('/remove_team', methods = ['POST'])
def remove_team():
    
    session['teams'].pop(request.form['team'])
   
    print(session)
    


    return render_template('main.html')


@app.route('/add_team', methods = ['POST'])
def add_team():
    

    session['teams'][request.form['teamName']] = {}


    return render_template('main.html')


if __name__ == '__main__':
    app.run()



"""
new data structure:
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