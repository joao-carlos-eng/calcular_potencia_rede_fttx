# calcular a distancia entre dois pontos
import math


def distancia_dois_pontos(ponto1, ponto2):
    x1, y1, z1 = ponto1
    x2, y2, z2 = ponto2

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def correct_coordinates(postes, caixas, trajetos, raio):
    """
    Corrige as coordenadas das caixas e dos trajetos dos postes utilizando o método OSNAP.

    Args:
        postes (list): Lista de coordenadas dos postes.
        caixas (list): Lista de coordenadas das caixas.
        trajetos (list): Lista de coordenadas dos trajetos.
        raio (float): Raio de aplicação do método OSNAP.

    Returns:
        None
    """

    def apply_osnap(lista, string, raio):
        """
        Aplica o método OSNAP em uma string de coordenadas.

        Args:
            lista (list): Lista de coordenadas a serem comparadas.
            string (str): String de coordenadas a serem corrigidas.
            raio (float): Raio de aplicação do método OSNAP.

        Returns:
            str: String de coordenadas corrigidas pelo método OSNAP.
        """
        out = ''
        lista2 = string.split()
        for i in lista2:
            out = out + f'{i} '

        for i in lista2:
            x = i.split(',')
            for p in lista:
                if distancia_dois_pontos(p, x) <= raio:
                    out = out.replace(f'{i}', f'{p[0]},{p[1]},{p[2]}')
        return out

    # Corrigir as coordenadas das caixas
    for caixa in caixas:
        caixa['coordenadas'] = apply_osnap(postes, caixa['coordenadas'], raio)

    # Corrigir o trajeto dos postes
    for trajeto in trajetos:
        trajeto['coordenadas'] = apply_osnap(
            postes, trajeto['coordenadas'], raio
        )
