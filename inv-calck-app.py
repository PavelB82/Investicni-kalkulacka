import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Nastavení vzhledu stránky
st.set_page_config(page_title="Kombinovaná investiční kalkulačka", layout="wide")

st.title("📊 Interaktivní investiční kalkulačka")
st.markdown("Simulace kombinovaného portfolia (**60 % akcie, 25 % dluhopisy, 15 % nemovitosti**) na horizontu až 40 let.")

# Boční panel pro uživatelské vstupy
st.sidebar.header("Vstupní parametry")
initial_investment = st.sidebar.number_input("Počáteční jednorázový vklad (Kč):", value=850000, step=50000, format="%d")
monthly_investment = st.sidebar.number_input("Pravidelná měsíční úložka (Kč):", value=5000, step=500, format="%d")
horizon = st.sidebar.slider("Investiční horizont (roky):", min_value=1, max_value=40, value=20)

st.sidebar.subheader("Očekávané roční výnosy (Neutrální)")
r_eq = st.sidebar.slider("Globální akcie (váha 60 %):", 0.0, 15.0, 8.0, 0.5) / 100
r_bo = st.sidebar.slider("Dluhopisy (váha 25 %):", 0.0, 10.0, 4.0, 0.5) / 100
r_re = st.sidebar.slider("Nemovitosti (váha 15 %):", 0.0, 10.0, 5.0, 0.5) / 100

st.sidebar.subheader("Riziko")
volatility = st.sidebar.slider("Roční volatilita portfolia (σ) (%):", 5.0, 20.0, 10.0, 0.5) / 100

# Matematické výpočty scénářů
w_eq, w_bo, w_re = 0.60, 0.25, 0.15
r_neutral = (w_eq * r_eq) + (w_bo * r_bo) + (w_re * r_re)
horizon_vol = volatility / np.sqrt(horizon)

r_pes = r_neutral - horizon_vol
r_opt = r_neutral + horizon_vol

# Příprava polí pro ukládání vývoje v čase
years = np.arange(0, horizon + 1)
val_pes = np.zeros(horizon + 1)
val_neu = np.zeros(horizon + 1)
val_opt = np.zeros(horizon + 1)

# Nastavení nultého roku (počáteční vklad)
val_pes[0] = initial_investment
val_neu[0] = initial_investment
val_opt[0] = initial_investment

# Výpočet složeného úročení s pravidelným měsíčním vkladem rok po roce
for y in range(1, horizon + 1):
    val_pes[y] = val_pes[y-1] * (1 + r_pes) + monthly_investment * 12 * (1 + r_pes / 2)
    val_neu[y] = val_neu[y-1] * (1 + r_neutral) + monthly_investment * 12 * (1 + r_neutral / 2)
    val_opt[y] = val_opt[y-1] * (1 + r_opt) + monthly_investment * 12 * (1 + r_opt / 2)

# Vykreslení výsledných karet (Metrics) nad grafem
col1, col2, col3 = st.columns(3)
col1.metric("Pesimistický scénář (-1σ)", f"{val_pes[-1]:,.0f} Kč".replace(",", " "), f"{r_pes*100:.2f} % p.a.", delta_color="inverse")
col2.metric("Neutrální scénář (Základ)", f"{val_neu[-1]:,.0f} Kč".replace(",", " "), f"{r_neutral*100:.2f} % p.a.")
col3.metric("Optimistický scénář (+1σ)", f"{val_opt[-1]:,.0f} Kč".replace(",", " "), f"{r_opt*100:.2f} % p.a.")

# Tvorba interaktivního grafu přes Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=val_neu, name="Neutrální scénář", line=dict(color="#1F4E78", width=3)))
fig.add_trace(go.Scatter(x=years, y=val_opt, name="Optimistický scénář", line=dict(color="#2E7D32", width=2, dash="dash")))
fig.add_trace(go.Scatter(x=years, y=val_pes, name="Pesimistický scénář", line=dict(color="#C62828", width=2, dash="dash")))

# Formátování designu grafu a automatické dynamické osy X
fig.update_layout(
    title=f"Projekce vývoje investice (Horizont {horizon} let)",
    xaxis_title="Roky investování",
    yaxis_title="Hodnota portfolia (Kč)",
    hovermode="x unified",
    template="plotly_white",
    xaxis=dict(
        tickmode='linear', 
        tick0=0, 
        dtick=1 if horizon <= 15 else 2 if horizon <= 25 else 5
    )
)

# Zobrazení grafu na webové stránce
st.plotly_chart(fig, use_container_width=True)
