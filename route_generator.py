# module route_generator.py

def get_caixas_by_type(caixas, type_):
    """Retorna uma lista de caixas com o tipo especificado."""
    return [caixa for caixa in caixas if caixa['type'] == type_]


def get_cabos_by_type(cabos, type_):
    """Retorna uma lista de cabos com o tipo especificado."""
    return [cabo for cabo in cabos if cabo['type'] == type_]


def get_caixa_by_coordinate(caixas, coordinate):
    """Retorna a caixa com a coordenada especificada, ou None se não houver nenhuma."""
    for caixa in caixas:
        if caixa['coordinates'] == coordinate:
            return caixa
    return None


def get_poste_by_coordinate(postes, coordinate):
    """Retorna o poste com a coordenada especificada, ou None se não houver nenhum."""
    for poste in postes:
        if poste['coordinates'] == coordinate:
            return poste
    return None


def create_cables_routers(pop, poste_list, cabo_list, caixa_list):
    routers = []
    """Cria uma rota a partir do POP."""
    router = [pop['name'].upper()]
    coordinates = [pop['coordinates']]
    start = pop['name']
    cables = []
    end = None

    naps = get_caixas_by_type(caixa_list, 'nap') + get_caixas_by_type(caixa_list, 'cto')
    ceos_hubs = get_caixas_by_type(caixa_list, 'ceo') + get_caixas_by_type(caixa_list, 'hub')

    # Busca cabos que partem do POP
    for cabo in cabo_list:
        if cabo['type'] == 'bkb' and cabo['coordinates'].startswith(pop['coordinates']):
            cables.append(cabo['name'].capitalize())
            router_bkb = list(router)
            coordinates_bkb = list(coordinates)

            # Percorre a lista de coordenadas procurando interceptações do cabo
            for coordinate in cabo['coordinates'].split():

                caixa = get_caixa_by_coordinate(naps, coordinate)
                if caixa is not None:
                    router_bkb.append(caixa['name'].upper())
                    coordinates_bkb.append(caixa['coordinates'])
                    end = caixa['name'].upper()
                    routers.append({
                        'start': start,
                        'end': end,
                        'router': router_bkb,
                        'cable': cables,
                        'coordinates': coordinates_bkb,
                    })

                for ceo_hub in ceos_hubs:
                    if ceo_hub['coordinates'] == coordinate:
                        router_bkb.append(ceo_hub['name'].upper())
                        router_ceo_hub = list(router_bkb)
                        coordinates_bkb.append(ceo_hub['coordinates'])
                        coordinates_ceo_hub = list(coordinates_bkb)
                        end = ceo_hub['name']
                        routers.append({
                            'start': start,
                            'end': end,
                            'router': router_ceo_hub,
                            'cable': cables,
                            'coordinates': coordinates_ceo_hub,
                        })

                        ramais = get_cabos_by_type(cabo_list, 'ramal')
                        for ramal in ramais:
                            # verifica se oramal está invertido e corrige
                            if ramal['coordinates'].endswith(ceo_hub['coordinates']):
                                ramal['coordinates'] = ramal['coordinates'].split()[::-1]

                            elif ramal['coordinates'].startswith(ceo_hub['coordinates']):
                                router_ramal = list(router_bkb)
                                cable_ramal = list(cables)
                                cable_ramal.append(ramal['name'].capitalize())
                                coordinates_ramal = list(coordinates_bkb)

                                for new_coordinate in ramal['coordinates'].split():
                                    caixa = get_caixa_by_coordinate(naps, new_coordinate)

                                    if caixa is not None:
                                        router_ramal.append(caixa['name'].upper())
                                        router_nap = list(router_ramal)
                                        coordinates_ramal.append(caixa['coordinates'])
                                        coordinates_nap = list(coordinates_ramal)
                                        end = caixa['name'].upper()
                                        routers.append({
                                            'start': start,
                                            'end': end,
                                            'router': router_nap,
                                            'cable': cable_ramal,
                                            'coordinates': coordinates_nap,
                                        })

                                    for poste in poste_list:
                                        if poste['coordinates'] == new_coordinate and \
                                                poste['coordinates'] not in coordinates_ramal:
                                            router_ramal.append(poste['name'])
                                            coordinates_ramal.append(poste['coordinates'])
                                            break

                for poste in poste_list:
                    if poste['coordinates'] == coordinate and poste['coordinates'] not in coordinates_bkb:
                        router_bkb.append(poste['name'])
                        coordinates_bkb.append(poste['coordinates'])
                        break

            if end is None:
                print(f'Cabo {cabo["name"]} não conecta a nenhuma caixa de emenda óptica.')
            elif end == start:
                print(f'Cabo {cabo["name"]} conecta o POP diretamente à caixa {end}.')

    return routers
