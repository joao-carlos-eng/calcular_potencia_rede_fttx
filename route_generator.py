# module route_generator.py
from copy import deepcopy


def get_cabos_by_type(cabos, type_):
    """Retorna uma lista de cabos com o tipo especificado."""
    return [cabo for cabo in cabos if cabo['type'] == type_]


def get_item_by_attribute(items, attribute, value):
    """Retorna a caixa com o atributo especificado, ou None se não houver nenhuma."""
    for item in items:
        if item[attribute] == value:
            return item
    return None


def get_item_by_coordinate(items, coordinate):
    """Retorna a caixa com a coordenada especificada, ou None se não houver nenhuma."""
    for item in items:
        if item['coordinates'][0] == coordinate:
            return item
    return None


def create_router(element, router_reference=None):
    """
    :param router_reference: rota de referência para caso a rota seja criada a partir de uma rota já existente
    :param element: elemento que será adicionado a rota
    :return:
    """
    if router_reference is not None:
        start = router_reference['start']
        router = router_reference['router']
        cable = router_reference['cable']
        coordinates = router_reference['coordinates']

        router.append(element['name'].upper())
        new_router = list(router)
        coordinates.append(element['coordinates'][0])
        new_coordinates = list(coordinates)
        end = element['name']
        return {
            'start': start,
            'end': end,
            'router': new_router,
            'cable': cable,
            'coordinates': new_coordinates,
        }
# Se não houver uma rota de referência, cria uma rota
# implementar esse trecho


def get_router_by_end(routers, end, coordinates=False):
    """Retorna uma rota com o fim especificado, ou None se não houver nenhum."""
    if coordinates:
        for router in routers:
            if router['coordinates'][-1] == end:
                return router
        return None
    else:
        for router in routers:
            if router['end'] == end:
                return router
        return None


def create_cables_routers(pop, poste_list, cabo_list, caixa_list):
    routers = []
    """Cria uma rota a partir do POP."""
    router_master = {
        'start': pop['name'],
        'end': None,
        'router': [pop['name'].upper()],
        'cable': [],
        'coordinates': [pop['coordinates'][0]],
    }

    naps = [caixa for caixa in caixa_list if caixa['type'] in ('nap', 'cto')]
    ceos_hubs = [caixa for caixa in caixa_list if caixa['type'] in ('ceo', 'hub')]

    # primeiro bloco, rotas a partir do POP
    backbones = get_cabos_by_type(cabo_list, 'bkb')
    # Busca cabos que partem do POP
    for cabo in reversed(backbones):
        cabo_start = cabo['coordinates'][0]
        cabo_end = cabo['coordinates'][-1]
        if cabo_start == router_master['coordinates'][0] or cabo_end == router_master['coordinates'][0]:
            if cabo_end == pop['coordinates'][0]: cabo['coordinates'].reverse()
            router_master['cable'].append(cabo['name'].capitalize())
            for coordinate in cabo['coordinates'][1:]:
                if get_item_by_coordinate(ceos_hubs, coordinate):
                    element = get_item_by_coordinate(ceos_hubs, coordinate)
                elif get_item_by_coordinate(naps, coordinate):
                    element = get_item_by_coordinate(naps, coordinate)
                else:
                    element = get_item_by_coordinate(poste_list, coordinate)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    router = create_router(element, router_master)
                    routers.append(router)

                elif element['type'] not in router_master['coordinates']:
                    router_master['router'].append(element['name'])
                    router_master['coordinates'].append(element['coordinates'][0])
            backbones.remove(cabo)

    for cabo in reversed(backbones):
        cabo_start = cabo['coordinates'][0]  # coordenada inicial do cabo
        if get_router_by_end(routers, cabo_start, coordinates=True):  # verifica se existe uma rota que comece no
            # final de outra

            router_derivacao = deepcopy(get_router_by_end(routers, cabo_start, coordinates=True))
            router_derivacao['cable'].append(cabo['name'].capitalize())
            for coordinate in cabo['coordinates'][1:]:
                if get_item_by_coordinate(ceos_hubs, coordinate):
                    element = get_item_by_coordinate(ceos_hubs, coordinate)
                elif get_item_by_coordinate(naps, coordinate):
                    element = get_item_by_coordinate(naps, coordinate)
                else:
                    element = get_item_by_coordinate(poste_list, coordinate)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    print(f'{element["name"]} abordada pelo cabo {cabo["name"]}#2')
                    router = create_router(element, router_derivacao)
                    routers.append(router)
                    print('router: ', router)

                elif element['type'] not in router_derivacao['coordinates']:
                    print(f'{element["name"]} abordada pelo cabo {cabo["name"]}#3')
                    router_derivacao['router'].append(element['name'])
                    router_derivacao['coordinates'].append(element['coordinates'][0])
            backbones.remove(cabo)
    return routers

# segundo bloco, rotas a partir dos ceos/hubs
# Busca cabos que partem das ceos/hubs


'''ramais = get_cabos_by_type(cabo_list, 'ramal')
for ramal in ramais:
    end = None
    ramal_start = ramal['coordinates'][0]
    ramal_end = ramal['coordinates'][-1]
    ceo_hub = get_item_by_coordinate(ceos_hubs, ramal_start)
    # verifica se o ramal está invertido e corrige
    if ramal_end in [caixa['coordinates'][0] for caixa in ceos_hubs]:
        print(f'Cabo do ramal {ramal["name"]} invertido. Corrigindo...')
        ramal['coordinates'] = ramal['coordinates'][::-1]
        ramal_start = ramal['coordinates'][0]
        ceo_hub = get_item_by_coordinate(ceos_hubs, ramal_start)

    elif ceo_hub is not None:
        print(f'Ramal {ramal["name"]} interceptado pela ceo {ceo_hub["name"]}#4')
        aux = get_router_by_end(routers, ceo_hub['name'])
        router_ramal = list(aux['router'])
        cable_ramal = list(aux['cable'])
        cable_ramal.append(ramal['name'].capitalize())
        coordinates_ramal = list(aux['coordinates'])

        for coordinate in ramal['coordinates'][1:]:
            caixa = get_item_by_coordinate(naps, coordinate)
            if caixa is not None:
                print(f'Caixa {caixa["name"]} interceptada pelo cabo {ramal["name"]}#5')
                router_ramal.append(caixa['name'].upper())
                router_nap = list(router_ramal)
                coordinates_ramal.append(caixa['coordinates'][0])
                coordinates_nap = list(coordinates_ramal)
                end = caixa['name'].upper()
                routers.append(
                    create_router(start, end, router_nap, cable_ramal, coordinates_nap)
                )
            poste = get_item_by_coordinate(poste_list, coordinate)
            if poste is not None and poste['coordinates'][0] not in coordinates_ramal:
                router_ramal.append(poste['name'])
                coordinates_ramal.append(poste['coordinates'][0])
            
            for derivacao in ramais:
                if derivacao['coordinates'][0] == new_coordinate and derivacao != ramal:
                    for cord_derivacao in derivacao['coordinates'][1:]:
                        caixa = get_item_by_coordinate(naps, cord_derivacao)
                        if caixa is not None:
                            print(
                                f'Caixa {caixa["name"]} '
                                f'interceptada pelo cabo {derivacao["name"]}#6')
                            router_derivacao = list(router_nap)
                            cable_derivacao = list(cable_ramal)
                            cable_derivacao.append(derivacao['name'].capitalize())
                            coordinates_derivacao = list(coordinates_nap)
                            router_derivacao.append(caixa['name'].upper())
                            coordinates_derivacao.append(caixa['coordinates'][0])
                            end = caixa['name'].upper()
                            routers.append(
                                create_router(start, end, router_derivacao, cable_derivacao,
                                              coordinates_derivacao)
                            )
                            break
                    break
        
    derivacoes = get_cabos_by_type(cabo_list, 'bkb')
    for derivacao in derivacoes:
        if derivacao['coordinates'][0] == ceo_hub['coordinates'][0] and derivacao != cabo:
            for cord_derivacao in derivacao['coordinates'][1:]:
                caixa = get_item_by_coordinate(ceos_hubs, cord_derivacao)
                if caixa is not None:
                    print(f'Caixa {caixa["name"]} interceptada pelo cabo {derivacao["name"]}#7')
                    router_derivacao = list(router_ceo_hub)
                    cable_derivacao = list(cables)
                    cable_derivacao.append(derivacao['name'].capitalize())
                    coordinates_derivacao = list(coordinates_ceo_hub)
                    router_derivacao.append(caixa['name'].upper())
                    coordinates_derivacao.append(caixa['coordinates'][0])
                    end = caixa['name'].upper()
                    routers.append(
                        create_router(start, end, router_derivacao, cable_derivacao,
                                      coordinates_derivacao)
                    )
                    break
            break
        break'''
