from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]

    print(nome)
    print(email)
    print(senha)

    return "Cadastro realizado!"


app.run(debug=True)