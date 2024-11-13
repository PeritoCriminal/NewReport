from datetime import datetime
import re

def format_text_with_year(text, date=None):
    """
    Função que formata o número do laudo, protocolo e boletim de ocorrência.
    Recebe uma string `text` e uma data `date`, formatando o texto para garantir que termina com '/YYYY'.
    """

    if date is None:
        date = datetime.now()
    else:
        try:
            date = datetime.strptime(str(date), "%d/%m/%Y")
        except ValueError:
            date = datetime.now()

    year = date.strftime("%Y")
    
    text = text.replace(" ", "")
    
    if re.search(r"/\d{4}$", text):
        return text.upper()

    try:
        main_text = int(text.split('/')[0])
        main_text = f"{main_text:,}".replace(",", ".")
        text = f"{main_text}/{year}"
    except ValueError:

        text = f"{text}/{year}"
    
    return text.upper()
