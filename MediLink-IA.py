from importlib.metadata import files

import streamlit as st
from datetime import datetime
import pandas as pd
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="MediLink IA",
    page_icon="🩺",
    layout="centered"
)

# ESTILOS CSS
st.markdown("""
<style>

.stApp {
    background-color: #c2c2c2;
}

h1 {
    color: #00913f !important;
    text-align: center;
}

h2 {
    color: #134f5c !important;
}

h3 {
    color: #134f5c !important;
}

p {
    color: black !important;
}

div[data-testid="stWidgetLabel"] p {
    color: white !important;
    font-weight: 600 !important;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 2rem;
}

.caja {
    background-color: white;
    padding: 8px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# TÍTULO
st.title("🩺 MediLink IA")

st.markdown("""
<div class="caja" style="
display:flex;
align-items:center;
justify-content:center;
height:70px;
">

<p style="
color:black !important;
font-weight:600;
margin:0;
font-size:20px;
">
SISTEMA INTELIGENTE DE ORIENTACIÓN PARA TELEMEDICINA
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background-color:#f8d7da;
color:#b81414;
padding:15px;
border-radius:12px;
font-weight:600;
margin-bottom:20px;
border:1px solid #f5c2c7;
">

⚠️ Este sistema no reemplaza la evaluación de un profesional de salud. ⚠️

</div>
""", unsafe_allow_html=True)

inicio = datetime.now()

# DATOS DEL PACIENTE
st.markdown('<div class="caja">', unsafe_allow_html=True)

st.header("📋 Datos del paciente")
historia_clinica = st.text_input("Número de historia clínica del paciente")
edad = st.number_input("Edad del paciente", min_value=0, max_value=120, step=1)

temperatura = st.number_input(
    "Temperatura corporal (°C)",
    min_value=30.0,
    max_value=45.0,
    step=0.1
)

saturacion = st.number_input(
    "Saturación de oxígeno (%)",
    min_value=50,
    max_value=100,
    step=1
)

frecuencia = st.number_input(
    "Frecuencia cardíaca",
    min_value=30,
    max_value=200,
    step=1
)

st.markdown("</div>", unsafe_allow_html=True)

# SÍNTOMAS
st.markdown('<div class="caja">', unsafe_allow_html=True)

st.header("🩹 Síntomas reportados")

tos = st.selectbox("¿Presenta tos?", ["No", "Sí"])

dolor_garganta = st.selectbox(
    "¿Presenta dolor de garganta?",
    ["No", "Sí"]
)

dificultad_respiratoria = st.selectbox(
    "¿Presenta dificultad respiratoria?",
    ["No", "Sí"]
)

dolor_corporal = st.selectbox(
    "¿Presenta dolor corporal?",
    ["No", "Sí"]
)

st.markdown("</div>", unsafe_allow_html=True)

# BOTÓN
st.markdown("""
<style>
div.stButton > button {
    background-color: #00913f;
    color: white !important;
    font-size: 16px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

if st.button("🔍 Evaluar paciente"):

    if historia_clinica.strip() == "":
        st.error("Debe ingresar el número de historia clínica del paciente.")
    
    elif not historia_clinica.isdigit():
        st.error("La historia clínica debe contener solo números.")
    elif len(historia_clinica) != 7:
        st.error("La historia clínica debe tener exactamente 7 dígitos.")
    
    elif edad == 0:
        st.error("Debe ingresar una edad válida.")

    elif temperatura == 30.0:
        st.error("Debe ingresar la temperatura del paciente.")

    elif saturacion == 50:
        st.error("Debe ingresar la saturación real del paciente.")

    elif frecuencia == 30:
        st.error("Debe ingresar la frecuencia cardíaca real del paciente.")

    else:

        prioridad = "BAJA"
        motivos = []

        if saturacion < 92:
            prioridad = "ALTA"
            motivos.append("saturación de oxígeno baja")

        if dificultad_respiratoria == "Sí":
            prioridad = "ALTA"
            motivos.append("dificultad respiratoria")

        if temperatura >= 39:
            prioridad = "ALTA"
            motivos.append("fiebre alta")

        if frecuencia > 120:
            prioridad = "ALTA"
            motivos.append("frecuencia cardíaca elevada")

        if prioridad != "ALTA":

            sintomas = 0

            if temperatura >= 38:
                sintomas += 1
                motivos.append("fiebre moderada")

            if tos == "Sí":
                sintomas += 1
                motivos.append("tos")

            if dolor_garganta == "Sí":
                sintomas += 1
                motivos.append("dolor de garganta")

            if dolor_corporal == "Sí":
                sintomas += 1
                motivos.append("dolor corporal")

            if sintomas >= 1:
                prioridad = "MEDIA"

        fin = datetime.now()
        tiempo_atencion = round((fin - inicio).total_seconds(), 2)

        st.markdown('<div class="caja">', unsafe_allow_html=True)

        st.header("📊 Resultado de orientación")

        if prioridad == "ALTA":
            st.error("Prioridad ALTA")
            recomendacion = "Se recomienda atención médica inmediata."

        elif prioridad == "MEDIA":
            st.warning("Prioridad MEDIA")
            recomendacion = "Se recomienda teleconsulta médica."

        else:
            st.success("Prioridad BAJA")
            recomendacion = "Se recomienda seguimiento general."

        st.write("### Recomendación")
        st.write(recomendacion)

        st.write("### Motivos identificados")

        if motivos:
            for motivo in motivos:
                st.write("•", motivo)
        else:
            st.write("No se identificaron signos de alarma.")

        st.write("### Tiempo de orientación")
        st.write(tiempo_atencion, "segundos")

        datos = {
            "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Historia_Clinica": [historia_clinica],
            "Edad": [edad],
            "Temperatura": [temperatura],
            "Saturacion": [saturacion],
            "Frecuencia_Cardiaca": [frecuencia],
            "Tos": [tos],
            "Dolor_Garganta": [dolor_garganta],
            "Dificultad_Respiratoria": [dificultad_respiratoria],
            "Dolor_Corporal": [dolor_corporal],
            "Prioridad": [prioridad],
            "Motivos": [", ".join(motivos) if motivos else "Sin signos de alarma"],
            "Recomendacion": [recomendacion],
            "Tiempo_Orientacion_Segundos": [tiempo_atencion]
        }

        df = pd.DataFrame(datos)

        archivo = "HISTORIAL DE PACIENTES.xlsx"

        if os.path.exists(archivo):
            df_existente = pd.read_excel(archivo)
            df_final = pd.concat([df_existente, df], ignore_index=True)
            df_final.to_excel(archivo, index=False, engine="openpyxl")
        else:
            df.to_excel(archivo, index=False, engine="openpyxl")

        st.success("✅ Registro guardado correctamente.")

        if st.button("➕ Registrar nuevo paciente"):
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

with st.sidebar:

    st.header("🔒 Historial clínico")

    clave = st.text_input("Contraseña", type="password")

    if clave == "personal2026":

        archivo = "HISTORIAL DE PACIENTES.xlsx"

        if os.path.exists(archivo):

            df_historial = pd.read_excel(archivo)

            columnas_mostrar = [
                "Fecha",
                "Historia_Clinica",
                "Edad",
                "Temperatura",
                "Saturacion",
                "Frecuencia_Cardiaca",
                "Prioridad",
                "Recomendacion"
            ]

            df_mostrar = df_historial[columnas_mostrar].copy()

            df_mostrar["Semaforo"] = df_mostrar["Prioridad"].map({
                "ALTA": "🔴 ALTA",
                "MEDIA": "🟡 MEDIA",
                "BAJA": "🟢 BAJA"
            })

            st.success("Acceso concedido")

            buscar_hc = st.text_input("Buscar historia clínica")

            if buscar_hc:
                df_filtrado = df_mostrar[
                    df_mostrar["Historia_Clinica"].astype(str).str.contains(
                        buscar_hc,
                        case=False,
                        na=False
                    )
                ]
                st.dataframe(df_filtrado, use_container_width=True)
            else:
                st.dataframe(df_mostrar, use_container_width=True)
                st.download_button(
        label="📥 Descargar historial en Excel",
        data=files,
        file_name="HISTORIAL DE PACIENTES.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

        else:
            st.warning("Aún no existen registros.")

    elif clave != "":
        st.error("Contraseña incorrecta.")