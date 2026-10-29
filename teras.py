import math
import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("Teraskonstruktsiooni projekt")

# --- KOOSTAVAD KONSTANTID (Mitte-muudetavad) ---
g_plekk_kg = 10.0
g_roov_kg = 10.0
g_fassaad_kg = 20.0

mu = 0.80
gamma_M0 = 1.00
gamma_M1 = 1.00
gamma_M2 = 1.25

E = 210000.0  # N/mm²
eta = 1.2

# --- PROFIILIDE ANDMEBAAS (HEA) ---
profiilide_andmed = {
    "HEA": {
        "HE 100 A": {"G": 16.7, "A": 21.2, "h": 96, "b": 100, "tw": 5.0, "tf": 8.0, "r": 12.0, "Iy": 349.2, "Wel_y": 72.75, "Wpl_y": 83.01, "iy": 4.0, "Iz": 133.8, "Wel_z": 26.76, "Wpl_z": 41.14, "iz": 2.5, "It": 5.283, "Iw": 2.581},
        "HE 120 A": {"G": 19.9, "A": 25.3, "h": 114, "b": 120, "tw": 5.0, "tf": 8.0, "r": 12.0, "Iy": 606.1, "Wel_y": 106.3, "Wpl_y": 119.4, "iy": 4.8, "Iz": 230.8, "Wel_z": 38.48, "Wpl_z": 58.85, "iz": 3.0, "It": 6.041, "Iw": 6.471},
        "HE 140 A": {"G": 24.7, "A": 31.4, "h": 133, "b": 140, "tw": 5.5, "tf": 8.5, "r": 12.0, "Iy": 1033.0, "Wel_y": 155.3, "Wpl_y": 173.4, "iy": 5.7, "Iz": 389.3, "Wel_z": 55.61, "Wpl_z": 84.84, "iz": 3.5, "It": 8.101, "Iw": 15.06},
        "HE 160 A": {"G": 30.4, "A": 38.8, "h": 152, "b": 160, "tw": 6.0, "tf": 9.0, "r": 15.0, "Iy": 1672.0, "Wel_y": 220.1, "Wpl_y": 245.1, "iy": 6.5, "Iz": 615.5, "Wel_z": 76.94, "Wpl_z": 117.6, "iz": 3.9, "It": 12.09, "Iw": 31.4},
        "HE 180 A": {"G": 35.5, "A": 45.3, "h": 171, "b": 180, "tw": 6.0, "tf": 9.5, "r": 15.0, "Iy": 2510.0, "Wel_y": 293.6, "Wpl_y": 324.8, "iy": 7.4, "Iz": 924.6, "Wel_z": 102.7, "Wpl_z": 156.4, "iz": 4.5, "It": 14.88, "Iw": 60.21},
        "HE 200 A": {"G": 42.3, "A": 53.8, "h": 190, "b": 200, "tw": 6.5, "tf": 10.0, "r": 18.0, "Iy": 3692.0, "Wel_y": 388.6, "Wpl_y": 429.4, "iy": 8.2, "Iz": 1335.0, "Wel_z": 133.5, "Wpl_z": 203.8, "iz": 4.9, "It": 21.04, "Iw": 108.0},
        "HE 220 A": {"G": 50.5, "A": 64.3, "h": 210, "b": 220, "tw": 7.0, "tf": 11.0, "r": 18.0, "Iy": 5409.0, "Wel_y": 515.2, "Wpl_y": 568.4, "iy": 9.1, "Iz": 1954.0, "Wel_z": 177.6, "Wpl_z": 270.5, "iz": 5.5, "It": 28.61, "Iw": 193.2},
        "HE 240 A": {"G": 60.3, "A": 76.8, "h": 230, "b": 240, "tw": 7.5, "tf": 12.0, "r": 21.0, "Iy": 7763.0, "Wel_y": 675.0, "Wpl_y": 744.6, "iy": 10.0, "Iz": 2768.0, "Wel_z": 230.7, "Wpl_z": 351.6, "iz": 6.0, "It": 42.14, "Iw": 328.4},
        "HE 260 A": {"G": 68.2, "A": 86.8, "h": 250, "b": 260, "tw": 7.5, "tf": 12.5, "r": 24.0, "Iy": 10450.0, "Wel_y": 836.3, "Wpl_y": 919.7, "iy": 10.9, "Iz": 3667.0, "Wel_z": 282.1, "Wpl_z": 430.1, "iz": 6.4, "It": 54.19, "Iw": 516.3},
        "HE 280 A": {"G": 76.4, "A": 97.3, "h": 270, "b": 280, "tw": 8.0, "tf": 13.0, "r": 24.0, "Iy": 13670.0, "Wel_y": 1012.0, "Wpl_y": 1112.0, "iy": 11.8, "Iz": 4762.0, "Wel_z": 340.1, "Wpl_z": 518.1, "iz": 6.9, "It": 63.45, "Iw": 785.3},
        "HE 300 A": {"G": 88.3, "A": 112.5, "h": 290, "b": 300, "tw": 8.5, "tf": 14.0, "r": 27.0, "Iy": 18260.0, "Wel_y": 1259.0, "Wpl_y": 1383.0, "iy": 12.7, "Iz": 6309.0, "Wel_z": 420.6, "Wpl_z": 641.1, "iz": 7.4, "It": 87.76, "Iw": 1199.0},
        "HE 320 A": {"G": 97.6, "A": 124.4, "h": 310, "b": 300, "tw": 9.0, "tf": 15.5, "r": 27.0, "Iy": 22920.0, "Wel_y": 1479.0, "Wpl_y": 1628.0, "iy": 13.5, "Iz": 6985.0, "Wel_z": 465.6, "Wpl_z": 709.7, "iz": 7.4, "It": 111.8, "Iw": 1512.0},
        "HE 340 A": {"G": 105.0, "A": 133.5, "h": 330, "b": 300, "tw": 9.5, "tf": 16.5, "r": 27.0, "Iy": 27690.0, "Wel_y": 1678.0, "Wpl_y": 1850.0, "iy": 14.4, "Iz": 7435.0, "Wel_z": 495.7, "Wpl_z": 755.9, "iz": 7.4, "It": 131.4, "Iw": 1824.0},
        "HE 360 A": {"G": 112.0, "A": 142.8, "h": 350, "b": 300, "tw": 10.0, "tf": 17.5, "r": 27.0, "Iy": 33080.0, "Wel_y": 1890.0, "Wpl_y": 2088.0, "iy": 15.2, "Iz": 7886.0, "Wel_z": 525.7, "Wpl_z": 802.2, "iz": 7.4, "It": 153.3, "Iw": 2176.0},
        "HE 400 A": {"G": 125.0, "A": 159.0, "h": 390, "b": 300, "tw": 11.0, "tf": 19.0, "r": 27.0, "Iy": 45060.0, "Wel_y": 2311.0, "Wpl_y": 2561.0, "iy": 16.8, "Iz": 8563.0, "Wel_z": 570.9, "Wpl_z": 872.8, "iz": 7.3, "It": 193.1, "Iw": 2942.0},
        "HE 450 A": {"G": 140.0, "A": 178.0, "h": 440, "b": 300, "tw": 11.5, "tf": 21.0, "r": 27.0, "Iy": 63720.0, "Wel_y": 2896.0, "Wpl_y": 3215.0, "iy": 18.9, "Iz": 9465.0, "Wel_z": 631.0, "Wpl_z": 965.5, "iz": 7.2, "It": 250.1, "Iw": 4147.0},
        "HE 500 A": {"G": 155.0, "A": 197.5, "h": 490, "b": 300, "tw": 12.0, "tf": 23.0, "r": 27.0, "Iy": 86970.0, "Wel_y": 3549.0, "Wpl_y": 3948.0, "iy": 20.9, "Iz": 10360.0, "Wel_z": 691.1, "Wpl_z": 1058.0, "iz": 7.2, "It": 317.8, "Iw": 5643.0},
        "HE 550 A": {"G": 166.0, "A": 211.8, "h": 540, "b": 300, "tw": 12.5, "tf": 24.0, "r": 27.0, "Iy": 111930.0, "Wel_y": 4145.0, "Wpl_y": 4621.0, "iy": 22.9, "Iz": 10810.0, "Wel_z": 721.2, "Wpl_z": 1106.0, "iz": 7.1, "It": 360.3, "Iw": 7188.0},
        "HE 600 A": {"G": 178.0, "A": 226.5, "h": 590, "b": 300, "tw": 13.0, "tf": 25.0, "r": 27.0, "Iy": 141200.0, "Wel_y": 4786.0, "Wpl_y": 5350.0, "iy": 24.9, "Iz": 11270.0, "Wel_z": 751.4, "Wpl_z": 1155.0, "iz": 7.0, "It": 406.8, "Iw": 8978.0},
        "HE 650 A": {"G": 190.0, "A": 241.6, "h": 640, "b": 300, "tw": 13.5, "tf": 26.0, "r": 27.0, "Iy": 175170.0, "Wel_y": 5474.0, "Wpl_y": 6136.0, "iy": 26.9, "Iz": 11720.0, "Wel_z": 781.5, "Wpl_z": 1204.0, "iz": 6.9, "It": 457.6, "Iw": 11020.0},
        "HE 700 A": {"G": 204.0, "A": 260.5, "h": 690, "b": 300, "tw": 14.5, "tf": 27.0, "r": 27.0, "Iy": 215300.0, "Wel_y": 6240.0, "Wpl_y": 7031.0, "iy": 28.7, "Iz": 12170.0, "Wel_z": 811.9, "Wpl_z": 1256.0, "iz": 6.8, "It": 521.5, "Iw": 13350.0},
        "HE 800 A": {"G": 224.0, "A": 285.8, "h": 790, "b": 300, "tw": 15.0, "tf": 28.0, "r": 30.0, "Iy": 303440.0, "Wel_y": 7682.0, "Wpl_y": 8699.0, "iy": 32.5, "Iz": 12630.0, "Wel_z": 842.5, "Wpl_z": 1312.0, "iz": 6.6, "It": 608.6, "Iw": 18290.0},
        "HE 900 A": {"G": 252.0, "A": 320.5, "h": 890, "b": 300, "tw": 16.0, "tf": 30.0, "r": 30.0, "Iy": 422070.0, "Wel_y": 9484.0, "Wpl_y": 10810.0, "iy": 36.2, "Iz": 13540.0, "Wel_z": 903.1, "Wpl_z": 1414.0, "iz": 6.4, "It": 749.0, "Iw": 24960.0},
        "HE 1000 A": {"G": 272.0, "A": 346.8, "h": 990, "b": 300, "tw": 16.5, "tf": 31.0, "r": 30.0, "Iy": 553840.0, "Wel_y": 11180.0, "Wpl_y": 12820.0, "iy": 39.9, "Iz": 14000.0, "Wel_z": 933.6, "Wpl_z": 1469.0, "iz": 6.3, "It": 834.8, "Iw": 32070.0},
    },
    "IPE": {
        "IPE 80": {"G": 6.0, "A": 7.6, "h": 80, "b": 46, "tw": 3.8, "tf": 5.2, "r": 5.0, "Iy": 80.13, "Wel_y": 20.03, "Wpl_y": 23.21, "iy": 3.2, "Iz": 8.489, "Wel_z": 3.69, "Wpl_z": 5.817, "iz": 1.0, "It": 0.672, "Iw": 0.117},
        "IPE 100": {"G": 8.1, "A": 10.3, "h": 100, "b": 55, "tw": 4.1, "tf": 5.7, "r": 7.0, "Iy": 171.0, "Wel_y": 34.2, "Wpl_y": 39.4, "iy": 4.0, "Iz": 15.91, "Wel_z": 5.788, "Wpl_z": 9.145, "iz": 1.2, "It": 1.157, "Iw": 0.351},
        "IPE 120": {"G": 10.4, "A": 13.2, "h": 120, "b": 64, "tw": 4.4, "tf": 6.3, "r": 7.0, "Iy": 317.7, "Wel_y": 52.95, "Wpl_y": 60.72, "iy": 4.9, "Iz": 27.66, "Wel_z": 8.646, "Wpl_z": 13.58, "iz": 1.4, "It": 1.69, "Iw": 0.889},
        "IPE 140": {"G": 12.9, "A": 16.4, "h": 140, "b": 73, "tw": 4.7, "tf": 6.9, "r": 7.0, "Iy": 541.2, "Wel_y": 77.31, "Wpl_y": 88.34, "iy": 5.7, "Iz": 44.91, "Wel_z": 12.3, "Wpl_z": 19.24, "iz": 1.6, "It": 2.399, "Iw": 1.981},
        "IPE 160": {"G": 15.8, "A": 20.1, "h": 160, "b": 82, "tw": 5.0, "tf": 7.4, "r": 9.0, "Iy": 869.2, "Wel_y": 108.6, "Wpl_y": 123.8, "iy": 6.5, "Iz": 68.31, "Wel_z": 16.66, "Wpl_z": 26.09, "iz": 1.8, "It": 3.54, "Iw": 3.958},
        "IPE 180": {"G": 18.8, "A": 23.9, "h": 180, "b": 91, "tw": 5.3, "tf": 8.0, "r": 9.0, "Iy": 1316.0, "Wel_y": 146.3, "Wpl_y": 166.4, "iy": 7.4, "Iz": 100.8, "Wel_z": 22.16, "Wpl_z": 34.59, "iz": 2.0, "It": 4.726, "Iw": 7.431},
        "IPE 200": {"G": 22.4, "A": 28.5, "h": 200, "b": 100, "tw": 5.6, "tf": 8.5, "r": 12.0, "Iy": 1943.0, "Wel_y": 194.3, "Wpl_y": 220.6, "iy": 8.2, "Iz": 142.3, "Wel_z": 28.47, "Wpl_z": 44.61, "iz": 2.2, "It": 6.915, "Iw": 12.98},
        "IPE 220": {"G": 26.2, "A": 33.4, "h": 220, "b": 110, "tw": 5.9, "tf": 9.2, "r": 12.0, "Iy": 2771.0, "Wel_y": 251.9, "Wpl_y": 285.4, "iy": 9.1, "Iz": 204.8, "Wel_z": 37.25, "Wpl_z": 58.11, "iz": 2.4, "It": 9.03, "Iw": 22.67},
        "IPE 240": {"G": 30.7, "A": 39.1, "h": 240, "b": 120, "tw": 6.2, "tf": 9.8, "r": 15.0, "Iy": 3891.0, "Wel_y": 324.3, "Wpl_y": 366.6, "iy": 9.9, "Iz": 283.6, "Wel_z": 47.27, "Wpl_z": 73.92, "iz": 2.6, "It": 12.95, "Iw": 37.39},
        "IPE 270": {"G": 36.1, "A": 45.9, "h": 270, "b": 135, "tw": 6.6, "tf": 10.2, "r": 15.0, "Iy": 5789.0, "Wel_y": 428.8, "Wpl_y": 483.9, "iy": 11.2, "Iz": 419.8, "Wel_z": 62.2, "Wpl_z": 96.95, "iz": 3.0, "It": 15.9, "Iw": 70.57},
        "IPE 300": {"G": 42.2, "A": 53.8, "h": 300, "b": 150, "tw": 7.1, "tf": 10.7, "r": 15.0, "Iy": 8356.0, "Wel_y": 557.0, "Wpl_y": 628.3, "iy": 12.4, "Iz": 603.7, "Wel_z": 80.5, "Wpl_z": 125.2, "iz": 3.3, "It": 19.91, "Iw": 125.9},
        "IPE 330": {"G": 49.1, "A": 62.6, "h": 330, "b": 160, "tw": 7.5, "tf": 11.5, "r": 18.0, "Iy": 11760.0, "Wel_y": 713.1, "Wpl_y": 804.3, "iy": 13.7, "Iz": 788.1, "Wel_z": 98.51, "Wpl_z": 153.6, "iz": 3.5, "It": 28.06, "Iw": 199.0},
        "IPE 360": {"G": 57.1, "A": 72.7, "h": 360, "b": 170, "tw": 8.0, "tf": 12.7, "r": 18.0, "Iy": 16260.0, "Wel_y": 903.6, "Wpl_y": 1019.0, "iy": 14.9, "Iz": 1043.0, "Wel_z": 122.7, "Wpl_z": 191.0, "iz": 3.7, "It": 37.44, "Iw": 313.5},
        "IPE 400": {"G": 66.3, "A": 84.5, "h": 400, "b": 180, "tw": 8.6, "tf": 13.5, "r": 21.0, "Iy": 23120.0, "Wel_y": 1156.0, "Wpl_y": 1307.0, "iy": 16.5, "Iz": 1317.0, "Wel_z": 146.4, "Wpl_z": 229.0, "iz": 3.9, "It": 51.27, "Iw": 490.0},
        "IPE 450": {"G": 77.6, "A": 98.8, "h": 450, "b": 190, "tw": 9.4, "tf": 14.6, "r": 21.0, "Iy": 33740.0, "Wel_y": 1499.0, "Wpl_y": 1701.0, "iy": 18.4, "Iz": 1675.0, "Wel_z": 176.4, "Wpl_z": 276.3, "iz": 4.1, "It": 66.74, "Iw": 791.0},
        "IPE 500": {"G": 90.7, "A": 115.5, "h": 500, "b": 200, "tw": 10.2, "tf": 16.0, "r": 21.0, "Iy": 48190.0, "Wel_y": 1927.0, "Wpl_y": 2194.0, "iy": 20.4, "Iz": 2141.0, "Wel_z": 214.1, "Wpl_z": 335.8, "iz": 4.3, "It": 89.09, "Iw": 1249.0},
        "IPE 550": {"G": 106.0, "A": 134.4, "h": 550, "b": 210, "tw": 11.1, "tf": 17.2, "r": 24.0, "Iy": 67110.0, "Wel_y": 2440.0, "Wpl_y": 2787.0, "iy": 22.3, "Iz": 2667.0, "Wel_z": 254.0, "Wpl_z": 400.5, "iz": 4.4, "It": 122.8, "Iw": 1884.0},
        "IPE 600": {"G": 122.0, "A": 156.0, "h": 600, "b": 220, "tw": 12.0, "tf": 19.0, "r": 24.0, "Iy": 92080.0, "Wel_y": 3069.0, "Wpl_y": 3512.0, "iy": 24.2, "Iz": 3387.0, "Wel_z": 307.9, "Wpl_z": 485.6, "iz": 4.6, "It": 165.2, "Iw": 2845.0},
    }
}

# --- SIDEBAR SISENDID ---
st.sidebar.header("1. Hoone lähteandmed")
L = st.sidebar.number_input("Hoone pikkus L (m)", min_value=0.0, value=40.0, step=1.0)
B = st.sidebar.number_input("Hoone laius B (m)", min_value=0.0, value=20.0, step=1.0)
b = st.sidebar.number_input("Raamide vahe b (m)", min_value=0.1, value=5.0, step=1.0)
H = st.sidebar.number_input("Posti arvutuskõrgus H (m)", min_value=0.0, value=9.0, step=0.5)
r_tk = st.sidebar.number_input("Roovide koguarv (tk)", min_value=2, value=9, step=1)

st.sidebar.header("2. Koormuste sisendid")
s_k = st.sidebar.number_input("Lume normkoormus maapinnal s_k (kN/m²)", value=1.75, step=0.05)
w_e_H = st.sidebar.number_input("Tuulerõhk w_e,H (kN/m²)", value=-0.455, step=0.05)

st.sidebar.header("3. Terase valik")
teras_klass = st.sidebar.selectbox("Terase klass", ["S235", "S355"], index=1)

st.sidebar.header("4. Tala ristlõike valik")
tala_sarja_valik = st.sidebar.selectbox("Tala valik", ["HEA", "IPE"])
saadaval_profiilid = list(profiilide_andmed[tala_sarja_valik].keys())
vaike_index = 1 if len(saadaval_profiilid) > 1 else 0
valitud_profiil = st.sidebar.selectbox("Profiili tüüp", saadaval_profiilid, index=vaike_index)
# --- ARVUTUSED ---
raamide_arv = int(L / b) + 1 if b > 0 else 0
roove_poolel = r_tk / 2
katuse_projektsioon_poolel = B / 2
vahede_arv_poolel = max(1, math.ceil(roove_poolel) - 1)
roovide_samm = katuse_projektsioon_poolel / vahede_arv_poolel

q_s = mu * s_k
prof_parand = profiilide_andmed[tala_sarja_valik][valitud_profiil]

g_tala_kg_m = prof_parand["G"]
g_tala_kn_m = g_tala_kg_m / 100.0


s_k_kg = s_k * 100
q_s_kg = q_s * 100
w_e_H_kg = w_e_H * 100
g_plekk_kn = g_plekk_kg / 100
g_roov_kn = g_roov_kg / 100
g_fassaad_kn = g_fassaad_kg / 100

koormusala = b * roovide_samm
F_q_s = q_s * koormusala
F_w_e_H = w_e_H * koormusala
F_g_plekk = g_plekk_kn * koormusala
F_g_roov = g_roov_kn * koormusala

if teras_klass == "S235":
    f_y = 235.0
    f_u = 360.0
    epsilon = 1.0
else:
    f_y = 355.0
    f_u = 510.0
    epsilon = 0.81

f_yd = f_y / gamma_M0

# --- SLS sisejõudude vaikeväärtused ---
# Tala sildeks kasutatakse hoone laiust B. Tala omakaal on lauskoormus;
# pleki, roovide, lume ja tuule koormused mõjuvad punktkoormustena.
span = B
n_roove = max(2, int(r_tk))
n_punktkoormusi = n_roove - 1  # ääres pool koormust, vahepeal täiskoormused

# Arvutab punktkoormuse tekitatud momendi kasutaja antud valemi järgi.
def punktkoormuse_moment(F, span, samm, roovide_arv):
    if samm <= 0:
        return 0.0
    parandus = 0.0 if roovide_arv % 2 == 1 else samm * F / 8.0
    return F * span**2 / (8.0 * samm) - parandus

def sisejoud_vaike(gamma_G, gamma_Q, lumi=False, tuul=False):
    # Tala omakaalu lauskoormuse moment: q*L^2/8.
    M_tala = gamma_G * g_tala_kn_m * span**2 / 8.0

    # Punktkoormustest tulenevad momendid. Koormustegurid rakendatakse igale koormusele.
    M_plekk = punktkoormuse_moment(gamma_G * F_g_plekk, span, roovide_samm, n_roove)
    M_roov = punktkoormuse_moment(gamma_G * F_g_roov, span, roovide_samm, n_roove)
    M_lumi = punktkoormuse_moment(gamma_Q * F_q_s, span, roovide_samm, n_roove) if lumi else 0.0
    M_tuul = punktkoormuse_moment(gamma_Q * F_w_e_H, span, roovide_samm, n_roove) if tuul else 0.0
    M = M_tala + M_plekk + M_roov + M_lumi + M_tuul

    # Sümmeetrilise tala reaktsioon: lauskoormuse summa + punktkoormuste summa, jagatud kahega.
    q_tala = gamma_G * g_tala_kn_m
    summa_punkt = n_punktkoormusi * (gamma_G * (F_g_plekk + F_g_roov)
                                     + (gamma_Q * F_q_s if lumi else 0.0)
                                     + (gamma_Q * F_w_e_H if tuul else 0.0))
    R = (q_tala * span + summa_punkt) / 2.0

    # Põikjõud toe juures: reaktsioonist lahutatakse äärepunkti koormusest pool.
    F_aar = (gamma_G * (F_g_plekk + F_g_roov)
             + (gamma_Q * F_q_s if lumi else 0.0)
             + (gamma_Q * F_w_e_H if tuul else 0.0)) / 2.0
    V = R - F_aar
    return M, V, R

# SLS 1 = ULS1 koormused: 1,2 omakaal + 1,5 lumi.
M_vaike_sls1, V_vaike_sls1, R_vaike_sls1 = sisejoud_vaike(1.2, 1.5, lumi=True)
# SLS 2 = ULS2 koormused: 1,0 omakaal + 1,5 tuul.
M_vaike_sls2, V_vaike_sls2, R_vaike_sls2 = sisejoud_vaike(1.0, 1.5, tuul=True)

st.sidebar.header("Sisejõud")

# SLS 1 sisendid
st.sidebar.subheader("ULS 1")

st.sidebar.markdown("$M_{max,uls1}$ [kNm]")
M_max_sls1 = st.sidebar.number_input("M_max,uls1", min_value=-1.0e9, value=float(M_vaike_sls1), step=1.0, label_visibility="collapsed")

st.sidebar.markdown("$V_{max,uls1}$ [kN]")
V_max_sls1 = st.sidebar.number_input("V_max,uls1", min_value=-1.0e9, value=float(V_vaike_sls1), step=1.0, label_visibility="collapsed")

st.sidebar.markdown("$R_{max,uls1}$ [kN]")
R_max_sls1 = st.sidebar.number_input("R_max,uls1", min_value=-1.0e9, value=float(R_vaike_sls1), step=1.0, label_visibility="collapsed")

st.sidebar.markdown("---")

# SLS 2 sisendid
st.sidebar.subheader("ULS 2")

st.sidebar.markdown("$M_{max,uls2}$ [kNm]")
M_max_sls2 = st.sidebar.number_input("M_max,uls2", min_value=-1.0e9, value=float(M_vaike_sls2), step=1.0, label_visibility="collapsed")

st.sidebar.markdown("$V_{max,uls2}$ [kN]")
V_max_sls2 = st.sidebar.number_input("V_max,uls2", min_value=-1.0e9, value=float(V_vaike_sls2), step=1.0, label_visibility="collapsed")

st.sidebar.markdown("$R_{max,uls2}$ [kN]")
R_max_sls2 = st.sidebar.number_input("R_max,uls2", min_value=-1.0e9, value=float(R_vaike_sls2), step=1.0, label_visibility="collapsed")





# --- PEALEHT: EXCELI STIILIS MARKDOWN TABELID ---
st.header("2. Lähteandmed")
st.subheader("Hoone geomeetria")
geomeetria_markdown = f"""

| Tähis | Parameeter | Väärtus | Ühik |
| :--- | :--- | :--- | :--- |
| $L$ | Hoone pikkus | {L:.2f} | m |
| $B$ | Hoone laius | {B:.2f} | m |
| $b$ | Raamide vahe | {b:.2f} | m |
| $H$ | Posti arvutuskõrgus | {H:.2f} | m |
| | Roovide koguarv | {r_tk} | tk |
| | Raamide arv hoones | {raamide_arv} | tk |
| | Roovide horisontaalne samm | {roovide_samm:.3f} | m |
"""
st.markdown(geomeetria_markdown)

st.subheader("Koormused")
koormused_markdown = f"""

| Tähis | Koormuse nimetus | kg/m² | kN/m² | kN/m | kN |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $s_k$ | Lume normkoormus maapinnal | {s_k_kg:.2f} | {s_k:.3f} | | |
| $q_s$ | Lume normkoormus katusel | {q_s_kg:.2f} | {q_s:.3f} | | {F_q_s:.3f} |
| $w_{{e,H}}$ | Katuse välispinnale mõjuv tuulerõhk | {w_e_H_kg:.2f} | {w_e_H:.3f} | | {F_w_e_H:.3f} |
| | Profiilpleki omakaal | {g_plekk_kg:.2f} | {g_plekk_kn:.3f} | | {F_g_plekk:.3f} |
| | Katuseroovide omakaal | {g_roov_kg:.2f} | {g_roov_kn:.3f} | | {F_g_roov:.3f} |
| | Tala omakaal | | | {g_tala_kn_m:.3f} | |
| | Fassaadi omakaal | {g_fassaad_kg:.2f} | {g_fassaad_kn:.3f} | | |
"""
st.markdown(koormused_markdown)

st.subheader("Varu- ja kujutegurid")
tegurid_markdown = f"""

| Tähis | Teguri nimetus | Väärtus |
| :--- | :--- | :--- |
| $\mu$ | Lume koormuse kujutegur | {mu:.1f} |
| $\gamma_{{M0}}$ | Teraskonstruktsiooni osavarutegur (ristlõike kandevõime) | {gamma_M0:.2f} |
| $\gamma_{{M1}}$ | Teraskonstruktsiooni osavarutegur (stabiilsus) | {gamma_M1:.2f} |
| $\gamma_{{M2}}$ | Teraskonstruktsiooni osavarutegur (netoristlõike purunemine) | {gamma_M2:.2f} |
"""
st.markdown(tegurid_markdown)

st.subheader("Terase omadused")
terase_markdown = f"""

| Tähis | Parameeter | Väärtus | Ühik |
| :--- | :--- | :--- | :--- |
| | Terase klass | {teras_klass} | |
| $f_y$ | Normatiivne voolavuspiir | {f_y:.0f} | N/mm² |
| $f_u$ | Tõmbetugevus | {f_u:.0f} | N/mm² |
| $\epsilon$ | Materjali tugevus tegur | {epsilon:.2f} | |
| $E$ | Elastsusmoodul | {E:.1f} | N/mm² |
| $\eta$ | Lõikepindala tegur | {eta:.1f} | |
| $f_{{yd}}$ | Arvutuslik voolavuspiir | {f_yd:.0f} | N/mm² |
"""
st.markdown(terase_markdown)

st.subheader("Valitud profiili geomeetria")
profiil_markdown = f"""

| Tähis | Parameeter | Väärtus | Ühik |
| :--- | :--- | :--- | :--- |
| | Valitud profiil | **{valitud_profiil}** | |
| $G$ | Kaal meetri kohta | {prof_parand["G"]:.1f} | kg/m |
| $A$ | Ristlõikepindala | {prof_parand["A"]:.1f} | cm² |
| $h$ | Kõrgus | {prof_parand["h"]:.0f} | mm |
| $b$ | Laius | {prof_parand["b"]:.0f} | mm |
| $t_w$ | Seina paksus | {prof_parand["tw"]:.1f} | mm |
| $t_f$ | Vöö paksus | {prof_parand["tf"]:.1f} | mm |
| $r$ | Ümarusraadius | {prof_parand["r"]:.1f} | mm |
| $I_y$ | Inertsimoment tugeva telje suhtes | {prof_parand["Iy"]:.1f} | cm⁴ |
| $W_{{el,y}}$ | Elastne vastupanumoment tugeva telje suhtes | {prof_parand["Wel_y"]:.1f} | cm³ |
| $W_{{pl,y}}$ | Plastne vastupanumoment tugeva telje suhtes | {prof_parand["Wpl_y"]:.1f} | cm³ |
| $i_y$ | Inertsiiraadius tugeva telje suhtes | {prof_parand["iy"]:.1f} | cm |
| $I_z$ | Inertsimoment nõrga telje suhtes | {prof_parand["Iz"]:.1f} | cm⁴ |
| $W_{{el,z}}$ | Elastne vastupanumoment nõrga telje suhtes | {prof_parand["Wel_z"]:.1f} | cm³ |
| $W_{{pl,z}}$ | Plastne vastupanumoment nõrga telje suhtesme  | {prof_parand["Wpl_z"]:.1f} | cm³ |
| $i_z$ | Inertsiiraadius nõrga telje suhtes | {prof_parand["iz"]:.1f} | cm |
| $I_t$ | Väände inertsimoment | {prof_parand["It"]:.3f} | cm⁴ |
| $I_w$ | Sektoriaalne inertsimoment | {prof_parand["Iw"]:.3f} | cm⁶ x10³ |
"""
st.markdown(profiil_markdown)

# --- ARVUTUSKOORMUSTE PEATÜKK (KOLM VEERGU) ---
st.header("3. Arvutuskoormused ja arvutusmudel")

# Luuakse 3 võrdset veergu Exceli-stiilis tabelite jaoks
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### ULS 1: 1,2 OK + 1,5 Lumi")
    # Lumi on määratud nulliks (0), omakaalud korrutatakse 1.2-ga, tuul on 0
    uls1_markdown = f"""

| Koormuse nimetus | Lauskoormus [kN/m] | Punktkoormus [kN] |
| :--- | :---: | :---: |
| Tala omakaal | {1.2 * g_tala_kn_m:.3f} | — |
| Profiilpleki omakaal | — | {1.2 * F_g_plekk:.3f} |
| Katuseroovide omakaal | — | {1.2 * F_g_roov:.3f} |
| Lume koormus katusel | — | {1.5 * F_q_s:.3f} |
| Katuse tuulerõhk | — | {0.000:.3f} |
"""
    st.markdown(uls1_markdown)

with col2:
    st.markdown("##### ULS 2: 1,0 OK + 1,5 Tuul")
    # Omakaalud korrutatakse 1.0-ga, tuul korrutatakse 1.5-ga, lumi on 0
    sls2_markdown = f"""

| Koormuse nimetus | Lauskoormus [kN/m] | Punktkoormus [kN] |
| :--- | :---: | :---: |
| Tala omakaal | {1.0 * g_tala_kn_m:.3f} | — |
| Profiilpleki omakaal | — | {1.0 * F_g_plekk:.3f} |
| Katuseroovide omakaal | — | {1.0 * F_g_roov:.3f} |
| Lume koormus katusel | — | {0.000:.3f} |
| Katuse tuulerõhk | — | {1.5 * F_w_e_H:.3f} |
"""
    st.markdown(sls2_markdown)

with col3:
    st.markdown("##### SLS 1: 1,0 OK + 0,2 Lumi")
    # Omakaalud korrutatakse 1.0-ga, lumi korrutatakse 0.2-ga, tuul on 0
    sls1_markdown = f"""

| Koormuse nimetus | Lauskoormus [kN/m] | Punktkoormus [kN] |
| :--- | :---: | :---: |
| Tala omakaal | {1.0 * g_tala_kn_m:.3f} | — |
| Profiilpleki omakaal | — | {1.0 * F_g_plekk:.3f} |
| Katuseroovide omakaal | — | {1.0 * F_g_roov:.3f} |
| Lume koormus katusel | — | {0.2 * F_q_s:.3f} |
| Katuse tuulerõhk | — | {0.000:.3f} |
"""
    st.markdown(sls1_markdown)

st.markdown("---")


# --- 5. RISTLÕIKEKLASSI MÄÄRAMINE ---
st.header("4. Ristlõikeklassi määramine")
h = prof_parand["h"]
b_prof = prof_parand["b"]
tw = prof_parand["tw"]
tf = prof_parand["tf"]
r_val = prof_parand.get("r", 12.0)

# 1. VÖÖ (Surutud element)
c_voo = (b_prof - tw - 2 * r_val) / 2
suhe_voo = c_voo / tf

if suhe_voo <= 9 * epsilon:
    klass_voo = 1
    vordlus_voo = f"≤ 9·ε = {9 * epsilon:.2f}"
elif suhe_voo <= 10 * epsilon:
    klass_voo = 2
    vordlus_voo = f"≤ 10·ε = {10 * epsilon:.2f}"
elif suhe_voo <= 14 * epsilon:
    klass_voo = 3
    vordlus_voo = f"≤ 14·ε = {14 * epsilon:.2f}"
else:
    klass_voo = 4
    vordlus_voo = f"> 14·ε = {14 * epsilon:.2f}"

# 2. SEIN (Painutatud element, siseosa sirge kõrgus c)
c_sein = h - 2 * tf - 2 * r_val
suhe_sein = c_sein / tw

if suhe_sein <= 72 * epsilon:
    klass_sein = 1
    vordlus_sein = f"≤ 72·ε = {72 * epsilon:.2f}"
elif suhe_sein <= 83 * epsilon:
    klass_sein = 2
    vordlus_sein = f"≤ 83·ε = {83 * epsilon:.2f}"
elif suhe_sein <= 124 * epsilon:
    klass_sein = 3
    vordlus_sein = f"≤ 124·ε = {124 * epsilon:.2f}"
else:
    klass_sein = 4
    vordlus_sein = f"> 124·ε = {124 * epsilon:.2f}"

kogu_klass = max(klass_voo, klass_sein)

st.write(f"Vöö: c/t = {c_voo:.1f}/{tf:.1f} = {suhe_voo:.2f} {vordlus_voo} $\\Rightarrow$ ristlõikeklass {klass_voo}")
st.write(f"Sein: c/t = {c_sein:.1f}/{tw:.1f} = {suhe_sein:.2f} {vordlus_sein} $\\Rightarrow$ ristlõikeklass {klass_sein}")
st.write(f"**Kogu profiili ristlõikeklass: {kogu_klass}**")

# --- KANDEVÕIME KONTROLLI ABIFUNKTSIOON ---
def kuva_ed_rd_kontroll(pealkiri, Ed, Rd, uhik="", Ed_symbol=r"E_D", Rd_symbol=r"R_D"):
    """Kuvab LaTeX-kujul konkreetse sisejõu ja vastava kandevõime suhte."""
    if Rd is None or not math.isfinite(float(Rd)) or Rd <= 0:
        st.error(f"{pealkiri}: kandevõimet ei saa kontrollida (R_d puudub või on ≤ 0).")
        return
    suhe_ed_rd = abs(float(Ed)) / float(Rd)
    mark = r"<" if suhe_ed_rd < 1.0 else r"\geq"
    st.latex(
        r"{\footnotesize \frac{" + Ed_symbol + r"}{" + Rd_symbol + r"} = "
        + rf"\frac{{{abs(float(Ed)):.2f}}}{{{float(Rd):.2f}}} = {suhe_ed_rd:.3f} {mark} 1"
        + r"}"
    )
    if suhe_ed_rd < 1.0:
        st.success(f"{pealkiri}: kandevõime tagatud.")
    else:
        st.error(f"{pealkiri}: kandevõime EI OLE tagatud.")

# --- 6. PAINDEVÕIME ARVUTUS ---
st.header("5. Paindekandevõime")

# Loeme vajalikud väärtused profiili andmetest ja terase omadustest
W_pl_y = prof_parand["Wpl_y"]  # cm³
W_el_y = prof_parand["Wel_y"]  # cm³

# Kontrollime ristlõikeklassi ilma 'in' operaatorita, et vältida süntaksivigu
if kogu_klass == 1 or kogu_klass == 2:
    # Klass 1 ja 2 kasutavad plastset vastupanumomenti
    M_Rd = (W_pl_y * 1000 * f_y) / gamma_M0 / 10**6  # Teisendus kNm
    valem_tekst = r"M_{c,Rd} = \frac{W_{pl,y} \cdot f_y}{\gamma_{M0}}"
    tehe_tekst = f"\\frac{{{W_pl_y:.1f} \\cdot 10^3 \\cdot {f_y:.0f}}}{{{gamma_M0:.2f}}} \\cdot 10^{{-6}} = {M_Rd:.2f} \\text{{ kNm}}"
else:
    # Klass 3 kasutab elastset vastupanumomenti
    M_Rd = (W_el_y * 1000 * f_y) / gamma_M0 / 10**6
    valem_tekst = r"M_{c,Rd} = \frac{W_{el,y} \cdot f_y}{\gamma_{M0}}"
    tehe_tekst = f"\\frac{{{W_el_y:.1f} \\cdot 10^3 \\cdot {f_y:.0f}}}{{{gamma_M0:.2f}}} \\cdot 10^{{-6}} = {M_Rd:.2f} \\text{{ kNm}}"

# Kuvame esimese reana üldise valemi
st.latex(r"{\footnotesize " + valem_tekst + r"}")

# Kuvame teise reana numbrilise tehte ja vastuse
st.latex(r"{\footnotesize M_{c,Rd} = " + tehe_tekst + r"}")



st.write("**ULS 1 kontroll (paindemoment):**")
kuva_ed_rd_kontroll("ULS 1 paindekandevõime", M_max_sls1, M_Rd, "kNm", r"M_{Ed}", r"M_{c,Rd}")
st.write("**ULS 2 kontroll (paindemoment):**")
kuva_ed_rd_kontroll("ULS 2 paindekandevõime", M_max_sls2, M_Rd, "kNm", r"M_{Ed}", r"M_{c,Rd}")

# --- 7. LÕIKEKANDEVÕIME ARVUTUS ---
st.header("6. Põikjõukandevõime")

# Loeme vajalikud parameetrid profiili andmetest ja konstantidest
A = prof_parand["A"]  # cm²
h = prof_parand["h"]  # mm
b_prof = prof_parand["b"]  # mm
tw = prof_parand["tw"]  # mm
tf = prof_parand["tf"]  # mm
r_val = prof_parand.get("r", 12.0)  # mm

# Teisendame ristlõikepindala A ruutmillimeetritesse (cm² * 100)
A_mm2 = A * 100.0

# Kõrgus vööde vahel h_w (mm)
h_w = h - 2 * tf

# Lõikepindala A_v arvutus valtsitud I- ja H-profiilidele (Seina sihis koormatud)
A_v_valem_a = A_mm2 - 2 * b_prof * tf + (tw + 2 * r_val) * tf
A_v_miinimum = eta * h_w * tw

# Määrame märgiks > või < sõltuvalt tingimusest
mark = ">" if A_v_valem_a >= A_v_miinimum else "<"
A_v = max(A_v_valem_a, A_v_miinimum)

# Plastne põikjõukandevõime V_pl,Rd (kN)
V_pl_Rd = (A_v * f_y) / (math.sqrt(3) * gamma_M0) / 1000.0

# Kuvame esimese reana valemi ja tingimuse suhte
valem_rida = r"A_v = A - 2bt_f + (t_w + 2r)t_f \geq \eta h_w t_w"
st.latex(r"{\footnotesize " + valem_rida + r"}")

# Kuvame teise reana numbrilise tehte ja võrdluse
tehe_rida = f"{A_mm2:.1f} - 2 \\cdot {b_prof} \\cdot {tf} + ({tw} + 2 \\cdot {r_val}) \\cdot {tf} = {A_v_valem_a:.1f} \\text{{ mm}}^2 {mark} {eta:.1f} \\cdot {h_w:.1f} \\cdot {tw} = {A_v_miinimum:.1f} \\text{{ mm}}^2 \\Rightarrow A_v = {A_v:.1f} \\text{{ mm}}^2"
st.latex(r"{\footnotesize " + tehe_rida + r"}")

# Kandevõime valem ja arvutus kokku
valem_Vrd = r"V_{pl,Rd} = \frac{A_v \cdot f_y}{\sqrt{3} \cdot \gamma_{M0}}"
tehe_Vrd = f"\\frac{{{A_v:.1f} \\cdot {f_y:.0f}}}{{\\sqrt{{3}} \\cdot {gamma_M0:.2f}}} \\cdot 10^{{-3}} = {V_pl_Rd:.2f} \\text{{ kN}}"
st.latex(r"{\footnotesize " + f"{valem_Vrd} = {tehe_Vrd}" + r"}")

st.write("**ULS 1 kontroll (põikjõud):**")
kuva_ed_rd_kontroll("ULS 1 plastne põikjõukandevõime", V_max_sls1, V_pl_Rd, "kN", r"V_{Ed}", r"V_{pl,Rd}")
st.write("**ULS 2 kontroll (põikjõud):**")
kuva_ed_rd_kontroll("ULS 2 plastne põikjõukandevõime", V_max_sls2, V_pl_Rd, "kN", r"V_{Ed}", r"V_{pl,Rd}")

# --- 8. TALA SEINA NIHKESTABIILSUS ---
st.header("7. Tala seina nihkestabiilsus")

# Loeme vajalikud parameetrid
h = prof_parand["h"]  # mm
tf = prof_parand["tf"]  # mm
tw = prof_parand["tw"]  # mm

# Seina kõrgus vööde vahel h_w
h_w = h - 2 * tf
suhe_nihke = h_w / tw
piir_nihke = 60 * epsilon

# Kontrollime nihkestabiilsuse vajadust
valem_nihke_kontroll = r"\frac{h_w}{t_w} \leq 60\varepsilon"
tehe_nihke_kontroll = f"\\frac{{{h_w:.1f}}}{{{tw:.1f}}} = {suhe_nihke:.2f} \\leq 60 \\cdot {epsilon:.2f} = {piir_nihke:.2f}"

st.latex(r"{\footnotesize " + valem_nihke_kontroll + " = " + tehe_nihke_kontroll + r"}")

V_bw_Rd = None
if suhe_nihke > piir_nihke:
    st.write("**Nihkestabiilsuse täiendav kontroll on vajalik.**")

    st.write("Leitakse seina tingsaledus $\\bar{\\lambda}_w$:")
    lambda_w = h_w / (86.4 * epsilon * tw)
    valem_lambda = r"\bar{\lambda}_w = \frac{h_w}{86.4 \cdot \varepsilon \cdot t_w}"
    tehe_lambda = f"\\frac{{{h_w:.1f}}}{{86.4 \\cdot {epsilon:.2f} \\cdot {tw:.1f}}} = {lambda_w:.3f}"
    st.latex(r"{\footnotesize " + valem_lambda + " = " + tehe_lambda + r"}")

    st.write("Mõlketegur $\\chi_w$ leitakse tingimuste hulgast:")
    valem_chi_tingimus = r"\chi_w = \begin{cases} 1,2 & \bar{\lambda}_w < 0,69 \\ 0,83/\bar{\lambda}_w & 0,69 \leq \bar{\lambda}_w < 1,08 \\ 1,37/(0,7 + \bar{\lambda}_w) & \bar{\lambda}_w \geq 1,08 \text{ ja jäik toeribi} \\ 0,83/\bar{\lambda}_w & \bar{\lambda}_w \geq 1,08 \text{ ja painduv toeribi} \end{cases}"
    st.latex(r"{\footnotesize " + valem_chi_tingimus + r"}")

    # Määratakse, milline valem valiti ja arvutatakse chi_w
    if lambda_w < 0.69:
        chi_w = 1.2
        valem_chi = r"\chi_w = 1.2"
        tehe_chi = "1.2"
    elif 0.69 <= lambda_w < 1.08:
        chi_w = 0.83 / lambda_w
        valem_chi = r"\chi_w = \frac{0.83}{\bar{\lambda}_w}"
        tehe_chi = f"\\frac{{0.83}}{{{lambda_w:.3f}}} = {chi_w:.3f}"
    else:
        chi_w = 0.83 / lambda_w
        valem_chi = r"\chi_w = \frac{0.83}{\bar{\lambda}_w} \text{ (painduv toeribi)}"
        tehe_chi = f"\\frac{{0.83}}{{{lambda_w:.3f}}} = {chi_w:.3f}"
        
    st.write(f"Kuna $\\bar{{\\lambda}}_w = {lambda_w:.3f}$, siis valiti ja arvutati väärtus:")
    st.latex(r"{\footnotesize " + valem_chi + " = " + tehe_chi + r"}")

    st.write("Arvutatakse seina nihkestabiilsusel põhinev lõikekandevõime $V_{bw,Rd}$:")
    V_bw_Rd = (chi_w * f_y * h_w * tw) / (math.sqrt(3) * gamma_M1) / 1000.0
    valem_Vbw = r"V_{bw,Rd} = \frac{\chi_w \cdot f_{yw} \cdot h_w \cdot t_w}{\sqrt{3} \cdot \gamma_{M1}}"
    tehe_Vbw = f"\\frac{{{chi_w:.3f} \\cdot {f_y:.0f} \\cdot {h_w:.1f} \\cdot {tw:.1f}}}{{\\sqrt{{3}} \\cdot {gamma_M1:.2f}}} \\cdot 10^{{-3}} = {V_bw_Rd:.2f} \\text{{ kN}}"
    st.latex(r"{\footnotesize " + valem_Vbw + " = " + tehe_Vbw + r"}")

else:
    st.write(f"Pole vaja kontrollida")

# ULS-kontrollid kuvatakse ainult siis, kui seina nihkestabiilsuse
# täiendav arvutus on geomeetrilise tingimuse järgi vajalik.
if V_bw_Rd is not None:
    st.write("**ULS 1 kontroll (seina nihkestabiilsus):**")
    kuva_ed_rd_kontroll("ULS 1 seina nihkestabiilsus", V_max_sls1, V_bw_Rd, "kN", r"V_{Ed}", r"V_{bw,Rd}")
    st.write("**ULS 2 kontroll (seina nihkestabiilsus):**")
    kuva_ed_rd_kontroll("ULS 2 seina nihkestabiilsus", V_max_sls2, V_bw_Rd, "kN", r"V_{Ed}", r"V_{bw,Rd}")

# --- 9. KOHALIK MÕLKUMINE ---
st.header("8. Kandevõime koondatud põikkoormuse suhtes")

# Loeme vajalikud parameetrid profiilist ja materjalist
h = prof_parand["h"]  # mm
bf = prof_parand["b"]  # mm
tw = prof_parand["tw"]  # mm
tf = prof_parand["tf"]  # mm
r_val = prof_parand.get("r", 12.0)  # mm

h_w = h - 2 * tf  # mm

# Jäiga toetuspinna pikkus s_s on ette antud konstant
s_s = 20.0

st.write("Rroovi toetuspikkus talale on antud lähteandmetes:")
st.latex(r"{\footnotesize s_s = 20.0 \text{ mm}}")

st.write("Koormuse mõjumisviisist sõltuv tegur $k_F$ valitakse tingimuste hulgast:")
valem_kf_tingimus = r"k_F = \begin{cases} 6 + 2 (h_w/a)^2, & \text{juhtum a} \\ 3,5 + 2 (h_w/a)^2, & \text{juhtum (b)} \\ 2 + 6 \frac{s_s + c}{h_w} \leq 6, & \text{juhtum (c)} \end{cases}"
st.latex(r"{\footnotesize " + valem_kf_tingimus + r"}")

st.write("Kuna talal on ainult toeribid otsas (juhtum (a) ja põikiribide vahekaugust $a$ pole), võetakse konstandiks:")
k_F = 6.0
st.latex(r"{\footnotesize k_F = 6.0}")

st.write("Arvutatakse abitegur $m_1$:")
m1 = bf / tw
valem_m1 = r"m_1 = \frac{b_f}{t_w}"
tehe_m1 = f"\\frac{{{bf:.1f}}}{{{tw:.1f}}} = {m1:.2f}"
st.latex(r"{\footnotesize " + valem_m1 + " = " + tehe_m1 + r"}")

st.write("Tegur $m_2$ sõltub tingsaledusest $\\bar{\\lambda}_F$ järgmiselt:")
valem_m2_tingimus = r"m_2 = \begin{cases} 0,02 \left(\frac{h_w}{t_f}\right)^2, & \bar{\lambda}_F > 0,5 \\ 0, & \bar{\lambda}_F \leq 0,5 \end{cases}"
st.latex(r"{\footnotesize " + valem_m2_tingimus + r"}")

st.write("Arvutatakse kriitiline jõud $F_{cr}$:")
F_cr = 0.9 * k_F * E * (tw**3) / h_w
valem_Fcr = r"F_{cr} = 0.9 \cdot k_F \cdot E \cdot \frac{t_w^3}{h_w}"
tehe_Fcr = f"0.9 \\cdot {k_F:.1f} \\cdot {E:.0f} \\cdot \\frac{{{tw:.1f}^3}}{{{h_w:.1f}}} = {F_cr:.1f} \\text{{ N}}"
st.latex(r"{\footnotesize " + valem_Fcr + " = " + tehe_Fcr + r"}")

st.write("Tehakse esmane tingsaledusarvutus eeldusel, et $m_2 = 0$:")
ly_esialgne = s_s + 2 * tf * (1 + math.sqrt(m1 + 0))
lambda_F_esialgne = math.sqrt((ly_esialgne * tw * f_y) / F_cr)

if lambda_F_esialgne > 0.5:
    m2 = 0.02 * (h_w / tf) ** 2
    valem_m2 = r"m_2 = 0.02 \left(\frac{h_w}{t_f}\right)^2"
    tehe_m2 = f"0.02 \\cdot \\left(\\frac{{{h_w:.1f}}}{{{tf:.1f}}}\\right)^2 = {m2:.2f}"
else:
    m2 = 0.0
    valem_m2 = r"m_2 = 0"
    tehe_m2 = "0"

st.write(f"Kuna esialgne $\\bar{{\\lambda}}_F = {lambda_F_esialgne:.3f}$, siis arvutatakse lõplik $m_2$:")
st.latex(r"{\footnotesize " + valem_m2 + " = " + tehe_m2 + r"}")

st.write("Arvutatakse efektiivne koormamispikkus $l_y$:")
l_y = s_s + 2 * tf * (1 + math.sqrt(m1 + m2))
valem_ly = r"l_y = s_s + 2t_f (1 + \sqrt{m_1 + m_2})"
tehe_ly = f"{s_s:.1f} + 2 \\cdot {tf:.1f} \\cdot (1 + \\sqrt{{{m1:.2f} + {m2:.2f}}}) = {l_y:.1f} \\text{{ mm}}"
st.latex(r"{\footnotesize " + valem_ly + " = " + tehe_ly + r"}")

st.write("Leitakse kohalikule mõlkumisele vastav tingsaledus $\\bar{\\lambda}_F$:")
lambda_F = math.sqrt((l_y * tw * f_y) / F_cr)
valem_lambdaF = r"\bar{\lambda}_F = \sqrt{\frac{l_y \cdot t_w \cdot f_{yw}}{F_{cr}}}"
tehe_lambdaF = f"\\sqrt{{\\frac{{{l_y:.1f} \\cdot {tw:.1f} \\cdot {f_y:.0f}}}{{{F_cr:.1f}}}}} = {lambda_F:.3f}"
st.latex(r"{\footnotesize " + valem_lambdaF + " = " + tehe_lambdaF + r"}")

st.write("Leitakse vähendustegur $\\chi_F$:")
chi_F = min(0.5 / lambda_F, 1.0) if lambda_F > 0 else 1.0
valem_chiF = r"\chi_F = \frac{0.5}{\bar{\lambda}_F} \leq 1.0"
tehe_chiF = f"\\frac{{0.5}}{{{lambda_F:.3f}}} = {chi_F:.3f}"
st.latex(r"{\footnotesize " + valem_chiF + " = " + tehe_chiF + r"}")

st.write("Arvutatakse efektiivne koormamispikkus $L_{eff}$:")
L_eff = chi_F * l_y
valem_Leff = r"L_{eff} = \chi_F \cdot l_y"
tehe_Leff = f"{chi_F:.3f} \\cdot {l_y:.1f} = {L_eff:.1f} \\text{{ mm}}"
st.latex(r"{\footnotesize " + valem_Leff + " = " + tehe_Leff + r"}")

st.write("Arvutatakse seina arvutuslik kandevõime kohaliku mõlkumise suhtes $F_{Rd}$:")
F_Rd = (f_y * L_eff * tw) / gamma_M1 / 1000.0
valem_FRd = r"F_{Rd} = \frac{f_{yw} \cdot L_{eff} \cdot t_w}{\gamma_{M1}}"
tehe_FRd = f"\\frac{{{f_y:.0f} \\cdot {L_eff:.1f} \\cdot {tw:.1f}}}{{{gamma_M1:.2f}}} \\cdot 10^{{-3}} = {F_Rd:.2f} \\text{{ kN}}"
st.latex(r"{\footnotesize " + valem_FRd + " = " + tehe_FRd + r"}")

st.write("**ULS 1 kontroll (kohalik mõlkumine):**")
kuva_ed_rd_kontroll("ULS 1 kohaliku mõlkumise kandevõime", R_max_sls1, F_Rd, "kN", r"R_{Ed}", r"F_{Rd}")
st.write("**ULS 2 kontroll (kohalik mõlkumine):**")
kuva_ed_rd_kontroll("ULS 2 kohaliku mõlkumise kandevõime", R_max_sls2, F_Rd, "kN", r"R_{Ed}", r"F_{Rd}")

# --- 10. JÄIKUSRIBIDE DIMENSIOONEERIMINE ---
st.header("9. Toeribide dimensioneerimine")

R_Ed = max(abs(R_max_sls1), abs(R_max_sls2))  # suurim sisestatud toereaktsioon, kN
vaba_ruum_toe_pool = 125.0  # mm (vaba ruumi mõõt e)
V_Ed = max(abs(V_max_sls1), abs(V_max_sls2))

# Loeme vajalikud parameetrid olemasolevast profiilist
h = prof_parand["h"]
b = prof_parand["b"]
tf = prof_parand["tf"]
tw = prof_parand["tw"]
h_w = h - 2 * tf  # mm

st.write("Määratakse toeribi efektiivpindala hulka kuuluv seinaosa laius kummalgi pool ribi:")

b_eff = 15 * epsilon * tw
st.latex(r"{\footnotesize b_{eff} = 15 \cdot \varepsilon \cdot t_w = 15 \cdot " + f"{epsilon:.2f} \\cdot {tw:.1f} = {b_eff:.1f}" + r" \text{ mm}}")

st.write("Otsapoolse osa arvutuspikkus")

# Määratakse vasak ja parem efektiivne laius
b_eff_p = b_eff
if b_eff > vaba_ruum_toe_pool:
    b_eff_v = vaba_ruum_toe_pool
else:
    b_eff_v = b_eff

st.latex(r"{\footnotesize b_{eff,v} = \min(125; b_{eff}) = " + f"{b_eff_v:.1f}" + r" \text{ mm}}")

# Arvutatakse maksimaalne ribi laius b_s, et see ei ulatuks vööst välja
b_s_max = (b - tw) / 2.0

# Toeribi plaadi mõõtmete sisestamine (b_s vaikeväärtus ja maksimum on b_s_max ning t_s vaikeväärtus on seina paksus tw)
col_ribi1, col_ribi2 = st.columns(2)
with col_ribi1:
    b_s = st.number_input("Toeribi plaadi laius $b_s$ (ühel pool seina) [mm]:", value=float(b_s_max), max_value=float(b_s_max), step=5.0, key=f"b_s_input_{b}_{tw}")
with col_ribi2:
    t_s = st.number_input("Toeribi plaadi paksus $t_s$ [mm]:", value=float(tw), step=1.0, key=f"t_s_input_{b}_{tw}")

st.write("Kahepoolse ribi efektiivpindalaks kujuneb:")

# Kogu koondatud efektiivpindala arvutus As
A_s = (2 * b_s + tw) * t_s + (b_eff_v + b_eff_p) * tw

valem_as = r"A_s = (2 \cdot b_s + t_w) \cdot t_s + (b_{eff,v} + b_{eff,p}) \cdot t_w"
tehe_as = f"(2 \\cdot {b_s:.1f} + {tw:.1f}) \\cdot {t_s:.1f} + ({b_eff_v:.1f} + {b_eff_p:.1f}) \\cdot {tw:.1f} = {A_s:.1f} \\text{{ mm}}^2"
st.latex(r"{\footnotesize " + valem_as + " = " + tehe_as + r"}")

# --- KONSTRUKTIIVSED KONTROLLID JA NÕUDED ---
st.write("Toeribi konstruktiivsete nõuete kontroll:")

# 1. Ristlõikepindala vähemalt 4 * h_w * t_w^2 / e
A_s_plates = 2 * b_s * t_s
A_s_min_konstruktiivne = 4 * (h_w * (tw**2)) / vaba_ruum_toe_pool
mark_pindala = r"\ge" if A_s_plates >= A_s_min_konstruktiivne else r"<"

st.write("Ribaterastest koosneva kahepoolse põikribi plaatide pindala nõue:")
valem_amin = r"2 \cdot b_s \cdot t_s \ge 4 \frac{h_w \cdot t_w^2}{e}"
tehe_amin = f"2 \\cdot {b_s:.1f} \\cdot {t_s:.1f} = {A_s_plates:.1f} \\text{{ mm}}^2 \\rightarrow 4 \\cdot \\frac{{{h_w:.1f} \\cdot {tw:.1f}^2}}{{{vaba_ruum_toe_pool:.1f}}} = {A_s_plates:.1f} \\text{{ mm}}^2 {mark_pindala} {A_s_min_konstruktiivne:.1f} \\text{{ mm}}^2"
st.latex(r"{\footnotesize " + valem_amin + r" \rightarrow " + tehe_amin + r"}")

if A_s_plates < A_s_min_konstruktiivne:
    st.error("Plaatide pindala nõue ei ole täidetud! Toeribi vajab suuremaid mõõtmeid.")

# --- INERTSIMOMENT JA SELLE KONSTRUKTIIVNE KONTROLL ---
I_st = (t_s * (2 * b_s + tw)**3) / 12
st.write("Ristlõike inertsimoment seina telje suhtes $I_{st}$:")
st.latex(r"{\footnotesize I_{st} = \frac{t_s \cdot (2 \cdot b_s + t_w)^3}{12} = \frac{" + f"{t_s:.1f} \\cdot (2 \\cdot {b_s:.1f} + {tw:.1f})^3" + r"}{12} = " + f"{I_st:.1f}" + r" \text{ mm}^4}")

# Inertsimomendi konstruktiivne miinimumnõue seina ristisuunas
I_st_min_konstruktiivne = 4 * h_w * (tw**2)
mark_ist = r"\ge" if I_st >= I_st_min_konstruktiivne else r"<"

st.write("Toeribi efektiivristlõike inertsimomendi konstruktiivne nõue:")
valem_imin = r"I_{st} \ge 4 \cdot h_w \cdot t_w^2"
tehe_imin = f"{I_st:.1f} \\text{{ mm}}^4 \\rightarrow 4 \\cdot {h_w:.1f} \\cdot {tw:.1f}^2 = {I_st:.1f} \\text{{ mm}}^4 {mark_ist} {I_st_min_konstruktiivne:.1f} \\text{{ mm}}^4"
st.latex(r"{\footnotesize " + valem_imin + r" \rightarrow " + tehe_imin + r"}")

if I_st < I_st_min_konstruktiivne:
    st.error("Inertsimomendi konstruktiivne nõue ei ole täidetud! Suurenda ribi mõõtmeid.")


# --- INERTSIMOMENT ---
I_st = (t_s * (2 * b_s + tw)**3) / 12
st.write("Ristlõike inertsimoment seina telje suhtes $I_{st}$:")
st.latex(r"{\footnotesize I_{st} = \frac{t_s \cdot (2 \cdot b_s + t_w)^3}{12} = \frac{" + f"{t_s:.1f} \\cdot (2 \\cdot {b_s:.1f} + {tw:.1f})^3" + r"}{12} = " + f"{I_st:.1f}" + r" \text{ mm}^4}")

# Inertsimomendi konstruktiivne miinimumnõue seina ristisuunas
I_st_min_konstruktiivne = 4 * h_w * (tw**2)
mark_ist = r"\ge" if I_st >= I_st_min_konstruktiivne else r"<"

st.write("Toeribi efektiivristlõike inertsimomendi konstruktiivne nõue:")
valem_imin = r"I_{st} \ge 4 \cdot h_w \cdot t_w^2"
tehe_imin = f"{I_st:.1f} \\text{{ mm}}^4 \\rightarrow 4 \\cdot {h_w:.1f} \\cdot {tw:.1f}^2 = {I_st_min_konstruktiivne:.1f} \\text{{ mm}}^4 {mark_ist} {I_st_min_konstruktiivne:.1f} \\text{{ mm}}^4"
st.latex(r"{\footnotesize " + valem_imin + r" \rightarrow " + tehe_imin + r"}")

if I_st < I_st_min_konstruktiivne:
    st.error("Inertsimomendi konstruktiivne nõue ei ole täidetud! Suurenda ribi mõõtmeid.")

# Inertsi-raadiuse arvutus i
i_s = math.sqrt(I_st / A_s)
st.write("Ristlõike inertsi-raadius $i$:")
st.latex(r"{\footnotesize i = \sqrt{\frac{I_{st}}{A_s}} = \sqrt{\frac{" + f"{I_st:.1f}" + r"}{" + f"{A_s:.1f}" + r"}} = " + f"{i_s:.1f}" + r" \text{ mm}}")

# Jäikusribi arvutusliku survejõu N_s,Ed taustaarvutus (ilma tekstita ekraanile kuvamata)
if 'lambda_w' in locals() and lambda_w > 0:
    vahendusosa = (1.0 / (lambda_w**2)) * (f_y * h_w * tw) / (math.sqrt(3) * gamma_M1) / 1000.0
    N_s_Ed = V_Ed - vahendusosa
    if N_s_Ed < 0:
        N_s_Ed = 0.0
else:
    N_s_Ed = V_Ed

# Ribi kinnitusviisi valik vööde külge
kinnitusviis = st.selectbox(
    "Toeribi kinnitusviis vööde külge:",
    options=["mõlemast otsast vööde külge keevitatud", "kinnitatud vaid ühest otsast"],
    index=0
)

if kinnitusviis == "mõlemast otsast vööde külge keevitatud":
    st.write("Kuna ribi on mõlemast otsast vööde külge keevitatud, võetakse stabiilsusarvutustes nõtkepikkuseks:")
    le_ribi = 0.75 * h_w
    st.latex(r"{\footnotesize l_e = 0,75 \cdot h_w = 0,75 \cdot " + f"{h_w:.1f} = {le_ribi:.1f} \\text{{ mm}}" + r"}")
else:
    st.write("Kuna ribi on kinnitatud vaid ühest otsast, võetakse stabiilsusarvutustes nõtkepikkuseks:")
    le_ribi = h_w
    st.latex(r"{\footnotesize l_e = h_w = " + f"{h_w:.1f} \\text{{ mm}}" + r"}")

lambda_bar_s = (le_ribi / (math.pi * i_s)) * math.sqrt(f_y / E)

st.write("Toeribi tinglik saledus $\\bar{\\lambda}_s$:")
st.latex(r"{\footnotesize \bar{\lambda}_s = \frac{l_e}{\pi \cdot i_s} \cdot \sqrt{\frac{f_y}{E}} = \frac{" + f"{le_ribi:.1f}" + r"}{\pi \cdot " + f"{i_s:.1f}" + r"} \cdot \sqrt{\frac{" + f"{f_y:.0f}" + r"}{" + f"{E:.0f}" + r"}} = " + f"{lambda_bar_s:.3f}" + r"}")

st.write("Abimuutuja $\\Phi_s$ arvutus nõtkekõvera $c$ järgi:")
alpha = 0.49
st.write(f"$\\alpha = {alpha}$")
phi_s = 0.5 * (1.0 + alpha * (lambda_bar_s - 0.2) + lambda_bar_s**2)
st.latex(r"{\footnotesize \Phi_s = 0,5 \cdot [1 + 0,49 \cdot (\bar{\lambda}_s - 0,2) + \bar{\lambda}_s^2] = 0,5 \cdot [1 + 0,49 \cdot (" + f"{lambda_bar_s:.3f}" + r" - 0,2) + " + f"{lambda_bar_s:.3f}" + r"^2] = " + f"{phi_s:.3f}" + r"}")

chi = min(1.0, 1.0 / (phi_s + math.sqrt(phi_s**2 - lambda_bar_s**2)))
st.write("Toeribi nõtkekoefitsient $\\chi$:")
st.latex(r"{\footnotesize \chi = \frac{1}{\Phi_s + \sqrt{\Phi_s^2 - \bar{\lambda}_s^2}} = \frac{1}{" + f"{phi_s:.3f}" + r" + \sqrt{" + f"{phi_s:.3f}" + r"^2 - " + f"{lambda_bar_s:.3f}" + r"^2}} = " + f"{chi:.3f}" + r"}")

N_b_Rd = (chi * A_s * f_y) / gamma_M1 / 1000.0
st.write("Toeribi nõtkekandevõime $N_{b,Rd}$:")
st.latex(r"{\footnotesize N_{b,Rd} = \frac{\chi \cdot A_s \cdot f_y}{\gamma_{M1}} = \frac{" + f"{chi:.3f} \\cdot {A_s:.1f} \\cdot {f_y:.0f}" + r"}{" + f"{gamma_M1:.2f}" + r"} \cdot 10^{-3} = " + f"{N_b_Rd:.2f}" + r" \text{ kN}}")

# Toeribi stabiilsuse kontroll mõlema koormusjuhtumi jaoks eraldi.
st.write("Toeribi stabiilsuse kontroll:")

if 'lambda_w' in locals() and lambda_w > 0:
    vahendusosa = (1.0 / (lambda_w**2)) * (f_y * h_w * tw) / (math.sqrt(3) * gamma_M1) / 1000.0
else:
    vahendusosa = 0.0

def arvuta_ribi_survejoud(R_Ed_case):
    return max(0.0, abs(float(R_Ed_case)) - vahendusosa)

N_s_Ed_sls1 = arvuta_ribi_survejoud(R_max_sls1)
N_s_Ed_sls2 = arvuta_ribi_survejoud(R_max_sls2)
N_s_Ed = max(N_s_Ed_sls1, N_s_Ed_sls2)

st.write("**ULS 1 kontroll (jäikusribi):**")
kuva_ed_rd_kontroll("ULS 1 jäikusribi stabiilsus", N_s_Ed_sls1, N_b_Rd, "kN", r"N_{s,Ed}", r"N_{b,Rd}")
st.write("**ULS 2 kontroll (jäikusribi):**")
kuva_ed_rd_kontroll("ULS 2 jäikusribi stabiilsus", N_s_Ed_sls2, N_b_Rd, "kN", r"N_{s,Ed}", r"N_{b,Rd}")














# ==============================================================================
# --- 11. KIIVEKANDEVÕIME JA KRIITILINE PAINDEMOMENT ---
# ==============================================================================
st.header("10. Kiivekandevõime")

# Profiili andmete lugemine ja teisendamine mm ühikutesse ühiseks kasutamiseks
I_z = prof_parand["Iz"]    # cm⁴
I_t = prof_parand["It"]    # cm⁴
I_w = prof_parand["Iw"]    # cm⁶ x10³
h = prof_parand["h"]        # mm

I_z_mm4 = I_z * 1e4
I_t_mm4 = I_t * 1e4
I_w_mm6 = I_w * 1e9

if M_max_sls1 > 0 or M_max_sls2 < 0:
    st.write("Kriitilise paindemomendi arvutusvalem ja muutujate selgitused:")
    valem_mcr = r"M_{cr} = C_1 \frac{\pi^2 E I_z}{L^2} \left[ \sqrt{\frac{I_w}{I_z} + \frac{L^2}{2,6\pi^2} \cdot \frac{I_t}{I_z} + (C_2 z_g)^2} - (C_2 z_g) \right]"
    st.latex(r"{\footnotesize " + valem_mcr + r"}")
    
    st.markdown("""
    * $M_{cr}$ – elastsusteooria kohane kriitiline paindemoment kiivel
    * $z_g$ – koormuse rakenduspunkti kaugus varda teljest
    * $I_w$ – sektoriaalinertsimoment
    * $I_t$ – vabaväände inertsimoment
    * $I_z$ – inertsimoment $z$-telje suhtes
    """)

    st.write("Määratakse ristlõike suhte põhjal kiivekõver ja hälbetegur:")
    col_tab1, col_tab2 = st.columns(2)
    with col_tab1:
        st.markdown("**Tabel 4.2.2. Kiivekõverad**")
        st.markdown("| Piirid | Kiivekõver |\n| :--- | :---: |\n| $h/b \\le 2$ | **b** |\n| $h/b > 2$ | **c** |")
    with col_tab2:
        st.markdown("**Tabel 4.2.1. Hälbetegurid**")
        st.markdown("| Kiivekõver | a | b | c | d |\n| :--- | :---: | :---: | :---: | :---: |\n| $\\alpha_{LT}$ | 0.21 | 0.34 | 0.49 | 0.76 |")

    suhe_hb = h / b_prof
    if suhe_hb <= 2.0:
        kiivekover = "b"
        alpha_LT = 0.34
        mark_suhe = r"\leq 2"
    else:
        kiivekover = "c"
        alpha_LT = 0.49
        mark_suhe = r"> 2"
        
    st.write("Ristlõike kõrguse ja laiuse suhe:")
    st.latex(r"{\footnotesize \frac{h}{b} = \frac{" + f"{h:.1f}" + r"}{" + f"{b_prof:.1f}" + r"} = " + f"{suhe_hb:.2f} {mark_suhe}" + r"}")
    st.write(f"Vastavalt tabelile 4.2.2 on kiivekõveraks {kiivekover} ja hälbeteguriks:")
    st.latex(r"{\footnotesize \alpha_{LT} = " + f"{alpha_LT}" + r"}")

    # --- ALAMPEATÜKK: SLS 1 ---
    st.subheader("ULS 1")
    if M_max_sls1 > 0:
        # SLS 1 puhul surutakse kokku ülemine vöö, põiksuunaliseks toetussammuks on katuseroovide samm L_cr_m_sls1 = roovide_samm
        L_cr_m_sls1 = roovide_samm
        L_cr_mm_sls1 = L_cr_m_sls1 * 1000.0
        
        st.write("Lumekoormuse all surutakse kokku tala ülemine vöö, mida toetavad põikisuunas katuseroovid:")
        st.write("Põiksuunas toetatud roovide kaugus:")
        st.latex(r"{\footnotesize L = " + f"{L_cr_m_sls1:.3f} \\text{{ m}} = {L_cr_mm_sls1:.1f} \\text{{ mm}}" + r"}")
        
        # M_min ja M_max sisestusväljad psi arvutamiseks
        st.write("Määratakse lõigu otste paindemomendid suhte $\\psi$ ja teguri $C_1$ leidmiseks:")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            M_min_input = st.number_input("$M_{min}$ [kNm]:", value=0.0, step=0.1, key="m_min_input_sls1")
        with col_m2:
            M_max_input = st.number_input("$M_{max}$ [kNm]:", value=M_max_sls1, step=0.1, key="m_max_input_sls1")
            
        if M_max_input == 0:
            psi_sls1 = 1.0
        else:
            psi_sls1 = M_min_input / M_max_input
            
        # Piiratakse matemaatiliselt tabeli rajadesse [-1, 1]
        psi_sls1 = max(-1.0, min(1.0, psi_sls1))
        
        st.latex(r"{\footnotesize \psi = \frac{M_{min}}{M_{max}} = \frac{" + f"{M_min_input:.2f}" + r"}{" + f"{M_max_input:.2f}" + r"} = " + f"{psi_sls1:.3f}" + r"}")
        
        # Tabeli andmed interpoleerimiseks (psi väärtused peavad olema kasvavas järjekorras np.interp jaoks)
        psi_tabel = [-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00]
        c1_tabel  = [2.55,  2.57,  2.33,  2.05,  1.77, 1.52, 1.31, 1.14, 1.00]
        
        # Lineaarne interpoleerimine
        C1_sls1 = float(np.interp(psi_sls1, psi_tabel, c1_tabel))
        
        # Kuvatakse tabel otse ekraanile, et see oleks kogu aeg nähtav
        st.markdown("**Tabel 4.2.3. Teguri $C_1$ väärtused otstest paindemomendiga koormatud varda korral**")
        st.markdown("""

        | $\psi$ | $C_1$ |
        | :---: | :---: |
        | +1,00 | 1,00 |
        | +0,75 | 1,14 |
        | +0,50 | 1,31 |
        | +0,25 | 1,52 |
        | 0 | 1,77 |
        | -0,25 | 2,05 |
        | -0,50 | 2,33 |
        | -0,75 | 2,57 |
        | -1,00 | 2,55 |
        """)
            
        st.write("Teguri $C_1$ saame tabelist interpoleerimise teel:")
        st.latex(r"{\footnotesize C_1 = " + f"{C1_sls1:.3f}" + r"}")

        
        # M_cr arvutamine SLS 1 jaoks (ilma C2 ja zg liidendita)
        osa_pii_sls1 = (math.pi**2 * E * I_z_mm4) / (L_cr_mm_sls1**2)
        juurrettava_1_sls1 = I_w_mm6 / I_z_mm4
        juurrettava_2_sls1 = (L_cr_mm_sls1**2 * I_t_mm4) / (2.6 * math.pi**2 * I_z_mm4)
        
        osa_juuri_sls1 = math.sqrt(juurrettava_1_sls1 + juurrettava_2_sls1)
        M_cr_Nmm_sls1 = C1_sls1 * osa_pii_sls1 * osa_juuri_sls1
        M_cr_kNm_sls1 = M_cr_Nmm_sls1 / 1e6
        
        arvudega_valem_sls1 = (
            rf"M_{{cr,uls1}} = {C1_sls1:.3f} \cdot \frac{{\pi^2 \cdot {E:.0f} \cdot {I_z_mm4:.0f}}}{{{L_cr_mm_sls1:.0f}^2}} \cdot "
            rf"\sqrt{{\frac{{{I_w_mm6:.0f}}}{{{I_z_mm4:.0f}}} + \frac{{{L_cr_mm_sls1:.0f}^2}}{{2,6\pi^2}} \cdot \frac{{{I_t_mm4:.0f}}}{{{I_z_mm4:.0f}}}}} \cdot 10^{{-6}}"
        )
        st.latex(r"{\footnotesize " + arvudega_valem_sls1 + r"}")
        st.latex(r"{\footnotesize M_{cr,uls1} = " + f"{M_cr_kNm_sls1:.2f} \\text{{ kNm}}" + r"}")
        
        # --- KIIVETINGSALEDUS SLS 1 ---
        st.write("Leitakse kiivetingsaledus:")
        if kogu_klass == 1 or kogu_klass == 2:
            W_y_cm3 = prof_parand["Wpl_y"]
            W_y_tahis = "W_{pl,y}"
        else:
            W_y_cm3 = prof_parand["Wel_y"]
            W_y_tahis = "W_{el,y}"
        W_y_mm3 = W_y_cm3 * 1000.0
        M_cr_Nmm_arvutus_sls1 = M_cr_kNm_sls1 * 1e6
        lambda_bar_LT_sls1 = math.sqrt((W_y_mm3 * f_y) / M_cr_Nmm_arvutus_sls1)
        arvudega_lambda_LT_sls1 = rf"\sqrt{{\frac{{{W_y_mm3:.1f} \cdot {f_y:.0f}}}{{{M_cr_Nmm_arvutus_sls1:.1f}}}}} = {lambda_bar_LT_sls1:.3f}"
        st.latex(r"{\footnotesize \bar{\lambda}_{LT} = \sqrt{\frac{" + W_y_tahis + r" \cdot f_y}{M_{cr}}} = " + arvudega_lambda_LT_sls1 + r"}")
        
        st.write(f"Vastavalt leitud suhtele on kiivekõver {kiivekover} ja hälbetegur $\\alpha_{{LT}} = {alpha_LT}$")
        
        # --- ABISUURUS PHI_LT SLS 1 ---
        st.write("Arvutatakse abisuurus:")
        phi_LT_sls1 = 0.5 * (1.0 + alpha_LT * (lambda_bar_LT_sls1 - 0.4) + 0.75 * (lambda_bar_LT_sls1**2))
        arvudega_phi_LT_sls1 = rf"0,5 \cdot \left[ 1 + {alpha_LT} \cdot ({lambda_bar_LT_sls1:.3f} - 0,4) + 0,75 \cdot {lambda_bar_LT_sls1:.3f}^2 \right] = {phi_LT_sls1:.3f}"
        st.latex(r"{\footnotesize \Phi_{LT} = 0,5 \cdot \left[ 1 + \alpha_{LT} \cdot (\bar{\lambda}_{LT} - 0,4) + 0,75 \cdot \bar{\lambda}_{LT}^2 \right] = " + arvudega_phi_LT_sls1 + r"}")
        
        # --- KIIVETEGUR CHI_LT SLS 1 ---
        st.write("Leitakse kiivetegur:")
        nimetaja_juur_sls1 = phi_LT_sls1**2 - 0.75 * (lambda_bar_LT_sls1**2)
        if nimetaja_juur_sls1 < 0:
            nimetaja_juur_sls1 = 0.0
        chi_LT_sls1 = 1.0 / (phi_LT_sls1 + math.sqrt(nimetaja_juur_sls1))
        chi_LT_sls1 = min(chi_LT_sls1, 1.0)
        arvudega_chi_LT_sls1 = rf"\frac{{1}}{{{phi_LT_sls1:.3f} + \sqrt{{{phi_LT_sls1:.3f}^2 - 0,75 \cdot {lambda_bar_LT_sls1:.3f}^2}}}} = {chi_LT_sls1:.3f}"
        st.latex(r"{\footnotesize \chi_{LT} = \frac{1}{\Phi_{LT} + \sqrt{\Phi_{LT}^2 - 0,75 \cdot \bar{\lambda}_{LT}^2}} \leq 1.0 = " + arvudega_chi_LT_sls1 + r"}")
        
        # --- ARVUTUSLIK KIIVEKANDEVÕIME SLS 1 ---
        st.write("Arvutatakse tala arvutuslik kiivekandevõime:")
        M_b_Rd_sls1 = (chi_LT_sls1 * W_y_mm3 * f_y) / gamma_M1 / 1e6
        arvudega_Mb_Rd_sls1 = rf"\frac{{{chi_LT_sls1:.3f} \cdot {W_y_mm3:.1f} \cdot {f_y:.0f}}}{{{gamma_M1:.2f}}} \cdot 10^{{-6}} = {M_b_Rd_sls1:.2f} \text{{ kNm}}"
        st.latex(r"{\footnotesize M_{b,Rd} = \frac{\chi_{LT} \cdot " + W_y_tahis + r" \cdot f_y}{\gamma_{M1}} = " + arvudega_Mb_Rd_sls1 + r"}")
        
        st.write("**Kiivekandevõime stabiilsuskontroll (ULS 1):**")
        kuva_ed_rd_kontroll("ULS 1 kiivekandevõime", M_max_sls1, M_b_Rd_sls1, "kNm", r"M_{Ed}", r"M_{b,Rd}")
    else:
        st.info("Kuna lumekoormusest momendi suund ei muutu, siis eraldi selle kandevõimet pole vaja kontrollida")


    # --- ALAMPEATÜKK: SLS 2 ---
    st.subheader("ULS 2")
    if M_max_sls2 < 0:
        # SLS 2 puhul surutakse kokku alumine vöö, põiksuunaliseks toetussammuks on kogu hoone laius B
        L_cr_m_sls2 = B
        L_cr_mm_sls2 = L_cr_m_sls2 * 1000.0
        st.write("Kuna tuul muudab momendi suunda, siis muutub ka arvutuspikkus (põiksuunas toetamata alumine vöö):")
        st.write("Põiksuunas toetatud punktide vahekaugus L:")
        st.latex(r"{\footnotesize L = " + f"{L_cr_m_sls2:.3f} \\text{{ m}} = {L_cr_mm_sls2:.1f} \\text{{ mm}}" + r"}")
        
        # SLS 2 kordajad on fikseeritud täpsete tabeliväärtustega ilma muutmise võimaluseta
        C1_sls2 = 1.127
        C2_sls2 = 0.454
        
        # Koormuse rakenduspunkti kaugus varda teljest z_g
        z_g_sls2 = - h / 2.0 # mm
        st.write("Koormuse rakenduspunkti kaugus varda teljest $z_g$:")
        st.latex(r"{\footnotesize z_g = " + f"{z_g_sls2:.1f} \\text{{ mm}}" + r"}")
        st.write("Kordajad tabelist:")
        st.latex(r"{\footnotesize C_1 = " + f"{C1_sls2:.3f} \\quad C_2 = {C2_sls2:.3f}" + r"}")
        
        # --- TAASLOODUD ARVUTUS: Siin tekitatakse muutuja M_cr_kNm_sls2 ---
        osa_pii_sls2 = (math.pi**2 * E * I_z_mm4) / (L_cr_mm_sls2**2)
        juurrettava_1_sls2 = I_w_mm6 / I_z_mm4
        juurrettava_2_sls2 = (L_cr_mm_sls2**2 * I_t_mm4) / (2.6 * math.pi**2 * I_z_mm4)
        juurrettava_3_sls2 = (C2_sls2 * z_g_sls2)**2
        osa_juuri_sls2 = math.sqrt(juurrettava_1_sls2 + juurrettava_2_sls2 + juurrettava_3_sls2)
        osa_loppu_sls2 = C2_sls2 * z_g_sls2
        
        M_cr_Nmm_sls2 = C1_sls2 * osa_pii_sls2 * (osa_juuri_sls2 - osa_loppu_sls2)
        M_cr_kNm_sls2 = M_cr_Nmm_sls2 / 1e6  # <--- See rida oli kadunud
        
        if kogu_klass == 1 or kogu_klass == 2:
            W_y_tahis = "W_{pl,y}"
        else:
            W_y_tahis = "W_{el,y}"
            
        arvudega_valem_sls2 = (
            rf"M_{{cr,uls2}} = {C1_sls2:.3f} \cdot \frac{{\pi^2 \cdot {E:.0f} \cdot {I_z_mm4:.0f}}}{{{L_cr_mm_sls2:.0f}^2}} \cdot \left[ "
            rf"\sqrt{{\frac{{{I_w_mm6:.0f}}}{{{I_z_mm4:.0f}}} + \frac{{{L_cr_mm_sls2:.0f}^2}}{{2,6\pi^2}} \cdot \frac{{{I_t_mm4:.0f}}}{{{I_z_mm4:.0f}}} + ({C1_sls2:.3f} \cdot {z_g_sls2:.1f})^2}} "
            rf"- ({C2_sls2:.3f} \cdot {z_g_sls2:.1f}) \right] \cdot 10^{{-6}}"
        )
        st.latex(r"{\footnotesize " + arvudega_valem_sls2 + r"}")
        st.latex(r"{\footnotesize M_{cr,uls2} = " + f"{M_cr_kNm_sls2:.2f} \\text{{ kNm}}" + r"}")
        
        # --- KIIVETINGSALEDUS SLS 2 ---
        st.write("Leitakse kiivetingsaledus:")
        M_cr_Nmm_arvutus_sls2 = M_cr_kNm_sls2 * 1e6
        lambda_bar_LT_sls2 = math.sqrt((W_y_mm3 * f_y) / M_cr_Nmm_arvutus_sls2)
        arvudega_lambda_LT_sls2 = rf"\sqrt{{\frac{{{W_y_mm3:.1f} \cdot {f_y:.0f}}}{{{M_cr_Nmm_arvutus_sls2:.1f}}}}} = {lambda_bar_LT_sls2:.3f}"
        st.latex(r"{\footnotesize \bar{\lambda}_{LT} = \sqrt{\frac{" + W_y_tahis + r" \cdot f_y}{M_{cr}}} = " + arvudega_lambda_LT_sls2 + r"}")
        
        st.write(f"Vastavalt leitud suhtele on kiivekõver {kiivekover} and hälbetegur $\\alpha_{{LT}} = {alpha_LT}$")
        
        # --- ABISUURUS PHI_LT SLS 2 ---
        st.write("Arvutatakse abisuurus:")
        phi_LT_sls2 = 0.5 * (1.0 + alpha_LT * (lambda_bar_LT_sls2 - 0.4) + 0.75 * (lambda_bar_LT_sls2**2))
        arvudega_phi_LT_sls2 = rf"0,5 \cdot \left[ 1 + {alpha_LT} \cdot ({lambda_bar_LT_sls2:.3f} - 0,4) + 0,75 \cdot {lambda_bar_LT_sls2:.3f}^2 \right] = {phi_LT_sls2:.3f}"
        st.latex(r"{\footnotesize \Phi_{LT} = 0,5 \cdot \left[ 1 + \alpha_{LT} \cdot (\bar{\lambda}_{LT} - 0,4) + 0,75 \cdot \bar{\lambda}_{LT}^2 \right] = " + arvudega_phi_LT_sls2 + r"}")
        
        # --- KIIVETEGUR CHI_LT SLS 2 ---
        st.write("Leitakse kiivetegur:")
        nimetaja_juur_sls2 = phi_LT_sls2**2 - 0.75 * (lambda_bar_LT_sls2**2)
        if nimetaja_juur_sls2 < 0:
            nimetaja_juur_sls2 = 0.0
        chi_LT_sls2 = 1.0 / (phi_LT_sls2 + math.sqrt(nimetaja_juur_sls2))
        chi_LT_sls2 = min(chi_LT_sls2, 1.0)
        arvudega_chi_LT_sls2 = rf"\frac{{1}}{{{phi_LT_sls2:.3f} + \sqrt{{{phi_LT_sls2:.3f}^2 - 0,75 \cdot {lambda_bar_LT_sls2:.3f}^2}}}} = {chi_LT_sls2:.3f}"
        st.latex(r"{\footnotesize \chi_{LT} = \frac{1}{\Phi_{LT} + \sqrt{\Phi_{LT}^2 - 0,75 \cdot \bar{\lambda}_{LT}^2}} \leq 1.0 = " + arvudega_chi_LT_sls2 + r"}")
        
        # --- ARVUTUSLIK KIIVEKANDEVÕIME SLS 2 ---
        st.write("Arvutatakse tala arvutuslik kiivekandevõime:")
        M_b_Rd_sls2 = (chi_LT_sls2 * W_y_mm3 * f_y) / gamma_M1 / 1e6
        arvudega_Mb_Rd_sls2 = rf"\frac{{{chi_LT_sls2:.3f} \cdot {W_y_mm3:.1f} \cdot {f_y:.0f}}}{{{gamma_M1:.2f}}} \cdot 10^{{-6}} = {M_b_Rd_sls2:.2f} \text{{ kNm}}"
        st.latex(r"{\footnotesize M_{b,Rd} = \frac{\chi_{LT} \cdot " + W_y_tahis + r" \cdot f_y}{\gamma_{M1}} = " + arvudega_Mb_Rd_sls2 + r"}")
        
        st.write("**Kiivekandevõime stabiilsuskontroll (ULS 2):**")
        kuva_ed_rd_kontroll("ULS 2 kiivekandevõime", M_max_sls2, M_b_Rd_sls2, "kNm", r"M_{Ed}", r"M_{b,Rd}")
    else:
        st.info("Kuna tuule koormusest momendi suund ei muutu, siis eraldi selle kandevõimet pole vaja kontrollida")




