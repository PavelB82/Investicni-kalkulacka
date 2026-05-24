{\rtf1\ansi\ansicpg1250\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw16840\paperh23820\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import streamlit as st\
import numpy as np\
import plotly.graph_objects as go\
\
# Nastaven\'ed vzhledu str\'e1nky\
st.set_page_config(page_title="Kombinovan\'e1 investi\uc0\u269 n\'ed kalkula\u269 ka", layout="wide")\
\
st.title("\uc0\u55357 \u56522  Interaktivn\'ed investi\u269 n\'ed kalkula\u269 ka")\
st.markdown("Simulace kombinovan\'e9ho portfolia (**60 % akcie, 25 % dluhopisy, 15 % nemovitosti**) na horizontu a\'9e 40 let.")\
\
# Bo\uc0\u269 n\'ed panel pro u\'9eivatelsk\'e9 vstupy\
st.sidebar.header("Vstupn\'ed parametry")\
initial_investment = st.sidebar.number_input("Po\uc0\u269 \'e1te\u269 n\'ed jednor\'e1zov\'fd vklad (K\u269 ):", value=850000, step=50000, format="%d")\
monthly_investment = st.sidebar.number_input("Pravideln\'e1 m\uc0\u283 s\'ed\u269 n\'ed \'falo\'9eka (K\u269 ):", value=5000, step=500, format="%d")\
horizon = st.sidebar.slider("Investi\uc0\u269 n\'ed horizont (roky):", min_value=1, max_value=40, value=20)\
\
st.sidebar.subheader("O\uc0\u269 ek\'e1van\'e9 ro\u269 n\'ed v\'fdnosy (Neutr\'e1ln\'ed)")\
r_eq = st.sidebar.slider("Glob\'e1ln\'ed akcie (v\'e1ha 60 %):", 0.0, 15.0, 8.0, 0.5) / 100\
r_bo = st.sidebar.slider("Dluhopisy (v\'e1ha 25 %):", 0.0, 10.0, 4.0, 0.5) / 100\
r_re = st.sidebar.slider("Nemovitosti (v\'e1ha 15 %):", 0.0, 10.0, 5.0, 0.5) / 100\
\
st.sidebar.subheader("Riziko")\
volatility = st.sidebar.slider("Ro\uc0\u269 n\'ed volatilita portfolia (\u963 ) (%):", 5.0, 20.0, 10.0, 0.5) / 100\
\
# Matematick\'e9 v\'fdpo\uc0\u269 ty sc\'e9n\'e1\u345 \u367 \
w_eq, w_bo, w_re = 0.60, 0.25, 0.15\
r_neutral = (w_eq * r_eq) + (w_bo * r_bo) + (w_re * r_re)\
horizon_vol = volatility / np.sqrt(horizon)\
\
r_pes = r_neutral - horizon_vol\
r_opt = r_neutral + horizon_vol\
\
# P\uc0\u345 \'edprava pol\'ed pro ukl\'e1d\'e1n\'ed v\'fdvoje v \u269 ase\
years = np.arange(0, horizon + 1)\
val_pes = np.zeros(horizon + 1)\
val_neu = np.zeros(horizon + 1)\
val_opt = np.zeros(horizon + 1)\
\
# Nastaven\'ed nult\'e9ho roku (po\uc0\u269 \'e1te\u269 n\'ed vklad)\
val_pes[0] = initial_investment\
val_neu[0] = initial_investment\
val_opt[0] = initial_investment\
\
# V\'fdpo\uc0\u269 et slo\'9een\'e9ho \'faro\u269 en\'ed s pravideln\'fdm m\u283 s\'ed\u269 n\'edm vkladem rok po roce\
for y in range(1, horizon + 1):\
    val_pes[y] = val_pes[y-1] * (1 + r_pes) + monthly_investment * 12 * (1 + r_pes / 2)\
    val_neu[y] = val_neu[y-1] * (1 + r_neutral) + monthly_investment * 12 * (1 + r_neutral / 2)\
    val_opt[y] = val_opt[y-1] * (1 + r_opt) + monthly_investment * 12 * (1 + r_opt / 2)\
\
# Vykreslen\'ed v\'fdsledn\'fdch karet (Metrics) nad grafem\
col1, col2, col3 = st.columns(3)\
col1.metric("Pesimistick\'fd sc\'e9n\'e1\uc0\u345  (-1\u963 )", f"\{val_pes[-1]:,.0f\} K\u269 ".replace(",", " "), f"\{r_pes*100:.2f\} % p.a.", delta_color="inverse")\
col2.metric("Neutr\'e1ln\'ed sc\'e9n\'e1\uc0\u345  (Z\'e1klad)", f"\{val_neu[-1]:,.0f\} K\u269 ".replace(",", " "), f"\{r_neutral*100:.2f\} % p.a.")\
col3.metric("Optimistick\'fd sc\'e9n\'e1\uc0\u345  (+1\u963 )", f"\{val_opt[-1]:,.0f\} K\u269 ".replace(",", " "), f"\{r_opt*100:.2f\} % p.a.")\
\
# Tvorba interaktivn\'edho grafu p\uc0\u345 es Plotly\
fig = go.Figure()\
fig.add_trace(go.Scatter(x=years, y=val_neu, name="Neutr\'e1ln\'ed sc\'e9n\'e1\uc0\u345 ", line=dict(color="#1F4E78", width=3)))\
fig.add_trace(go.Scatter(x=years, y=val_opt, name="Optimistick\'fd sc\'e9n\'e1\uc0\u345 ", line=dict(color="#2E7D32", width=2, dash="dash")))\
fig.add_trace(go.Scatter(x=years, y=val_pes, name="Pesimistick\'fd sc\'e9n\'e1\uc0\u345 ", line=dict(color="#C62828", width=2, dash="dash")))\
\
# Form\'e1tov\'e1n\'ed designu grafu a automatick\'e9 dynamick\'e9 osy X\
fig.update_layout(\
    title=f"Projekce v\'fdvoje investice (Horizont \{horizon\} let)",\
    xaxis_title="Roky investov\'e1n\'ed",\
    yaxis_title="Hodnota portfolia (K\uc0\u269 )",\
    hovermode="x unified",\
    template="plotly_white",\
    xaxis=dict(\
        tickmode='linear', \
        tick0=0, \
        dtick=1 if horizon <= 15 else 2 if horizon <= 25 else 5\
    )\
)\
\
# Zobrazen\'ed grafu na webov\'e9 str\'e1nce\
st.plotly_chart(fig, use_container_width=True)}