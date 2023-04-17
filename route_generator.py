"""
Vamos começar criando a função create_cable_routes que receberá como parâmetros o dicionário pop, uma lista de dicionários caixas, uma lista de dicionários cabos, uma lista de dicionários postes, uma lista de dicionários hubs e uma lista de dicionários ceos.

Dentro da função, vamos criar um dicionário chamado coordinates_dict para guardar as coordenadas de cada objeto. Em seguida, vamos criar um dicionário chamado objects_dict para guardar todas as informações de cada objeto (caixas, postes, hubs e ceos) e o objeto em si.

Com o objects_dict criado, vamos percorrer a lista de cabos e para cada cabo, vamos criar uma lista de coordenadas a partir dos postes e caixas que fazem parte desse cabo. Depois, vamos adicionar essa lista de coordenadas ao coordinates_dict, para que possamos acessá-la mais facilmente quando criarmos as rotas.

Por fim, vamos percorrer a lista de caixas e para cada caixa, vamos criar uma rota partindo do pop até a caixa em questão. Para isso, vamos utilizar o algoritmo de Dijkstra para encontrar o caminho mais curto entre os dois pontos, usando a lista de coordenadas e o objects_dict.

Durante a criação da rota, vamos adicionar as informações dos objetos (postes, hubs e ceos) pelos quais o cabo passa e a lista de cabos que fazem parte dessa rota. Por fim, vamos adicionar a rota ao resultado final.
"""
from typing import Dict, List


def create_cable_routes(
        pop: Dict[str, str],
        devices: List[Dict[str, str]],
        cables: List[Dict[str, str]]
) -> List[Dict[str, List[str]]]:
    # Criar dicionários que mapeiam o nome de cada dispositivo e cabo para seus respectivos dicionários
    device_dict = {device["name"]: device for device in devices}
    cable_dict = {cable["name"]: cable for cable in cables}

    routes = []

    # Para cada caixa de distribuição (NAP ou CEO)
    for device in devices:
        if device["type"] in ["nap", "ceo"]:

            # Cria uma rota para cada cabo conectado a esta caixa
            for cable_name in device.get("cables", []):
                cable = cable_dict[cable_name]

                # Encontra o poste de origem e o de destino para o cabo
                start_poste_name, end_poste_name = cable["coordinates"].strip().split()

                # Verifica se a caixa está conectada a um dos postes
                if start_poste_name == device.get("poste"):
                    start_device = device_dict[start_poste_name]
                    end_device = device_dict[end_poste_name]
                elif end_poste_name == device.get("poste"):
                    start_device = device_dict[end_poste_name]
                    end_device = device_dict[start_poste_name]
                else:
                    # O cabo não está conectado a esta caixa, pular para o próximo
                    continue

                # Cria uma rota para o par de dispositivos encontrados
                route = {
                    "start": pop["name"],
                    "end": device["name"],
                    "router": [pop["name"]],
                    "cable": [cable["name"]],
                    "coordinates": [pop["coordinates"]],
                }

                # Adiciona os postes intermediários à rota
                for intermediate_poste_name in cable["router"]:
                    intermediate_poste = device_dict[intermediate_poste_name]
                    route["router"].append(intermediate_poste_name)
                    route["cable"].append(cable["name"])
                    route["coordinates"].append(intermediate_poste["coordinates"])

                # Adiciona a caixa final à rota
                route["router"].append(device["name"])
                route["coordinates"].append(device["coordinates"])

                # Adiciona a rota à lista de rotas
                routes.append(route)

    return routes
