from coordinate_correction import correct_coordinates
from data_extraction import extract_cxs_and_cbs, extract_data
from file_handling import read_kml
from route_generator import create_cables_routers
from utilities import calculate_cable_approaches, simulate_signal_transmission


def main():
    # Ler o arquivo KML
    kml = read_kml('exemplo-rede-fttx.kml')

    # Extrair as informações de pop, postes, bkbs, ceos, placas, ramais, cbs e cxs
    data = extract_data(kml)
    pop = data['pop']
    postes = data['postes']
    bkbs = data['bkbs']
    ceos = data['ceos']
    placas = data['placas']
    ramais = data['ramais']
    cbs = data['cbs']
    cxs = data['cxs']

    # Extrair todas as caixas e trajetos dos ramais
    caixas, cabos = extract_cxs_and_cbs(ramais)

    # Corrigir as coordenadas das caixas e trajeto dos postes
    raio = 5.0  # Define o raio de aplicação do osnap
    correct_coordinates(postes, caixas, cabos, raio)

    # Criar as rotas dos cabos com base nas linhas do arquivo KML
    rotas = create_cables_routers(pop, postes, cabos, caixas+ceos)

    # Calcular as abordagens dos cabos com base nas caixas
    calculate_cable_approaches(caixas)

    # Simular a transmissão de sinal e calcular as perdas de sinal
    simulate_signal_transmission(pop, rotas, caixas)


if __name__ == '__main__':
    main()
