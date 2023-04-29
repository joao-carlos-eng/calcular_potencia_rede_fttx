# module test_route_generator.py

from route_generator import create_cables_routers

postes = [
    {
        'name': 'Poste 1',
        'coordinates': ['-39.45170171578749,-4.051798564221868,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 2',
        'coordinates': ['-39.45041824186209,-4.051802355041452,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 3',
        'coordinates': ['-39.45167937274898,-4.052405604432771,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 4',
        'coordinates': ['-39.45014857544662,-4.052420669624774,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 5',
        'coordinates': ['-39.45063404928503,-4.051312748851081,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 6',
        'coordinates': ['-39.45144385107923,-4.053001161209534,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 7',
        'coordinates': ['-39.45084136905412,-4.052739216034889,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 8',
        'coordinates': ['-39.45098763992067,-4.052059624520663,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 9',
        'coordinates': ['-39.45120344431534,-4.051561062014795,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 10',
        'coordinates': ['-39.451846,-4.053180,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 11',
        'coordinates': ['-39.452307,-4.052223,0'],
        'type': 'poste',
    },
    {
        'name': 'Poste 12',
        'coordinates': ['-39.450844,-4.050841,0'],
        'type': 'poste',
    },
]

caixas = [
    {
        'name': 'CX1',
        'coordinates': ['-39.45063404928503,-4.051312748851081,0'],
        'type': 'nap',
        'poste': 'Poste 5',
    },
    {
        'name': 'CX2',
        'coordinates': ['-39.45170171578749,-4.051798564221868,0'],
        'type': 'nap',
        'poste': 'Poste 1',
    },
    {
        'name': 'CX3',
        'coordinates': ['-39.45041824186209,-4.051802355041452,0'],
        'type': 'nap',
        'poste': 'Poste 2',
    },
    {
        'name': 'CX4',
        'coordinates': ['-39.45014857544662,-4.052420669624774,0'],
        'type': 'nap',
        'poste': 'Poste 4',
    },
    {
        'name': 'CX8',
        'coordinates': ['-39.450844,-4.050841,0'],
        'type': 'nap',
        'poste': ['Poste 12'],
    },
]

cabos = [
    {
        'name': 'Cabo 1',
        'coordinates': ['-39.45167937274898,-4.052405604432771,0',
                        '-39.45098763992067,-4.052059624520663,0',
                        '-39.45041824186209,-4.051802355041452,0',
                        '-39.45063404928503,-4.051312748851081,0',
                        '-39.45120344431534,-4.051561062014795,0',
                        '-39.45170171578749,-4.051798564221868,0'],
        'type': 'ramal',
    },
    {
        'name': 'Cabo 2',
        'coordinates': ['-39.45144385107923,-4.053001161209534,0',
                        '-39.45084136905412,-4.052739216034889,0',
                        '-39.45014857544662,-4.052420669624774,0'],
        'type': 'ramal',
    },
    {
        'name': 'Cabo 3',
        'coordinates': ['-39.451846,-4.053180,0',
                        '-39.45144385107923,-4.053001161209534,0',
                        '-39.45167937274898,-4.052405604432771,0'],
        'type': 'bkb',
    },
    {
        'name': 'Cabo 4',
        'coordinates': ['-39.45167937274898,-4.052405604432771,0',
                        '-39.452307,-4.052223,0', ],
        'type': 'bkb',
    },
    {
        'name': 'Cabo 5',
        'coordinates': ['-39.45063404928503,-4.051312748851081,0',
                        '-39.450844,-4.050841,0', ],
        'type': 'ramal',
    },
]

ceos = [
    {
        'name': 'CX5',
        'coordinates': ['-39.45167937274898,-4.052405604432771,0'],
        'type': 'ceo',
        'poste': ['Poste 3'],
    },
]

hubs = [
    {
        'name': 'CX6',
        'coordinates': ['-39.45144385107923,-4.053001161209534,0'],
        'type': 'hub',
        'poste': ['Poste 6'],
    },
    {
        'name': 'CX7',
        'coordinates': ['-39.452307,-4.052223,0'],
        'type': 'hub',
        'poste': ['Poste 11'],
    },
]

pop = {
    'name': 'POP 1',
    'coordinates': ['-39.451846,-4.053180,0'],
    'poste': ['Poste 10'],
}

expected_routes = [
    {
        'start': 'POP 1',
        'end': 'CX1',
        'router': ['POP 1', 'CX6', 'CX5', 'Poste 8', 'CX3', 'CX1'],
        'cable': ['Cabo 3', 'Cabo 1'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
            '-39.45098763992067,-4.052059624520663,0',
            '-39.45041824186209,-4.051802355041452,0',
            '-39.45063404928503,-4.051312748851081,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX2',
        'router': ['POP 1', 'CX6', 'CX5', 'Poste 8', 'CX3', 'CX1', 'Poste 9', 'CX2', ],
        'cable': ['Cabo 3', 'Cabo 1'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
            '-39.45098763992067,-4.052059624520663,0',
            '-39.45041824186209,-4.051802355041452,0',
            '-39.45063404928503,-4.051312748851081,0',
            '-39.45120344431534,-4.051561062014795,0',
            '-39.45170171578749,-4.051798564221868,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX3',
        'router': ['POP 1', 'CX6', 'CX5', 'Poste 8', 'CX3'],
        'cable': ['Cabo 3', 'Cabo 1'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
            '-39.45098763992067,-4.052059624520663,0',
            '-39.45041824186209,-4.051802355041452,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX4',
        'router': ['POP 1', 'CX6', 'Poste 7', 'CX4'],
        'cable': ['Cabo 3', 'Cabo 2'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45084136905412,-4.052739216034889,0',
            '-39.45014857544662,-4.052420669624774,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX5',
        'router': ['POP 1', 'CX6', 'CX5'],
        'cable': ['Cabo 3'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX6',
        'router': ['POP 1', 'CX6'],
        'cable': ['Cabo 3'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX7',
        'router': ['POP 1', 'CX6', 'CX5', 'CX7'],
        'cable': ['Cabo 3', 'Cabo 4'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
            '-39.452307,-4.052223,0',
        ],
    },
    {
        'start': 'POP 1',
        'end': 'CX8',
        'router': ['POP 1', 'CX6', 'CX5', 'Poste 8', 'CX3', 'CX1', 'CX8', ],
        'cable': ['Cabo 3', 'Cabo 5'],
        'coordinates': [
            '-39.451846,-4.053180,0',
            '-39.45144385107923,-4.053001161209534,0',
            '-39.45167937274898,-4.052405604432771,0',
            '-39.45098763992067,-4.052059624520663,0',
            '-39.45041824186209,-4.051802355041452,0',
            '-39.45063404928503,-4.051312748851081,0',
            '-39.45120344431534,-4.051561062014795,0',
            '-39.45170171578749,-4.051798564221868,0',
        ],
    },
]

caixas_geral = caixas + ceos + hubs

resultado = {cx['end']: cx for cx in create_cables_routers(pop, postes, cabos, caixas_geral)}
esperado = {cx['end']: cx for cx in expected_routes}


def test_create_cable_routes_result_for_cx_1_nap():
    assert resultado['CX1'] == esperado['CX1']


def test_create_cable_routes_result_for_cx_2_nap():
    assert resultado['CX2'] == esperado['CX2']


def test_create_cable_routes_result_for_cx_5_ceo():
    assert resultado['CX5'] == esperado['CX5']


def test_create_cable_routes_result_for_cx_6_hub():
    assert resultado['CX6'] == esperado['CX6']


def test_create_cable_routes_result_for_cx_7_hub():
    """
    HUB derivando do bkbone na CEO 1
    :return:
    """
    assert resultado['CX7'] == esperado['CX7']


def test_create_cable_routers_result_for_cx_8_nap():
    """
    nap derivando do ramal 1
    :return:
    """
    assert resultado['CX8'] == esperado['CX8']
