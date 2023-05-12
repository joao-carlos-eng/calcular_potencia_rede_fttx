# modulo data_extraction.py
def placemark_coordinates(placemark):
    geometry = placemark.find('{http://www.opengis.net/kml/2.2}Point')
    if geometry is None:
        geometry = placemark.find('{http://www.opengis.net/kml/2.2}LineString')
    coordinates = geometry.coordinates.text.strip()
    return coordinates


def extract_data(kml):
    postes = []
    bkbs = []
    ceos = []
    ramais = []
    pop = None

    # Busca a pasta exemplo-rede-fttx
    rede_folder = kml.Document.Folder
    for subfolder in rede_folder.Folder:
        subfolder_name = subfolder.name.text.lower()
        if 'ftt' in subfolder_name:
            fttx_folder = subfolder
            for placemark in fttx_folder.Placemark:
                if 'pop' in placemark.name.text.lower():
                    coordinates = [placemark_coordinates(placemark)]
                    pop = {
                        'name': placemark.name.text.strip(),
                        'coordinates': coordinates,
                        'type': 'pop',
                    }
            for subsubfolder in fttx_folder.Folder:
                subsubfolder_name = subsubfolder.name.text.lower()
                if subsubfolder_name == 'bkb':
                    for placemark in subsubfolder.Placemark:
                        try:
                            name = placemark.name.text.strip()
                        except AttributeError:
                            name = f'BKB {subsubfolder.index(placemark) + 1}'
                        coordinates = placemark_coordinates(placemark).split(' ')
                        bkbs.append(
                            {
                                'name': name,
                                'coordinates': coordinates,
                                'bkb_id': subsubfolder.index(placemark) + 1,
                                'type': 'bkb',
                            }
                        )
                elif subsubfolder_name in ['ceos', 'hubs']:
                    cnt = 0
                    for placemark in subsubfolder.Placemark:
                        cnt += 1
                        try:
                            name = placemark.name.text.strip()
                        except AttributeError:
                            name = None
                        if name == 'HUB' or name is None:
                            name = f'CEO {cnt}'
                        coordinates = [placemark_coordinates(placemark)]
                        type_ = 'ceo' if 'ceo' in subsubfolder_name.lower() else 'hub'
                        ceos.append(
                            {
                                'name': name,
                                'coordinates': coordinates,
                                'type': type_,
                            }
                        )
                elif 'placa' in subsubfolder_name:
                    try:
                        for sub_placa in subsubfolder.Folder:
                            if (
                                    'ramal' in sub_placa.name.text.lower()
                                    or 'rede' in sub_placa.name.text.lower()
                            ):
                                ramal = {
                                    'cxs': [],
                                    'cbs': [],
                                    'name': sub_placa.name.text.strip(),
                                    'type': 'ramal',
                                }
                                try:
                                    for sub_ramal in sub_placa.Folder:
                                        cnt = 0
                                        sub_ramal_name = (sub_ramal.name.text.lower())
                                        if sub_ramal_name == 'cb':
                                            for placemark in sub_ramal.Placemark:
                                                cnt += 1
                                                name = placemark.name.text.strip()
                                                if name == 'Caminho sem título' or not name:
                                                    name = f'CB {cnt} - {ramal["name"]}'
                                                coordinates = placemark_coordinates(placemark).split(' ')
                                                ramal['cbs'].append(
                                                    {
                                                        'name': name,
                                                        'coordinates': coordinates,
                                                        'type': 'ramal',
                                                    }
                                                )
                                        elif sub_ramal_name in [
                                            'cx',
                                            'naps',
                                            'ctos',
                                        ]:
                                            for (placemark) in sub_ramal.Placemark:
                                                try:
                                                    name = (placemark.name.text.strip())
                                                except AttributeError:
                                                    name = f'CX {sub_ramal.index(placemark) + 1}'
                                                coordinates = [placemark_coordinates(placemark)]
                                                ramal['cxs'].append(
                                                    {
                                                        'name': name,
                                                        'coordinates': coordinates,
                                                        'type': 'nap',
                                                    }
                                                )
                                    ramais.append(ramal)
                                except AttributeError:
                                    # erro quando não tem subpastas de ramais
                                    pass
                    except AttributeError:
                        # erro quando não tem subpastas de placas
                        pass
        elif subfolder_name == 'mapeamento' or subfolder_name == 'poste':
            poste_pop = None
            try:
                for placemark in subfolder.Placemark:
                    name = f'Poste {subfolder.index(placemark) + 1}'
                    coordinates = [placemark_coordinates(placemark)]
                    postes.append(
                        {
                            'name': name,
                            'coordinates': coordinates,
                            'type': 'poste',
                        }
                    )
                    if coordinates == pop['coordinates']:
                        poste_pop = postes[-1]
                if not poste_pop:
                    postes.append({
                        'name': 'Poste POP',
                        'coordinates': pop['coordinates'],
                        'type': 'poste',
                    })
                print(f'Foram encontrados {len(postes)} postes.')
            except AttributeError:
                print('Não há postes no arquivo KML.')

    if pop is None:
        info_pop = input('Informe o nome do POP: ')
        coordinates_pop = input('Informe as coordenadas do POP: ')
        pop = {
            'name': info_pop,
            'coordinates': coordinates_pop,
            'type': 'pop',
        }

    return {
        'pop': pop,
        'postes': postes,
        'bkbs': bkbs,
        'ceos': ceos,
        'ramais': ramais,
    }


def extract_cxs_and_cbs(ramais):
    """
    Extrai todas as caixas e trajetos dos ramais.

    Args:
        ramais: uma lista contendo as informações dos ramais.

    Returns:
        Uma tupla contendo as seguintes informações:
        - caixas: informações sobre as caixas encontradas nos ramais.
        - trajetos: informações sobre os trajetos encontrados nos ramais.
    """
    caixas = []
    cabos = []
    for ramal in ramais:
        for cx in ramal['cxs']:
            cx['name_audiencia'] = ramal['name'] + ': ' + cx['name']
            caixas.append(cx)
        for cb in ramal['cbs']:
            cb['name_audiencia'] = ramal['name'] + ': ' + cb['name']
            cabos.append(cb)

    return caixas, cabos


def validar_elementos(caixas, cabos, pop):
    """
    Valida os elementos, verificando se todas as caixas estão em algum cabo e se
    -os bkb's começam e terminam em uma CEO ou HUB
    -os ramais começam em uma CEO e termina em uma NAP.

    Args:
        caixas: uma lista contendo as informações das caixas.
        cabos: uma lista contendo as informações dos cabos.
        pop: um dicionario contendo as informações do pop.

    Returns:
        uma lista contendo os elementos validos
    """
    coords_naps = [nap['coordinates'][0] for nap in caixas if nap['type'] == 'nap' or nap['type'] == 'cto']
    coords_ceos = [hub['coordinates'][0] for hub in caixas if hub['type'] == 'hub' or hub['type'] == 'ceo']

    coords_bkb = [co for bkb in cabos if bkb['type'] == 'bkb' for co in bkb['coordinates']]
    coords_ramais = [co for ramal in cabos if ramal['type'] == 'ramal' for co in ramal['coordinates']]

    for cabo in cabos:
        start = cabo['coordinates'][0]
        end = cabo['coordinates'][-1]
        cx_start = False
        cx_end = False
        if cabo['type'] == 'bkb':

            if start not in pop['coordinates'] and start not in coords_ceos:
                print(f'Caixa inicial do {cabo["name"]} não encontrada')
            else:
                cx_start = True
            if end not in coords_ceos and end not in coords_naps:
                print(f'Caixa final do {cabo["name"]} não encontrada')
            else:
                cx_end = True
            if cx_start and cx_end:
                print(f'BKB {cabo["name"]} está conectado')

        elif cabo['type'] == 'ramal':
            if start not in coords_ceos and start not in coords_naps:
                print(f'Caixa inicial do {cabo["name"]} não encontrada')
            else:
                cx_start = True
            if end not in coords_naps:
                print(f'Caixa final do {cabo["name"]} não encontrada')
            else:
                cx_end = True

            if cx_start and cx_end:
                print(f'ramal {cabo["name"]} está conectado')

    for caixa in caixas:
        co = caixa['coordinates'][0]
        if co not in coords_ramais and co not in coords_bkb:
            print(f'Caixa {caixa["name"]} não encontrada em nenhum cabo')
            print(f'caixa: {caixa["coordinates"][0].split(",")[1]},{caixa["coordinates"][0].split(",")[0]}')
