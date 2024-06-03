from flask import Flask, request, render_template
from sistema_experto import SistemaRecomendaciones, RecomendacionPais
import json

app = Flask(__name__)

with open('landing\info_paises.json') as f:
   datos = json.load(f)

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/recomendar", methods=["POST"])
def recomendar():
   clima_deseado = request.form["clima"].lower()
   idioma_deseado = request.form["idioma"].lower()
   aspectos_deseados = request.form["aspectos"].lower().split(',')

   sistema = SistemaRecomendaciones(datos)
   sistema.reset()
   sistema.cargar_hechos()
   sistema.declare(RecomendacionPais(clima=clima_deseado, idioma=idioma_deseado, aspectos=aspectos_deseados))
   sistema.run()

   recomendaciones = sistema.priorizar_recomendaciones()
   detalles_recomendaciones = {pais: datos[pais] for pais in recomendaciones}
   #print(detalles_recomendaciones)
   return render_template('result.html', recomendaciones=detalles_recomendaciones)

if __name__ == '__main__':
   app.run(debug=True)