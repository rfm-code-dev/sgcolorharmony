import streamlit as st
import colorsys

# 1. Valores de intensidade válidos no hardware do Mega Drive (0 a 7 mapeados para 0-255)
VDP_STEPS = [0, 36, 73, 109, 146, 182, 219, 255]

def quantize_to_genesis(rgb):
    """Aproxima uma cor RGB comum para a paleta de 512 cores do Mega Drive."""
    return tuple(min(VDP_STEPS, key=lambda x: abs(x - c)) for c in rgb)

def rgb_to_sgdk_hex(rgb):
    """Converte RGB do Mega Drive para o formato hexadecimal lido pelo SGDK (0x0BGR)."""
    r, g, b = rgb
    r_vdp = VDP_STEPS.index(r) * 2
    g_vdp = VDP_STEPS.index(g) * 2
    b_vdp = VDP_STEPS.index(b) * 2
    vdp_value = (b_vdp << 8) | (g_vdp << 4) | r_vdp
    return f"0x{vdp_value:04X}"

def calculate_harmonies(base_rgb, angle):
    """Calcula uma cor harmônica rotacionando a Matiz (Hue) no espaço HSV."""
    r, g, b = [c / 255.0 for c in base_rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Rotaciona a matiz baseado no ângulo desejado (360 graus = 1.0)
    h_new = (h + (angle / 360.0)) % 1.0
    
    r_res, g_res, b_res = colorsys.hsv_to_rgb(h_new, s, v)
    rgb_raw = (int(r_res * 255), int(g_res * 255), int(b_res * 255))
    return quantize_to_genesis(rgb_raw)

# --- INTERFACE DO STREAMLIT ---
st.set_page_config(page_title="Mega Drive Color Harmony", page_icon="🎮")
st.title("🎮 Mega Drive Color Harmony Tool")
st.markdown("Calcule harmonias de cores travadas estritamente na paleta de **512 cores (9-bit RGB)** do VDP do Sega Genesis/Mega Drive.")

# Seleção da cor base usando o seletor nativo
st.sidebar.header("Configurações")
picker_color = st.sidebar.color_picker("Escolha a Cor Base", "#FF0000")

# Converte o hex do seletor para RGB puro
r_base = int(picker_color[1:3], 16)
g_base = int(picker_color[3:5], 16)
b_base = int(picker_color[5:7], 16)

# Quantiza a cor base para o padrão do console
base_genesis = quantize_to_genesis((r_base, g_base, b_base))
hex_base_genesis = f"#{base_genesis[0]:02X}{base_genesis[1]:02X}{base_genesis[2]:02X}"

# Cálculos das harmonias
comp_genesis = calculate_harmonies(base_genesis, 180)
hex_comp_genesis = f"#{comp_genesis[0]:02X}{comp_genesis[1]:02X}{comp_genesis[2]:02X}"

triade1_genesis = calculate_harmonies(base_genesis, 120)
hex_t1_genesis = f"#{triade1_genesis[0]:02X}{triade1_genesis[1]:02X}{triade1_genesis[2]:02X}"

triade2_genesis = calculate_harmonies(base_genesis, 240)
hex_t2_genesis = f"#{triade2_genesis[0]:02X}{triade2_genesis[1]:02X}{triade2_genesis[2]:02X}"

# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader("🎨 Paleta Gerada (Convertida para o Hardware)")

# Componente visual para mostrar as cores lado a lado
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Cor Base**")
    st.color_picker("Base", hex_base_genesis, key="p1", disabled=True)
    st.code(f"RGB: {base_genesis}\nSGDK: {rgb_to_sgdk_hex(base_genesis)}")

with col2:
    st.markdown("**Complementar**")
    st.color_picker("Complementar", hex_comp_genesis, key="p2", disabled=True)
    st.code(f"RGB: {comp_genesis}\nSGDK: {rgb_to_sgdk_hex(comp_genesis)}")

with col3:
    st.markdown("**Tríade 1**")
    st.color_picker("Tríade 1", hex_t1_genesis, key="p3", disabled=True)
    st.code(f"RGB: {triade1_genesis}\nSGDK: {rgb_to_sgdk_hex(triade1_genesis)}")

with col4:
    st.markdown("**Tríade 2**")
    st.color_picker("Tríade 2", hex_t2_genesis, key="p4", disabled=True)
    st.code(f"RGB: {triade2_genesis}\nSGDK: {rgb_to_sgdk_hex(triade2_genesis)}")

# Código Pronto para o SGDK
st.subheader("💻 Código Pronto para o SGDK (C Array)")
sgdk_array = f"u16 my_palette[4] = {{\n    {rgb_to_sgdk_hex(base_genesis)}, {rgb_to_sgdk_hex(comp_genesis)}, {rgb_to_sgdk_hex(triade1_genesis)}, {rgb_to_sgdk_hex(triade2_genesis)}\n}};"
st.code(sgdk_array, language="c")

