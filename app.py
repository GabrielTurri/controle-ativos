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

@app.route('/cadastro-manutencao', methods=["GET","POST"])
def cadastroManutencao():
    return render_template('cadastro-manutencao.html', ativos=ATIVOS)

@app.route('/cadastro-modelo', methods=["GET","POST"])
def cadastroModelo():
    return render_template('cadastro-modelo.html')

@app.route('/cadastro-grupo', methods=["GET","POST"])
def cadastroGrupo():
    return render_template('cadastro-grupo.html')

@app.route('/cadastro-licenca', methods=["GET","POST"])
def cadastroLicenca():
    return render_template('cadastro-licenca.html', ativos=ATIVOS)

@app.route('/ativos')
def ativos():
    return render_template('ativos.html', ativos=ATIVOS)


if __name__ == "__main__":
    app.run(debug=True)