import grpc
from concurrent import futures
import time
import json
import produtos_pb2
import produtos_pb2_grpc
import os
from google.protobuf import empty_pb2

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "./dados/produtos.json"))

# Carregar produtos

def carregar_produtos():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar produtos

def guardar_produtos(produtos):
    with open(DATA_FILE, "w") as f:
        json.dump(produtos, f, indent=2)

class ProdutoService(produtos_pb2_grpc.ProdutoServiceServicer):

    # Listar Produtos

    def ListarProdutos(self, request, context):
        produtos = carregar_produtos()
        resposta = produtos_pb2.ListaProdutos()
        for p in produtos:
            produto = produtos_pb2.Produto(
                id=p["id"],
                nome=p["nome"],
                marca=p["marca"],
                preco=p["preco"],
                stock=p["stock"],
                tela=p["caracteristicas"]["tela"],
                bateria=p["caracteristicas"]["bateria"],
                armazenamento=p["caracteristicas"]["armazenamento"]
            )
            resposta.produtos.append(produto)
        return resposta

    def ListarProdutosStream(self, request, context):
        produtos = carregar_produtos()
        for p in produtos:
            yield produtos_pb2.Produto(
                id=p["id"],
                nome=p["nome"],
                marca=p["marca"],
                preco=p["preco"],
                stock=p["stock"],
                tela=p["caracteristicas"]["tela"],
                bateria=p["caracteristicas"]["bateria"],
                armazenamento=p["caracteristicas"]["armazenamento"]
            )

    # Adicinar Produtos

    def AdicionarProduto(self, request, context):
        produtos = carregar_produtos()
        for p in produtos:
            if p["id"] == request.id:
                return produtos_pb2.ProdutoResponse(sucesso=False, mensagem="Produto com este ID já existe.")
        
        novo_produto = {
            "id": request.id,
            "nome": request.nome,
            "marca": request.marca,
            "preco": request.preco,
            "stock": request.stock,
            "caracteristicas": {
                "tela": request.tela,
                "bateria": request.bateria,
                "armazenamento": request.armazenamento
            }
        }
        produtos.append(novo_produto)
        guardar_produtos(produtos)
        return produtos_pb2.ProdutoResponse(sucesso=True, mensagem="Produto adicionado com sucesso.")

    # Editar Produtos

    def EditarProduto(self, request, context):
        produtos = carregar_produtos()
        for p in produtos:
            if p["id"] == request.id:
                p["nome"] = request.nome
                p["marca"] = request.marca
                p["preco"] = request.preco
                p["stock"] = request.stock
                p["caracteristicas"]["tela"] = request.tela
                p["caracteristicas"]["bateria"] = request.bateria
                p["caracteristicas"]["armazenamento"] = request.armazenamento
                guardar_produtos(produtos)
                return produtos_pb2.ProdutoResponse(sucesso=True, mensagem="Produto editado com sucesso.")
        return produtos_pb2.ProdutoResponse(sucesso=False, mensagem="Produto não encontrado.")

    def RemoverProduto(self, request, context):
        produtos = carregar_produtos()
        novos = [p for p in produtos if p["id"] != request.id]
        if len(produtos) == len(novos):
            return produtos_pb2.ProdutoResponse(sucesso=False, mensagem="Produto não encontrado.")
        guardar_produtos(novos)
        return produtos_pb2.ProdutoResponse(sucesso=True, mensagem="Produto removido com sucesso.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    produtos_pb2_grpc.add_ProdutoServiceServicer_to_server(ProdutoService(), server)
    
    # Porta 50051
    server.add_insecure_port('[::]:50051')
    print("gRPC server a correr em http://localhost:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
