def extract_data(kml):
    postes = []
    bkbs = []
    ceos = []
    placas = []
    ramais = []
    cbs = []
    cxs = []
    pop = None

    for folder in kml.Document.Folder:
        folder_name = folder.xpath("./kml:name", namespaces={"kml": "http://www.opengis.net/kml/2.2"})
        if not folder_name:
            continue
        folder_name = folder_name[0].text.lower()
        if folder_name == 'FTTx':
            for subfolder in folder.Folder:
                if subfolder.name == 'BKB':
                    for placemark in subfolder.Placemark:
                        bkbs.append(
                            {
                                'name': placemark.name,
                                'coordinates': placemark.Point.coordinates.text.strip(),
                            }
                        )
                elif subfolder.name == 'CEOs':
                    for placemark in subfolder.Placemark:
                        ceos.append(
                            {
                                'name': placemark.name,
                                'coordinates': placemark.Point.coordinates.text.strip(),
                            }
                        )
                elif 'placa' in subfolder.name.lower():
                    placas.append(subfolder)
                    for placa_folder in subfolder.Folder:
                        if 'ramal' in placa_folder.name.lower():
                            ramais.append(placa_folder)
                            for ramal_folder in placa_folder.Folder:
                                if ramal_folder.name.lower() == 'cb':
                                    for placemark in ramal_folder.Placemark:
                                        cbs.append(
                                            {
                                                'name': placemark.name,
                                                'coordinates': placemark.LineString.coordinates.text.strip(),
                                            }
                                        )
                                elif ramal_folder.name.lower() == 'cx':
                                    for placemark in ramal_folder.Placemark:
                                        cxs.append(
                                            {
                                                'name': placemark.name,
                                                'coordinates': placemark.Point.coordinates.text.strip(),
                                            }
                                        )
                elif subfolder.name.lower() == 'pop':
                    pop = subfolder.Placemark[0]
        elif hasattr(folder, 'name') and folder_name.lower() == 'mapeamento':

            for placemark in folder.Placemark:
                postes.append(
                    {
                        'name': placemark.name,
                        'coordinates': placemark.Point.coordinates.text.strip(),
                    }
                )

    return pop, postes, bkbs, ceos, placas, ramais, cbs, cxs


def extract_cxs_and_cbs(ramais):
    caixas = []
    trajetos = []
    for ramal in ramais:
        for cx in ramal['cx']:
            caixas.append(cx)
        for cb in ramal['cb']:
            trajetos.append(cb)
    return caixas, trajetos
