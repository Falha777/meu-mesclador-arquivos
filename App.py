import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from openpyxl import BytesIO

# Configuração da página
st.set_page_config(page_title="Super Mesclador", layout="centered")
st.title("🔧 Ferramenta de Unificação de Arquivos")

# Menu Lateral para escolher a ferramenta
opcao = st.sidebar.selectbox(
    "Escolha a ferramenta:",
    ("Mesclar PDFs", "Mesclar Planilhas (CSV/Excel)")
)

# --- FUNCIONALIDADE 1: MESCLAR PDFS ---
if opcao == "Mesclar PDFs":
    st.header("📂 Juntar Arquivos PDF")
    st.write("Faça upload de vários PDFs e baixe um único arquivo unificado.")

    # Upload de múltiplos arquivos
    uploaded_pdfs = st.file_uploader("Arraste seus PDFs aqui", type="pdf", accept_multiple_files=True)

    if uploaded_pdfs:
        if st.button("Mesclar PDFs"):
            merger = PdfWriter()
            
            # Loop para adicionar cada arquivo enviado
            for pdf in uploaded_pdfs:
                merger.append(pdf)
            
            # Salvar em memória (BytesIO) para download
            output = BytesIO()
            merger.write(output)
            merger.close()
            output.seek(0)
            
            # Botão de Download
            st.success("PDFs mesclados com sucesso!")
            st.download_button(
                label="📥 Baixar PDF Unificado",
                data=output,
                file_name="pdf_unificado.pdf",
                mime="application/pdf"
            )

# --- FUNCIONALIDADE 2: MESCLAR PLANILHAS ---
elif opcao == "Mesclar Planilhas (CSV/Excel)":
    st.header("📊 Juntar Planilhas")
    st.write("Junte vários arquivos CSV ou Excel em uma única tabela mestre.")

    # Upload
    uploaded_sheets = st.file_uploader("Arraste suas planilhas aqui", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_sheets:
        if st.button("Unificar Dados"):
            lista_de_dados = []
            
            try:
                for arquivo in uploaded_sheets:
                    # Verifica a extensão para ler corretamente
                    if arquivo.name.endswith('.csv'):
                        df = pd.read_csv(arquivo)
                    else:
                        df = pd.read_excel(arquivo)
                    lista_de_dados.append(df)
                
                # O comando mágico que junta tudo
                df_final = pd.concat(lista_de_dados, ignore_index=True)
                
                st.write("Prévia dos dados unificados:")
                st.dataframe(df_final.head()) # Mostra as primeiras linhas
                
                # Converter para CSV para download
                csv_final = df_final.to_csv(index=False).encode('utf-8')
                
                st.success(f"{len(uploaded_sheets)} planilhas foram unificadas!")
                st.download_button(
                    label="📥 Baixar Planilha Unificada (CSV)",
                    data=csv_final,
                    file_name="planilha_unificada.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Erro ao processar os arquivos: {e}")

                st.info("Dica: Certifique-se de que todas as planilhas têm as mesmas colunas.")
