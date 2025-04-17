import graphene
import json
from jsonschema import validate, ValidationError
import os

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "./dados/produtos.json"))
SCHEMA_FILE = "schema.json"

# Carregar o schema Json para validação
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

# Adicionar um novo produto

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

# Editar um produto

class EditarProduto(graphene.Mutation):
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
        produtos = carregar_produtos()
        for p in produtos:
            if p["id"] == id:
                p["nome"] = nome
                p["marca"] = marca
                p["preco"] = preco
                p["stock"] = stock
                p["caracteristicas"] = {
                    "tela": tela,
                    "bateria": bateria,
                    "armazenamento": armazenamento
                }

                try:
                    validate(p, schema_json)
                except ValidationError as e:
                    return EditarProduto(ok=False, mensagem=f"Erro: {e.message}")

                guardar_produtos(produtos)
                return EditarProduto(ok=True, mensagem="Produto editado com sucesso")
        
        return EditarProduto(ok=False, mensagem="Produto não encontrado")

# Remover um Produto

class RemoverProduto(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    mensagem = graphene.String()

    def mutate(self, info, id):
        produtos = carregar_produtos()
        novos = [p for p in produtos if p["id"] != id]

        if len(novos) == len(produtos):
            return RemoverProduto(ok=False, mensagem="Produto não encontrado.")

        guardar_produtos(novos)
        return RemoverProduto(ok=True, mensagem="Produto removido com sucesso.")


class Mutation(graphene.ObjectType):
    adicionar_produto = AdicionarProduto.Field()
    editar_produto = EditarProduto.Field()
    remover_produto = RemoverProduto.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
