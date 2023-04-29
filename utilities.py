# module utilities.py
from coordinate_correction import distancia_dois_pontos


def calculate_cable_approaches(caixas, cabos):
    """
    Calcula a quantidade de abordagens de cada cabo em cada caixa
    :param caixas: lista de dicionários com informações das caixas de emenda
    :param cabos: lista de dicionários com informações dos cabos
    :return: None
    """
    for caixa in caixas:
        abordagens = 0
        coord_cx = caixa['coordinates'][0]
        for cabo in cabos:
            co = cabo['coordinates']
            if coord_cx in co:
                if co[0] == coord_cx or co[-1] == coord_cx:
                    abordagens += 1
                else:
                    print(
                        f'Caixa {caixa["name"]} abordada pelo cabo {cabo["name"]}, '
                        f'no trecho {co.index(caixa["coordinates"][0])}')
                    abordagens += 2
        caixa['abordagens'] = abordagens


def calculate_connector_loss(connector_count, connector_loss):
    return connector_count * connector_loss


def calculate_splice_loss(splice_count, splice_loss):
    return splice_count * splice_loss


def calculate_cable_loss(cable_length, cable_attenuation):
    return cable_length * cable_attenuation


def calculate_final_signal(initial_signal, total_loss):
    return initial_signal - total_loss


def get_caixa_by_name(caixas, caixa_name):
    for caixa in caixas:
        if caixa['name'] == caixa_name:
            return caixa
    return {'type': None}


def simulate_signal_transmission(pop, rotas, caixas, data_sheets, topology):
    ds = data_sheets
    initial_signal = float(pop['signal'])

    # Parâmetros de perda (ajuste conforme necessário)
    connector_loss = ds['Conectores']  # Perda por conector (dB)
    splice_loss = ds['Emendas_por_fusion']  # Perda por emenda (dB)
    cable_attenuation = ds['Fibra_1310nm']  # Atenuação do cabo (dB/km)
    hub_splitter = ds['Splitter_1x16'] if topology == '1x128' else ds['Splitter_1x8']
    nap_splitter = ds['Splitter_1x8']

    for caixa in caixas:
        # Inicializar perdas
        connector_loss_total = 0
        splice_loss_total = 0
        cable_loss_total = 0
        splitter_loss_total = 0

        # Encontrar a rota que conecta a caixa atual
        rota_caixa = None
        for rota in rotas:
            if rota['end'] == caixa['name']:
                rota_caixa = rota
                break

        if rota_caixa:
            # calcular perdas e sinal final para cada caixa
            connector_count = 4
            splice_count = 2  # 1 em cada extremidade do cabo

            # Calcule o comprimento do cabo com base nas coordenadas das rotas
            coords = rota_caixa['coordinates']
            cable_length = sum(distancia_dois_pontos(coords[i], coords[i + 1])
                               for i in range(len(coords) - 1)) / 1000  # Converter para km
            for caixa_name in rota_caixa['router']:
                if get_caixa_by_name(caixas, caixa_name)['type'] == 'hub':
                    splice_count += 2
                    # Adicionar 10m para cada hub
                    cable_length += 0.01 if rota_caixa['router'][-1] == caixa_name else 0.02
                    splitter_loss_total += hub_splitter

                elif get_caixa_by_name(caixas, caixa_name)['type'] == 'ceo':
                    splice_count += 1
                    cable_length += 0.02  # Adicionar 20m para o CEO
                elif get_caixa_by_name(caixas, caixa_name)['type'] == 'nap':
                    splice_count += 1
                    # Adicionar 10m para cada NAP
                    cable_length += 0.01 if caixa_name == caixa['name'] else 0.02
                    splitter_loss_total += nap_splitter if caixa_name == caixa['name'] else 0

            # Calcular perdas por conector
            connector_loss_total = calculate_connector_loss(connector_count, connector_loss)

            splice_loss_total = calculate_splice_loss(splice_count, splice_loss)

            cable_loss_total = calculate_cable_loss(cable_length, cable_attenuation)

        total_loss = (connector_loss_total + splice_loss_total + cable_loss_total + splitter_loss_total)
        final_signal = calculate_final_signal(initial_signal, total_loss)

        caixa['sinal_final'] = round(final_signal)

        print(f"Caixa {caixa['name']}: Sinal final = {final_signal} dBm")
