# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
import os
from dash import Dash, dcc, html

from flask_bootstrap import Bootstrap 

from unidecode import unidecode
from wtforms.validators import Length
from wtforms import TextAreaField

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField 
from wtforms.validators import DataRequired

from flask import render_template, request, session
from flask import Flask  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = False
dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/'
)

dash_app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
])

@app.route("/dash")
def my_dash_app():
    return dash_app.index()


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    text = TextAreaField('Quel est votre texte ?', validators=[Length(min=10)])
    file = FileField('File')
    submit = SubmitField('Submit')

@app.route('/wtf', methods=['GET', 'POST'])
def index():
    name = None
    text = None
    occurrence = None
    occurrence_file = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        text_to_analyze = unidecode(text.lower())
        occurrence = text_to_analyze.lower().count("paris")
        occurrence += text_to_analyze.lower().count("ville de lumiere")
        
        uploaded_file = form.file.data
        lines = uploaded_file.read()
        text_to_analyze =lines.lower().decode('utf-8')
        occurrence_file = text_to_analyze.lower().count("paris")
        occurrence_file += text_to_analyze.lower().count("ville de lumiere")

        
    return render_template('bootstrap.html', form=form, name=name, text=text, occurrence= occurrence, occurrence_file=occurrence_file)



@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    return "Hello !"

@app.route('/user/<name>')   # URL '/' to be handled by main() route handler
def bonjour(name):
    if(len(name) > 20):
        return "Je n'ai pas envie de te dire Bonjour, tu as un nom TROP long !", 413
    return 'Bonjour '+name+' !'

@app.route('/ia')   # URL '/' to be handled by main() route handler
def ia():
    return  render_template('user.html')

@app.route('/resultat',methods = ['POST'])
def resultat():
  result = request.form
  name = result['name']
  email = result['email']
  return render_template("resultat.html", name=name, email=email)



if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp