import pandas as pd
import streamlit as st

# Create a sample DataFrame
df = pd.DataFrame({
    'Variável': ['A', 'B', 'C'],
    'Média': [1.2, 2.3, 3.4],
    'Desvio Padrão': [0.1, 0.2, 0.3]
})

# Create an HTML table with right-aligned column headers
html_table = """
<table>
  <tr>
    <th style="text-align: right;">Variável</th>
    <th style="text-align: right;">Média</th>
    <th style="text-align: right;">Desvio Padrão</th>
  </tr>
"""

# Add the DataFrame rows to the HTML table
for index, row in df.iterrows():
    html_table += f"""
  <tr>
    <td>{row['Variável']}</td>
    <td style="text-align: right;">{row['Média']:.2f}</td>
    <td style="text-align: right;">{row['Desvio Padrão']:.2f}</td>
  </tr>
"""

# Close the HTML table
html_table += """
</table>
"""

# Display the HTML table in Streamlit
st.markdown(html_table, unsafe_allow_html=True)