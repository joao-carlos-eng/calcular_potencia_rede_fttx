# module route_generator.py
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_cabos_by_type(cabos, type_):
    """Retorna uma lista de cabos com o tipo especificado."""
    return [cabo for cabo in cabos if cabo['type'] == type_]


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

    else:
        return {
            'start': element['name'],
            'end': element['name'],
            'router': [element['name'].upper()],
            'cable': [],
            'coordinates': [element['coordinates'][0]],
        }


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


def get_element_by_list_coordinates(coordinate, list_ceos=None, list_naps=None, poste_list=None):
    if get_item_by_coordinate(list_ceos, coordinate):
        return get_item_by_coordinate(list_ceos, coordinate)
    elif get_item_by_coordinate(list_naps, coordinate):
        return get_item_by_coordinate(list_naps, coordinate)
    else:
        return get_item_by_coordinate(poste_list, coordinate)


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
                element = get_element_by_list_coordinates(coordinate, list_ceos=ceos_hubs, list_naps=naps,
                                                          poste_list=poste_list)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    router = create_router(element, router_master)
                    logging.info(f'router {router["end"]} criado a partir do POP')
                    routers.append(router)

                elif element['type'] == 'poste' and element['coordinates'][0]:
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
                element = get_element_by_list_coordinates(coordinate, list_ceos=ceos_hubs, list_naps=naps,
                                                          poste_list=poste_list)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    router = create_router(element, router_derivacao)
                    logging.info(f'router {router["end"]} criado a partir de {router_derivacao["end"]}')
                    routers.append(router)

                elif element['type'] == 'poste' and element['coordinates'][0]:
                    router_derivacao['router'].append(element['name'])
                    router_derivacao['coordinates'].append(element['coordinates'][0])
            backbones.remove(cabo)
            del router_derivacao

    # segundo bloco, rotas a partir dos ceos/hubs
    ramais = get_cabos_by_type(cabo_list, 'ramal')
    # Busca cabos que partem das ceos/hubs
    for cabo in reversed(ramais):
        cabo_start = cabo['coordinates'][0]  # coordenada inicial do cabo
        if get_router_by_end(routers, cabo_start, coordinates=True):
            router_ramal = deepcopy(get_router_by_end(routers, cabo_start, coordinates=True))
            router_ramal['cable'].append(cabo['name'].capitalize())
            for coordinate in cabo['coordinates'][1:]:
                element = get_element_by_list_coordinates(coordinate, list_ceos=ceos_hubs, list_naps=naps,
                                                          poste_list=poste_list)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    router = create_router(element, router_ramal)
                    logging.info(f'router {router["end"]} criado a partir de {router_ramal["end"]}')
                    routers.append(router)

                elif element['type'] == 'poste' and element['coordinates'][0]:
                    router_ramal['router'].append(element['name'])
                    router_ramal['coordinates'].append(element['coordinates'][0])
            ramais.remove(cabo)
            del router_ramal

    # Busca cabos que partem das naps
    for cabo in reversed(ramais):
        cabo_start = cabo['coordinates'][0]
        if get_router_by_end(routers, cabo_start, coordinates=True):
            router_ramal = deepcopy(get_router_by_end(routers, cabo_start, coordinates=True))
            router_ramal['cable'].append(cabo['name'].capitalize())
            for coordinate in cabo['coordinates'][1:]:
                element = get_element_by_list_coordinates(coordinate, list_ceos=ceos_hubs, list_naps=naps,
                                                          poste_list=poste_list)

                if element['type'] in ('nap', 'cto', 'ceo', 'hub'):
                    router = create_router(element, router_ramal)
                    logging.info(f'router {router["end"]} criado a partir de {router_ramal["end"]}')
                    routers.append(router)

                elif element['type'] == 'poste' and element['coordinates'][0]:
                    router_ramal['router'].append(element['name'])
                    router_ramal['coordinates'].append(element['coordinates'][0])
            ramais.remove(cabo)
            del router_ramal

    for cabo in backbones:
        if cabo:
            print('Cabo não utilizado: {}'.format(cabo['name']))
    for cabo in ramais:
        if cabo:
            print('Cabo não utilizado: {}'.format(cabo['name']))

    return routers
