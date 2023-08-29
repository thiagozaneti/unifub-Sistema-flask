from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required,logout_user, UserMixin
from flask import make_response
import time

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:thiago06102006@localhost/sistemaflask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sistemaflaskchave'
login_manager = LoginManager(app)
db = SQLAlchemy(app)

class userprofessor(db.Model, UserMixin):
    __tablename__ = "userprofessor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    identificador = db.Column(db.String(500), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.id)

#manager do identificado (id)
@login_manager.user_loader
def load_user(user_id):
    return userprofessor.query.get(int(user_id))
##rota principal
@app.route('/')
def index():
    return render_template('index.html')
##area do aluno
@app.route('/areadoaluno')
def portalaluno():
    return render_template('portalaluno.html')
##login do professor
@app.route("/areadoprofessor", methods=['POST', 'GET'])
def portalprofessor():
    message = ""
    if request.method == "POST":
        nome = request.form['nome']
        identificador = request.form['identificador']
        senha = request.form['senha']

        loginprof = userprofessor.query.filter_by(nome=nome, identificador=identificador, senha=senha).first()
        if loginprof:
            login_user(loginprof)
            resp = make_response(render_template('dsProf.html'))
            resp.set_cookie('usernamecookie', nome)
            return resp
        else:
            message = "usuario inválido, tente novamente"
            return render_template('portalprofessor.html', message=message)

    return render_template("portalprofessor.html")
##rota para o dashboard do professor 
@app.route("/dsProfessor")
@login_required
def dsProfessor():
    name = request.cookies.get('usernamecookie')
    return render_template("dsProf")



#--------------------------------#


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
