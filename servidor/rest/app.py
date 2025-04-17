from flask import Flask, request, jsonify
import json
from jsonschema import validate, ValidationError
from jsonpath_ng.ext import parse
from collections import OrderedDict
import os

app = Flask(__name__)

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "./dados/produtos.json"))
SCHEMA_FILE = "schema.json"

# Carregar esquema JSON
with open(SCHEMA_FILE) as f:
    schema = json.load(f)

# Utilitários
def carregar_produtos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)
    
# Ordena os campos ao guardar
def ordenar_produto(p):
    return OrderedDict([
        ("id", p["id"]),
        ("nome", p["nome"]),
        ("marca", p["marca"]),
        ("preco", p["preco"]),
        ("stock", p["stock"]),
        ("caracteristicas", OrderedDict([
            ("tela", p.get("caracteristicas", {}).get("tela", "n/a")),
            ("bateria", p.get("caracteristicas", {}).get("bateria", "n/a")),
            ("armazenamento", p.get("caracteristicas", {}).get("armazenamento", "n/a")),
        ]))
    ])

def guardar_produtos(produtos):
    produtos_ordenados = [ordenar_produto(p) for p in produtos]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos_ordenados, f, indent=2, ensure_ascii=False)

# === CRUD ===

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(carregar_produtos())

@app.route("/produtos/<int:produto_id>", methods=["GET"])
def obter_produto(produto_id):
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/produtos", methods=["POST"])
def adicionar_produto():
    produto = request.get_json()
    try:
        validate(produto, schema)
    except ValidationError as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": e.message}), 400

    produtos = carregar_produtos()
    produtos.append(produto)
    guardar_produtos(produtos)
    return jsonify({"mensagem": "Produto adicionado"}), 201

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    novos_dados = request.get_json()
    try:
        validate(novos_dados, schema)
    except ValidationError as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": e.message}), 400

    produtos = carregar_produtos()
    for i, p in enumerate(produtos):
        if p["id"] == produto_id:
            produtos[i] = novos_dados
            guardar_produtos(produtos)
            return jsonify({"mensagem": "Produto atualizado"})
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    produtos = carregar_produtos()
    produtos = [p for p in produtos if p["id"] != produto_id]
    guardar_produtos(produtos)
    return jsonify({"mensagem": "Produto removido"})

# --- Exportar/Importar JSON ---

@app.route("/exportar", methods=["GET"])
def exportar_json():
    produtos = carregar_produtos()
    return jsonify(produtos)

@app.route("/importar", methods=["POST"])
def importar_json():
    novos_produtos = request.get_json()
    for produto in novos_produtos:
        try:
            validate(produto, schema)
        except ValidationError as e:
            return jsonify({"erro": "Erro ao importar produto", "detalhes": e.message}), 400
    guardar_produtos(novos_produtos)
    return jsonify({"mensagem": "Importação concluída"})

# --- Consulta JSONPath ---

@app.route("/consulta", methods=["GET"])
def consulta_jsonpath():
    query = request.args.get("q")
    print("Recebido JSONPath:", query)
    if not query:
        return jsonify({"erro": "Parametro 'q' obrigatório"}), 400

    produtos = carregar_produtos()
    try:
        jsonpath_expr = parse(query)
        resultados = [match.value for match in jsonpath_expr.find(produtos)]
        return jsonify(resultados)
    except Exception as e:
        print("Erro JSONPath:", str(e))
        return jsonify({"erro": "Erro ao processar JSONPath", "detalhes": str(e)}), 400


if __name__ == "__main__":
    
    # Porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
