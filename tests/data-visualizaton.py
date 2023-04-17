import xml.etree.ElementTree as Et

from pykml.factory import KML_ElementMaker as KML
from test_coordinate_correction import cabos, caixas, postes

# Cria o documento KML
doc = KML.kml(
    KML.Document(
        KML.Folder(
            # Adiciona os postes como pontos
            *[
                KML.Placemark(
                    KML.name(poste['name']),
                    KML.Point(KML.coordinates(poste['coordinates'])),
                )
                for poste in postes
            ],
            # Adiciona as caixas como pontos
            *[
                KML.Placemark(
                    KML.name(caixa['name']),
                    KML.Point(KML.coordinates(caixa['coordinates'])),
                )
                for caixa in caixas
            ],
            # Adiciona os cabos como linhas
            *[
                KML.Placemark(
                    KML.name(cabo['name']),
                    KML.LineString(KML.coordinates(cabo['coordinates'])),
                )
                for cabo in cabos
            ],
        )
    )
)

# Salva o arquivo KML
"""with open('pontos_e_linhas.kml', 'w') as f:
    f.write(etree.tostring(doc).decode())"""

# Carrega o KML
kmldoc = Et.parse('pontos_e_linhas.kml')
root = kmldoc.getroot()

postes = []
caixas = []
cabos = []
NAMESPACE = '{http://www.opengis.net/kml/2.2}'
for folder in root[0].findall(f'{NAMESPACE}Folder'):
    print(folder[0].text)
    if folder.find(f'{NAMESPACE}name').text == 'ramais':
        for placemark in folder.findall(f'{NAMESPACE}Placemark'):
            linestring = placemark.find(f'{NAMESPACE}LineString')
            if linestring is not None:
                coordinates = linestring.find(
                    f'{NAMESPACE}coordinates'
                ).text.strip()
                cb = {
                    'name': placemark.find(f'{NAMESPACE}name').text,
                    'coordinates': coordinates,
                    'type': 'ramal',
                }
                cabos.append(cb)
    elif folder.find(f'{NAMESPACE}name').text == 'postes':
        for placemark in folder.findall(f'{NAMESPACE}Placemark'):
            point = placemark.find(f'{NAMESPACE}Point')
            if point is not None:
                coordinates = point.find(
                    f'{NAMESPACE}coordinates'
                ).text.strip()
                poste = {
                    'name': placemark.find(f'{NAMESPACE}name').text,
                    'coordinates': coordinates,
                    'type': 'poste',
                }
                postes.append(poste)

    elif folder.find(f'{NAMESPACE}name').text == 'naps':
        for placemark in folder.findall(f'{NAMESPACE}Placemark'):
            point = placemark.find(f'{NAMESPACE}Point')
            if point is not None:
                coordinates = point.find(
                    f'{NAMESPACE}coordinates'
                ).text.strip()
                nap = {
                    'name': placemark.find(f'{NAMESPACE}name').text,
                    'coordinates': coordinates,
                    'type': 'nap',
                }
                caixas.append(nap)
    elif folder.find(f'{NAMESPACE}name').text == 'ceos':
        for placemark in folder.findall(f'{NAMESPACE}Placemark'):
            point = placemark.find(f'{NAMESPACE}Point')
            if point is not None:
                coordinates = point.find(
                    f'{NAMESPACE}coordinates'
                ).text.strip()
                ceo = {
                    'name': placemark.find(f'{NAMESPACE}name').text,
                    'coordinates': coordinates,
                    'type': 'ceo',
                }
                caixas.append(ceo)

    elif folder.find(f'{NAMESPACE}name').text == 'bkb':
        for placemark in folder.findall(f'{NAMESPACE}Placemark'):
            linestring = placemark.find(f'{NAMESPACE}LineString')
            if linestring is not None:
                coordinates = linestring.find(
                    f'{NAMESPACE}coordinates'
                ).text.strip()
                bkb = {
                    'name': placemark.find(f'{NAMESPACE}name').text,
                    'coordinates': coordinates,
                    'type': 'bkb',
                }
                cabos.append(bkb)

for poste in postes:
    print(poste)
