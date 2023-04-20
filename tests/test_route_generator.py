# module test_route_generator.py

from route_generator import create_cables_routers

postes = [
    {
        'name': 'Poste 1',
        'coordinates': '-39.45170171578749,-4.051798564221868,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 2',
        'coordinates': '-39.45041824186209,-4.051802355041452,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 3',
        'coordinates': '-39.45167937274898,-4.052405604432771,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 4',
        'coordinates': '-39.45014857544662,-4.052420669624774,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 5',
        'coordinates': '-39.45063404928503,-4.051312748851081,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 6',
        'coordinates': '-39.45144385107923,-4.053001161209534,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 7',
        'coordinates': '-39.45084136905412,-4.052739216034889,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 8',
        'coordinates': '-39.45098763992067,-4.052059624520663,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 9',
        'coordinates': '-39.45120344431534,-4.051561062014795,0',
        'type': 'poste',
    },
    {
        'name': 'Poste 10',
        'coordinates': '-39.451846,-4.053180,0',
        'type': 'poste',
    },
]

caixas = [
    {
        'name': 'CX1',
        'coordinates': '-39.45063404928503,-4.051312748851081,0',
        'type': 'nap',
        'poste': 'Poste 5',
    },
    {
        'name': 'CX2',
        'coordinates': '-39.45170171578749,-4.051798564221868,0',
        'type': 'nap',
        'poste': 'Poste 1',
    },
    {
        'name': 'CX3',
        'coordinates': '-39.45041824186209,-4.051802355041452,0',
        'type': 'nap',
        'poste': 'Poste 2',
    },
    {
        'name': 'CX4',
        'coordinates': '-39.45014857544662,-4.052420669624774,0',
        'type': 'nap',
        'poste': 'Poste 4',
    },
]

cabos = [
    {
        'name': 'Cabo 1',
        'coordinates': '-39.45167937274898,-4.052405604432771,0 '
                       '-39.45098763992067,-4.052059624520663,0 '
                       '-39.45041824186209,-4.051802355041452,0 '
                       '-39.45063404928503,-4.051312748851081,0 '
                       '-39.45120344431534,-4.051561062014795,0 '
                       '-39.45170171578749,-4.051798564221868,0',
        'type': 'ramal',
    },
    {
        'name': 'Cabo 2',
        'coordinates': '-39.45144385107923,-4.053001161209534,0 '
                       '-39.45084136905412,-4.052739216034889,0 '
                       '-39.45014857544662,-4.052420669624774,0',
        'type': 'ramal',
    },
    {
        'name': 'Cabo 3',
        'coordinates': '-39.451846,-4.053180,0 '
                       '-39.45144385107923,-4.053001161209534,0 '
                       '-39.45167937274898,-4.052405604432771,0',
        'type': 'bkb',
    },
]

ceos = [
    {
        'name': 'CX5',
        'coordinates': '-39.45167937274898,-4.052405604432771,0',
        'type': 'ceo',
        'poste': 'Poste 3',
    },
]

hubs = [
    {
        'name': 'CX6',
        'coordinates': '-39.45144385107923,-4.053001161209534,0',
        'type': 'hub',
        'poste': 'Poste 6',
    },
]

pop = {
    'name': 'POP 1',
    'coordinates': '-39.451846,-4.053180,0',
    'poste': 'Poste 10',
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
]

caixas_geral = caixas + ceos + hubs

resultado = {cx['end']: cx for cx in create_cables_routers(pop, postes, cabos, caixas_geral)}
esperado = {cx['end']: cx for cx in expected_routes}


def test_create_cable_routes():
    assert resultado['CX1'] == esperado['CX1']
    assert resultado['CX2'] == esperado['CX2']
    assert resultado['CX3'] == esperado['CX3']
    assert resultado['CX4'] == esperado['CX4']
    assert resultado['CX5'] == esperado['CX5']
    assert resultado['CX6'] == esperado['CX6']

