from coordinate_correction import correct_coordinates

# Define os dados de teste
postes = [
    {
        'name': 'Poste 1',
        'coordinates': '-39.45170171578749,-4.051798564221868,0',
    },
    {
        'name': 'Poste 2',
        'coordinates': '-39.45041824186209,-4.051802355041452,0',
    },
    {
        'name': 'Poste 3',
        'coordinates': '-39.45167937274898,-4.052405604432771,0',
    },
    {
        'name': 'Poste 4',
        'coordinates': '-39.45014857544662,-4.052420669624774,0',
    },
    {
        'name': 'Poste 5',
        'coordinates': '-39.45063404928503,-4.051312748851081,0',
    },
]

caixas = [
    {'name': 'CX1', 'coordinates': '-39.45061121049186,-4.051317243901951,0'},
    {'name': 'CX2', 'coordinates': '-39.45170580097942,-4.051775984081074,0'},
    {'name': 'CX3', 'coordinates': '-39.45036797960606,-4.051774176984686,0'},
    {'name': 'CX4', 'coordinates': '-39.45015722936202,-4.052364217337001,0'},
    {'name': 'CX5', 'coordinates': '-39.45165552611553,-4.052428230360745,0'},
]

cabos = [
    {
        'name': 'Cabo 1',
        'coordinates': '-39.45171019044917,-4.051775014353245,0 '
        '-39.45061378397123,-4.051311334685768,0 '
        '-39.45041901888729,-4.051785086711799,0 '
        '-39.45168539893018,-4.052388847794529,0',
    },
    {
        'name': 'Cabo 2',
        'coordinates': '-39.4504127706509,-4.051785028167089,0 '
        '-39.45027973863841,-4.052074233376988,0 '
        '-39.45015949311684,-4.052358216459917,0',
    },
    {
        'name': 'Cabo 3',
        'coordinates': '-39.45169203296878,-4.052437505357072,0 '
        '-39.4517475097681,-4.051793388333383,0',
    },
]


def test_correct_coordinates():
    # Executa a correção de coordenadas
    raio = 10
    correct_coordinates(postes, caixas, cabos, raio)

    # Verifica se as coordenadas foram corrigidas adequadamente
    assert postes == [
        {
            'name': 'Poste 1',
            'coordinates': '-39.45170171578749,-4.051798564221868,0',
        },
        {
            'name': 'Poste 2',
            'coordinates': '-39.45041824186209,-4.051802355041452,0',
        },
        {
            'name': 'Poste 3',
            'coordinates': '-39.45167937274898,-4.052405604432771,0',
        },
        {
            'name': 'Poste 4',
            'coordinates': '-39.45014857544662,-4.052420669624774,0',
        },
        {
            'name': 'Poste 5',
            'coordinates': '-39.45063404928503,-4.051312748851081,0',
        },
    ]

    assert caixas == [
        {
            'name': 'CX1',
            'coordinates': '-39.45063404928503,-4.051312748851081,0',
            'poste': 'Poste 5',
        },
        {
            'name': 'CX2',
            'coordinates': '-39.45170171578749,-4.051798564221868,0',
            'poste': 'Poste 1',
        },
        {
            'name': 'CX3',
            'coordinates': '-39.45041824186209,-4.051802355041452,0',
            'poste': 'Poste 2',
        },
        {
            'name': 'CX4',
            'coordinates': '-39.45014857544662,-4.052420669624774,0',
            'poste': 'Poste 4',
        },
        {
            'name': 'CX5',
            'coordinates': '-39.45167937274898,-4.052405604432771,0',
            'poste': 'Poste 3',
        },
    ]

    assert cabos == [
        {
            'name': 'Cabo 1',
            'coordinates':
            '-39.45170171578749,-4.051798564221868,0 '
            '-39.45063404928503,-4.051312748851081,0 '
            '-39.45041824186209,-4.051802355041452,0 '
            '-39.45167937274898,-4.052405604432771,0',
            'postes': ['Poste 1', 'Poste 5', 'Poste 2', 'Poste 3'],
        },
        {
            'name': 'Cabo 2',
            'coordinates':
            '-39.45041824186209,-4.051802355041452,0 '
            '-39.45014857544662,-4.052420669624774,0',
            'postes': ['Poste 2', 'Poste 4'],
        },
        {
            'name': 'Cabo 3',
            'coordinates':
            '-39.45167937274898,-4.052405604432771,0 '
            '-39.45170171578749,-4.051798564221868,0',
            'postes': ['Poste 3', 'Poste 1'],
        },
    ]
