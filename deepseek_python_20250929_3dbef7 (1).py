import streamlit as st
import random
import json
from datetime import datetime
import base64

# Configuração da página
st.set_page_config(
    page_title="BibleTok Generator 2.0",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .theme-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        color: white;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .theme-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .generated-script {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    .bible-verse {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Base de dados de temas bíblicos
BIBLE_THEMES = {
    "Histórias do Antigo Testamento": [
        "A Criação do Mundo - Gênesis 1-2",
        "Adão e Eva no Jardim do Éden - Gênesis 3",
        "Caim e Abel - Gênesis 4",
        "A Arca de Noé - Gênesis 6-9",
        "A Torre de Babel - Gênesis 11",
        "A Chamada de Abraão - Gênesis 12",
        "O Sacrifício de Isaque - Gênesis 22",
        "Jacó e Esaú - Gênesis 25-27",
        "José e seus Irmãos - Gênesis 37-50",
        "Moisés e a Sarça Ardente - Êxodo 3",
        "As 10 Pragas do Egito - Êxodo 7-12",
        "A Travessia do Mar Vermelho - Êxodo 14",
        "Os 10 Mandamentos - Êxodo 20",
        "Davi e Golias - 1 Samuel 17",
        "Daniel na Cova dos Leões - Daniel 6",
        "Jonas e o Grande Peixe - Jonas 1-4"
    ],
    "Milagres de Jesus": [
        "A Transformação da Água em Vinho - João 2",
        "A Cura do Filho do Oficial - João 4",
        "A Cura do Paralítico - João 5",
        "A Multiplicação dos Pães e Peixes - João 6",
        "Jesus Anda sobre as Águas - Mateus 14",
        "A Cura do Cego de Nascença - João 9",
        "A Ressurreição de Lázaro - João 11",
        "A Cura dos Dez Leprosos - Lucas 17"
    ],
    "Parábolas de Jesus": [
        "O Bom Samaritano - Lucas 10",
        "O Filho Pródigo - Lucas 15",
        "O Semeador - Mateus 13",
        "O Bom Pastor - João 10",
        "A Ovelha Perdida - Lucas 15",
        "O Rico e Lázaro - Lucas 16",
        "Os Talentos - Mateus 25",
        "As Dez Virgens - Mateus 25"
    ],
    "Personagens Inspiradores": [
        "A Fé de Abraão - Hebreus 11",
        "A Coragem de Ester - Ester 4",
        "A Paciência de Jó - Jó 1-2",
        "A Lealdade de Rute - Rute 1",
        "A Sabedoria de Salomão - 1 Reis 3",
        "A Ousadia de Pedro - Atos 2",
        "A Transformação de Paulo - Atos 9",
        "A Força de Sansão - Juízes 16"
    ],
    "Ensinamentos Principais": [
        "O Sermão da Montanha - Mateus 5-7",
        "O Maior Mandamento - Mateus 22",
        "A Oração do Pai Nosso - Mateus 6",
        "As Bem-Aventuranças - Mateus 5",
        "O Fruto do Espírito - Gálatas 5",
        "A Armadura de Deus - Efésios 6",
        "O Amor de 1 Coríntios 13 - 1 Coríntios 13",
        "A Grande Comissão - Mateus 28"
    ]
}

# Personagens e estilos
CHARACTERS = {
    "🎭 Narrador Dramático": "Conta a história com muita emoção e suspense",
    "🤔 Questionador Curioso": "Faz perguntas que o público também faria",
    "💫 Contador de Histórias": "Estilo tradicional, como avô contando histórias",
    "🔥 Pregador Energético": "Cheio de energia e paixão pela mensagem",
    "🎯 Professor Sábio": "Explica com clareza e profundidade",
    "😊 Amigo Próximo": "Conversa íntima, como um amigo contando algo importante"
}

VIDEO_STYLES = {
    "📖 Animação Bíblica": "Ilustrações estilo desenho animado bíblico",
    "🎬 Documentário": "Estilo National Geographic com imagens reais",
    "💭 Motion Graphics": "Textos animados e gráficos explicativos",
    "🎭 Dramatização": "Atores representando a cena bíblica",
    "📝 Texto Criativo": "Foco em legendas criativas e tipografia",
    "🎨 Arte Digital": "Arte digital moderna inspirada na história"
}

# Função para gerar temas aleatórios
def generate_random_themes():
    selected_themes = []
    categories = list(BIBLE_THEMES.keys())
    
    # Garante pelo menos um tema de cada categoria
    for category in categories:
        if BIBLE_THEMES[category]:
            selected_themes.append(random.choice(BIBLE_THEMES[category]))
    
    # Completa com temas aleatórios até ter 8
    while len(selected_themes) < 8:
        random_category = random.choice(categories)
        random_theme = random.choice(BIBLE_THEMES[random_category])
        if random_theme not in selected_themes:
            selected_themes.append(random_theme)
    
    random.shuffle(selected_themes)
    return selected_themes

# Função principal para gerar roteiro
def generate_script(theme, character, style, custom_elements=None):
    theme_name = theme.split(" - ")[0]
    bible_reference = theme.split(" - ")[1] if " - " in theme else "Bíblia"
    
    script_template = f"""
🎬 **ROTEIRO BÍBLICO - {theme_name.upper()}**

📖 **REFERÊNCIA:** {bible_reference}
🎭 **PERSONAGEM:** {character}
🎨 **ESTILO:** {style}

---

⏱️ **ESTRUTURA DO VÍDEO (45 segundos):**

**[0-8s] 🎣 GANCHO IMPACTANTE:**
"Você sabia que {generate_hook(theme_name)}?"

**[8-20s] 📖 CONTEXTO DRAMÁTICO:**
{generate_context(theme_name)}

**[20-35s] 💫 CLÍMAX DA HISTÓRIA:**
{generate_climax(theme_name)}

**[35-42s] 💡 LIÇÃO PRÁTICA:**
{generate_lesson(theme_name)}

**[42-45s] 📲 CHAMADA PARA AÇÃO:**
"Qual parte dessa história mais tocou você? Comenta! 👇❤️"

---

🎯 **ELEMENTOS VISUAIS SUGERIDOS:**
{generate_visual_elements(style)}

📊 **HASHTAGS RECOMENDADAS:**
#Bíblia #HistóriaBíblica #Fé #Deus #Jesus #Espiritualidade #Motivação #Superação

💡 **DICA DE GRAVAÇÃO:** Use transições suaves e mantenha contato visual com a câmera!

*Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}*
"""
    
    return script_template

# Funções auxiliares para gerar conteúdo
def generate_hook(theme):
    hooks = [
        f"essa história de {theme} pode transformar sua perspectiva sobre a vida?",
        f"existe um segredo incrível por trás de {theme} que poucos conhecem?",
        f"o que {theme} tem a ver com os desafios que você enfrenta hoje?",
        f"como {theme} pode te dar forças para vencer suas batalhas?",
        f"a emocionante história de {theme} que vai tocar seu coração!"
    ]
    return random.choice(hooks)

def generate_context(theme):
    contexts = [
        f"Em um momento crucial, os personagens enfrentaram desafios que testaram sua fé de formas inesperadas.",
        f"A situação parecia impossível, mas através da obediência a Deus, algo extraordinário estava prestes a acontecer.",
        f"Num contexto de grandes dificuldades, a intervenção divina mostrou que nada é impossível para Deus.",
        f"Enquanto todos duvidavam, uma fé inabalável abriu caminho para um milagre surpreendente."
    ]
    return random.choice(contexts)

def generate_climax(theme):
    climaxes = [
        f"O momento de virada chegou quando, contra todas as expectativas, Deus agiu de forma poderosa e transformadora.",
        f"Quando tudo parecia perdido, uma luz de esperança brilhou mostrando o cuidado e amor divino.",
        f"No ponto mais crítico da história, a fidelidade foi recompensada de maneira extraordinária.",
        f"A surpresa foi tão grande que mudou para sempre a vida de todos os envolvidos."
    ]
    return random.choice(climaxes)

def generate_lesson(theme):
    lessons = [
        f"Essa história nos ensina que a fé em Deus pode mover montanhas e transformar situações impossíveis.",
        f"A lição principal é que a obediência a Deus sempre traz bênçãos, mesmo quando não entendemos Seus planos.",
        f"Nos mostra que Deus está sempre no controle, mesmo quando tudo parece desmoronar ao nosso redor.",
        f"Ensina que o amor e misericórdia de Deus são maiores que qualquer erro ou fracasso nosso."
    ]
    return random.choice(lessons)

def generate_visual_elements(style):
    elements = {
        "📖 Animação Bíblica": "• Ilustrações em aquarela estilo bíblico\n• Personagens com roupas da época\n• Cenários históricos detalhados",
        "🎬 Documentário": "• Imagens reais do local histórico\n• Reconstituições profissionais\n• Mapas e localizações geográficas",
        "💭 Motion Graphics": "• Textos animados em movimento\n• Ícones e símbolos explicativos\n• Transições dinâmicas entre cenas",
        "🎭 Dramatização": "• Atores representando personagens\n• Cenários montados com precisão\n• Figurinos históricos autênticos",
        "📝 Texto Criativo": "• Tipografia expressiva\n• Efeitos de texto dinâmicos\n• Cores que representam emoções",
        "🎨 Arte Digital": "• Arte digital moderna\n• Cores vibrantes e contrastantes\n• Elementos abstratos significativos"
    }
    return elements.get(style, "• Use elementos visuais que complementem a narrativa")

# Interface principal
def main():
    st.markdown('<h1 class="main-header">📖 BIBLETOK GENERATOR 2.0</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        st.info("Configure seu roteiro bíblico perfeito!")
        
        selected_character = st.selectbox(
            "🎭 Escolha o Personagem:",
            options=list(CHARACTERS.keys()),
            format_func=lambda x: f"{x} - {CHARACTERS[x]}"
        )
        
        selected_style = st.selectbox(
            "🎨 Escolha o Estilo do Vídeo:",
            options=list(VIDEO_STYLES.keys()),
            format_func=lambda x: f"{x} - {VIDEO_STYLES[x]}"
        )
        
        st.header("📊 Estatísticas")
        st.metric("Temas Disponíveis", sum(len(themes) for themes in BIBLE_THEMES.values()))
        st.metric("Categorias", len(BIBLE_THEMES))
        st.metric("Estilos de Vídeo", len(VIDEO_STYLES))
    
    # Layout principal com abas
    tab1, tab2, tab3 = st.tabs(["🎲 Gerar Temas", "📝 Criar Roteiro", "📚 Biblioteca"])
    
    with tab1:
        st.header("🎲 Seletor de Temas Bíblicos")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Gerar 8 Novos Temas", use_container_width=True):
                st.session_state.random_themes = generate_random_themes()
        
        # Exibir temas
        if 'random_themes' not in st.session_state:
            st.session_state.random_themes = generate_random_themes()
        
        st.subheader("✨ Temas Sugeridos para Seus Vídeos:")
        
        # Criar grid de temas
        cols = st.columns(2)
        for i, theme in enumerate(st.session_state.random_themes):
            with cols[i % 2]:
                if st.button(
                    f"**{theme}**", 
                    key=f"theme_{i}",
                    use_container_width=True
                ):
                    st.session_state.selected_theme = theme
                    st.success(f"Tema selecionado: {theme}")
    
    with tab2:
        st.header("📝 Criar Roteiro Completo")
        
        # Seleção de tema
        theme_options = []
        for category, themes in BIBLE_THEMES.items():
            theme_options.extend(themes)
        
        selected_theme = st.selectbox(
            "📖 Escolha um Tema Bíblico:",
            options=theme_options,
            index=0,
            help="Selecione um tema ou use um dos temas gerados automaticamente"
        )
        
        # Botão para gerar roteiro
        if st.button("🎬 Gerar Roteiro Completo", type="primary", use_container_width=True):
            with st.spinner("Criando seu roteiro bíblico incrível..."):
                script = generate_script(selected_theme, selected_character, selected_style)
                
                # Exibir roteiro
                st.markdown('<div class="generated-script">', unsafe_allow_html=True)
                st.markdown(script)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Botão para copiar
                st.code(script, language="markdown")
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar Roteiro",
                    data=script,
                    file_name=f"roteiro_biblico_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    with tab3:
        st.header("📚 Biblioteca de Temas Bíblicos")
        
        for category, themes in BIBLE_THEMES.items():
            with st.expander(f"📂 {category} ({len(themes)} temas)"):
                for theme in themes:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"• {theme}")
                    with col2:
                        if st.button("Usar", key=f"use_{theme}"):
                            st.session_state.selected_theme = theme
                            st.success(f"Tema selecionado: {theme}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**BibleTok Generator 2.0** • Criado com ❤️ para compartilhar a Palavra de Deus • "
        "Baseado na Bíblia NTLH"
    )

if __name__ == "__main__":
    main()