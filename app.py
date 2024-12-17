from dotenv import load_dotenv
from PIL import Image
import pytesseract
import google.generativeai as genai
import json
import re
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import sqlite3

# Here I start the flesk application.
app = Flask(__name__)

# Loading the .env file
load_dotenv()


# It is crucial that the pytesseract path is indicated
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Upload rules
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS']= {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Pytesseract function to transcribe image
def extract_text(img_name):
    try:
        image = Image.open(img_name)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error on process a image: {e}"

# Gemini AI function for jsonfy image
def generate_json_ai(text):
    clean_response = ""

    try:
        genai.configure(api_key=os.getenv("TOKEN_API_GEMINI"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # This prompt is what defines the JSON AI's return.
        prompt = (
            f"Por favor, analise a foto do cardápio e extraia as informações de cada produto. "
            f"Para cada produto, forneça as seguintes informações em formato JSON: "
            f"- Título do produto "
            f"- Descrição do produto "
            f"- Preço do produto "
            f"Cada produto deve ser representado como um objeto com as chaves `title`, `description` e `price`. "
            f"O resultado final deve ser uma lista de objetos JSON, onde cada objeto representa um produto do cardápio. "
            f"Exemplo de formato desejado: "
            f"[ "
            f"{{ \"title\": \"Produto 1\", \"description\": \"Descrição do Produto 1\", \"price\": \"R$ 10,00\" }}, "
            f"{{ \"title\": \"Produto 2\", \"description\": \"Descrição do Produto 2\", \"price\": \"R$ 20,00\" }}, "
            f"{{ \"title\": \"Produto 3\", \"description\": \"Descrição do Produto 3\", \"price\": \"R$ 30,00\" }} "
            f"] "
            f"Certifique-se de que a descrição e o preço estejam claramente identificados e que o formato do preço seja consistente "
            f"(exemplo: R$ 10,00 ou 10,00). Eis o cardápio: {text}"
        )

        response = model.generate_content(prompt)
        clean_response = re.sub(r'```json|```', '', response.text).strip()
        data = json.loads(clean_response)
        return data
        
    except Exception as e:
         return {"error": f"Failed to generate JSON: {e}"}

    
# Route image upload by invoking the respective functions
@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)


        text = extract_text(filename)
        result = generate_json_ai(text)

        result_json = json.dumps(result)

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shop_res (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            json_data TEXT NOT NULL
            )
            ''')
        cursor.execute("INSERT INTO shop_res (json_data) VALUES (?)", (result_json,))
        conn.commit()
        conn.close()

        return redirect(url_for('results_page'))

    return jsonify({'error': 'Invalid file type'}), 400

# Menus page rendering route
@app.route("/results_page")
def results_page():
    return render_template("results.html")

# Menus data rendering route
@app.route("/results_data")
def results():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT json_data FROM shop_res")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()

    return jsonify(results=results)

# Delete all menus json on db
@app.route('/delete_all', methods=['POST'])
def delete_all():

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM shop_res")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao deletar itens: {e}")

    return redirect(url_for('index'))  

# Main route
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)