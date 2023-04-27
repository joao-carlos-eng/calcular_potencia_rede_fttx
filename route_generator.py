# module route_generator.py


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


def create_router(start, end, router, cable, coordinates):
    return {
        'start': start,
        'end': end,
        'router': router,
        'cable': cable,
        'coordinates': coordinates,
    }


def create_cables_routers(pop, poste_list, cabo_list, caixa_list):
    routers = []
    """Cria uma rota a partir do POP."""
    router = [pop['name'].upper()]
    coordinates = [pop['coordinates'][0]]
    start = pop['name']
    cables = []

    naps = [caixa for caixa in caixa_list if caixa['type'] in ('nap', 'cto')]
    ceos_hubs = [caixa for caixa in caixa_list if caixa['type'] in ('ceo', 'hub')]

    # primeiro bloco, rotas a partir do POP
    # Busca cabos que partem do POP
    backbones = get_cabos_by_type(cabo_list, 'bkb')
    for cabo in backbones:
        end = None
        if cabo['coordinates'][0] == pop['coordinates'][0]:
            cables.append(cabo['name'].capitalize())
            router_bkb = list(router)
            coordinates_bkb = list(coordinates)
            print([ceo['name'] for ceo in ceos_hubs])
            print()
            # Percorre a lista de coordenadas procurando interceptações do cabo
            for coordinate in cabo['coordinates'][1:]:
                caixa = get_item_by_coordinate(naps, coordinate)
                if caixa is not None:
                    print(f'Caixa {caixa["name"]} interceptada pelo cabo {cabo["name"]}2#')
                    router_bkb.append(caixa['name'].upper())
                    coordinates_bkb.append(caixa['coordinates'][0])
                    end = caixa['name'].upper()
                    routers.append(create_router(start, end, router_bkb, cables, coordinates_bkb))

                for ceo_hub in ceos_hubs:

                    if ceo_hub['coordinates'][0] == coordinate:
                        print(f'Caixa {ceo_hub["name"]} interceptada pelo cabo {cabo["name"]}#3')
                        router_bkb.append(ceo_hub['name'].upper())
                        router_ceo_hub = list(router_bkb)
                        coordinates_bkb.append(ceo_hub['coordinates'][0])
                        coordinates_ceo_hub = list(coordinates_bkb)
                        end = ceo_hub['name']
                        routers.append(create_router(start, end, router_ceo_hub, cables, coordinates_ceo_hub))
                        break

                        '''ramais = get_cabos_by_type(cabo_list, 'ramal')
                        for ramal in ramais:
                            # verifica se o ramal está invertido e corrige
                            if ramal['coordinates'][-1] == ceo_hub['coordinates'][0]:
                                print(f'Cabo do ramal {ramal["name"]} invertido. Corrigindo...')
                                ramal['coordinates'] = ramal['coordinates'][::-1]

                            elif ramal['coordinates'][0] == ceo_hub['coordinates'][0]:
                                print(f'Ramal {ramal["name"]} interceptado pelo cabo {cabo["name"]}#4')
                                router_ramal = list(router_bkb)
                                cable_ramal = list(cables)
                                cable_ramal.append(ramal['name'].capitalize())
                                coordinates_ramal = list(coordinates_bkb)

                                for new_coordinate in ramal['coordinates'][1:]:
                                    caixa = get_item_by_coordinate(naps, new_coordinate)
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
                                    poste = get_item_by_coordinate(poste_list, new_coordinate)
                                    if poste is not None:
                                        router_ramal.append(poste['name'])
                                        coordinates_ramal.append(poste['coordinates'][0])
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
                poste = get_item_by_coordinate(poste_list, coordinate)
                if poste is not None:
                    router_bkb.append(poste['name'])
                    coordinates_bkb.append(poste['coordinates'][0])

        if end is None:
            print(f'Cabo {cabo["name"]} não conecta a nenhuma caixa de emenda óptica.')
        elif end == start:
            print(f'Cabo {cabo["name"]} conecta o POP diretamente à caixa {end}.')

    return routers
