def create_cable_routes(pop, trajetos, bkbs, ceos, ramais):
    rotas = []
    
    # Conecte o POP aos bkbs
    for bkb in bkbs:
        rota_bkb = {
            "start": pop["coordenadas"],
            "end": bkb["coordenadas"],
            "type": "bkb"
        }
        rotas.append(rota_bkb)

    # Conecte os bkbs às ceos
    for ceo in ceos:
        for bkb in bkbs:
            if ceo["bkb_id"] == bkb["id"]:
                rota_ceo = {
                    "start": bkb["coordenadas"],
                    "end": ceo["coordenadas"],
                    "type": "ceo"
                }
                rotas.append(rota_ceo)
                break

    # Conecte as ceos aos ramais
    for ramal in ramais:
        for ceo in ceos:
            if ramal["ceo_id"] == ceo["id"]:
                rota_ramal = {
                    "start": ceo["coordenadas"],
                    "end": ramal["coordenadas"],
                    "type": "ramal"
                }
                rotas.append(rota_ramal)
                break

    return rotas




def calculate_cable_approaches(caixas):
    for caixa in caixas:
        # Neste exemplo, vamos assumir que a quantidade de abordagens é igual ao número da caixa
        # Você pode substituir esta lógica pela lógica correta para calcular as abordagens
        abordagens = int(caixa['name'].split()[-1])
        caixa['abordagens'] = abordagens


def simulate_signal_transmission(inicio, rotas, caixas):
    # Implemente a lógica para simular a transmissão de sinal e calcular as perdas de sinal
    total_loss = 0

    for route in rotas:
        start = route['start']
        end = route['end']

        # Calcular a distância entre o ponto inicial e o final do cabo
        distance = distancia_dois_pontos(start, end)

        # Calcular a perda de sinal para o cabo atual
        # Aqui você pode adicionar sua lógica para calcular a perda de sinal com base na distância e outros fatores, como atenuação do cabo, etc.
        cable_loss = calculate_cable_loss(distance)

        # Atualizar a perda total de sinal
        total_loss += cable_loss

    return total_loss
