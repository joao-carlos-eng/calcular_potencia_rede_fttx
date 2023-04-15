from data_extraction import extract_data, extract_cxs_and_cbs
from file_handling import read_kml


import pytest


@pytest.fixture
def ramais():
    return [
        {
            'cxs': [
                {'name': 'CX1', 'coordinates': '-40,-20'},
                {'name': 'CX2', 'coordinates': '-40,-30'},
                {'name': 'CX3', 'coordinates': '-50,-30'},
            ],
            'cbs': [
                {'name': 'CB1', 'coordinates': '-60,-30'},
            ],
        },
        {
            'cxs': [
                {'name': 'CX4', 'coordinates': '-30,-20'},
                {'name': 'CX5', 'coordinates': '-30,-30'},
                {'name': 'CX6', 'coordinates': '-40,-20'},
                {'name': 'CX7', 'coordinates': '-40,-10'},
            ],
            'cbs': [
                {'name': 'CB2', 'coordinates': '-50,-20'},
                {'name': 'CB3', 'coordinates': '-50,-10'},
            ],
        },
        {
            'cxs': [
                {'name': 'CX8', 'coordinates': '-30,-10'},
                {'name': 'CX9', 'coordinates': '-20,-10'},
            ],
            'cbs': [],
        },
    ]


def test_extract_data():
    # Define o caminho do arquivo KML de teste
    kml_file_path = 'tests/exemplo-rede-fttx.kml'

    # Extrai os dados do arquivo KML
    kml = extract_data(read_kml(kml_file_path))

    # Verifica se todos os dados foram extraídos corretamente
    assert kml['pop'] == {
        'name': 'pop',
        'coordinates': '-39.57911885557474,-3.988987830802047,0',
    }
    assert len(kml['postes']) == 396
    assert len(kml['bkbs']) == 1
    assert len(kml['ceos']) == 1
    assert len(kml['placas']) == 3
    assert len(kml['ramais']) == 2
    assert len(kml['cbs']) == 4
    assert len(kml['cxs']) == 9


def test_extract_cxs_and_cbs(ramais):
    # Extrai as caixas e trajetos dos ramais
    caixas, trajetos = extract_cxs_and_cbs(ramais)

    # Verifica se todas as caixas e trajetos foram extraídos corretamente
    assert len(caixas) == 9
    assert len(trajetos) == 3
