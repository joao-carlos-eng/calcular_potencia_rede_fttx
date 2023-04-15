# calcular a distancia entre dois pontos


from math import sin, cos, sqrt, atan2, radians


def distancia_dois_pontos(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    # Raio da Terra em metros
    R = 6371000

    # Converte as coordenadas para radianos
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Calcula as diferenças de latitude e longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calcula a distância entre os pontos
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(R * c)

    return round(distance)


def correct_coordinates(postes, caixas, cabos, raio):
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

    def apply_osnap(pontos_referencia, cord_a_corrigir, raio):
        """
        Aplica o método OSNAP em uma string de coordenadas.

        Args:
            pontos_referencia (list): Lista de dicionário dos postes com coordenadas para referência.
            cord_a_corrigir (dict): Dicionario do ponto ou cabo com da coordenada a serem corrigidas.
            raio (float): Raio de aplicação do método OSNAP.

        Returns:
            str: String de coordenadas corrigidas pelo método OSNAP.
        """
        string_coordinates = cord_a_corrigir['coordinates']
        list_cords_corrigir = string_coordinates.split(' ')

        if cord_a_corrigir.get('postes') is not None:
            key = 'postes'
        else:
            key = 'poste'

        for cord_n, cord in enumerate(list_cords_corrigir):  # para cada cordenada a ser corrigida (cord)
            x = cord.split(',')
            for p_num, p in enumerate(pontos_referencia):  # para cada poste de referencia (p)
                co = p['coordinates'].split(',')
                if distancia_dois_pontos(co[0], co[1], x[0], x[1]) <= raio:
                    list_cords_corrigir[cord_n] = p['coordinates']
                    if key == 'postes':
                        cord_a_corrigir[key][cord_n] = pontos_referencia[p_num]['name']
                    else:
                        cord_a_corrigir[key] = pontos_referencia[p_num]['name']
                    break

        cord_corrigido = []
        for a, b in zip(list_cords_corrigir, cord_a_corrigir[key]):
            if b is not None:
                cord_corrigido.append(a)

        if len(cord_corrigido) == 1:
            return cord_corrigido[0]
        return ' '.join(cord_corrigido).strip()

    # Corrigir as coordenadas das caixas
    for caixa in caixas:
        print('testando caixa: ', caixa['name'])
        caixa['poste'] = None
        caixa['coordinates'] = apply_osnap(postes, caixa, raio)

    # Corrigir o trajeto dos cabos
    for cabo in cabos:
        print('testando cabo: ', cabo['name'])
        cabo['postes'] = [None for _ in range(len(cabo['coordinates'].split(' ')))]
        cabo['coordinates'] = apply_osnap(postes, cabo, raio)
        cabo['postes'] = [p for p in cabo['postes'] if p is not None]
