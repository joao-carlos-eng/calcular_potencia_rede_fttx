# module test_utilities.py
from main import data_sheets
from utilities import calculate_cable_approaches, simulate_signal_transmission
from tests.test_route_generator import cabos, pop, expected_routes, caixas_geral

caixas = caixas_geral.copy()

pop['signal'] = 4
# sinal_cx = sinal_inicial -
# (perda_cabo * comprimento_cabo + perda_conector * conectores + perda_emendas * emendas + perda_splitter)
sinal_cx1 = pop['signal'] - ((404 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 10.5 + 13.7)
sinal_cx2 = pop['signal'] - ((424 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 10.5 + 13.7)
sinal_cx3 = pop['signal'] - ((396 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 10.5 + 13.7)
sinal_cx4 = pop['signal'] - ((237 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 10.5 + 13.7)
sinal_cx5 = pop['signal'] - ((150 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 13.7)
sinal_cx6 = pop['signal'] - ((60 / 1000) * 0.35 + 4 * 0.3 + 5 * 0.1 + 13.7)


def test_calculate_cable_approaches():
    calculate_cable_approaches(caixas, cabos)

    assert caixas[0]['abordagens'] == 2
    assert caixas[1]['abordagens'] == 1
    assert caixas[2]['abordagens'] == 2
    assert caixas[3]['abordagens'] == 1
    assert caixas[4]['abordagens'] == 2
    assert caixas[5]['abordagens'] == 3

    print(caixas[0])


def test_simulate_signal_transmission():
    simulate_signal_transmission(pop, expected_routes, caixas, data_sheets, topology='1x128')

    assert caixas[0]['sinal_final'] == round(sinal_cx1)
    assert caixas[1]['sinal_final'] == round(sinal_cx2)
    assert caixas[2]['sinal_final'] == round(sinal_cx3)
    assert caixas[3]['sinal_final'] == round(sinal_cx4)
    assert caixas[4]['sinal_final'] == round(sinal_cx5)
    assert caixas[5]['sinal_final'] == round(sinal_cx6)
