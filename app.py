from flask import Flask, render_template, request

app = Flask(__name__)

ATIVOS = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro-ativos', methods=["GET","POST"])
def cadastroAtivos():
    return render_template('cadastro-ativos.html')

@app.route('/cadastro', methods=["POST"])
def cadastro():
    patrimonio = request.form.get("patrimonio")
    modelo = request.form.get("modelo")
    ATIVOS[patrimonio] = modelo
    return render_template('cadastro.html')

@app.route('/ativos')
def ativos():
    return render_template('ativos.html', ativos=ATIVOS)


if __name__ == "__main__":
    app.run(debug=True)