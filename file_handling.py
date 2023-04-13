from pykml import parser

# Função para ler o arquivo KML e extrair as informações
def read_kml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        kml_content = file.read()
    kml_content = kml_content.replace(
        '<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0"?>'
    )
    kml = parser.fromstring(kml_content)
    return kml
