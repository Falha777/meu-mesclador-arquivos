import streamlit as st
import pandas as pd
from pypdf import PdfWriter
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Super Mesclador", layout="centered")
st.title("🔧 Ferramenta de Unificação Automática")

# Menu Lateral
opcao = st.sidebar.selectbox(
    "Escolha a ferramenta:",
    ("Mesclar PDFs", "Mesclar Planilhas (CSV/Excel)")
)

# --- FUNCIONALIDADE 1: MESCLAR PDFS ---
if opcao == "Mesclar PDFs":
    st.header("📂 Juntar Arquivos PDF")
    st.info("Arraste os arquivos e o botão de download aparecerá automaticamente.")

    # Upload
    uploaded_pdfs = st.file_uploader("Arraste seus PDFs aqui", type="pdf", accept_multiple_files=True)

    # Lógica Automática (Roda assim que tem arquivos)
    if uploaded_pdfs:
        if len(uploaded_pdfs) > 1:
            try:
                st.write("⏳ Processando arquivos...")
                
                merger = PdfWriter()
                for pdf in uploaded_pdfs:
                    merger.append(pdf)
                
                output = BytesIO()
                merger.write(output)
                merger.close()
                output.seek(0)
                
                st.success("Pronto! Seus arquivos foram unificados.")
                
                # Botão de Download aparece direto
                st.download_button(
                    label="📥 BAIXAR PDF UNIFICADO AGORA",
                    data=output,
                    file_name="pdf_completo.pdf",
                    mime="application/pdf",
                    type="primary"  # Deixa o botão destacado
                )
            except Exception as e:
                st.error(f"Erro ao mesclar: {e}")
        else:
            st.warning("Por favor, envie pelo menos 2 arquivos PDF para mesclar.")

# --- FUNCIONALIDADE 2: MESCLAR PLANILHAS ---
elif opcao == "Mesclar Planilhas (CSV/Excel)":
    st.header("📊 Juntar Planilhas")
    st.info("O sistema detecta e junta as planilhas automaticamente.")

    uploaded_sheets = st.file_uploader("Arraste suas planilhas aqui", type=["csv", "xlsx"], accept_multiple_files=True)

    # Lógica Automática
    if uploaded_sheets:
        if len(uploaded_sheets) > 1:
            lista_de_dados = []
            try:
                st.write("⏳ Lendo planilhas...")
                for arquivo in uploaded_sheets:
                    if arquivo.name.endswith('.csv'):
                        df = pd.read_csv(arquivo)
                    else:
                        df = pd.read_excel(arquivo)
                    lista_de_dados.append(df)
                
                # Junta tudo
                df_final = pd.concat(lista_de_dados, ignore_index=True)
                
                # Prepara o CSV
                csv_final = df_final.to_csv(index=False).encode('utf-8')
                
                st.success(f"Sucesso! {len(uploaded_sheets)} planilhas unidas.")
                
                # Mostra uma prévia
                st.dataframe(df_final.head(3))
                
                # Botão de Download Direto
                st.download_button(
                    label="📥 BAIXAR PLANILHA COMPLETA",
                    data=csv_final,
                    file_name="planilha_unificada.csv",
                    mime="text/csv",
                    type="primary"
                )
            except Exception as e:
                st.error(f"Erro: {e}")
                st.info("Verifique se as colunas das planilhas são iguais.")
