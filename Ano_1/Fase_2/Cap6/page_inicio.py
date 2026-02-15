import streamlit as st

for i in range(2):
    st.write("")

with st.container(border=True):
    st.page_link("page_culturas.py", label=":green[**$$\\underline{Culturas}$$**] - Com quais culturas você deseja trabalhar?", icon="🌱")
    st.page_link("page_areas.py", label=":green[**$$\\underline{Áreas\\,de\\,Plantio}$$**] - Calcule as áreas de plantio para cada cultura.", icon="📐")
    st.page_link("page_insumos.py", label=":green[**$$\\underline{Manejo\\,de\\,Insumos}$$**] - Calcule as quantidades necessárias.", icon="⚖️")
    st.page_link("page_estatisticas.py", label=":green[**$$\\underline{Estatísticas}$$**] - Descubra os números de sua fazenda.", icon="📈")
    st.page_link("page_meteorologia.py", label=":green[**$$\\underline{Meteorologia}$$**] - Pesquise as condições climáticas em uma cidade.", icon="🌦️")
    st.page_link("page_receita.py", label=":green[**$$\\underline{Cálculo\\,de\\,Receita}$$**] - Calcule a receita de sua fazenda.", icon="💵")
