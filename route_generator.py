# module route_generator.py
def create_cables_routers(pop, postes, cabos, caixas):
    # Inicializa variáveis
    routers = []
    ceos = [ceo for ceo in caixas if ceo['type'] == 'ceo']
    hubs = [hub for hub in caixas if hub['type'] == 'hub']
    naps = [nap for nap in caixas if nap['type'] == 'nap']
    ramais = [ramal for ramal in cabos if ramal['type'] == 'ramal']

    # Busca cabos que partem do POP
    for cabo in cabos:
        if cabo['type'] == 'bkb' and cabo['coordinates'].startswith(pop['coordinates']):
            # iniciando uma nova rota
            start = pop['name']
            router_pop = [pop['name'].upper()]
            cables_pop = [cabo['name'].capitalize()]
            coordinates_clabe_pop = [pop['coordinates']]
            end = None

            print(f'cabo: {cabo["name"]}')
            # percorre a lista de coordenadas procurando interceptações do cabo
            for coordinate in cabo['coordinates'].split():

                # Percorre a lista de caixas procurando interceptações do cabo
                # testar depois se é melhor fazer uma lista com todas as caixas
                # testar depois essa situação
                for caixa in naps:
                    if caixa['coordinates'] == coordinate:
                        print(f"router criada: {caixa['name']}", end=' ')
                        router_caixa = list(router_pop)
                        router_caixa.append(caixa['name'])
                        coordinates_clabe_pop.append(caixa['coordinates'])
                        end = caixa['name'].upper()
                        routers.append({
                            'start': start,
                            'end': end,
                            'router': router_caixa,
                            'cable': coordinates_clabe_pop,
                            'coordinates': coordinates_clabe_pop,
                        })
                        print(routers[-1])
                        break

                # Percorre a lista de CEO+HUBs procurando interceptações do cabo
                for ceo_hub in ceos + hubs:
                    if ceo_hub['coordinates'] == coordinate:
                        print(f"router criada: {ceo_hub['name'].upper()}")
                        router_pop.append(ceo_hub['name'].upper())
                        router_ceo_hub = list(router_pop)
                        cable_ceo_hub = list(cables_pop)
                        coordinates_clabe_pop.append(ceo_hub['coordinates'])
                        coordinates_ceo_hub = list(coordinates_clabe_pop)
                        routers.append({
                            'start': start,
                            'end': ceo_hub['name'],
                            'router': router_ceo_hub,
                            'cable': cable_ceo_hub,
                            'coordinates': coordinates_ceo_hub,
                        })
                        print(routers[-1], '\n\n')
                        end = ceo_hub['name']

                        # Percorre a lista de cabos novamente procurando ramificações
                        for ramal in ramais:
                            if ramal['coordinates'].endswith(ceo_hub['coordinates']):
                                ramal['coordinates'] = ramal['coordinates'].split()[::-1]

                            elif ramal['coordinates'].startswith(ceo_hub['coordinates']):
                                router_ramal = list(router_ceo_hub)
                                cable_ramal = list(cable_ceo_hub)
                                cable_ramal.append(ramal['name'].capitalize())
                                coordinates_ramal = list(coordinates_ceo_hub)

                                print(f'ramal: {ramal["name"]}')
                                for new_coordinate in ramal['coordinates'].split():
                                    # Percorre a lista de NAPs procurando interceptações do ramal
                                    for nap in naps:
                                        # Se a caixa for do tipo CTO/NAP, cria rota até o NAP
                                        if (nap['type'] == 'cto' or nap['type'] == 'nap') and \
                                                nap['coordinates'] == new_coordinate:
                                            print(f"router criada: {nap['name'].upper()}")
                                            router_ramal.append(nap['name'].upper())
                                            router_nap = list(router_ramal)
                                            coordinates_ramal.append(nap['coordinates'])
                                            coordinates_nap = list(coordinates_ramal)
                                            end = nap['name'].upper()
                                            routers.append({
                                                'start': pop['name'],
                                                'end': end,
                                                'router': router_nap,
                                                'cable': cable_ramal,
                                                'coordinates': coordinates_nap,
                                            })
                                            print(routers[-1], '\n\n')
                                            break
                                    # Percorre a lista de postes procurando interceptações do ramal
                                    for poste in postes:
                                        if poste['coordinates'] == new_coordinate and \
                                                poste['coordinates'] not in coordinates_ramal:
                                            router_ramal.append(poste['name'])
                                            coordinates_ramal.append(poste['coordinates'])
                                            break

                for poste in postes:
                    if poste['coordinates'] == coordinate and poste['coordinates'] not in coordinates_clabe_pop:
                        router_pop.append(poste['name'])
                        coordinates_clabe_pop.append(poste['coordinates'])
                        break
            if end is None:
                print(
                    f'Cabo {cabo["name"]} não conecta a nenhuma caixa de emenda óptica.')
            elif end == start:
                print(f'Cabo {cabo["name"]} conecta o POP diretamente à caixa {end}.')
    return routers
