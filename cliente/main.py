import requests
import grpc
import sys
import os
import json
import xml.etree.ElementTree as ET
from zeep import Client as ZeepClient
from gql import gql, Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport
from google.protobuf import empty_pb2
from xml.dom import minidom
from collections import OrderedDict

# === gRPC imports ====

grpc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../servidor/grpc"))
if grpc_path not in sys.path:
    sys.path.insert(0, grpc_path)
from produtos_pb2 import Produto
from produtos_pb2_grpc import ProdutoServiceStub

EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "exportados"))
IMPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "importar"))

# === Funções REST ===

def rest_listar():
    return requests.get("http://localhost:5000/produtos").json()

def rest_adicionar(prod):
    return requests.post("http://localhost:5000/produtos", json=prod).text

def rest_editar_interativo(produto_id):
    try:
        resposta = requests.get(f"http://localhost:5000/produtos/{produto_id}")
        if resposta.status_code != 200:
            return "Produto não encontrado."

        produto = resposta.json()
        print(f"\nProduto atual: {produto['nome']} ({produto['marca']}) - {produto['preco']}€")
        print("Deixa em branco para manter o valor atual.\n")

        for campo in ["nome", "marca", "preco", "stock"]:
            valor = input(f"{campo.capitalize()} [{produto[campo]}]: ")
            if valor != "":
                if campo == "preco":
                    produto[campo] = float(valor)
                elif campo == "stock":
                    produto[campo] = int(valor)
                else:
                    produto[campo] = valor

        carac = produto.get("caracteristicas", {})
        for campo in ["tela", "bateria", "armazenamento"]:
            valor = input(f"{campo.capitalize()} [{carac.get(campo, '')}]: ")
            if valor != "":
                carac[campo] = valor
        produto["caracteristicas"] = carac

        resposta = requests.put(f"http://localhost:5000/produtos/{produto_id}", json=produto)
        if resposta.status_code == 200:
            return "Produto atualizado com sucesso."
        else:
            return "Erro ao atualizar: " + str(resposta.json())
    except Exception as e:
        return f"Erro: {e}"

def rest_remover(id):
    return requests.delete(f"http://localhost:5000/produtos/{id}").text

def rest_consultar_jsonpath():
    query = input("Expressão JSONPath (ex: $[?(@.preco < 100)]): ")
    resposta = requests.get("http://localhost:5000/consulta", params={"q": query})
    if resposta.status_code == 200:
        resultados = resposta.json()
        if isinstance(resultados, list):
            for p in resultados:
                if isinstance(p, dict):
                    print(f"[{p.get('id')}] {p.get('nome')} ({p.get('marca')}) - {p.get('preco')}€")
                else:
                    print(p)
        else:
            print(resultados)
    else:
        print("Erro:", resposta.json())


# === Funções SOAP ===

def soap_client():
    return ZeepClient("http://localhost:8000/?wsdl")

def soap_adicionar(prod):
    client = soap_client()
    carac = prod.get("caracteristicas", {})
    return client.service.addProduto(
        prod.get("id"),
        prod.get("nome"),
        prod.get("marca"),
        prod.get("preco"),
        prod.get("stock"),
        carac.get("tela", "n/a"),
        carac.get("bateria", "n/a"),
        carac.get("armazenamento", "n/a")
    )

def soap_editar_interativo(produto_id):
    client = soap_client()
    produtos = client.service.getProdutos()
    
    produto = next((p for p in produtos if p.id == produto_id), None)
    if not produto:
        return "Produto não encontrado."

    print(f"\nProduto atual: {produto.nome} ({produto.marca}) - {produto.preco}€")
    print("Deixa em branco para manter o valor atual.\n")

    nome = input(f"Nome [{produto.nome}]: ") or produto.nome
    marca = input(f"Marca [{produto.marca}]: ") or produto.marca
    preco = input(f"Preço [{produto.preco}]: ")
    preco = float(preco) if preco else produto.preco
    stock = input(f"Stock [{produto.stock}]: ")
    stock = int(stock) if stock else produto.stock
    tela = input(f"Tela [{produto.tela}]: ") or produto.tela
    bateria = input(f"Bateria [{produto.bateria}]: ") or produto.bateria
    armazenamento = input(f"Armazenamento [{produto.armazenamento}]: ") or produto.armazenamento

    return client.service.editarProduto(produto_id, nome, marca, preco, stock, tela, bateria, armazenamento)

def soap_listar():
    client = soap_client()
    return client.service.getProdutos()

def soap_remover(id):
    client = soap_client()
    return client.service.deleteProduto(id)

# === Funções GraphQL ===

def graphql_listar():
    client = GQLClient(
        transport=RequestsHTTPTransport(url="http://localhost:5001/graphql", verify=True, retries=3),
        fetch_schema_from_transport=False,
    )
    query = gql("""
        query {
            produtos {
                id
                nome
                marca
                preco
                stock
                caracteristicas {
                    tela
                    bateria
                    armazenamento
                }
            }
        }
    """)
    return client.execute(query)["produtos"]


# Adicionar um produto

def graphql_adicionar(prod):
    client = GQLClient(
        transport=RequestsHTTPTransport(url="http://localhost:5001/graphql", verify=True, retries=3),
        fetch_schema_from_transport=False,
    )

    mutation = gql("""
        mutation AdicionarProduto(
            $id: Int!, $nome: String!, $marca: String!, $preco: Float!,
            $stock: Int!, $tela: String!, $bateria: String!, $armazenamento: String!
        ) {
            adicionarProduto(
                id: $id,
                nome: $nome,
                marca: $marca,
                preco: $preco,
                stock: $stock,
                tela: $tela,
                bateria: $bateria,
                armazenamento: $armazenamento
            ) {
                ok
                mensagem
            }
        }
    """)

    variaveis = {
        "id": prod["id"],
        "nome": prod["nome"],
        "marca": prod["marca"],
        "preco": prod["preco"],
        "stock": prod["stock"],
        "tela": prod["caracteristicas"]["tela"],
        "bateria": prod["caracteristicas"]["bateria"],
        "armazenamento": prod["caracteristicas"]["armazenamento"]
    }

    resultado = client.execute(mutation, variable_values=variaveis)
    return resultado["adicionarProduto"]["mensagem"]

# Editar um Produto

def graphql_editar_interativo(produto_id):
    produtos = graphql_listar()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if not produto:
        return "Produto não encontrado."

    print(f"\nProduto atual: {produto['nome']} ({produto['marca']}) - {produto['preco']}€")
    print("Deixa em branco para manter o valor atual.\n")

    nome = input(f"Nome [{produto['nome']}]: ") or produto["nome"]
    marca = input(f"Marca [{produto['marca']}]: ") or produto["marca"]
    preco = input(f"Preço [{produto['preco']}]: ")
    preco = float(preco) if preco else produto["preco"]
    stock = input(f"Stock [{produto.get('stock', 0)}]: ")
    stock = int(stock) if stock else produto.get("stock", 0)
    tela = input(f"Tela [{produto['caracteristicas']['tela']}]: ") or produto['caracteristicas']['tela']
    bateria = input(f"Bateria [{produto['caracteristicas']['bateria']}]: ") or produto['caracteristicas']['bateria']
    armazenamento = input(f"Armazenamento [{produto['caracteristicas']['armazenamento']}]: ") or produto['caracteristicas']['armazenamento']


    client = GQLClient(
        transport=RequestsHTTPTransport(url="http://localhost:5001/graphql", verify=True, retries=3),
        fetch_schema_from_transport=False,
    )

    mutation = gql("""
        mutation EditarProduto(
            $id: Int!, $nome: String!, $marca: String!, $preco: Float!,
            $stock: Int!, $tela: String!, $bateria: String!, $armazenamento: String!
        ) {
            editarProduto(
                id: $id,
                nome: $nome,
                marca: $marca,
                preco: $preco,
                stock: $stock,
                tela: $tela,
                bateria: $bateria,
                armazenamento: $armazenamento
            ) {
                ok
                mensagem
            }
        }
    """)

    variaveis = {
        "id": produto_id,
        "nome": nome,
        "marca": marca,
        "preco": preco,
        "stock": stock,
        "tela": tela,
        "bateria": bateria,
        "armazenamento": armazenamento
    }

    resultado = client.execute(mutation, variable_values=variaveis)
    return resultado["editarProduto"]["mensagem"]

# Remover um produto

def graphql_remover(id):
    client = GQLClient(
        transport=RequestsHTTPTransport(url="http://localhost:5001/graphql", verify=True, retries=3),
        fetch_schema_from_transport=False,
    )

    mutation = gql("""
        mutation RemoverProduto($id: Int!) {
            removerProduto(id: $id) {
                ok
                mensagem
            }
        }
    """)

    variaveis = {"id": id}
    resultado = client.execute(mutation, variable_values=variaveis)
    return resultado["removerProduto"]["mensagem"]


# === Funções gRPC ===

def grpc_listar():
    stub = ProdutoServiceStub(grpc.insecure_channel("localhost:50051"))
    return stub.ListarProdutosStream(empty_pb2.Empty())

# Adicionar Produtos

def grpc_adicionar(prod):
    stub = ProdutoServiceStub(grpc.insecure_channel("localhost:50051"))
    novo = Produto(
        id=prod["id"],
        nome=prod["nome"],
        marca=prod["marca"],
        preco=prod["preco"],
        stock=prod["stock"],
        tela=prod["caracteristicas"].get("tela", "n/a"),
        bateria=prod["caracteristicas"].get("bateria", "n/a"),
        armazenamento=prod["caracteristicas"].get("armazenamento", "n/a")
    )
    resposta = stub.AdicionarProduto(novo)
    return resposta.mensagem

# Editar Produtos

def grpc_editar_interativo(produto_id):
    stub = ProdutoServiceStub(grpc.insecure_channel("localhost:50051"))
    produtos = list(stub.ListarProdutosStream(empty_pb2.Empty()))

    produto = next((p for p in produtos if p.id == produto_id), None)
    if not produto:
        return "Produto não encontrado."

    print(f"\nProduto atual: {produto.nome} ({produto.marca}) - {produto.preco}€")
    print("Deixa em branco para manter o valor atual.\n")

    nome = input(f"Nome [{produto.nome}]: ") or produto.nome
    marca = input(f"Marca [{produto.marca}]: ") or produto.marca
    preco = input(f"Preço [{produto.preco}]: ")
    preco = float(preco) if preco else produto.preco
    stock = input(f"Stock [{produto.stock}]: ")
    stock = int(stock) if stock else produto.stock
    tela = input(f"Tela [{produto.tela}]: ") or produto.tela
    bateria = input(f"Bateria [{produto.bateria}]: ") or produto.bateria
    armazenamento = input(f"Armazenamento [{produto.armazenamento}]: ") or produto.armazenamento

    novo = Produto(
        id=produto_id,
        nome=nome,
        marca=marca,
        preco=preco,
        stock=stock,
        tela=tela,
        bateria=bateria,
        armazenamento=armazenamento
    )

    resposta = stub.EditarProduto(novo)
    return resposta.mensagem

# Remover Produtos

def grpc_remover(id):
    stub = ProdutoServiceStub(grpc.insecure_channel("localhost:50051"))
    from produtos_pb2 import ProdutoId
    resposta = stub.RemoverProduto(ProdutoId(id=id))
    return resposta.mensagem


# === Exportar / Importar ===

def exportar_json(produtos):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    ordenados = []
    for p in produtos:
        ordenado = OrderedDict()
        ordenado["id"] = p["id"]
        ordenado["nome"] = p["nome"]
        ordenado["marca"] = p["marca"]
        ordenado["preco"] = p["preco"]
        ordenado["stock"] = p["stock"]
        ordenado["caracteristicas"] = OrderedDict()
        carac = p.get("caracteristicas", {})
        ordenado["caracteristicas"]["tela"] = carac.get("tela", "n/a")
        ordenado["caracteristicas"]["bateria"] = carac.get("bateria", "n/a")
        ordenado["caracteristicas"]["armazenamento"] = carac.get("armazenamento", "n/a")
        ordenados.append(ordenado)

    with open(os.path.join(EXPORT_DIR, "produtos_exportados.json"), "w", encoding="utf-8") as f:
        json.dump(ordenados, f, indent=2, ensure_ascii=False)

def exportar_xml(produtos):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    root = ET.Element("produtos")
    for p in produtos:
        elem = ET.SubElement(root, "produto")
        ET.SubElement(elem, "id").text = str(p["id"])
        ET.SubElement(elem, "nome").text = p["nome"]
        ET.SubElement(elem, "marca").text = p["marca"]
        ET.SubElement(elem, "preco").text = str(p["preco"])
        ET.SubElement(elem, "stock").text = str(p["stock"])

        carac = p.get("caracteristicas", {})
        carac_elem = ET.SubElement(elem, "caracteristicas")
        ET.SubElement(carac_elem, "tela").text = carac.get("tela", "n/a")
        ET.SubElement(carac_elem, "bateria").text = carac.get("bateria", "n/a")
        ET.SubElement(carac_elem, "armazenamento").text = carac.get("armazenamento", "n/a")

    # Estruturar o ficheiro XML a exportar
    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(os.path.join(EXPORT_DIR, "produtos_exportados.xml"), "w", encoding="utf-8") as f:
        f.write(pretty_xml)


def importar_json():
    with open(os.path.join(IMPORT_DIR, "produtos_importar.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def importar_xml():
    path = os.path.join(IMPORT_DIR, "produtos_importar.xml")
    tree = ET.parse(path)
    root = tree.getroot()
    produtos = []
    for elem in root.findall("produto"):
        carac_elem = elem.find("caracteristicas")
        produto = {
            "id": int(elem.find("id").text),
            "nome": elem.find("nome").text,
            "marca": elem.find("marca").text,
            "preco": float(elem.find("preco").text),
            "stock": int(elem.find("stock").text),
            "caracteristicas": {
                "tela": carac_elem.find("tela").text if carac_elem is not None else "n/a",
                "bateria": carac_elem.find("bateria").text if carac_elem is not None else "n/a",
                "armazenamento": carac_elem.find("armazenamento").text if carac_elem is not None else "n/a",
            }
        }
        produtos.append(produto)
    return produtos


# === Formatação ===

def mostrar_produto(p):
    if isinstance(p, dict):
        print(f"[{p.get('id')}] {p.get('nome')} ({p.get('marca')}) - {p.get('preco')}€")
    else:
        print(f"[{p.id}] {p.nome} ({p.marca}) - {p.preco}€")

# === Menu ===

def menu():
    while True:
        print("\n======== MENU ========")
        print("1. Mostrar Produtos")
        print("2. Adicionar Produto")
        print("3. Editar Produto")
        print("4. Remover Produto")
        print("5. Exportar para JSON")
        print("6. Exportar para XML")
        print("7. Importar de JSON")
        print("8. Importar de XML")
        print("9. Consulta JSONPath")
        print("0. Sair")
        op = input("Opção: ")

        if op == "0":
            break

        # Mostrar Produtos
        if op == "1":
            print("Escolha o serviço:")
            print("1. REST\n2. SOAP\n3. GraphQL\n4. gRPC")
            svc = input("Serviço: ")

            if svc == "1":
                [mostrar_produto(p) for p in rest_listar()]
            elif svc == "2":
                produtos = soap_listar()
                for p in produtos:
                    print(f"[{p.id}] {p.nome} ({p.marca}) - {p.preco}€")
            elif svc == "3":
                [mostrar_produto(p) for p in graphql_listar()]
            elif svc == "4":
                [mostrar_produto(p) for p in grpc_listar()]

        # Adicionar Produtos
        elif op == "2":
            print("Escolha o serviço:")
            print("1. REST\n2. SOAP\n3. GraphQL\n4. gRPC")
            svc = input("Serviço: ")

            p = {
                "id": int(input("ID: ")),
                "nome": input("Nome: "),
                "marca": input("Marca: "),
                "preco": float(input("Preço: ")),
                "stock": int(input("Stock: ")),
                "caracteristicas": {
                    "tela": input("Tela: "),
                    "bateria": input("Bateria: "),
                    "armazenamento": input("Armazenamento: ")
                }
            }

            if svc == "1":
                print(rest_adicionar(p))
            elif svc == "2":
                print(soap_adicionar(p))
            elif svc == "3":
                print(graphql_adicionar(p))
            elif svc == "4": 
                print(grpc_adicionar(p))


        # Editar Produtos
        elif op == "3":
            print("Escolha o serviço:")
            print("1. REST\n2. SOAP\n3. GraphQL\n4. gRPC")
            svc = input("Serviço: ")
            id = int(input("ID do produto a editar: "))
            if svc == "1":
                print(rest_editar_interativo(id))
            elif svc == "2":
                print(soap_editar_interativo(id))
            elif svc == "3":
                print(graphql_editar_interativo(id))
            elif svc == "4":
                print(grpc_editar_interativo(id))


        # Remover Produtos
        elif op == "4":
            print("Escolha o serviço:")
            print("1. REST\n2. SOAP\n3. GraphQL\n4. gRPC")
            svc = input("Serviço: ")
            id = int(input("ID: "))
            if svc == "1":
                print(rest_remover(id))
            elif svc == "2":
                print(soap_remover(id))
            elif svc == "3":
                print(graphql_remover(id))
            elif svc == "4":
                print(grpc_remover(id))

        # Exportar para Json
        elif op == "5":
            exportar_json(rest_listar())
            print("Exportado para JSON.")

        # Exportar para XML
        elif op == "6":
            exportar_xml(rest_listar())
            print("Exportado para XML.")

        # Importar de JSON
        elif op == "7":
            for p in importar_json():
                print(rest_adicionar(p))

        # Importar XML
        elif op == "8":
            for p in importar_xml():
                print(rest_adicionar(p))
                
        # Consulta com JSONPath
        elif op == "9":
            rest_consultar_jsonpath()



if __name__ == "__main__":
    menu()
