# module utilities.py
from coordinate_correction import distancia_dois_pontos
import logging


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
                    abordagens += 2

        caixa['abordagens'] = abordagens


def calculate_connector_loss(connector_count, connector_loss):
    return round(connector_count * connector_loss, 2)


def calculate_splice_loss(splice_count, splice_loss):
    return round(splice_count * splice_loss, 2)


def calculate_cable_loss(cable_length, cable_attenuation):
    return round(cable_length * cable_attenuation, 2)


def calculate_final_signal(initial_signal, total_loss):
    return round(initial_signal - total_loss, 2)


def get_caixa_by_coordinate(caixas, coordinate):
    """Retorna a caixa com a coordenada especificada, ou None se não houver nenhuma."""
    for caixa in caixas:
        if caixa['coordinates'][0] == coordinate:
            return caixa
    return {'type': 'poste'}


def simulate_signal_transmission(pop, rotas, caixas, data_sheets, topology):
    ds = data_sheets
    initial_signal = float(pop['signal'])

    # Parâmetros de perda (ajuste conforme necessário)
    connector_loss = ds['Conectores']  # Perda por conector (dB)
    splice_loss = ds['Emendas_por_fusion']  # Perda por emenda (dB)
    cable_attenuation = ds['Fibra_1310nm']  # Atenuação do cabo (dB/km)
    hub_splitter = ds['Splitter_1x16'] if topology == '1x128' else ds['Splitter_1x8']
    nap_splitter = ds['Splitter_1x8']

    for rota in rotas:
        caixa = get_caixa_by_coordinate(caixas, rota['coordinates'][-1])
        # Inicializar perdas
        splitter_loss_total = 0

        # calcular perdas e sinal final para cada caixa
        connector_count = 4
        splice_count = 2  # 1 em cada extremidade do cabo
        splitter_loss_total += hub_splitter
        # Calcule o comprimento do cabo com base nas coordenadas das rotas
        coords = rota['coordinates']
        cable_length = round(sum(distancia_dois_pontos(coords[i], coords[i + 1])
                                 for i in range(len(coords) - 1)) / 1000, 2)  # Converter para km
        for coordinate in rota['coordinates'][1:]:
            elemento = get_caixa_by_coordinate(caixas, coordinate)
            if elemento['type'] == 'hub':
                splice_count += 2
                cable_length += 0.015 if rota['coordinates'][-1] == coordinate else 0.03


            elif elemento['type'] == 'ceo':
                cable_length += 0.03  # Adicionar 20m para o CEO

            elif elemento['type'] == 'nap':
                splice_count += 1  # Adicionar 10m para cada NAP
                cable_length += 0.01 if rota['coordinates'][-1] == coordinate else 0.02
                splitter_loss_total += nap_splitter if rota['coordinates'][-1] == coordinate else 0

        # Calcular perdas por conector
        connector_loss_total = calculate_connector_loss(connector_count, connector_loss)

        splice_loss_total = calculate_splice_loss(splice_count, splice_loss)

        cable_loss_total = calculate_cable_loss(cable_length, cable_attenuation)

        total_loss = (connector_loss_total + splice_loss_total + cable_loss_total + splitter_loss_total)
        final_signal = calculate_final_signal(initial_signal, total_loss)

        caixa['sinal_final'] = round(final_signal, 2)

        logging.info(f"Caixa {caixa['name']}-{caixa['coordinates']}: \n"
                     f"Sinal final = {final_signal} dBm\n"
                     f"({initial_signal} - {total_loss})\n"
                     f"({connector_loss_total} + {splice_loss_total} + {cable_loss_total} + {splitter_loss_total})\n"
                     f"({connector_count} * {connector_loss} + {splice_count} * {splice_loss} + {cable_length} * "
                     f"{cable_attenuation} + {splitter_loss_total})\n"
                     f"({total_loss})\n\n")
