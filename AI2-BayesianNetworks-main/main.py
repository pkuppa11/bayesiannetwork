# Pranav Kuppa 2.13.2023
# Kim AI2, Period 7

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from Networks import *
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['INFO'] = 'static/struct'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        if allowed_file(file.filename):
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
            model = predict("AI2-BayesianNetworks-main/static/files/" + file.filename)
            req = request.form["text"]
            if req == "":
                A = model.get_probability({"B":False})                                   # Odds of Burglary = False
                B = model.get_given_probability(("A", False), {"B":True, "E":False})    # Odds of Alarm = False, given Burglary = True & Earthquake = True
                C = model.get_given_probability(("B", True), {"J":True, "M":True})      # Odds of Burglary = True, given JohnCalls = True & MaryCalls = True
                scores = {"P(~B):" : A, "P(~A|B,~E):" : B, "P(B|J,M):" : C}
                return render_template('results.html', results=scores)
            else:
                scores = {}
                if "|" not in req:
                    req_list = req.split(",")
                    rs = {}
                    for r in req_list:
                        rs[r[-1]] = ("~" not in r)
                    scores["P("+req+")"] = model.get_probability(rs)
                else:
                    req_list = req.split("|")
                    given_list = req_list[1].split(",")
                    gs = {}
                    for r in given_list:
                        gs[r[-1]] = ("~" not in r)
                    scores["P("+req+")"] = model.get_given_probability((req_list[0], ("~" not in r)), gs)
                return render_template('results.html', results=scores)
    return render_template('index.html', form=form)

ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    # xxx.png
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def predict(file):
        is_disc=False
        is_cond=False
        discretes = []
        conditionals = []
        lat_cond = []

        df = pd.read_csv(file, header=None)
        #print(df.head)
        for index, row in df.iterrows():
            if(row[0].strip() == "Discrete"):
                is_disc = True
            elif(row[0].strip() == "Conditional"):
                is_cond = True
                is_disc = False
            else:
                if is_disc:
                    discretes.append((row[0], {True:float(row[1]), False:float(row[2])}))
                if is_cond:
                    if isfloat(row[1]):
                        lat_cond[-1].append((tuple([row[0][i]=="T" for i in range(len(row[0]))]), float(row[1])))
                    else:
                        if len(lat_cond) != 0:
                            conditionals.append([i for i in lat_cond])
                            lat_cond = []
                        lat_cond.append(row[0])
                        lat_cond.append(row[1].split(","))
                        lat_cond.append([])
        if len(lat_cond) != 0:
            conditionals.append(tuple(lat_cond))
            lat_cond = []
        #print(conditionals)

        model = BayesianTree()
        for disc in discretes:
            model.set_discretes(disc)     
        for cond in conditionals:
            model.set_conditionals((cond[0], (cond[2], cond[1])))
        
        return model
                         
                  
            

        
        #data = {'prediction': prediction.item(), 'class_name': str(prediction.item())}
        #return jsonify(data)
    #except:
        #return jsonify({'error': 'error during prediction'})

#predict("AI2-BayesianNetworks-main/csv_test.csv")

if __name__ == '__main__':
    app.run(debug=True)