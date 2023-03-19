from flask import Flask, render_template, request, session, json
from flask_session import Session

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
    return render_template('main.html')


@app.route('/add_to_list', methods = ['POST', 'GET'])
def add_to_list():
   if request.method == 'POST':
    formitem = request.form
    print('got from form: ', formitem)
    
    
    if (formitem['playerName'] == '1'):
        session.clear()
        session.update({
            'teamWin' : {},
            'teamLose' : {}
        })
    
    else:
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
    print(s)
    win_ratings = []
    lose_ratings = []
    for member in s['teamWin']: #TODO this is bad, fix
        print(member) #this only gives the key
        win_ratings.append(Rating(mu=float(member['mu']), sigma=float(member['sigma'])))
    for member in s['teamLose']:
        
        
        lose_ratings.append(Rating(mu=float(member['mu']), sigma=float(member['sigma'])))

    print(win_ratings, lose_ratings)
    rated = rate([tuple(win_ratings), tuple(lose_ratings)])
    print(rated)

    i = 0
    for member in s['teamWin']:
        
        member['mu'] = rated[0][i].mu
        member['sigma'] = rated[0][i].sigma
        i+=1
    i = 0
    for member in s['teamLose']:
        key = list(member.keys())[0]
        member[key]['mu'] = rated[1][i].mu
        member[key]['sigma'] = rated[1][i].sigma
        i+=1

    return render_template('main.html')

@app.route('/remove', methods = ['POST'])
def remove():
    s = dict(session.items())
    print(request.form)
    #form = dict(request.form)['playerName'].split('\'')[1] #unholy, find a better solution
    
    s['teamWin'].pop(request.form['playerName'], '') 
    s['teamLose'].pop(request.form['playerName'], '')
    
   
    print(s)
    return render_template('main.html')

if __name__ == '__main__':
    app.run()


"""
new data structure todo
session:
{
    "teams" : {
        "teamWin" : {
            "playerName" : 
                {
                "sigma" : "",
                "mu" : "",
                "experience" : "",
                "isInSquad" : "",
                etc.
            },

        }

        "teamLose" : []
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