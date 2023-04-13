import math
from coordinate_correction import correct_coordinates
from data_extraction import extract_cxs_and_cbs, extract_data

from file_handling import read_kml
from utilities import (
    calculate_cable_approaches,
    create_cable_routes,
    simulate_signal_transmission,
)

# Função principal
def main():
    # Ler o arquivo KML
    kml = read_kml('exemplo-rede-fttx.kml')

    # Extrair as informações de pop, postes, bkbs, ceos, placas, ramais, cbs e cxs
    pop, postes, bkbs, ceos, placas, ramais, cbs, cxs = extract_data(kml)

    # Extrair todas as caixas e trajetos dos ramais
    caixas, trajetos = extract_cxs_and_cbs(ramais)

    # Corrigir as coordenadas das caixas e trajeto dos postes
    raio = 5.0  # Define o raio de aplicação do osnap
    correct_coordinates(postes, caixas, trajetos, raio)

    # Criar as rotas dos cabos com base nas linhas do arquivo KML
    rotas = create_cable_routes(trajetos)

    # Calcular as abordagens dos cabos com base nas caixas
    calculate_cable_approaches(caixas)

    # Simular a transmissão de sinal e calcular as perdas de sinal
    simulate_signal_transmission(pop, postes, rotas, caixas)


if __name__ == '__main__':
    main()
