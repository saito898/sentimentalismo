from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import base64


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Análisis de Sentimiento",
    page_icon="💭",
    layout="wide"
)


# ============================================================
# ESTILOS - COLORES NEUTROS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');


/* ============================================================
   COLORES
   ============================================================ */

:root {
    --fondo: #F5F3F0;
    --blanco: #FFFFFF;
    --beige: #E8E2DA;
    --beige-oscuro: #D5CEC4;
    --gris: #77716A;
    --gris-oscuro: #393633;
    --negro: #242220;
    --verde: #788A78;
    --rojo: #9A7771;
    --gris-neutral: #85817B;
}


/* ============================================================
   FONDO GENERAL
   ============================================================ */

.stApp {
    background: #F5F3F0;
    font-family: 'DM Sans', sans-serif;
    color: #393633;
}


.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   TÍTULOS
   ============================================================ */

h1, h2, h3, h4 {
    font-family: 'DM Sans', sans-serif !important;
    color: #242220 !important;
}


/* ============================================================
   TÍTULO PRINCIPAL
   ============================================================ */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: #393633;
    margin-bottom: 0.3rem;
}


.main-subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #77716A;
    margin-bottom: 2rem;
}


/* ============================================================
   IMAGEN
   ============================================================ */

.image-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}


/* ============================================================
   TARJETA DE ANÁLISIS
   ============================================================ */

.analysis-card {
    background: #FFFFFF;
    border: 1px solid #E8E2DA;
    border-radius: 22px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(70, 65, 60, 0.08);
}


/* ============================================================
   INPUT
   ============================================================ */

.stTextInput input {
    background: #FFFFFF !important;
    color: #242220 !important;
    border: 2px solid #D5CEC4 !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}


.stTextInput input:focus {
    border-color: #85817B !important;
    box-shadow: 0 0 0 2px rgba(133, 129, 123, 0.15) !important;
}


.stTextInput input::placeholder {
    color: #99938C !important;
}


/* ============================================================
   EXPANDER
   ============================================================ */

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E8E2DA;
    border-radius: 18px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #EAE6E0;
    border-right: 1px solid #D5CEC4;
}


section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #242220 !important;
}


/* ============================================================
   RESULTADOS
   ============================================================ */

.result-box {
    background: #F8F6F3;
    border: 1px solid #E2DDD6;
    border-radius: 18px;
    padding: 1.3rem;
    margin-top: 1rem;
}


.metric-title {
    font-size: 0.9rem;
    color: #77716A;
}


.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #242220;
}


/* ============================================================
   MENSAJES DE SENTIMIENTO
   ============================================================ */

.positive {
    background: #E7ECE5;
    color: #536253;
    border-left: 5px solid #788A78;
    border-radius: 12px;
    padding: 1rem;
    font-weight: 600;
}


.negative {
    background: #EEE5E2;
    color: #785C57;
    border-left: 5px solid #9A7771;
    border-radius: 12px;
    padding: 1rem;
    font-weight: 600;
}


.neutral {
    background: #EAE8E5;
    color: #66625D;
    border-left: 5px solid #85817B;
    border-radius: 12px;
    padding: 1rem;
    font-weight: 600;
}


/* ============================================================
   DIVISORES
   ============================================================ */

hr {
    border: none;
    border-top: 1px solid #D5CEC4;
    margin: 2rem 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIÓN PARA REPRODUCIR AUDIO AUTOMÁTICAMENTE
# ============================================================

def reproducir_audio(archivo):

    try:

        with open(archivo, "rb") as audio_file:
            audio_bytes = audio_file.read()

        audio_base64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio autoplay>
            <source
                src="data:audio/mp3;base64,{audio_base64}"
                type="audio/mpeg"
            >
        </audio>
        """

        st.markdown(
            audio_html,
            unsafe_allow_html=True
        )

    except FileNotFoundError:

        st.warning(
            f"No se encontró el archivo de audio: {archivo}"
        )


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="main-title">'
    '💭 Análisis de Sentimiento'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-subtitle">'
    'Descubre qué emoción transmite tu texto'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# IMAGEN
# ============================================================

try:

    image = Image.open("emoticones.jpg")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            image,
            use_container_width=True
        )

except FileNotFoundError:

    st.warning(
        "No se encontró la imagen 'emoticones.jpg'."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.subheader("Polaridad y Subjetividad")

    st.write(
        """
        **Polaridad:** indica si el sentimiento expresado
        en el texto es positivo, negativo o neutral.

        Su valor va desde **-1** hasta **1**:

        • -1 → muy negativo  
        • 0 → neutral  
        • 1 → muy positivo

        **Subjetividad:** mide cuánto del contenido expresa
        opiniones, emociones o creencias frente a información
        objetiva.

        Su valor va desde **0** hasta **1**.
        """
    )


# ============================================================
# ANALIZAR TEXTO
# ============================================================

with st.expander(
    "🔍 Analizar texto",
    expanded=True
):

    st.subheader(
        "Escribe el texto que deseas analizar"
    )

    text = st.text_input(
        "Escribe por favor:",
        placeholder="Ejemplo: Hoy estoy muy feliz porque tuve un día increíble 😊"
    )


    # ========================================================
    # PROCESAMIENTO
    # ========================================================

    if text:

        translator = Translator()

        try:

            translation = translator.translate(
                text,
                src="es",
                dest="en"
            )

            trans_text = translation.text

            blob = TextBlob(trans_text)

            polarity = round(
                blob.sentiment.polarity,
                2
            )

            subjectivity = round(
                blob.sentiment.subjectivity,
                2
            )


            # ====================================================
            # RESULTADOS
            # ====================================================

            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="metric-title">
                            Polaridad
                        </div>
                        <div class="metric-value">
                            {polarity}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with col2:

                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="metric-title">
                            Subjetividad
                        </div>
                        <div class="metric-value">
                            {subjectivity}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ====================================================
            # SENTIMIENTO POSITIVO
            # ====================================================

            if polarity > 0:

                st.markdown(
                    """
                    <div class="positive">
                        😊 Es un sentimiento Positivo
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # GIF / LOTTIE

                try:

                    with open(
                        "perrito.json",
                        "r"
                    ) as source:

                        animation = json.load(source)

                    col1, col2, col3 = st.columns(
                        [1, 2, 1]
                    )

                    with col2:

                        st_lottie(
                            animation,
                            width=350
                        )

                except FileNotFoundError:

                    st.warning(
                        "No se encontró 'perrito.json'."
                    )


                # MÚSICA FELIZ AUTOMÁTICA

                reproducir_audio(
                    "feliz.mp3"
                )


            # ====================================================
            # SENTIMIENTO NEGATIVO
            # ====================================================

            elif polarity < 0:

                st.markdown(
                    """
                    <div class="negative">
                        😔 Es un sentimiento Negativo
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # GIF / LOTTIE

                try:

                    with open(
                        "triste.json",
                        "r"
                    ) as source:

                        animation = json.load(source)

                    col1, col2, col3 = st.columns(
                        [1, 2, 1]
                    )

                    with col2:

                        st_lottie(
                            animation,
                            width=350
                        )

                except FileNotFoundError:

                    st.warning(
                        "No se encontró 'triste.json'."
                    )


                # MÚSICA TRISTE AUTOMÁTICA

                reproducir_audio(
                    "triste.mp3"
                )


            # ====================================================
            # SENTIMIENTO NEUTRAL
            # ====================================================

            else:

                st.markdown(
                    """
                    <div class="neutral">
                        😐 Es un sentimiento Neutral
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # GIF / LOTTIE

                try:

                    with open(
                        "neutral.json",
                        "r"
                    ) as source:

                        animation = json.load(source)

                    col1, col2, col3 = st.columns(
                        [1, 2, 1]
                    )

                    with col2:

                        st_lottie(
                            animation,
                            width=350
                        )

                except FileNotFoundError:

                    st.warning(
                        "No se encontró 'neutral.json'."
                    )


        except Exception as e:

            st.error(
                f"No fue posible analizar el texto: {e}"
            )
