from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ajustes por marca y tipo de bicicleta
MARCAS_BICICLETAS = {
    'scott': {'ruta': 0.66, 'montaña': 0.60, 'híbrida': 0.64},
    'giant': {'ruta': 0.65, 'montaña': 0.59, 'híbrida': 0.63},
    'specialized': {'ruta': 0.67, 'montaña': 0.61, 'híbrida': 0.65},
    'trek': {'ruta': 0.64, 'montaña': 0.58, 'híbrida': 0.62},
    'cannondale': {'ruta': 0.66, 'montaña': 0.60, 'híbrida': 0.63},
    'merida': {'ruta': 0.65, 'montaña': 0.59, 'híbrida': 0.62},
    'bmc': {'ruta': 0.67, 'montaña': 0.61, 'híbrida': 0.64},
    'cube': {'ruta': 0.64, 'montaña': 0.58, 'híbrida': 0.62},
}


def calcular_talla_bicicleta(entrepierna_cm, tipo_bicicleta, marca):
    """
    Calcula la talla recomendada de bicicleta basada en tipo y marca.

    Args:
        entrepierna_cm (float): Longitud de la entrepierna en centímetros.
        tipo_bicicleta (str): Tipo de bicicleta ('ruta', 'montaña', 'híbrida').
        marca (str): Marca de bicicleta seleccionada.

    Returns:
        dict: Talla en centímetros, pulgadas y tamaño estándar (S, M, L, XL).
    """
    if marca in MARCAS_BICICLETAS and tipo_bicicleta in MARCAS_BICICLETAS[marca]:
        talla_cm = entrepierna_cm * MARCAS_BICICLETAS[marca][tipo_bicicleta]
    else:
        return {"error": "Tipo de bicicleta o marca no válidos"}

    talla_pulgadas = talla_cm / 2.54

    if talla_cm < 52:
        talla_estandar = 'S'
    elif 52 <= talla_cm < 56:
        talla_estandar = 'M'
    elif 56 <= talla_cm < 60:
        talla_estandar = 'L'
    else:
        talla_estandar = 'XL'

    return {
        "talla_cm": round(talla_cm, 2),
        "talla_pulgadas": round(talla_pulgadas, 2),
        "talla_estandar": talla_estandar
    }


@app.route('/')
def home():
    """Renderiza la página principal."""
    return render_template('index.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    """
    Recibe datos del formulario y calcula la talla de la bicicleta.
    """
    try:
        entrepierna = float(request.form['entrepierna'])
        tipo = request.form['tipo'].strip().lower()
        marca = request.form['marca'].strip().lower()

        resultado = calcular_talla_bicicleta(entrepierna, tipo, marca)

        if "error" in resultado:
            return jsonify({"error": resultado["error"]}), 400
        else:
            return jsonify(resultado)
    except ValueError:
        return jsonify({"error": "Datos inválidos. Asegúrate de ingresar números válidos."}), 400
    except KeyError as e:
        return jsonify({"error": f"Falta el campo requerido: {e}"}), 400


@app.route('/whatsapp')
def whatsapp():
    """
    Redirige a WhatsApp con un mensaje predefinido.
    """
    whatsapp_link = "https://wa.me/+573016208762?text=Hola,+vengo+desde+la+Calculadora+de+Tallas+En+Cicla"
    return jsonify({"message": "¡Únete a nuestro WhatsApp para más información!", "link": whatsapp_link})


if __name__ == "__main__":
    app.run(debug=True)



















   

