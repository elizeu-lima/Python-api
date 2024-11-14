from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Configuração do MongoDB Atlas
client = MongoClient("mongodb+srv://conjuntobelavista2:<db_password>@cluster0.qefi3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["conjuntobelavista2"]  # Substitua pelo nome do seu banco de dados
usuarios_collection = db["usuarios"]
carros_collection = db["carros"]

# Rotas para Usuários

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    usuario = {
        "nome": data.get("nome"),
        "telefone": data.get("telefone"),
        "data_criacao": datetime.utcnow(),
        "data_exclusao": None
    }
    usuarios_collection.insert_one(usuario)
    return jsonify({"message": "Usuário criado com sucesso!"}), 201

@app.route('/usuarios/<id>', methods=['DELETE'])
def excluir_usuario(id):
    result = usuarios_collection.update_one(
        {"_id": id},
        {"$set": {"data_exclusao": datetime.utcnow()}}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Usuário excluído com sucesso!"}), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

# Rotas para Carros

@app.route('/carros', methods=['POST'])
def criar_carro():
    data = request.json
    carro = {
        "modelo": data.get("modelo"),
        "cor": data.get("cor"),
        "valor": data.get("valor"),
        "ano_fabricacao": data.get("ano_fabricacao")
    }
    carros_collection.insert_one(carro)
    return jsonify({"message": "Carro cadastrado com sucesso!"}), 201

@app.route('/carros/<id>', methods=['PUT'])
def atualizar_carro(id):
    data = request.json
    update_data = {}
    if "modelo" in data:
        update_data["modelo"] = data["modelo"]
    if "cor" in data:
        update_data["cor"] = data["cor"]
    if "valor" in data:
        update_data["valor"] = data["valor"]
    if "ano_fabricacao" in data:
        update_data["ano_fabricacao"] = data["ano_fabricacao"]
    
    result = carros_collection.update_one({"_id": id}, {"$set": update_data})
    if result.modified_count > 0:
        return jsonify({"message": "Carro atualizado com sucesso!"}), 200
    return jsonify({"message": "Carro não encontrado"}), 404

@app.route('/carros/<id>', methods=['DELETE'])
def excluir_carro(id):
    result = carros_collection.delete_one({"_id": id})
    if result.deleted_count > 0:
        return jsonify({"message": "Carro excluído com sucesso!"}), 200
    return jsonify({"message": "Carro não encontrado"}), 404

@app.route('/carros', methods=['GET'])
def listar_carros():
    carros = list(carros_collection.find())
    for carro in carros:
        carro["_id"] = str(carro["_id"])  # Converte ObjectId para string
    return jsonify(carros), 200

# Inicialização da aplicação
if __name__ == '__main__':
    app.run(debug=True)
