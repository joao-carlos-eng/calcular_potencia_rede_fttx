# modulo coordinate_correction.py
from math import sqrt
import simplekml as kml


def apply_osnap(pontos_referencia, Place_a_corrigir, raio):
    """
    Aplica o método OSNAP em uma string de coordenadas.

    Args:
        pontos_referencia (list): Lista de dicionário dos postes com coordenadas para referência.
        Place_a_corrigir (dict): Dicionario do ponto ou cabo com da coordenada a serem corrigidas.
        raio (float): Raio de aplicação do método OSNAP.

    Returns:
        str: String de coordenadas corrigidas pelo método OSNAP.
    """
    list_cords_corrigir = Place_a_corrigir['coordinates']
    if Place_a_corrigir.get('postes') is not None:
        key = 'postes'
    else:
        key = 'poste'

    for cord_n, cord in enumerate(list_cords_corrigir):  # para cada coordenada a ser corrigida (cord)
        for p_num, p in enumerate(pontos_referencia):  # para cada poste de referencia (p)
            if distancia_dois_pontos(p['coordinates'][0], cord) <= raio:
                list_cords_corrigir[cord_n] = p['coordinates'][0]
                Place_a_corrigir[key][cord_n] = pontos_referencia[p_num]['name']
                break
        if Place_a_corrigir[key] is None:
            lat_lon = cord.split(',')[1] + ',' + cord.split(',')[0]
            print('Nenhum poste encontrado para a coordenada: ', lat_lon, 'do objeto: ', Place_a_corrigir['name'],
                  "verifique se a caixa está pocicionada corretamente ou tente um raio maior.")
            return

    cord_corrigido = []

    for a, b in zip(list_cords_corrigir, Place_a_corrigir[key]):
        if b is not None:
            cord_corrigido.append(a)

    return cord_corrigido


def distancia_dois_pontos(coord1, coord2):
    lat1, lat2 = coord1.split(',')[0], coord2.split(',')[0]
    lon1, lon2 = coord1.split(',')[1], coord2.split(',')[1]
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    # Calcula as diferenças de latitude e longitude
    cat1 = (lat1 - lat2) * 1852 * 60
    cat2 = (lon1 - lon2) * 1852 * 60

    h = sqrt((cat1 * cat1) + (cat2 * cat2))

    distance = round(h)

    return distance


def correct_coordinates(postes, caixas, cabos, raio):
    auditoria = kml.Kml(name='Auditoria')
    """
    Corrige as coordenadas das caixas e dos trajetos dos postes utilizando o método OSNAP.

    Args:
        postes (list): Lista de coordenadas dos postes.
        caixas (list): Lista de coordenadas das caixas.
        cabos (list): Lista de coordenadas dos cabos.
        raio (float): Raio de aplicação do método OSNAP.

    Returns:
        None
    """

    # Corrigir as coordenadas das caixas
    kml_caixas = auditoria.newfolder(name='Caixas')
    for caixa in caixas:
        print(caixa)
        co = caixa['coordinates'][0].split(',')
        caixa['poste'] = [None]
        caixa['coordinates'] = apply_osnap(postes, caixa, raio)
        pnt = kml_caixas.newpoint(name=caixa['name'], coords=[(float(co[0]), float(co[1]))])
        pnt.style.iconstyle.scale = 1
        try:
            co = caixa['coordinates'][0].split(',')
            pnt.coords = [(float(co[0]), float(co[1]))]
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png'
        except IndexError:
            pnt.description = 'Nenhum poste encontrado para a coordenada: ' + ','.join(co)
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png'

    # Corrigir o trajeto dos cabos
    kml_cabos = auditoria.newfolder(name='Cabos')
    for cabo in cabos:
        cabo['postes'] = [None for _ in range(len(cabo['coordinates']))]
        cabo['coordinates'] = apply_osnap(postes, cabo, raio)
        cabo['postes'] = [p for p in cabo['postes'] if p is not None]
        co = cabo['coordinates']
        co = [(float(c.split(',')[0]), float(c.split(',')[1])) for c in co]
        kml_cabos.newlinestring(name=cabo['name'], coords=co)

    kml_postes = auditoria.newfolder(name='Postes')
    for poste in postes:
        co = poste['coordinates'][0].split(',')
        pnt = kml_postes.newpoint(name=poste['name'], coords=[(float(co[0]), float(co[1]))])
        pnt.style.iconstyle.scale = 0.8
        pnt.style.iconstyle.labelstyle.scale = 0
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    auditoria.save('auditoria.kml')
