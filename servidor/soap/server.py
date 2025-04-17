from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne import ComplexModel
from xml.dom import minidom
import xml.etree.ElementTree as ET
from lxml import etree

XML_FILE = "produtos.xml"
XSD_FILE = "schema.xsd"

class ProdutoSOAP(ComplexModel):
    id = Integer
    nome = Unicode
    marca = Unicode
    preco = Float
    stock = Integer
    tela = Unicode
    bateria = Unicode
    armazenamento = Unicode

class ProdutoService(ServiceBase):

    @rpc(_returns=Iterable(ProdutoSOAP))
    def getProdutos(ctx):
        produtos = []
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for p in root.findall("produto"):
            produto = ProdutoSOAP()
            produto.id = int(p.find("id").text)
            produto.nome = p.find("nome").text
            produto.marca = p.find("marca").text
            produto.preco = float(p.find("preco").text)
            produto.stock = int(p.find("stock").text)

            carac = p.find("caracteristicas")
            produto.tela = carac.find("tela").text
            produto.bateria = carac.find("bateria").text
            produto.armazenamento = carac.find("armazenamento").text

            produtos.append(produto)
        return produtos


    @rpc(Integer, Unicode, Unicode, Float, Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def addProduto(ctx, id, nome, marca, preco, stock, tela, bateria, armazenamento):
        # Criar um novo elemento produto
        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        novo = ET.SubElement(root, "produto")
        ET.SubElement(novo, "id").text = str(id)
        ET.SubElement(novo, "nome").text = nome
        ET.SubElement(novo, "marca").text = marca
        ET.SubElement(novo, "preco").text = str(preco)
        ET.SubElement(novo, "stock").text = str(stock)

        carac = ET.SubElement(novo, "caracteristicas")
        ET.SubElement(carac, "tela").text = tela
        ET.SubElement(carac, "bateria").text = bateria
        ET.SubElement(carac, "armazenamento").text = armazenamento

        # Validar com XSD
        
        if validar_xml(tree) is False:
            return "Erro: XML inválido segundo XSD"

        salvar_pretty(tree, XML_FILE)
        return "Produto adicionado com sucesso"
    
    @rpc(Integer, Unicode, Unicode, Float, Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def editarProduto(ctx, id, nome, marca, preco, stock, tela, bateria, armazenamento):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    
        for p in root.findall("produto"):
            if int(p.find("id").text) == id:
                # Atualiza os campos existentes
                p.find("nome").text = nome
                p.find("marca").text = marca
                p.find("preco").text = str(preco)
                p.find("stock").text = str(stock)

                carac = p.find("caracteristicas")
                if carac is None:
                    carac = ET.SubElement(p, "caracteristicas")

                carac.find("tela").text = tela
                carac.find("bateria").text = bateria
                carac.find("armazenamento").text = armazenamento

                # Valida com XSD
                
                if validar_xml(tree) is False:
                    return "Erro: XML inválido segundo XSD"

                salvar_pretty(tree, XML_FILE)
                return "Produto atualizado com sucesso"
    
        return "Produto não encontrado"


    @rpc(Integer, _returns=Unicode)
    def deleteProduto(ctx, id):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for p in root.findall("produto"):
            if int(p.find("id").text) == id:
                root.remove(p)
                salvar_pretty(tree, XML_FILE)
                return "Produto removido"
        return "Produto não encontrado"

def validar_xml(tree):
    with open(XSD_FILE, 'rb') as f:
        schema_doc = etree.XML(f.read())
    schema = etree.XMLSchema(schema_doc)
    xml_data = etree.fromstring(ET.tostring(tree.getroot()))
    return schema.validate(xml_data)

# remover espaços desnecessários entre elementos

def limpar_espacos_em_branco(elem):
    for sub in list(elem):
        if sub.tail is not None and sub.tail.strip() == "":
            sub.tail = None
        limpar_espacos_em_branco(sub)

# Salvar o xml de forma bem estruturada

def salvar_pretty(tree, path):
    limpar_espacos_em_branco(tree.getroot())

    xml_str = ET.tostring(tree.getroot(), encoding="utf-8")
    dom = minidom.parseString(xml_str)

    pretty = "\n".join(
        [line for line in dom.toprettyxml(indent="  ").split("\n") if line.strip()]
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(pretty)

# Spyne App
app = Application(
    [ProdutoService],
    tns="catalogo.eletronica.soap",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    print("SOAP server a correr em http://localhost:8000")
    wsgi_app = WsgiApplication(app)
    
    # Porta 8000
    server = make_server("0.0.0.0", 8000, wsgi_app)
    server.serve_forever()
