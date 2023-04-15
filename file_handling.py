from pykml import parser


def read_kml(file_path):
    """
    Lê o arquivo KML no caminho especificado e retorna um objeto Python contendo as informações extraídas.

    :param file_path: str, caminho do arquivo KML a ser lido
    :return: Objeto Python contendo as informações do arquivo KML processado

    Exemplo de uso:

    kml = read_kml("exemplo-rede-fttx.kml")
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        kml_content = file.read()
    kml_content = kml_content.replace(
        '<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0"?>'
    )
    kml = parser.fromstring(kml_content)
    return kml
