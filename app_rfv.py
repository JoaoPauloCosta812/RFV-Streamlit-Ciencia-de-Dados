import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO


# Funções auxiliares
@st.cache_data
def convert_df(df):
    """Converte DataFrame em CSV (para download)"""
    return df.to_csv(index=False).encode('utf-8')

@st.cache_resource
def to_excel(df):
    """Converte DataFrame em arquivo Excel (para download)"""
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def recencia_class(x, r, q_dict):
    """Classifica recência (quanto menor, melhor)"""
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    """Classifica frequência e valor (quanto maior, melhor)"""
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'


# Função principal
def main():

    # Configurações da página
    st.set_page_config(
        page_title='Análise RFV - Segmentação de Clientes',
        page_icon='💎',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    # CSS customizado para visual mais bonito
    st.markdown("""
        <style>
        .main { background-color: #f9f9f9; }
        h1, h2, h3, h4 { color: #333333; }
        .metric-card {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stDownloadButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)


    # Cabeçalho
    st.title("Análise RFV - Segmentação de Clientes")
    st.markdown("""
    O modelo **RFV (Recência, Frequência e Valor)** permite segmentar clientes com base no comportamento de compra,
    identificando **os mais fiéis, os inativos e os potenciais churns**.  
    Essa segmentação é essencial para ações de **Marketing e CRM mais eficazes.**
    """)

    st.markdown("---")


    # Sidebar
    st.sidebar.header("📂 Upload de Arquivo")
    st.sidebar.write("Carregue um arquivo `.csv` contendo as colunas: `ID_cliente`, `DiaCompra`, `CodigoCompra`, `ValorTotal`.")
    st.sidebar.info("Dica: você pode usar o arquivo `dados_input.csv` fornecido pelo professor.")

    data_file = st.sidebar.file_uploader("Selecione o arquivo de dados", type=['csv','xlsx'])


    # Processamento
    if data_file is not None:
        # Leitura do arquivo
        if data_file.name.endswith('.csv'):
            df_compras = pd.read_csv(data_file, parse_dates=['DiaCompra'])
        else:
            df_compras = pd.read_excel(data_file, parse_dates=['DiaCompra'])

        st.success("✅ Dados carregados com sucesso!")
        st.dataframe(df_compras.head(), use_container_width=True)


        # 1. Recência
        dia_atual = df_compras['DiaCompra'].max()
        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente','DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)


        # 2. Frequência
        df_frequencia = df_compras[['ID_cliente','CodigoCompra']].groupby('ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente','Frequencia']


        # 3. Valor
        df_valor = df_compras[['ID_cliente','ValorTotal']].groupby('ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente','Valor']


        # 4. Tabela RFV final
        df_RFV = df_recencia.merge(df_frequencia, on='ID_cliente').merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)

        # Métricas principais
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card'><h3>📅 Data mais recente</h3><h2>{dia_atual.date()}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>👥 Clientes únicos</h3><h2>{df_RFV.shape[0]}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card'><h3>💰 Total gasto (R$)</h3><h2>{df_valor['Valor'].sum():,.2f}</h2></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📊 Segmentação RFV por Quartis")

        quartis = df_RFV.quantile(q=[0.25,0.5,0.75])
        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))
        df_RFV['RFV_Score'] = df_RFV.R_quartil + df_RFV.F_quartil + df_RFV.V_quartil

        st.dataframe(df_RFV.head(), use_container_width=True)

        # 5. Ações de Marketing
        st.subheader("🎯 Ações de Marketing/CRM sugeridas")
        dict_acoes = {
            'AAA': '💎 Cliente VIP: Enviar cupons exclusivos, brindes e pré-venda de produtos.',
            'DDD': '⚠️ Cliente inativo: Enviar ofertas de reativação.',
            'DAA': '🔥 Ex-cliente de alto valor: oferecer desconto especial de retorno.',
            'CAA': '🎁 Cliente em risco: ofertar promoção personalizada.',
        }
        df_RFV['Acoes_Marketing'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.dataframe(df_RFV[['Recencia','Frequencia','Valor','RFV_Score','Acoes_Marketing']].head(), use_container_width=True)


        # 6. Download
        df_xlsx = to_excel(df_RFV)
        st.download_button(
            label="📥 Baixar resultado em Excel",
            data=df_xlsx,
            file_name="RFV_resultado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Contagem de grupos
        st.markdown("---")
        st.subheader("📈 Quantidade de clientes por grupo RFV")
        st.bar_chart(df_RFV['RFV_Score'].value_counts())

    else:
        st.info("👈 Faça o upload de um arquivo para iniciar a análise RFV.")


# Execução
if __name__ == '__main__':
    main()
