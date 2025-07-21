
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from typing import Optional

@st.cache_data
def carregar_lottie(url: str):
    """Faz o download e cacheia uma animação Lottie a partir de uma URL."""
    resposta = requests.get(url)
    if resposta.status_code != 200:
        return None
    return resposta.json()

def mostrar_proxima_aba(nome_aba: str = "próxima aba", emoji: str = "➡️", animacao_url: Optional[str] = None):
    """
    Mostra uma instrução amigável com animação Lottie ao final da aba atual.

    Parâmetros:
    - nome_aba: texto da aba de destino
    - emoji: emoji que acompanha a mensagem
    - animacao_url: URL de uma animação Lottie (opcional, usa padrão se None)
    """
    
    animacao_url = animacao_url or "https://assets4.lottiefiles.com/packages/lf20_jzjvnjbb.json"
    anim = carregar_lottie(animacao_url) 
    st.markdown("<hr style='margin-top:2rem; margin-bottom:1rem;'>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align:center; color:#003366;'>Pronto para seguir?</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Clique na <b>{emoji} {nome_aba}</b> no início da página para continuar!</p>", unsafe_allow_html=True)

    
   

    if anim:
        st_lottie(anim, speed=1, height=150, width=150,key=f"proxima_{nome_aba}")
