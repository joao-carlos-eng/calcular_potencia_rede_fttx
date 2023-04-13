import xml.etree.ElementTree as ET


def tratar_mapeamento(arquivo):
    # Extrair cordenadas dos pontos e gerar um novo arquivo
    tree = ET.parse(arquivo)
    root = tree.getroot()

    # Extrair as coordenadas dos postes
    postes = []
    for i in root.iter('{http://www.opengis.net/kml/2.2}Point'):
        for j in i.iter('{http://www.opengis.net/kml/2.2}coordinates'):
            postes.append(j.text.split(','))

    # gera um novo arquivo kml com as cordenadas
    with open('postes.kml', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        document = ET.Element('Document')
        for i in postes:
            placemark = ET.SubElement(document, 'Placemark')
            point = ET.SubElement(placemark, 'Point')
            coordinates = ET.SubElement(point, 'coordinates')
            coordinates.text = f'{i[0]},{i[1]},{i[2]}'
        tree = ET.ElementTree(document)
        tree.write(f, encoding='unicode')


if __name__ == '__main__':
    arquivo = open('mapeamento.kml', 'r')
    tratar_mapeamento(arquivo)
