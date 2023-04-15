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
    placas = []
    ramais = []
    cbs = []
    cxs = []
    pop = None

    # Busca a pasta exemplo-rede-fttx
    rede_folder = kml.Document.Folder
    print(f'rede_folder: {rede_folder.name.text}')
    for subfolder in rede_folder.Folder:
        subfolder_name = subfolder.name.text.lower()
        print(f'subfolder_name: {subfolder_name}')
        if subfolder_name == 'fttx':
            fttx_folder = subfolder
            for placemark in fttx_folder.Placemark:
                if placemark.name.text.lower() == 'pop':
                    coordinates = placemark_coordinates(placemark)
                    pop = {
                        'name': placemark.name.text.strip(),
                        'coordinates': coordinates,
                    }
            for subsubfolder in fttx_folder.Folder:
                subsubfolder_name = subsubfolder.name.text.lower()
                print(f'subsubfolder_name: {subsubfolder_name}')
                if subsubfolder_name == 'bkb':
                    for placemark in subsubfolder.Placemark:
                        try:
                            name = placemark.name.text.strip()
                        except AttributeError:
                            name = f'BKB {subsubfolder.index(placemark)+1}'
                        coordinates = placemark_coordinates(placemark)
                        bkbs.append(
                            {
                                'name': name,
                                'coordinates': coordinates,
                                'bkb_id': subsubfolder.index(placemark) + 1,
                            }
                        )
                elif subsubfolder_name in ['ceos', 'hubs']:
                    for placemark in subsubfolder.Placemark:
                        try:
                            name = placemark.name.text.strip()
                        except AttributeError:
                            name = f'CEO {subsubfolder.index(placemark)+1}'
                        coordinates = placemark_coordinates(placemark)
                        ceos.append(
                            {
                                'name': name,
                                'coordinates': coordinates,
                            }
                        )
                elif 'placa' in subsubfolder_name:
                    placas.append(subsubfolder)
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
                                }
                                try:
                                    for sub_ramal in sub_placa.Folder:
                                        sub_ramal_name = sub_ramal.name.text.lower()
                                        if sub_ramal_name == 'cb':
                                            for placemark in sub_ramal.Placemark:
                                                coordinates = (
                                                    placemark_coordinates(
                                                        placemark
                                                    )
                                                )
                                                ramal['cbs'].append(
                                                    {
                                                        'name': placemark.name.text.strip(),
                                                        'coordinates': coordinates,
                                                    }
                                                )
                                                cbs.append(ramal['cbs'][-1]) #verificar se é necessário
                                        elif sub_ramal_name in [
                                            'cx',
                                            'naps',
                                            'ctos',
                                        ]:
                                            for placemark in sub_ramal.Placemark:
                                                try:
                                                    name = placemark.name.text.strip()
                                                except AttributeError:
                                                    name = f'CX {sub_ramal.index(placemark)+1}'
                                                coordinates = (
                                                    placemark_coordinates(
                                                        placemark
                                                    )
                                                )
                                                ramal['cxs'].append(
                                                    {
                                                        'name': name,
                                                        'coordinates': coordinates,
                                                    }
                                                )
                                                cxs.append(ramal['cxs'][-1]) #verificar se é necessário
                                                print(f'cx: {ramal["cxs"][-1]}')
                                    ramais.append(ramal)
                                except AttributeError:
                                    # erro quando não tem subpastas de ramais
                                    pass
                    except AttributeError:
                        # erro quando não tem subpastas de placas
                        pass
        elif subfolder_name == 'mapeamento' or subfolder_name == 'poste':
            for placemark in subfolder.Placemark:
                try:
                    name = placemark.name.text.strip()
                except AttributeError:
                    name = f'Poste {subfolder.index(placemark)+1}'
                coordinates = placemark_coordinates(placemark)
                postes.append(
                    {
                        'name': name,
                        'coordinates': coordinates,
                    }
                )

    return {
        'pop': pop,
        'postes': postes,
        'bkbs': bkbs,
        'ceos': ceos,
        'placas': placas,
        'ramais': ramais,
        'cbs': cbs,
        'cxs': cxs,
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
    trajetos = []
    for ramal in ramais:
        print(f'ramal: {ramal}')
        for cx in ramal['cxs']:
            caixas.append(cx)
        for cb in ramal['cbs']:
            trajetos.append(cb)

    return caixas, trajetos
