import graphene
import json
from jsonschema import validate, ValidationError
import os

DATA_FILE = "produtos.json"
SCHEMA_FILE = "schema.json"

# Carregar o schema JSON para validação
with open(SCHEMA_FILE) as f:
    schema_json = json.load(f)

def carregar_produtos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def guardar_produtos(produtos):
    with open(DATA_FILE, "w") as f:
        json.dump(produtos, f, indent=2)

# GraphQL Tipos
class CaracteristicasType(graphene.ObjectType):
    tela = graphene.String()
    bateria = graphene.String()
    armazenamento = graphene.String()

class ProdutoType(graphene.ObjectType):
    id = graphene.Int()
    nome = graphene.String()
    marca = graphene.String()
    preco = graphene.Float()
    stock = graphene.Int()
    caracteristicas = graphene.Field(CaracteristicasType)

class Query(graphene.ObjectType):
    produtos = graphene.List(ProdutoType)

    def resolve_produtos(root, info):
        return carregar_produtos()

class AdicionarProduto(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        nome = graphene.String(required=True)
        marca = graphene.String(required=True)
        preco = graphene.Float(required=True)
        stock = graphene.Int(required=True)
        tela = graphene.String(required=True)
        bateria = graphene.String(required=True)
        armazenamento = graphene.String(required=True)

    ok = graphene.Boolean()
    mensagem = graphene.String()

    def mutate(self, info, id, nome, marca, preco, stock, tela, bateria, armazenamento):
        novo_produto = {
            "id": id,
            "nome": nome,
            "marca": marca,
            "preco": preco,
            "stock": stock,
            "caracteristicas": {
                "tela": tela,
                "bateria": bateria,
                "armazenamento": armazenamento
            }
        }

        try:
            validate(novo_produto, schema_json)
        except ValidationError as e:
            return AdicionarProduto(ok=False, mensagem=f"Erro: {e.message}")

        produtos = carregar_produtos()
        produtos.append(novo_produto)
        guardar_produtos(produtos)

        return AdicionarProduto(ok=True, mensagem="Produto adicionado com sucesso")

class Mutation(graphene.ObjectType):
    adicionar_produto = AdicionarProduto.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
