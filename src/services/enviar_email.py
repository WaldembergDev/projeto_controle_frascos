import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv
from src.models.movimentacao import DetalheMovimentacaoEnum
import os

# carregando as variáveis de ambiente
load_dotenv(r'.venv\.env')

# corpo dos emails
def obter_corpo_email(detalhe_movimentacao: DetalheMovimentacaoEnum, cliente: str, solicitacao: str):
    if detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO:
        corpo = f'''Prezado(a) {cliente},

Confirmamos a retirada dos frascos conforme solicitado. Seguem os detalhes:

Data e hora da retirada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Número do Registro: {solicitacao}
Frascaria:
'''
        
    elif detalhe_movimentacao == DetalheMovimentacaoEnum.DEVOLUCAO:
        corpo = f'''Prezado(a) {cliente},

Confirmamos a devolução dos frascos. Seguem os detalhes:

Data e hora da devolução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Número do Registro: {solicitacao}
Frascaria:
'''
    return corpo

# assunto dos emails
def obter_assunto_email(detalhe_movimentacao: DetalheMovimentacaoEnum, cliente: str):
    if detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO:
        assunto = f'Retirada de Frascos Confirmada – {cliente}'
    elif detalhe_movimentacao == DetalheMovimentacaoEnum.DEVOLUCAO:
        assunto = f'Confirmação de Devolução de Frascos – {cliente}'
    return assunto

# criando uma função que envia um e-mail
def send_email(cliente: str, destinatario: str, detalhe_movimentacao: DetalheMovimentacaoEnum, solicitacao: int, lista_frasco: list):
    # carregando os dados de autenticação
    remetente = os.getenv('SENDER')
    senha = os.getenv('PASSWORD')
    # Assunto da mensagem
    assunto = obter_assunto_email(detalhe_movimentacao, cliente)
    # Corpo da mensagem
    corpo = obter_corpo_email(detalhe_movimentacao, cliente, solicitacao)
    
    corpo += "\n".join(f" - {frasco}: {quantidade} unidade(s)" for frasco, quantidade in lista_frasco)

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(remetente, senha)
       smtp_server.sendmail(remetente, destinatario, msg.as_string())
    return True