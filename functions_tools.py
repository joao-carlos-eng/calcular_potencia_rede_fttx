import xml.etree.ElementTree as ET
import os


def print_node(node, level=0):
    # Verifica se o tipo do elemento é 'Folder' ou 'Placemark'
    if node.tag.endswith('Folder') or node.tag.endswith('Placemark'):
        # Tenta obter o nome do nó a partir do atributo 'name'
        name_element = node.find('{http://www.opengis.net/kml/2.2}name')
        if name_element is not None:
            node_name = name_element.text
        else:
            node_name = ''

        # Se o nome não estiver presente, tenta obter a partir do atributo 'href'
        if not node_name:
            node_name = os.path.basename(node.attrib.get('href', ''))

        # Se ainda assim não houver nome, usa o tipo do elemento
        if not node_name:
            node_name = node.tag.split('}')[-1]

        # Imprime o tipo do elemento e o nome com indentação
        node_type = node.tag.split('}')[-1]
        print(' ' * level + f'[{node_type}] {node_name}')

    # Recursivamente imprime os filhos do nó atual
    for child in node:
        print_node(child, level + 2)


# Nome do arquivo KML a ser lido
kml_file = 'exemplo-rede-fttx.kml'

# Lê o arquivo KML
with open(kml_file, 'r', encoding='utf-8') as f:
    kml_str = f.read()

# Parseia o arquivo KML para um objeto ElementTree
kml = ET.fromstring(kml_str)

# Encontra o elemento Document que contém as pastas e arquivos
document = kml.find('{http://www.opengis.net/kml/2.2}Document')

# Imprime os nós da árvore de diretórios
print_node(document)
