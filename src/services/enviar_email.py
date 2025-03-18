import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# carregando as variáveis de ambiente
load_dotenv(r'.venv\.env')

# criando uma função que envia um e-mail
def send_email(cliente: str, destinatario: str, solicitacao: int, lista_frasco: list):
    # carregando os dados de autenticação
    remetente = os.getenv('SENDER')
    senha = os.getenv('PASSWORD')
    # Assunto da mensagem
    assunto = f'Retirada de Frascos Confirmada – {cliente}'
    # Corpo da mensagem
    corpo = f'''Prezado(a) {cliente},

Confirmamos a retirada dos frascos conforme solicitado. Seguem os detalhes:

Data da Retirada e hora de retirada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Número da Solicitação: {solicitacao}
Frascaria:
'''
    
    corpo += "\n".join(f" - {frasco}: {quantidade} unidade(s)" for frasco, quantidade in lista_frasco)
    

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(remetente, senha)
       smtp_server.sendmail(remetente, destinatario, msg.as_string())
    return True