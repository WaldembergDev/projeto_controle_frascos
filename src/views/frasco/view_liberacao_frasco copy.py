import streamlit as st
from streamlit_drawable_canvas import st_canvas

from PIL import Image
import io

from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_solicitacao_estoque import ControllerSolicitacaoEstoque

import time
# carregando os dados de clientes ativos
clientes = ControllerCliente.gerar_dicionario_clientes_ativos()

# carregando os dados dos frascos ativos
frascos = ControllerFrasco.gerar_dicionario_frascos_ativos()

# -- Inicio da tela principal -- 
st.header('Liberação de Frascos', divider=True)

responsavel = st.text_input('Responsável')


cliente = st.selectbox('Selecione um cliente', options=clientes)

# obtendo o id do cliente selecionado se existir cliente
if cliente:
    id_cliente = clientes[cliente]

if not 'botoes' in st.session_state:
    st.session_state['botoes'] = 1

col_adicionar, col_remover = st.columns(2)

with col_adicionar:
    botao_adicionar_frasco = st.button('Adicionar Frasco')

with col_remover:
    botao_remover_frasco = st.button('Remover Frasco')

if botao_adicionar_frasco:
    st.session_state.botoes += 1

if botao_remover_frasco:
    if st.session_state.botoes == 1:
        pass
    else:
        st.session_state.botoes -= 1

col1, col2 = st.columns(2)

for i in range(st.session_state.botoes):
    with col1:
        frasco = st.selectbox('Selecione um frasco', options=frascos, key=f'frasco_{i}')

    with col2:
        if frasco:
            # definindo a quantidade mínima e máxima de frascos se houver frasco para o cliente
            valor_maximo = ControllerFrasco.obter_quantidade_frascos_pelo_id((frascos[frasco]))
            valor_minimo = 1
        else:
            # definindo a quantidade mínima e máxima de frascos se não houver frascos para o cliente
            valor_maximo = 0
            valor_minimo = 0
        quantidade_frasco = st.number_input('Selecione a quantidade', min_value=0, step=1, key=f'quantidade_frasco_{i}', max_value=valor_maximo)

# Configurações do Canvas para assinatura
canvas_result = st_canvas(
    fill_color="white",  # Cor de fundo do canvas
    stroke_width=2,  # Largura do traço
    stroke_color="black",  # Cor do traço
    background_color="white",  # Cor de fundo
    width=500,  # Largura do canvas
    height=200,  # Altura do canvas
    drawing_mode="freedraw",  # Modo de desenho livre
    key="canvas",
)

# Função para converter a imagem do canvas para um formato binário (BLOB)
def converter_imagem(image_data):
    # Converte a imagem numpy para PIL
    img = Image.fromarray(image_data)
    # Salva a imagem em um buffer de bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')  # Salva como PNG
    img_byte_arr = img_byte_arr.getvalue()  # Obtém os dados binários da imagem
    return img_byte_arr

botao_salvar_dados = st.button('Salvar dados')

if botao_salvar_dados:
    dados_frascos = []
    for i in range(st.session_state.botoes):
        dados_frascos.append((frascos[st.session_state[f'frasco_{i}']], int(st.session_state[f'quantidade_frasco_{i}'])))
    solicitacao_salva = ControllerSolicitacaoEstoque.criar_solicitacao_com_itens(id_usuario=1,
                                                             responsavel=responsavel,
                                                               id_cliente=id_cliente,
                                                                 dados_frascos=dados_frascos,
                                                                 assinatura=converter_imagem(canvas_result.image_data))
    if solicitacao_salva == True:
        st.success('Solicitação realizada com sucesso!')
        time.sleep(3)
        st.rerun()
        