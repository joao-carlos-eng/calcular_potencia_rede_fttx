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
        if subfolder_name == 'fttx':
            fttx_folder = subfolder
            for placemark in fttx_folder.Placemark:
                if placemark.name.text.lower() == 'pop':
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
                    for placemark in subsubfolder.Placemark:
                        try:
                            name = placemark.name.text.strip()
                        except AttributeError:
                            name = f'CEO {subsubfolder.index(placemark) + 1}'
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
                                        sub_ramal_name = (sub_ramal.name.text.lower())
                                        if sub_ramal_name == 'cb':
                                            for (placemark) in sub_ramal.Placemark:
                                                coordinates = placemark_coordinates(placemark).split(' ')
                                                ramal['cbs'].append(
                                                    {
                                                        'name': placemark.name.text.strip(),
                                                        'coordinates': coordinates,
                                                        'type': 'cb',
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
            except AttributeError:
                print('Não há postes no arquivo KML.')

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


def validar_elementos(caixas, cabos):
    """
    Valida os elementos, verificando se todas as caixas estão em algum cabo e se
    -os bkb's começam e terminam em uma CEO ou HUB
    -os ramais começam em uma CEO e termina em uma NAP.

    Args:
        caixas: uma lista contendo as informações das caixas.
        cabos: uma lista contendo as informações dos cabos.

    Returns:
        uma lista contendo os elementos validos
    """
    coords_caixas = [cx['coordinates'][0] for cx in caixas]
    coords_cabos = [co for ca in cabos for co in ca['coordinates']]

    coords_cabos = set(coords_cabos)
    for cabo in cabos:
        if cabo['type'] == 'bkb':
            if cabo['coordinates'][0] not in coords_caixas:
                print(f'Caixa inicial do {cabo["name"]} não encontrada')
            if cabo['coordinates'][-1] not in coords_caixas:
                print(f'Caixa final do {cabo["name"]} não encontrada')

        elif cabo['type'] == 'ramal':
            if cabo['coordinates'][0] not in coords_caixas:
                print(f'Caixa {cabo["name"]} não encontrada')
            else:
                start = cabo['coordinates'][0]
            if cabo['coordinates'][-1] not in coords_caixas:
                print(f'Caixa {cabo["name"]} não encontrada')
            else:
                end = cabo['coordinates'][-1]

    for caixa in caixas:
        if caixa['coordinates'][0] not in coords_cabos:
            print(f'Caixa {caixa["name"]} não encontrada')
