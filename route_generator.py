def create_cables_routers(pop, postes, cabos, caixas, ceos, hubs):
    # Inicializa variáveis
    routers = {}
    router_count = 0

    # Busca cabos que partem do POP
    for cabo in cabos:
        if cabo['type'] == 'bkb' and cabo['coordinates'].startswith(pop['coordinates']):
            router_count += 1
            start = pop['name']
            end = None
            router = [pop['name']]
            cable = [cabo['name']]
            coordinates = cabo['coordinates'].split()
            print(f'cabo: {cabo["name"]}')
            # percorre a lista de coordenadas procurando interceptações do cabo
            for coordinate in coordinates:
                # Percorre a lista de postes procurando interceptações do cabo
                for poste in postes:
                    if poste['coordinates'] == coordinate:
                        print(poste['name'])
                        router.append(poste['name'])

                # Percorre a lista de caixas procurando interceptações do cabo
                for caixa in caixas:
                    if caixa['coordinates'] == coordinate:
                        print(caixa['name'])
                        router.append(caixa['name'])
                        end = caixa['name']
                        routers[cabo['name']] = {
                            'start': start,
                            'end': end,
                            'router': router,
                            'cable': cable,
                            'coordinates': coordinates,
                        }

                # Percorre a lista de CEO+HUBs procurando interceptações do cabo
                for ceo_hub in ceos + hubs:
                    if ceo_hub['coordinates'] == coordinate:
                        print(ceo_hub['type'])
                        router.append(ceo_hub['name'])

                        # Percorre a lista de cabos novamente procurando ramificações
                        for ramal in cabos:
                            print(f'routers: {routers}')
                            if ramal['type'] == 'ramal' and ramal['coordinates'].startswith(ceo_hub['coordinates']):
                                new_router_count = router_count + 1
                                new_router = list(router)
                                new_cable = list(cable)
                                new_coordinates = ramal['coordinates'].split()
                                new_end = None

                                # Percorre a lista de postes procurando interceptações do ramal
                                print(f'ramal: {ramal["name"]}')
                                for new_coordinate in new_coordinates:
                                    # Percorre a lista de postes procurando interceptações do ramal
                                    for poste in postes:
                                        if poste['coordinates'] == new_coordinate:
                                            print(poste['name'])
                                            new_router.append(poste['name'])
                                            break

                                    # Percorre a lista de NAPs procurando interceptações do ramal
                                    for nap in caixas:
                                        # Se a caixa for do tipo CTO/NAP, cria rota até o NAP
                                        if (nap['type'] == 'cto' or nap['type'] == 'nap') and \
                                                nap['coordinates'] == new_coordinate:
                                            print(nap['name'])
                                            router = routers[nap['name']]['router']
                                            cable = routers[nap['name']]['cable']
                                            coordinates = routers[nap['name']]['coordinates']
                                            routers[nap['name']] = {
                                                'start': nap['name'],
                                                'end': nap['name'],
                                                'router': router + [nap['name']],
                                                'cable': cable,
                                                'coordinates': coordinates + [nap['coordinates']],
                                            }
                                            break

                                        for l in range(len(cabos)):
                                            if cabos[l]['coordinates'][-1] == nap['coordinates'] and cabos[l]['type'] == 'ramal':
                                                router = routers[nap['name']]['router']
                                                cable = routers[nap['name']]['cable']
                                                coordinates = routers[nap['name']]['coordinates']
                                                routers[cabos[l]['start']] = {
                                                    'start': nap['name'],
                                                    'end': cabos[l]['end'],
                                                    'router': router + [cabos[l]['end']],
                                                    'cable': cable + [cabos[l]['name']],
                                                    'coordinates': coordinates + cabos[l]['coordinates'].split(),
                                                }
                                                routers[nap['name']]['end'] = cabos[l]['end']
                                                break
                                            else:
                                                continue
                                        break

                                        #routers[nap['name']]['router'] = new_router

                                if end is None:
                                    print(
                                        f'Cabo {cabo["name"]} não conecta a nenhuma caixa de emenda óptica.'
                                    )
                                elif end == start:
                                    print(
                                        f'Cabo {cabo["name"]} conecta o POP diretamente à caixa {end}.'
                                    )
                                return routers
