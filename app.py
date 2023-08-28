from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required,logout_user, UserMixin

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

@login_manager.user_loader
def load_user(user_id):
    return userprofessor.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areadoaluno')
def portalaluno():
    return render_template('portalaluno.html')

@app.route("/areadoprofessor", methods=['POST', 'GET'])
def portalprofessor():
    if request.method == "POST":
        nome = request.form['nome']
        identificador = request.form['identificador']
        senha = request.form['senha']
        
        loginprof = userprofessor.query.filter_by(nome=nome, identificador=identificador, senha=senha).first()

        if loginprof:
            login_user(loginprof)
            return render_template('dsProf.html')
        else:
            message = ""
            return render_template('portalprofessor.html', message=message)

    return render_template("portalprofessor.html")

@app.route("/dsProfessor")
@login_required
def dsProfessor():
    return render_template('dsProf.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
