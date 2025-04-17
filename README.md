# Catálogo de produtos eletrónicos - Trabalho Individual de Serviços Web Multitecnologia

Este projeto implementa um **catálogo de produtos eletrónicos** com suporte a quatro tipos de serviços web: **REST, SOAP, GraphQL e gRPC**, cada um com mecanismos próprios de validação e armazenamento de dados.

O link do vídeo de demonstração e o documento que faz a descrição de EndPoints e serviços encontram-se dentro da pasta "documentacao".
---

## Execução do Projeto

### Requisitos
- Docker e Docker Compose instalados

### Passos
1. Abrir terminal na raiz do projeto

2. (Opcional) Ativar o ambiente virtual Python:
    source venv/bin/activate

3. Executar os serviços com Docker Compose:
   sudo docker-compose up --build

4. Entrar na diretoria do cliente e executar o cliente através do ficheiro main.py
    cd cliente
    python main.py

## Exemplos de chamadas com Postman

### REST http://localhost:5000

Consulta com JSONPath:

- Nome de todos os produtos 

GET http://localhost:5000/consulta?q=$[*].nome

Resultado:
"Iphone 15 pro max",
"Auriculares Bluetooth",
"Coluna Bluetooth",
"Smartwatch GEN 8",
"Portátil UltraSlim",
"Tablet Pro 11"


- Produtos com preço abaixo de 100€

GET http://localhost:5000/consulta?q=$[?(@.preco < 100)]

Resultado:
{
        "caracteristicas": {
            "armazenamento": "n/a",
            "bateria": "500mAh",
            "tela": "n/a"
        },
        "id": 2,
        "marca": "Samsung",
        "nome": "Auriculares Bluetooth",
        "preco": 59.9,
        "stock": 50
    },
    {
        "caracteristicas": {
            "armazenamento": "n/a",
            "bateria": "2000mAh",
            "tela": "n/a"
        },
        "id": 3,
        "marca": "JBL",
        "nome": "Coluna Bluetooth",
        "preco": 79.99,
        "stock": 30
    }

- Listar os Produtos 

GET http://localhost:5000/produtos

Resultado:
{
        "caracteristicas": {
            "armazenamento": "256",
            "bateria": "500mAh",
            "tela": "6.1"
        },
        "id": 1,
        "marca": "Apple",
        "nome": "Iphone 15 pro max",
        "preco": 900.0,
        "stock": 30
    },
    {
        "caracteristicas": {
            "armazenamento": "n/a",
            "bateria": "500mAh",
            "tela": "n/a"
        },
        "id": 2,
        "marca": "Samsung",
        "nome": "Auriculares Bluetooth",
        "preco": 59.9,
        "stock": 50
    },
    {
        "caracteristicas": {
            "armazenamento": "n/a",
            "bateria": "2000mAh",
            "tela": "n/a"
        },
        "id": 3,
        "marca": "JBL",
        "nome": "Coluna Bluetooth",
        "preco": 79.99,
        "stock": 30
    },
    {
        "caracteristicas": {
            "armazenamento": "4GB",
            "bateria": "300mAh",
            "tela": "1.4 polegadas"
        },
        "id": 4,
        "marca": "Garmin",
        "nome": "Smartwatch GEN 8",
        "preco": 200.99,
        "stock": 20
    },
    {
        "caracteristicas": {
            "armazenamento": "512GB SSD",
            "bateria": "6000mAh",
            "tela": "15.6 polegadas"
        },
        "id": 5,
        "marca": "Lenovo",
        "nome": "Portátil UltraSlim",
        "preco": 849.0,
        "stock": 10
    },
    {
        "caracteristicas": {
            "armazenamento": "256GB",
            "bateria": "7500mAh",
            "tela": "11 polegadas"
        },
        "id": 6,
        "marca": "Huawei",
        "nome": "Tablet Pro 11",
        "preco": 399.99,
        "stock": 18
    },
    {
        "caracteristicas": {
            "armazenamento": "256",
            "bateria": "1500",
            "tela": "13"
        },
        "id": 7,
        "marca": "Xiaomi",
        "nome": "Xiaomi Android EU",
        "preco": 500.0,
        "stock": 20
    }

- Obter o Produto por ID

GET http://localhost:5000/produtos/1

Resultado:
{
    "caracteristicas": {
        "armazenamento": "256",
        "bateria": "500mAh",
        "tela": "6.1"
    },
    "id": 1,
    "marca": "Apple",
    "nome": "Iphone 15 pro max",
    "preco": 900.0,
    "stock": 30
}

- Adicionar um novo Produto

POST http://localhost:5000/produtos

Content-Type: application/json

body > raw > JSON

{
  "id": 99,
  "nome": "Drone 4K",
  "marca": "DJI",
  "preco": 299.99,
  "stock": 5,
  "caracteristicas": {
    "tela": "n/a",
    "bateria": "4000mAh",
    "armazenamento": "32GB"
  }
}

Resultado:

{
    "mensagem": "Produto adicionado"
}


- Editar Produto 

PUT http://localhost:5000/produtos/99

Content-Type: application/json

body > raw > JSON

{
  "id": 99,
  "nome": "Drone 4K Ultra",
  "marca": "DJI",
  "preco": 349.99,
  "stock": 6,
  "caracteristicas": {
    "tela": "n/a",
    "bateria": "5000mAh",
    "armazenamento": "64GB"
  }
}

Resultado:
{
    "mensagem": "Produto atualizado"
}

- Remover Produto

DELETE http://localhost:5000/produtos/99

Resultado:

{
    "mensagem": "Produto removido"
}

### SOAP http://localhost:8000/?wsdl

- Adicionar um Produto 

POST http://localhost:8000

Body > raw > XML

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cat="catalogo.eletronica.soap">
  <soapenv:Header/>
  <soapenv:Body>
    <cat:addProduto>
      <cat:id>101</cat:id>
      <cat:nome>Tablet Pro</cat:nome>
      <cat:marca>Huawei</cat:marca>
      <cat:preco>399.99</cat:preco>
      <cat:stock>8</cat:stock>
      <cat:tela>10.1 polegadas</cat:tela>
      <cat:bateria>7000mAh</cat:bateria>
      <cat:armazenamento>128GB</cat:armazenamento>
    </cat:addProduto>
  </soapenv:Body>
</soapenv:Envelope>

resultado:

<tns:addProdutoResult>Produto adicionado com sucesso</tns:addProdutoResult>


### GRAPHQL http://localhost:5001/graphql

- Lista de todos os Produtos

POST http://localhost:5001/graphql

Content-Type: application/json

Body > GraphQL
query { produtos { id nome marca preco } }

Resultado:

{
    "id": 1,
    "nome": "Iphone 15 pro max",
    "marca": "Apple",
    "preco": 900.0
},
{
    "id": 2,
    "nome": "Auriculares Bluetooth",
    "marca": "Samsung",
    "preco": 59.9
},
{
    "id": 3,
    "nome": "Coluna Bluetooth",
    "marca": "JBL",
    "preco": 79.99
},
{
    "id": 4,
    "nome": "Smartwatch GEN 8",
    "marca": "Garmin",
    "preco": 200.99
},
{
    "id": 5,
    "nome": "Portátil UltraSlim",
    "marca": "Lenovo",
    "preco": 849.0
},
{
    "id": 6,
    "nome": "Tablet Pro 11",
    "marca": "Huawei",
    "preco": 399.99
},
{
    "id": 7,
    "nome": "Xiaomi Android EU",
    "marca": "Xiaomi",
    "preco": 500.0
  }

- Mutation - Adicionar Produto

POST http://localhost:5001/graphql

Content-Type: application/json

Body > RAW > JSON
{
  "query": "mutation ($id: Int!, $nome: String!, $marca: String!, $preco: Float!, $stock: Int!, $tela: String!, $bateria: String!, $armazenamento: String!) { adicionarProduto(id: $id, nome: $nome, marca: $marca, preco: $preco, stock: $stock, tela: $tela, bateria: $bateria, armazenamento: $armazenamento) { ok mensagem } }",
  "variables": {
    "id": 111,
    "nome": "Câmara GoPro",
    "marca": "GoPro",
    "preco": 250.00,
    "stock": 10,
    "tela": "2 polegadas",
    "bateria": "1500mAh",
    "armazenamento": "64GB"
  }
}

resultado:

{
    "data": {
        "adicionarProduto": {
            "ok": true,
            "mensagem": "Produto adicionado com sucesso"
        }
    }
}

### GRPC localhost:50051

New Request → escolher gRPC.

Carregar o ficheiro .proto

Definir o Endpoint como localhost:50051

Escolher os métodos:


- ListarProdutos - Método Unário

Resultado
{
    "produtos": [
        {
            "id": 1,
            "nome": "Iphone 15 pro max",
            "marca": "Apple",
            "preco": 900,
            "stock": 30,
            "tela": "6.1",
            "bateria": "500mAh",
            "armazenamento": "256"
        },
        {
            "id": 2,
            "nome": "Auriculares Bluetooth",
            "marca": "Samsung",
            "preco": 59.900001525878906,
            "stock": 50,
            "tela": "n/a",
            "bateria": "500mAh",
            "armazenamento": "n/a"
        },
        {
            "id": 3,
            "nome": "Coluna Bluetooth",
            "marca": "JBL",
            "preco": 79.98999786376953,
            "stock": 30,
            "tela": "n/a",
            "bateria": "2000mAh",
            "armazenamento": "n/a"
        },
        {
            "id": 4,
            "nome": "Smartwatch GEN 8",
            "marca": "Garmin",
            "preco": 200.99000549316406,
            "stock": 20,
            "tela": "1.4 polegadas",
            "bateria": "300mAh",
            "armazenamento": "4GB"
        },
        {
            "id": 5,
            "nome": "Portátil UltraSlim",
            "marca": "Lenovo",
            "preco": 849,
            "stock": 10,
            "tela": "15.6 polegadas",
            "bateria": "6000mAh",
            "armazenamento": "512GB SSD"
        },
        {
            "id": 6,
            "nome": "Tablet Pro 11",
            "marca": "Huawei",
            "preco": 399.989990234375,
            "stock": 18,
            "tela": "11 polegadas",
            "bateria": "7500mAh",
            "armazenamento": "256GB"
        },
        {
            "id": 7,
            "nome": "Xiaomi Android EU",
            "marca": "Xiaomi",
            "preco": 500,
            "stock": 20,
            "tela": "13",
            "bateria": "1500",
            "armazenamento": "256"
        },
        {
            "id": 111,
            "nome": "Câmara GoPro",
            "marca": "GoPro",
            "preco": 250,
            "stock": 10,
            "tela": "2 polegadas",
            "bateria": "1500mAh",
            "armazenamento": "64GB"
        }
    ]
}

- Adicionar Produto:

{
  "id": 120,
  "nome": "Impressora HP",
  "marca": "HP",
  "preco": 89.99,
  "stock": 6,
  "tela": "n/a",
  "bateria": "n/a",
  "armazenamento": "n/a"
}

Resultado:

{
    "sucesso": true,
    "mensagem": "Produto adicionado com sucesso."
}


## Esquemas de validação utilizados

### REST

- schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "nome": { "type": "string" },
    "marca": { "type": "string" },
    "preco": { "type": "number" },
    "stock": { "type": "integer" },
    "caracteristicas": {
      "type": "object",
      "properties": {
        "tela": { "type": "string" },
        "bateria": { "type": "string" },
        "armazenamento": { "type": "string" }
      }
    }
  },
  "required": ["id", "nome", "marca", "preco", "stock", "caracteristicas"]
}


### SOAP

- schema.xsd

<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="produtos">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="produto" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="id" type="xs:int"/>
              <xs:element name="nome" type="xs:string"/>
              <xs:element name="marca" type="xs:string"/>
              <xs:element name="preco" type="xs:float"/>
              <xs:element name="stock" type="xs:int"/>
              <xs:element name="caracteristicas">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="tela" type="xs:string"/>
                    <xs:element name="bateria" type="xs:string"/>
                    <xs:element name="armazenamento" type="xs:string"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
