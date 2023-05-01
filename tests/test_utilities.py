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

calculate_cable_approaches(caixas, cabos)


def test_calculate_cable_approaches_cx_1():
    print(caixas[0]['name'])
    assert caixas[0]['abordagens'] == 3


def test_calculate_cable_approaches_cx_2():
    print(caixas[1]['name'])
    assert caixas[1]['abordagens'] == 1


def test_calculate_cable_approaches_cx_3():
    print(caixas[2]['name'])
    assert caixas[2]['abordagens'] == 2


def test_calculate_cable_approaches_cx_4():
    print(caixas[3]['name'])
    assert caixas[3]['abordagens'] == 1


def test_calculate_cable_approaches_cx_8():
    print(caixas[4]['name'])
    assert caixas[4]['abordagens'] == 1


def test_calculate_cable_approaches_cx_5():
    print(caixas[5]['name'])
    assert caixas[5]['abordagens'] == 3


test_signals = simulate_signal_transmission(pop, expected_routes, caixas, data_sheets, topology='1x128')


def test_sinal_cx_passando_por_ceo_hub_e_nap():
    assert caixas[0]['sinal_final'] == round(sinal_cx1, 2)


def test_sinal_ultima_cx_da_rede():
    assert caixas[1]['sinal_final'] == round(sinal_cx2, 2)


def test_sinal_cx_apos_ceo():
    assert caixas[2]['sinal_final'] == round(sinal_cx3, 2)


def test_sinal_cx_mais_proxima_do_pop():
    assert caixas[3]['sinal_final'] == round(sinal_cx4, 2)


def test_sinal_na_ceo():
    assert caixas[5]['sinal_final'] == round(sinal_cx5, 2)


def test_sinal_na_hub():
    assert caixas[5]['sinal_final'] == round(sinal_cx6, 2)
