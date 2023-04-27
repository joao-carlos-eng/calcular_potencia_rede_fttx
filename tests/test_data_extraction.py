from data_extraction import extract_cxs_and_cbs, extract_data
from file_handling import read_kml

ramais = [
    {
        'cxs': [
            {
                'name': 'NAP 01',
                'coordinates': '-39.5758662519886,-3.990060305913486,0',
            },
            {
                'name': 'NAP 02',
                'coordinates': '-39.57820396609554,-3.989712744848217,0',
            },
            {
                'name': 'NAP 03',
                'coordinates': '-39.57707719855426,-3.989754090927925,0',
            },
            {
                'name': 'NAP 04',
                'coordinates': '-39.57602635871888,-3.98968781615253,0',
            },
            {
                'name': 'NAP 05',
                'coordinates': '-39.57899655105052,-3.990622647411576,0',
            },
            {
                'name': 'NAP 06',
                'coordinates': '-39.57810837320175,-3.99043810452626,0',
            },
            {
                'name': 'NAP 07',
                'coordinates': '-39.57795981501609,-3.991005526907609,0',
            },
        ],
        'cbs': [
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.57902336229549,-3.989768396602615,0 -39.57857660836493,-3.989719645230724,'
                               '0 -39.57822090138983,-3.98970964332787,0 -39.57779605421111,-3.989665819833006,'
                               '0 -39.57753565868541,-3.989661043886263,0 -39.5771248697431,-3.989690912440432,'
                               '0 -39.57670403820798,-3.989652567328206,0 -39.57639723550049,-3.989607699338463,'
                               '0 -39.57599626508603,-3.989580160011324,0',
            },
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.57901978680526,-3.989771439457157,0 -39.57897776090429,-3.99024138642704,'
                               '0 -39.57900312480319,-3.990573397451354,0 -39.57873598530244,-3.990510950635505,'
                               '0 -39.57848986305207,-3.990501160927221,0 -39.57811719145111,-3.990399956200782,'
                               '0 -39.57804232839646,-3.990781543396513,0 -39.577939564955,-3.990977247534452,0',
            },
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.57810234557193,-3.990416353705633,0 -39.57790578742537,-3.990356816926941,'
                               '0 -39.5774232785938,-3.990275057624674,0 -39.57717684687891,-3.990242105046202,'
                               '0 -39.5769380037077,-3.990157272197264,0 -39.57652519944271,-3.990106543338448,'
                               '0 -39.57623710701041,-3.989995403474368,0 -39.57584616788707,-3.990002761197822,0',
            },
        ],
        'name': 'ramal 1',
    },
    {
        'cxs': [
            {
                'name': 'NAP 01',
                'coordinates': '-39.57943534773643,-3.989823713874169,0',
            },
            {
                'name': 'NAP 02',
                'coordinates': '-39.57997282093181,-3.990765559677421,0',
            },
            {
                'name': 'NAP 03',
                'coordinates': '-39.58112370541335,-3.990538079262746,0',
            },
            {
                'name': 'NAP 04',
                'coordinates': '-39.58218598086521,-3.99079823227716,0',
            },
            {
                'name': 'NAP 05',
                'coordinates': '-39.58316158989294,-3.991272297897569,0',
            },
            {
                'name': 'NAP 06',
                'coordinates': '-39.58047904411244,-3.990261161393476,0',
            },
            {
                'name': 'NAP 07',
                'coordinates': '-39.58077080437025,-3.989943272714021,0',
            },
            {
                'name': 'NAP 08',
                'coordinates': '-39.58164341237611,-3.990030989358803,0',
            },
        ],
        'cbs': [
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.57900556574339,-3.989765746954745,0 -39.57942983798463,-3.989757208878252,'
                               '0 -39.57976649794592,-3.989784151730999,0 -39.57998619501182,-3.98980438802467,'
                               '0 -39.57990058478702,-3.990104548320677,0 -39.57982681934836,-3.990477715455917,'
                               '0 -39.57993595408338,-3.990702951859538,0 -39.58041630461071,-3.990677347767646,'
                               '0 -39.5807630875305,-3.990418185437508,0 -39.58110022832381,-3.990473307499645,'
                               '0 -39.58143825237213,-3.990453432667388,0 -39.58180180968002,-3.990545066645721,'
                               '0 -39.58217483354819,-3.990736919410613,0 -39.58261163868327,-3.990956268938401,'
                               '0 -39.58286184201929,-3.991063030718691,0 -39.58316091407429,-3.99120272820688,0',
            },
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.57997940965837,-3.98981684683403,0 -39.5803367216537,-3.989829967432425,'
                               '0 -39.58051453623833,-3.989929085319091,0 -39.58073789024979,-3.989885748838252,'
                               '0 -39.5812386282121,-3.989961752304789,0 -39.58162626789842,-3.98998141838074,0',
            },
            {
                'name': 'Caminho sem título',
                'coordinates': '-39.58056121213412,-3.989893486100926,0 -39.58044711224038,-3.990191929151446,0',
            },
        ],
        'name': 'ramal 2',
    },
]

kml_file_path = 'tests/exemplo-rede-fttx.kml'

# Extrai os dados do arquivo KML
kml = extract_data(read_kml(kml_file_path))


def test_extracao_do_pop():
    # Define o caminho do arquivo KML de teste

    # Verifica se todos os dados foram extraídos corretamente
    assert kml['pop'] == {
        'name': 'pop',
        'coordinates': ['-39.57911885557474,-3.988987830802047,0'],
        'type': 'pop',
    }


def test_extracao_dos_postes():
    assert len(kml['postes']) == 397


def test_extracao_dos_cabos():
    assert len(kml['bkbs']) == 3


def test_extracao_das_ceos():
    assert len(kml['ceos']) == 6


def test_extracao_dos_ramais():
    assert len(kml['ramais']) == 8


def test_extract_cxs_and_cbs():
    # Extrai as caixas e trajetos dos ramais
    caixas, trajetos = extract_cxs_and_cbs(ramais)

    # Verifica se todas as caixas e trajetos foram extraídos corretamente
    assert len(caixas) == 15
    assert len(trajetos) == 6
