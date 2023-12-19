from flask import Flask, make_response

app = Flask(__name__)

palabras = {"perreo": "Baile que se ejecuta generalmente a ritmo de reguetón, con eróticos movimientos de caderas, y en el que, cuando se baila por parejas, el hombre se coloca habitualmente detrás de la mujer con los cuerpos muy juntos",
            "parkour":"Actividad deportiva desarrollada al aire libre, principalmente en entornos urbanos, que consiste en ir salvando los obstáculos que se encuentran en el camino, como diferencias de altura, escaleras, bancos, etc., mediante saltos, volteretas u otros movimientos.",
            "banner":"Mensaje publicitario situado en un espacio concreto de una página web y formado por imágenes fijas o en movimiento",
            "biometano":"Gas compuesto mayoritariamente de metano, obtenido mediante un proceso de depuración del biogás.",
            "cookie":"Pequeño archivo de texto enviado por un sitio web y almacenado en el navegador del usuario, cuyas actividades y preferencias captura. U. menos c. m.",
            "escriturista": "Persona especializada en el conocimiento de los libros sagrados, o que profesa sus enseñanzas."}


@app.route('/')
def inicio():
    return ('<h2>Bienvenido al programa que te mostrará las nuevas palabras de la RAE</h2>'
            '<h3>Protocolos disponibles</h3>'
            '<ul><li><pre>/soap</pre></li>'
            '<li><pre>/rest</pre></li></ul>')


@app.route("/rest/palabras")
def main_palabras():
    return "<h2>Métodos disponibles</h2><ul><li><pre>/palabras/&lt;palabra&gt;</pre></li><li><pre>/palabras/listar</pre></li><li><pre>/palabras/comprobar/&lt;palabra&gt;</pre></li></ul>"


@app.route("/rest/palabras/<palabra>")
def mostrar_palabra(palabra):
    if check_palabra(palabra) == "true":
        return palabras.get(palabra)
    else:
        return "Palabra inexistente en base de datos"


@app.route("/rest/palabras/listar")
def listar_palabra():

    cadena = ""
    for palabra in palabras.keys():
        cadena += palabra
        cadena += "\n<br/>"

    return str(cadena)


@app.route("/rest/soap/palabras/comprobar/<palabra>")
def check_palabra(palabra):

    if palabra in palabras:
        return "true"
    else:
        return "false"


soap_start = ('<?xml version="1.0" encoding="utf-8"?>\n<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-'
              'instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"\nxmlns:soap="http://schemas.xmlsoap.org/soap/'
              'envelope/">\n  <soap:Body>\n    <Definicion xmlns="http://tempuri.org/">\n      <Palabra>')

soap_middle = '</Palabra>\n      <Acepcion>'
soap_end = '</Acepcion>\n    </Definicion>\n  </soap:Body>\n</soap:Envelope>'


@app.route("/soap/palabras/<palabra>")
def generate_soap_response(palabra):
    if check_palabra(palabra) == "true":
        return soap_start + palabra + soap_middle + palabras.get(palabra) + soap_end
    else:
        return "Palabra inexistente en base de datos"


def mostrar_palabra_soap(palabra):
    response = make_response((generate_soap_response(palabra)), 200)
    response.mimetype = "plain/text"
    return response


if __name__ == '__main__':
    app.run()
