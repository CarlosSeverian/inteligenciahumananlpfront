from flask import Flask, request, jsonify, json, render_template
import requests
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder='html')

#inicialização do dataframe de seleção aleatória de filmes
df_movie = pd.read_csv('static/mostra.csv')

@app.route('/',  methods=['GET', 'POST'])
def index():
    indice = np.random.randint(df_movie.shape[0])
    filme = df_movie['movie'].iloc[indice]
    texto_usuario, Predicao = "", ""
    
    # Acorda o back end
    server_caminho = 'https://inteligenciahumananlpback.herokuapp.com'
    retorno = requests.get( server_caminho )
    if retorno.status_code != requests.codes.ok :
         return "<br><br><p><H3><CENTER>ERRO!!! - Back End inoperante. Tente mais tarde</CENTER></H3></p>"
   
    return render_template('index.html', Indice = str(indice), Filme = filme, Textodigitado = texto_usuario, Predicao=Predicao)
    
@app.route('/new/',  methods=['GET', 'POST'])
def new():
    indice = np.random.randint(df_movie.shape[0])
    filme = df_movie['movie'].iloc[indice]
    texto_usuario, Predicao = "", ""
    return render_template('index.html', Indice = str(indice), Filme = filme, Textodigitado = texto_usuario, Predicao=Predicao)


@app.route("/sendbackend/",  methods=['GET', 'POST'])
# Recebe como parametro uma lista de palavras
def sendbackend():
    # Recebo a digitação do formulário html
    texto_usuario = request.form['comentario']
    indice = request.form['Indice']
    filme = request.form['Filme'] 
     
    # envio a mensagem ao backend em json e recebo o retorno, também em json
    server_caminho = 'https://inteligenciahumananlpback.herokuapp.com/predict/'
    headers = {'Content-Type': 'application/json'}
    dados = {'avaliacao': texto_usuario}
    retorno = requests.post( server_caminho, headers=headers, data=json.dumps(dados) )
    Predicao = retorno.json()
    Predicao = Predicao['avaliacao']
    
    # Volto para a página html com o resultado
    return render_template('index.html', Indice = str(indice), Filme = filme, Textodigitado = texto_usuario, Predicao=Predicao)

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html')
    
    
if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0', debug=False)
    
    