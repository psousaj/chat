import re
from datetime import datetime as dt

current_period = dt.today().strftime('%m/%y')

saudacao = f"""
Olá, espero que esteja bem.
Gostaria de informar que seu Documento de Arrecadação Simplificado(DAS) 
período {current_period} está disponível, irei envia-lo em seguida.
Lembrando que é importante que o pagamento seja realizado
dentro do prazo estipulado para evitar juros e multa
"""

pdf = "PDF"

suggest = "\nQualquer dúvida ou sugestão entre em contato através do WhatsApp: https://wa.me/5588988412833."

disclaimer = f"""
{suggest}

Por favor, preciso que confirme o recebimento desta mensagem. 
Responda SIM, OK, ou RECEBI por gentileza.
"""


def print_and_request_input(message):
    print(message)
    return input()  # .lower().split()


# def process_input(words, retries, pendencies=False):
#     positive_responses = ["sim", "ok", "tá", "bom", "recebi", "ótimo",
#                           "beleza", "entendi", "show", "tá ótimo",
#                           "massa", "s", "manda", "mande", "envia", "pode", "👍", "''"""""""'''👍🏻,'"''👍'🏼'''''','"'👍🏿"""""""""""]
#     if any(word in words for word in positive_responses):
#         if pendencies:
#             print(f"\nVou enviar os arquivos agora mesmo! {suggest}")
#         # ----
#         if not pendencies:
#             print("\nObrigado por confirmar!")
#         return True

#     if pendencies and any(word in words for word in ["n", "nao", "pare", "parar", "stop", "não", "nao mande"]):
#         print(
#             f"\nTudo bem! caso necessite de mais alguma coisa, não hesite em nos perguntar! {suggest}")
#         return True  # Altere para retornar True aqui para encerrar o loop

#     if any(word in words for word in ["atendente", "humano", "pessoa", "atendimento", "atedente", "sair"]):
#         print("\nEstou lhe encaminhando para um de nossos atendentes. Aguarde por favor!")
#         print("\nOlá, SOU SEU ATENDENTE FICTÍCIO!!")
#         return True  # Altere para retornar True aqui para encerrar o loop

#     if retries >= 3:
#         print("\nEstou lhe encaminhando para um de nossos atendentes. Aguarde por favor!")
#         print("\nOlá, SOU SEU ATENDENTE FICTÍCIO!!")
#         return False  # Retorna false por causa da condição not no loop principal negando essa função logo negar false é true e o loop para

#     return False


# def process_input(user_input, retries, pendencies=False):
#     positive_responses = r"\b(sim|bacana|ok|tá|bom|recebi|ótimo|beleza|entendi|show|confirmado|confirme|tá\sótimo|massa|s|manda|mande|envia|pode|👍|👍🏾|👍🏻|👍🏼|👍🏿|pode\sser)\b"
#     negative_responses = r"\b(n|nao|pare|parar|stop|não|não\smande|nao\smande)\b"
#     assistance_requests = r"\b(atendente|humano|pessoa|atendimento|atedente|sair)\b"

#     if re.search(positive_responses, user_input, re.IGNORECASE) and not re.search(negative_responses, user_input, re.IGNORECASE):
#         if pendencies:
#             print(f"\nVou enviar os arquivos agora mesmo!")
#         else:
#             print("\nObrigado por confirmar!")
#         return True

#     if pendencies and re.search(negative_responses, user_input, re.IGNORECASE):
#         print(
#             f"\nTudo bem! Caso necessite de mais alguma coisa, não hesite em nos perguntar!")
#         return True

#     if re.search(assistance_requests, user_input, re.IGNORECASE) or retries >= 3:
#         print("\nEstou lhe encaminhando para um de nossos atendentes. Aguarde por favor!")
#         print("\nOlá, SOU SEU ATENDENTE FICTÍCIO!!")
#         return True

#     return False


def is_match(input_word, responses, exact_match):
    if exact_match:
        return any(word in input_word.split() for word in responses.split('|'))

    return bool(re.search(responses, input_word, re.IGNORECASE))


def process_input(words, retries, pendencies, exact_match):
    positive_responses = r"\b(sim|bacana|ok|tá|ta|bom|recebi|receb|na\shora|ótimo|beleza|blz|entendi|show|confirmado|confirme|tá\sótimo|massa|s|manda|mande|envia|pode|👍|👍🏾|👍🏻|👍🏼|👍🏿|pode\sser)\b"
    # |não\smande|nao\smande
    negative_responses = r"\b(n|nao|pare|parar|stop|não)\b"
    assistance_requests = r"\b(atendente|humano|pessoa|atendimento|atedente|sair)\b"

    if is_match(words, positive_responses, exact_match) and not is_match(words, negative_responses, exact_match):
        print(f"\nVou enviar os arquivos agora mesmo!") if pendencies else print(
            "\nObrigado por confirmar!")
        return True

    if pendencies and is_match(words, negative_responses, exact_match):
        print(
            f"\nTudo bem! Caso necessite de mais alguma coisa, não hesite em nos perguntar!")
        return True

    if is_match(words, assistance_requests, exact_match) or retries >= 3:
        print("\nEstou lhe encaminhando para um de nossos atendentes. Aguarde por favor!")
        print("\nOlá, SOU SEU ATENDENTE FICTÍCIO!!")
        return True

    return False


def generate_error_message(retries, pendencies):
    base_message = "\nDesculpe, não entendi. Por favor, responda SIM, OK ou "
    if pendencies:
        base_message += "NÃO caso não queira os boletos agora."
    else:
        base_message += "RECEBI."

    if retries >= 2:
        base_message += '\nSe precisar falar com um de nossos atendentes digite "atendente"'
    return base_message


def get_answer(pendencies=False, exact_match=False):
    retries = 1
    user_input = print_and_request_input("")

    while True:
        while not process_input(user_input, retries, pendencies, exact_match):
            if retries >= 3 and not process_input(user_input, retries, pendencies, exact_match):
                break

            user_input = print_and_request_input(
                generate_error_message(retries, pendencies))
            retries += 1
        break


def main(has_debit, pendencies=None, exact_match=False):
    print(saudacao)
    print(pdf)

    if has_debit:
        print(f"\nVocê tem as seguintes pendencias: {pendencies}")
        print("Deseja receber os boletos agora?")
        return get_answer(pendencies=True, exact_match=exact_match)

    print(disclaimer)
    return get_answer()


if __name__ == "__main__":
    has_debit = True
    pendencies = ['Abril/2020', 'Março/2021', 'Janeiro/2022']

    main(has_debit, pendencies, exact_match=False)
