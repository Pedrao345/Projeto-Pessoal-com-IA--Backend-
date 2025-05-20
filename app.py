from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai # Keep this import as is
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")

# --- CHANGE STARTS HERE ---
# Initialize the generative AI library
genai.configure(api_key=API_KEY)
# --- CHANGE ENDS HERE ---

def adivinhar_personagem(dicas):
    prompt = f"""
        Tente descobrir o personagem de Dragon Ball com as dicas que forem dadas: {dicas}.
        Em caso de dicas que sejam inapropriadas, por exemplo, de cunho sexual,
        nome do personagem, ignore-os, não gere o personagem e alerte o usuário sobre o uso responsável
        da ferramenta de adivinhação de personagem mantendo a mesma estrutura do JSON.
        O personagem pode ser de qualquer raça do universo de dragon ball, mas pode ser bem específico para adivinhar o personagem.
        Também pode ser de qualquer saga de dragon ball
        Retorne apenas as seguintes informações: o nome do personagem, idade oficial do personagem, episódio em que apareceu pela primeira vez, e o nível de poder oficial.
        Devolva no formato JSON se acordo com o modelo:
        personagem = {{
            "nome": "nome do personagem",
            "idade_oficial": "idade oficial"
            "primeira_aparicao": "episódio em que apareceu pela primeira vez",
            "dicas": [
                "dica 1",
                "dica 2",
                "dica 3"
            ],
            "nivel_de_poder": "nível de poder do personagem"
        }}
        """
    # --- CHANGE STARTS HERE ---
    # Now you can directly use genai.GenerativeModel
    model = genai.GenerativeModel("gemini-2.0-flash") # Using a more up-to-date model name
    response = model.generate_content(
        contents=prompt,
        generation_config={
            "response_mime_type": "application/json",
        }
    )
    # --- CHANGE ENDS HERE ---

    response = json.loads(response.text)
    return response

@app.route('/personagem', methods=['POST'])
def pesquisar_personagem():
    try:
        dados = request.get_json()

        if not dados or not isinstance(dados, dict):
            return jsonify({'error': 'Requisição JSON inválida. Esperava um dicionário.'}), 400

        dicas = dados.get('dicas', [])

        if not isinstance(dicas, list):
            return jsonify({'error': 'O campo "dicas" deve ser uma lista.'}), 400

        if len(dicas) < 3:
            return jsonify({'error': 'São necessários pelo menos 3 dicas.'}), 400

        response = adivinhar_personagem(dicas)

        return jsonify(response), 200

    except Exception as e:
        print(f"Um erro interno ocorreu na API: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)