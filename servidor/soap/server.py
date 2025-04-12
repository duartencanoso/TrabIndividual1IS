from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import xml.etree.ElementTree as ET
from lxml import etree

XML_FILE = "produtos.xml"
XSD_FILE = "schema.xsd"

class ProdutoService(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def getProdutos(ctx):
        produtos = []
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for p in root.findall("produto"):
            nome = p.find("nome").text
            produtos.append(nome)
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

        tree.write(XML_FILE)
        return "Produto adicionado com sucesso"

    @rpc(Integer, _returns=Unicode)
    def deleteProduto(ctx, id):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for p in root.findall("produto"):
            if int(p.find("id").text) == id:
                root.remove(p)
                tree.write(XML_FILE)
                return "Produto removido"
        return "Produto não encontrado"

def validar_xml(tree):
    with open(XSD_FILE, 'rb') as f:
        schema_doc = etree.XML(f.read())
    schema = etree.XMLSchema(schema_doc)
    xml_data = etree.fromstring(ET.tostring(tree.getroot()))
    return schema.validate(xml_data)

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
