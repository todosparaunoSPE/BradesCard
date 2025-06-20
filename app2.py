# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 13:18:30 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# -----------------------
# ENCABEZADO PROFESIONAL
# -----------------------
st.set_page_config(page_title="Simulación de Gestión de Cuentas", layout="wide")

st.title("📌 Simulación de Asignaciones de Cartera")
st.markdown("""
**Vacante:** Analista de Asignaciones de Cartera  
**Candidato:** Javier Horacio Pérez Ricárdez  

Esta aplicación la desarrollé como una demostración interactiva de las principales funciones que se desempeñan en la vacante mencionada. Permite simular:
- Exclusión de cuentas por estado (ARCO, aclaración, liquidado)
- Asignaciones por cartera (Administrativa, Extrajudicial)
- Envío de IVR
- Reportes de productividad
- Visualización dinámica con gráficas interactivas
""")

# -----------------------
# SIMULACIÓN DE DATOS
# -----------------------
np.random.seed(42)
num_cuentas = 100

data = {
    'ID_Cuenta': range(1, num_cuentas + 1),
    'Estado': np.random.choice(['Normal', 'Arco', 'Aclaración', 'Liquidado'], num_cuentas),
    'Cartera': np.random.choice(['Administrativa', 'Extrajudicial'], num_cuentas),
    'Fecha_Limite_Pago': [datetime.today() + timedelta(days=np.random.randint(-30, 30)) for _ in range(num_cuentas)],
    'Monto': np.round(np.random.uniform(1000, 50000, num_cuentas), 2),
    'IVR_Enviado': np.random.choice([False, True], num_cuentas)
}

df = pd.DataFrame(data)

# -----------------------
# SIDEBAR - FILTROS
# -----------------------
st.sidebar.title("🎛️ Filtros de Exclusión")
excluir_estado = st.sidebar.multiselect("Excluir cuentas por estado:", ['Arco', 'Aclaración', 'Liquidado'])
df_filtrado = df[~df['Estado'].isin(excluir_estado)]

carteras = st.sidebar.multiselect("Selecciona cartera:", df_filtrado['Cartera'].unique(), default=df_filtrado['Cartera'].unique())
df_filtrado = df_filtrado[df_filtrado['Cartera'].isin(carteras)]

# -----------------------
# MÉTRICAS PRINCIPALES
# -----------------------
col1, col2 = st.columns(2)
col1.metric("🔢 Total de cuentas activas", len(df_filtrado))
col2.metric("💰 Monto total", f"${df_filtrado['Monto'].sum():,.2f}")

# -----------------------
# TABLA DE CUENTAS
# -----------------------
st.subheader("📄 Detalle de cuentas filtradas")
st.dataframe(df_filtrado, use_container_width=True)

# -----------------------
# BOTÓN DE ENVÍO IVR
# -----------------------
st.subheader("📞 Simulación de Envío IVR")
if st.button("Enviar IVR a cuentas visibles"):
    df_filtrado['IVR_Enviado'] = True
    st.success("✅ IVR enviado exitosamente a las cuentas visibles.")
    st.dataframe(df_filtrado, use_container_width=True)

# -----------------------
# REPORTE DE PRODUCTIVIDAD
# -----------------------
st.subheader("📈 Reporte de Productividad por Cartera")
productividad = df_filtrado.groupby('Cartera').agg({'Monto': 'sum', 'ID_Cuenta': 'count'})
productividad.rename(columns={'Monto': 'Monto Total', 'ID_Cuenta': 'Cuentas'}, inplace=True)
st.table(productividad)

# -----------------------
# GRÁFICOS INTERACTIVOS
# -----------------------
st.subheader("📊 Gráficos Dinámicos")

# Gráfico 1: Cantidad de cuentas por cartera
fig1 = px.bar(df_filtrado, x='Cartera', title='Número de cuentas por cartera', color='Cartera',
              labels={'Cartera': 'Tipo de cartera'}, barmode='group')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Monto total por cartera (pie chart)
fig2 = px.pie(productividad.reset_index(), names='Cartera', values='Monto Total',
              title='Distribución del monto total por cartera')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Evolución del monto en el tiempo
df_linea = df_filtrado.copy()
df_linea['Fecha'] = df_linea['Fecha_Limite_Pago'].dt.date
line_plot = df_linea.groupby('Fecha').agg({'Monto': 'sum'}).reset_index()

fig3 = px.line(line_plot, x='Fecha', y='Monto', title='Evolución del monto según fecha límite de pago')
st.plotly_chart(fig3, use_container_width=True)
