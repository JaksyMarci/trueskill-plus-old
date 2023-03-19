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
 


app = Flask(__name__)
app.secret_key = 'any random string'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    
    session.update({
       'teamWin' : [],
       'teamLose' : []
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
            'teamWin' : [],
            'teamLose' : []
        })
    
    else:
        s=dict(session.items())
        team = formitem['team']
        playerName = formitem['playerName']
        s[team].append({playerName : {'mu' : '', 'sigma' : ''}})
        
        
        s[team][-1][playerName]['mu'] = formitem['mu']
        s[team][-1][playerName]['sigma'] = formitem['sigma']

        print(s)

   return render_template('main.html')

@app.route('/manage', methods = [])
def manage():
    return render_template('manage.html')

@app.route('/calculate', methods = ['POST'])
def calculate():
    s = dict(session.items())
    

    return render_template('main.html')

if __name__ == '__main__':
    app.run()


"""
session:
{
    "teams" : {
        "teamWin" : [],
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