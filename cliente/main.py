import requests
import grpc
import sys
import os

# caminho para a pasta 
grpc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../servidor/grpc"))

if grpc_path not in sys.path:
    sys.path.insert(0, grpc_path)
    
from zeep import Client as ZeepClient
from gql import gql, Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport
from produtos_pb2 import ProdutoId, Produto
from produtos_pb2_grpc import ProdutoServiceStub
from google.protobuf import empty_pb2


# --- REST ---
def testar_rest():
    print("\n--- REST ---")
    try:
        resposta = requests.get("http://localhost:5000/produtos")
        resposta.raise_for_status()
        produtos = resposta.json()
        print(f"  {len(produtos)} produtos encontrados.")
    except Exception as e:
        print("Erro REST:", e)

# --- SOAP ---
def testar_soap():
    print("\n--- SOAP ---")
    try:
        client = ZeepClient("http://localhost:8000/?wsdl")
        resultado = client.service.addProduto(
            99, "Power Bank 10000mAh", "EnerTech", 29.90, 15, "n/a", "10000mAh", "n/a"
        )
        print(" Produto adicionado:", resultado)
    except Exception as e:
        print("Erro SOAP:", e)

# --- GraphQL ---
def testar_graphql():
    print("\n--- GraphQL ---")
    try:
        # Usa transport e cliente da biblioteca gql
        transport = RequestsHTTPTransport(
            url="http://localhost:5001/graphql",
            verify=True,
            retries=3,
        )
        client = GQLClient(transport=transport, fetch_schema_from_transport=False)

        query = gql(
            """
            query {
              produtos {
                nome
                preco
              }
            }
            """
        )

        resultado = client.execute(query)
        for p in resultado["produtos"]:
            print(f" {p['nome']} - {p['preco']}€")
    except Exception as e:
        print(" Erro GraphQL:", e)

# --- gRPC ---
def testar_grpc():
    print("\n--- gRPC ---")
    try:
        canal = grpc.insecure_channel("localhost:50051")
        stub = ProdutoServiceStub(canal)
        produtos = stub.ListarProdutosStream(empty_pb2.Empty())
        for p in produtos:
            print(f" {p.id}: {p.nome} ({p.marca})")
    except Exception as e:
        print(" Erro gRPC:", e)

# --- Parte de execução ---
if __name__ == "__main__":
    testar_rest()
    testar_soap()
    testar_graphql()
    testar_grpc()
