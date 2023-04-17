# module utilities
from coordinate_correction import distancia_dois_pontos


def calculate_cable_approaches(caixas):
    for caixa in caixas:
        # Neste exemplo, vamos assumir que a quantidade de abordagens é igual ao número da caixa
        # Você pode substituir esta lógica pela lógica correta para calcular as abordagens
        abordagens = int(caixa['name'].split()[-1])
        caixa['abordagens'] = abordagens


def calculate_connector_loss(connector_count, connector_loss):
    return connector_count * connector_loss


def calculate_splice_loss(splice_count, splice_loss):
    return splice_count * splice_loss


def calculate_cable_loss(cable_length, cable_attenuation):
    return cable_length * cable_attenuation


def calculate_splitter_loss(splitter):
    return splitter['input'] - splitter['output']


def calculate_total_loss(
    connector_loss, splice_loss, cable_loss, splitter_loss
):
    return connector_loss + splice_loss + cable_loss + splitter_loss


def calculate_final_signal(initial_signal, total_loss):
    return initial_signal - total_loss


def simulate_signal_transmission(pop, rotas, caixas):
    initial_signal = float(input('Insira o sinal inicial (dBm): '))

    # Parâmetros de perda (ajuste conforme necessário)
    connector_loss = 0.5  # Perda por conector (dB)
    splice_loss = 0.1  # Perda por emenda (dB)
    cable_attenuation = 0.3  # Atenuação do cabo (dB/km)

    for caixa in caixas:
        # Inicializar perdas
        connector_loss_total = 0
        splice_loss_total = 0
        cable_loss_total = 0

        # Encontrar a rota que conecta a caixa atual
        rota_caixa = None
        for rota in rotas:
            if rota['end'] == caixa['coordenadas']:
                rota_caixa = rota
                break

        if rota_caixa:
            # Exemplo: calcular perdas e sinal final para cada caixa
            connector_count = 2
            splice_count = 1

            # Calcule o comprimento do cabo com base na distância entre as coordenadas inicial e final da rota
            cable_length = (
                distancia_dois_pontos(rota_caixa['start'], rota_caixa['end'])
                / 1000
            )  # Converter para km

            connector_loss_total = calculate_connector_loss(
                connector_count, connector_loss
            )
            splice_loss_total = calculate_splice_loss(
                splice_count, splice_loss
            )
            cable_loss_total = calculate_cable_loss(
                cable_length, cable_attenuation
            )

        total_loss = (
            connector_loss_total + splice_loss_total + cable_loss_total
        )
        final_signal = calculate_final_signal(initial_signal, total_loss)

        caixa['sinal_final'] = final_signal

        print(f"Caixa {caixa['nome']}: Sinal final = {final_signal:.2f} dBm")
