import streamlit as st
import json
import os
import shutil
import textwrap
import base64

# ==========================================================================
# CONFIGURAÇÕES E DIRETÓRIOS DINÂMICOS
# ==========================================================================
LINK_INSCRICAO = "https://survey123.arcgis.com/share/cee3256c9e044b688c79aa28ff2aab1f"
LINK_TRANSMISSAO = ""  # preencher com o link da transmissão ao vivo

# Configuração de Página do Streamlit
st.set_page_config(
    page_title="Seminário de Inteligência - EsIMEx",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================================
# HELPER: ASSETS ESTÁTICOS (servidos pelo Streamlit em /app/static/)
# ==========================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ASSETS_DIR = os.path.join(BASE_DIR, "static", "assets")

ASSET_SOURCE_DIRS = (
    os.path.join(BASE_DIR, "assets"),
    os.path.join(BASE_DIR, "imagens"),
    os.path.join(BASE_DIR, "imagens", "palestrantes"),
)

def sync_static_assets():
    """Copia assets/, imagens/ e imagens/palestrantes/ para static/assets/."""
    os.makedirs(STATIC_ASSETS_DIR, exist_ok=True)
    for folder in ASSET_SOURCE_DIRS:
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            if not name.endswith((".png", ".jpg", ".jpeg", ".webp", ".css", ".js")):
                continue
            src = os.path.join(folder, name)
            if not os.path.isfile(src):
                continue
            safe_name = name.replace(" ", "_")
            dst = os.path.join(STATIC_ASSETS_DIR, safe_name)
            if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy2(src, dst)

def static_asset_url(filename):
    return f"/app/static/assets/{filename}"

def image_to_data_url(path):
    """Converte imagem local para data URL base64 (evita problemas de path no iframe)."""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime};base64,{encoded}"

# Carrega os dados do arquivo JSON de extração, limpando marcações markdown se existirem
def load_event_data():
    with open(os.path.join(BASE_DIR, "extrato_os.json"), "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        return json.loads(content)

event_data = load_event_data()

# Carregar estilos
def load_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_css():
    return f"<style>{load_file(os.path.join(BASE_DIR, 'assets', 'style.css'))}</style>"

def load_streamlit_overrides():
    return f"<style>{load_file(os.path.join(BASE_DIR, 'assets', 'streamlit-overrides.css'))}</style>"

def load_tailwind_config():
    return load_file(os.path.join(BASE_DIR, "assets", "tailwind.config.js"))

css_content = load_css()
streamlit_overrides = load_streamlit_overrides()
tailwind_config_js = load_tailwind_config()

def b64(relative_path):
    """Retorna data URL base64 para um arquivo relativo ao BASE_DIR."""
    return image_to_data_url(os.path.join(BASE_DIR, relative_path))

img_qrcode    = b64("imagens/qrcode.png")
img_mourao    = b64("imagens/palestrantes/genMourao.jpeg")
_anna_placeholder = '<div class="w-32 h-32 rounded-full border-4 border-primary mb-4 bg-surface-container flex items-center justify-center"><span class="material-symbols-outlined text-5xl text-on-surface-variant">person</span></div>'
img_wellington = b64("imagens/palestrantes/profWellington.jpeg")
img_mauricio  = b64("imagens/palestrantes/mauriciuViegas.jpeg")
img_heitor    = b64("imagens/palestrantes/Tc R1 Heitor.jpeg")
img_marcio    = b64("imagens/palestrantes/marcioLopes.jpeg")
img_concepcao = b64("imagens/banner.jpeg")
img_auditorio = b64("imagens/auditorio_seminario.jpeg")

_brasil_path = os.path.join(BASE_DIR, "imagens", "palestrantes", "cel_brasil.jpeg")
if os.path.exists(_brasil_path):
    img_brasil = b64("imagens/palestrantes/cel_brasil.jpeg")
    _brasil_img_tag = f'<img class="w-32 h-32 rounded-full object-cover border-4 border-primary mb-4" src="{img_brasil}" alt="Cel R1 Mario Brasil">'
    _brasil_modal_img = img_brasil
else:
    img_brasil = ""
    _brasil_img_tag = '<div class="w-32 h-32 rounded-full border-4 border-primary mb-4 bg-surface-container flex items-center justify-center"><span class="material-symbols-outlined text-5xl text-on-surface-variant">person</span></div>'
    _brasil_modal_img = ""

# ==========================================================================
# PARSER: TIMELINE DINÂMICA
# ==========================================================================
def parse_timeline(agenda_list):
    html = ""
    for idx, item in enumerate(agenda_list):
        if ":" not in item:
            continue
        time_part, details = item.split(":", 1)
        time_part = time_part.strip()
        details = details.strip()
        
        is_painel = "Painel" in details
        is_break = any(word in details.lower() for word in ["coffee break", "intervalo", "almoço"])
        
        # Estilos com base no tipo de evento
        if is_painel:
            bullet = '<div class="absolute -left-[29px] top-1 md:static w-3.5 h-3.5 md:w-4 md:h-4 rounded-full bg-primary ring-4 ring-primary-container/30 mt-1 shadow-[0_0_10px_rgba(85,107,79,0.8)] flex-shrink-0"></div>'
            content = f"""
            <div class="flex-grow pb-6 md:border-b md:border-outline-variant/20 group-last:border-0 bg-primary/5 p-4 rounded-lg -ml-4 md:ml-0">
                <span class="inline-block px-2.5 py-1 bg-primary/10 text-primary text-xs font-semibold rounded mb-2">Painel de Discussão</span>
                <h4 class="font-body-lg text-body-lg font-semibold text-on-surface leading-snug">{details}</h4>
            </div>
            """
        elif is_break:
            bullet = '<div class="absolute -left-[29px] top-1 md:static w-3.5 h-3.5 md:w-4 md:h-4 rounded-full border-2 border-tertiary bg-surface mt-1 flex-shrink-0"></div>'
            content = f"""
            <div class="flex-grow pb-6 md:border-b md:border-outline-variant/20 group-last:border-0 flex items-center gap-3 text-tertiary">
                <span class="material-symbols-outlined text-lg">local_cafe</span>
                <h4 class="font-body-md text-body-md font-semibold">{details}</h4>
            </div>
            """
        else:
            bullet = '<div class="absolute -left-[29px] top-1 md:static w-3.5 h-3.5 md:w-4 md:h-4 rounded-full bg-secondary ring-4 ring-secondary-container/30 mt-1 flex-shrink-0"></div>'
            content = f"""
            <div class="flex-grow pb-6 md:border-b md:border-outline-variant/20 group-last:border-0">
                <h4 class="font-body-lg text-body-lg font-semibold text-on-surface">{details}</h4>
            </div>
            """
            
        html += f"""
        <div class="relative flex flex-col md:flex-row md:items-start gap-4 md:gap-8 group">
            {bullet}
            <div class="md:w-32 flex-shrink-0 font-label-caps text-label-caps text-on-surface-variant pt-1">{time_part}</div>
            {content}
        </div>
        """
    return html

timeline_dia1 = parse_timeline(event_data["ANEXO A – Programação Geral do Seminário"]["01 JUL 26 (4ª feira)"])
timeline_dia2 = parse_timeline(event_data["ANEXO A – Programação Geral do Seminário"]["02 JUL 26 (5ª feira)"])

# ==========================================================================
# RENDERIZAÇÃO DO HTML COMPLETO
# ==========================================================================
html_body = f"""
    <!-- 1. BARRA DE NAVEGAÇÃO (template: barra fixa full-width) -->
    <nav class="bg-surface/90 backdrop-blur-xl font-body-md text-body-md fixed top-0 left-0 right-0 w-full z-50 border-b border-outline-variant/20 shadow-sm">
        <div class="max-w-container-max mx-auto h-20 px-gutter flex justify-between items-center">
            <div class="font-headline-md text-headline-md font-bold text-primary flex items-center min-w-0">
                <span class="hidden sm:inline truncate">Seminário de Inteligência</span>
            </div>
            <div class="hidden md:flex gap-6 items-center">
                <a class="text-on-surface-variant hover:text-primary transition-all duration-300 font-medium" href="#destaques">Destaques</a>
                <a class="text-on-surface-variant hover:text-primary transition-all duration-300 font-medium" href="#sobre">Sobre</a>
                <a class="text-on-surface-variant hover:text-primary transition-all duration-300 font-medium" href="#programacao">Agenda</a>
                <a class="text-on-surface-variant hover:text-primary transition-all duration-300 font-medium" href="#palestrantes">Palestrantes</a>
                <a class="text-on-surface-variant hover:text-primary transition-all duration-300 font-medium" href="#inscricoes">Inscrições</a>
            </div>
        </div>
    </nav>

    <!-- 2. HERO SECTION — slideshow com crossfade -->
    <section id="inicio" style="position:relative; width:100%; height:600px; min-height:480px; display:flex; align-items:flex-end; justify-content:center; overflow:hidden; margin-bottom:6rem;">
        <img src="{img_concepcao}" alt="" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover; object-position:center 35%; z-index:0; animation:heroSlide1 14s ease-in-out infinite;">
        <img src="{img_auditorio}" alt="" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover; object-position:center 30%; z-index:0; animation:heroSlide2 14s ease-in-out infinite; opacity:0;">
        <div style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; background:linear-gradient(to top, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0.38) 100%);"></div>
        <div style="position:relative; z-index:2; text-align:center; padding:0 2rem 3rem; max-width:56rem; width:100%;">
            <span style="display:inline-block; padding:0.25rem 0.75rem; background:rgba(255,255,255,0.2); color:#fff; font-size:0.75rem; font-weight:600; border-radius:9999px; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;">
                32º Aniversário da EsIMEx
            </span>
            <h1 style="font-size:clamp(2rem,5vw,4rem); font-weight:700; color:#fff; line-height:1.1; margin-bottom:1.5rem; text-shadow:0 2px 20px rgba(0,0,0,0.7);">
                {event_data["SEMINÁRIO DE INTELIGÊNCIA"]}
            </h1>
            <p style="font-size:1.1rem; color:rgba(255,255,255,0.82); max-width:38rem; margin:0 auto 2rem; line-height:1.6;">
                Painéis estratégicos, intercâmbio de inteligência e segurança cibernética aplicada à defesa nacional
            </p>
            <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem;">
                <a href="#programacao" style="background:#3e5338; color:#fff; padding:0.75rem 2rem; border-radius:0.75rem; font-weight:600; text-decoration:none; display:inline-block;">Ver Programação</a>
            </div>
        </div>
    </section>

    <main class="max-w-container-max mx-auto px-gutter mb-section-gap">
        
        <!-- 3. ÁREA DE DESTAQUES -->
        <section id="destaques" class="mb-section-gap">
            <h2 class="font-label-caps text-label-caps text-primary mb-2 uppercase tracking-widest text-center">Temas de Destaque</h2>
            <h3 class="font-headline-md text-headline-md font-bold text-on-surface mb-8 text-center">Objetivos do Seminário</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Tema 1 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">insights</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">Inteligência Estratégica</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Análise de cenários macro e assessoria de alto nível para tomada de decisão no nível político-militar.</p>
                    </div>
                </div>
                <!-- Tema 2 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">shield</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">Contrainteligência</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Salvaguarda de conhecimentos, dados, infraestruturas críticas e proteção contra espionagem e sabotagem.</p>
                    </div>
                </div>
                <!-- Tema 3 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">psychology</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">Defesa Cognitiva</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Mitigação de operações de influência, desinformação sistemática e campanhas de manipulação informacional.</p>
                    </div>
                </div>
                <!-- Tema 4 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">smart_toy</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">IA aplicada à Inteligência</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Algoritmos inteligentes de processamento de Big Data, análise de linguagem natural e modelos preditivos de defesa.</p>
                    </div>
                </div>
                <!-- Tema 5 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">public</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">Geointeligência</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Sensoriamento remoto e sistemas GIS mapeando ameaças com análises de imagens de alta resolução temporal e espacial.</p>
                    </div>
                </div>
                <!-- Tema 6 -->
                <div class="glass-panel p-6 rounded-xl hover-lift border border-outline-variant/20 bg-surface-container-low flex items-start gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-2xl">lock</span>
                    </div>
                    <div>
                        <h4 class="font-body-lg text-body-lg font-semibold text-on-surface mb-2">Segurança Informacional</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Protocolos e metodologias avançadas de confidencialidade aplicados nas comunicações integradas das Forças.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 4. SOBRE O EVENTO -->
        <section id="sobre" class="mb-section-gap grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-5 order-2 lg:order-1">
                <h2 class="font-label-caps text-label-caps text-primary mb-4 uppercase tracking-widest">Finalidade</h2>
                <h3 class="font-headline-xl text-headline-xl font-headline-xl-mobile text-headline-xl-mobile text-on-surface mb-6 leading-tight">
                    O Seminário de Inteligência
                </h3>
                <p class="font-body-lg text-body-lg text-on-surface-variant mb-6 leading-relaxed">
                    {event_data["a. Concepção"]}
                </p>
                <div class="w-16 h-1.5 bg-tertiary rounded-full mb-6"></div>
                <div class="p-6 rounded-xl bg-surface-container-low border border-outline-variant/30 glass-panel">
                    <h4 class="font-body-lg text-body-lg font-bold text-primary mb-2">Comemoração Institucional</h4>
                    <p class="font-body-md text-body-md text-on-surface-variant">O evento celebra o transcurso do 32º aniversário da Escola de Inteligência Militar do Exército (EsIMEx), referência nacional na formação especializada de analistas.</p>
                </div>
            </div>
            <div class="lg:col-span-7 order-1 lg:order-2 rounded-xl overflow-hidden soft-shadow h-[420px] border border-outline-variant/20">
                <img alt="Concepção do Seminário" class="w-full h-full object-cover transition-transform duration-700 hover:scale-105" src="{img_auditorio}">
            </div>
        </section>

        <!-- 5. OBJETIVOS -->
        <section class="mb-section-gap bg-surface-container-low rounded-2xl p-8 md:p-12 border border-outline-variant/30 glass-panel relative overflow-hidden soft-shadow">
            <div class="absolute inset-0 opacity-5 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-primary via-transparent to-transparent"></div>
            <div class="relative z-10">
                <h2 class="font-label-caps text-label-caps text-primary mb-6 uppercase tracking-widest text-center">Objetivos Estratégicos</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <!-- Card 1 -->
                    <div class="p-6 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover-lift flex flex-col justify-between">
                        <div>
                            <span class="material-symbols-outlined text-primary text-3xl mb-4">swap_horiz</span>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface mb-2">Intercâmbio Doutrinário</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Promover a troca de conhecimentos e melhores práticas doutrinárias em inteligência.</p>
                        </div>
                    </div>
                    <!-- Card 2 -->
                    <div class="p-6 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover-lift flex flex-col justify-between">
                        <div>
                            <span class="material-symbols-outlined text-primary text-3xl mb-4">military_tech</span>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface mb-2">32 Anos da EsIMEx</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Celebrar e enaltecer a história e a contribuição estratégica da Escola de Inteligência Militar.</p>
                        </div>
                    </div>
                    <!-- Card 3 -->
                    <div class="p-6 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover-lift flex flex-col justify-between">
                        <div>
                            <span class="material-symbols-outlined text-primary text-3xl mb-4">visibility</span>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface mb-2">Consciência Situacional</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Ampliar a percepção do Sistema de Inteligência do Exército (SIEx) sobre a conjuntura nacional.</p>
                        </div>
                    </div>
                    <!-- Card 4 -->
                    <div class="p-6 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover-lift flex flex-col justify-between">
                        <div>
                            <span class="material-symbols-outlined text-primary text-3xl mb-4">group</span>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface mb-2">Integração SISBIN</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Fortalecer os laços de integração institucional entre o Exército e os órgãos do SISBIN.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 6. PROGRAMAÇÃO COMPLETA -->
        <section id="programacao" class="mb-section-gap">
            <h2 class="font-label-caps text-label-caps text-primary mb-8 uppercase tracking-widest text-center">Agenda Detalhada</h2>
            <div class="bg-surface-container-lowest rounded-xl soft-shadow p-6 md:p-10 border border-outline-variant/20">
                
                <!-- Abas da Timeline -->
                <div class="flex gap-8 border-b border-outline-variant/30 mb-8">
                    <button class="tab-btn pb-4 font-body-lg text-body-lg font-bold text-primary border-b-2 border-primary transition-all duration-200" onclick="switchTab(this, 'dia1')">01 JUL 26</button>
                    <button class="tab-btn pb-4 font-body-lg text-body-lg font-semibold text-on-surface-variant hover:text-primary transition-colors border-b-2 border-transparent transition-all duration-200" onclick="switchTab(this, 'dia2')">02 JUL 26</button>
                </div>
                
                <!-- Corpo da Timeline -->
                <div class="relative pl-6 md:pl-0">
                    <!-- Linha Vertical (Mobile) -->
                    <div class="md:hidden absolute left-0 top-0 bottom-0 w-px bg-tertiary/30"></div>
                    
                    <div class="space-y-8">
                        <div id="dia1" class="tab-content relative space-y-8">
                            {timeline_dia1}
                        </div>
                        <div id="dia2" class="tab-content hidden relative space-y-8">
                            {timeline_dia2}
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 7. PALESTRANTES -->
        <section id="palestrantes" class="mb-section-gap">
            <h2 class="font-label-caps text-label-caps text-primary mb-2 uppercase tracking-widest text-center">Corpo Docente</h2>
            <h3 class="font-headline-md text-headline-md font-bold text-on-surface mb-8 text-center">Palestrantes Confirmados</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Palestrante 1 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    <img class="w-32 h-32 rounded-full object-cover border-4 border-primary mb-4" src="{img_mourao}" alt="Senador Gen Ex Mourão">
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Senador Hamilton Mourão</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">CCAI</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('mourao')">
                        Ver Biografia
                    </button>
                </div>
                
                <!-- Palestrante 2 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    {_anna_placeholder}
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Anna Cruz</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">Esint / ABIN</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('anna')">
                        Ver Biografia
                    </button>
                </div>
                
                <!-- Palestrante 3 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    <img class="w-32 h-32 rounded-full object-cover border-4 border-primary mb-4" src="{img_wellington}" alt="Prof. Dr. Wellington">
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Prof. Dr. Wellington</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">ESD</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('wellington')">
                        Ver Biografia
                    </button>
                </div>
                
                <!-- Palestrante 3b - Cel R1 Brasil -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    {_brasil_img_tag}
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Cel R1 Mario Brasil</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">ESD</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('brasil')">
                        Ver Biografia
                    </button>
                </div>

                <!-- Palestrante 4 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    <img class="w-32 h-32 rounded-full object-cover object-top border-4 border-primary mb-4" src="{img_mauricio}" alt="Maurício Viegas">
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Maurício Viegas</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">STF</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('mauricio')">
                        Ver Biografia
                    </button>
                </div>
                
                <!-- Palestrante 5 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    <img class="w-32 h-32 rounded-full object-cover border-4 border-primary mb-4" src="{img_heitor}" alt="TC R1 Heitor">
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">TC R1 Heitor</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">Pluvia Inteligência</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('heitor')">
                        Ver Biografia
                    </button>
                </div>
                
                <!-- Palestrante 6 -->
                <div class="glass-panel p-6 rounded-xl border border-outline-variant/20 bg-surface-container-low text-center flex flex-col items-center hover-lift">
                    <img class="w-32 h-32 rounded-full object-cover border-4 border-primary mb-4" src="{img_marcio}" alt="Márcio Lopes">
                    <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Márcio Lopes</h4>
                    <p class="font-label-caps text-label-caps text-tertiary mb-4">Imagem / ArcGIS</p>
                    <button class="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300" onclick="showBio('marcio')">
                        Ver Biografia
                    </button>
                </div>
            </div>
        </section>

        <!-- 8. INSCRIÇÕES -->
        <section id="inscricoes" class="mb-section-gap relative rounded-2xl overflow-hidden glass-panel bg-surface-container-low border border-outline-variant/30 p-8 md:p-12 soft-shadow">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <div class="lg:col-span-8">
                    <span class="inline-block px-3 py-1 bg-primary/10 text-primary text-xs font-semibold rounded-full uppercase tracking-widest mb-4">
                        Credenciamento
                    </span>
                    <h3 class="font-headline-xl text-headline-xl font-headline-xl-mobile text-headline-xl-mobile text-on-surface mb-4 font-bold">
                        Inscrições para o Evento
                    </h3>
                    <div class="space-y-4 font-body-lg text-body-lg text-on-surface-variant mb-8 max-w-3xl">
                        <p class="leading-relaxed">
                            A inscrição é obrigatória.
                        </p>
                    </div>
                    <a href="{LINK_INSCRICAO}" target="_blank" class="inline-block bg-primary text-on-primary px-8 py-4 rounded-xl font-bold hover:bg-primary-container transition-all duration-300 shadow-md">
                        Acessar Formulário de Inscrição
                    </a>
                </div>
                <div class="lg:col-span-4 flex flex-col items-center justify-center p-6 bg-white rounded-xl border border-outline-variant/20">
                    <img class="w-48 h-48 object-contain" src="{img_qrcode}" alt="QR Code de Inscrição">
                    <p class="mt-4 text-sm text-on-surface-variant text-center">Aponte a câmera para se inscrever</p>
                </div>
            </div>
        </section>

        <!-- 9. INFORMAÇÕES OPERACIONAIS (BENTO GRID) -->
        <section class="mb-section-gap">
            <h2 class="font-label-caps text-label-caps text-primary mb-8 uppercase tracking-widest text-center">Logística e Protocolos</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Data e Local -->
                <div class="md:col-span-2 glass-panel p-8 rounded-xl soft-shadow flex flex-col justify-center bg-surface-container-lowest border border-outline-variant/20">
                    <div class="flex items-start gap-4 mb-6">
                        <span class="material-symbols-outlined text-primary text-3xl">event</span>
                        <div>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Data do evento</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">01 de julho (14h às 18h) e 02 de julho (09h às 17h) de 2026</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-4 mb-6">
                        <span class="material-symbols-outlined text-primary text-3xl">location_on</span>
                        <div>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Local</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Auditório General Sydrião - Escola de Inteligência Militar do Exército (EsIMEx)</p>
                        </div>
                    </div>
                </div>
                <!-- Coffee Break e Debates -->
                <div class="glass-panel p-8 rounded-xl soft-shadow flex flex-col justify-between bg-surface-container-low border border-outline-variant/20">
                    <div class="mb-6">
                        <span class="material-symbols-outlined text-tertiary text-3xl mb-2">local_cafe</span>
                        <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Coffee break</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">Intervalos para interação e networking.</p>
                    </div>
                    <div>
                        <span class="material-symbols-outlined text-tertiary text-3xl mb-2">forum</span>
                        <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Debates Mediados</h4>
                        <p class="font-body-md text-body-md text-on-surface-variant">30 minutos ao final de cada bloco de painéis com mediação da Divisão de Ensino.</p>
                    </div>
                </div>
                <!-- Uniformes (Civis e Militares) -->
                <div class="md:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
                    <div class="p-6 rounded-xl border border-tertiary/20 bg-surface-bright flex items-center gap-4 shadow-sm">
                        <span class="material-symbols-outlined text-primary text-3xl">military_tech</span>
                        <div>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Militares</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">9° B2 (Exército) e similares para cada Força.</p>
                        </div>
                    </div>
                    <div class="p-6 rounded-xl border border-tertiary/20 bg-surface-bright flex items-center gap-4 shadow-sm">
                        <span class="material-symbols-outlined text-primary text-3xl">business_center</span>
                        <div>
                            <h4 class="font-body-lg text-body-lg font-bold text-on-surface">Civis</h4>
                            <p class="font-body-md text-body-md text-on-surface-variant">Traje Esporte fino ou equivalente institucional.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Strategic Highlights Ticker -->
    <div class="w-full bg-surface-container-high border-y border-outline-variant/30 py-4 overflow-hidden flex items-center mb-24 relative">
        <div class="absolute left-0 w-16 h-full bg-gradient-to-r from-surface-container-high to-transparent z-10"></div>
        <div class="absolute right-0 w-16 h-full bg-gradient-to-l from-surface-container-high to-transparent z-10"></div>
        <div class="flex whitespace-nowrap animate-scroll gap-12 text-tertiary font-label-caps text-label-caps uppercase tracking-widest items-center">
            <span>32 anos da EsIMEx</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Integração SISBIN</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Inteligência Artificial Aplicada</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Defesa Cognitiva</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Consciência Situacional</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <!-- Duplicado para loop contínuo -->
            <span>32 anos da EsIMEx</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Integração SISBIN</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Inteligência Artificial Aplicada</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Defesa Cognitiva</span>
            <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>Consciência Situacional</span>
        </div>
    </div>

    <!-- 11. FOOTER -->
    <footer class="bg-surface-container-highest text-on-surface font-body-md text-body-md w-full py-16 border-t border-outline-variant/30">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-gutter px-gutter max-w-container-max mx-auto">
            <div class="col-span-1 md:col-span-2">
                <div class="font-headline-md text-headline-md font-bold text-primary mb-4">
                    Seminário de Inteligência
                </div>
                <p class="text-on-surface-variant mb-4">
                    © 2026 EsIMEx - Escola de Inteligência Militar do Exército. Todos os direitos reservados.
                </p>
                <p class="text-xs text-on-surface-variant/70 leading-relaxed">
                    Este portal destina-se a fins estritamente informativos e de intercâmbio acadêmico-militar. Toda a comunicação do evento segue canais seguros.
                </p>
            </div>
            <div class="col-span-1 flex flex-col gap-3 mt-6 md:mt-0">
                <h5 class="font-bold text-primary text-sm uppercase tracking-wider mb-2">Contato e Apoio</h5>
                <span class="text-on-surface-variant text-sm">Divisão de Doutrina e Pesquisa / EsIMEx</span>
                <a class="text-on-surface-variant hover:text-tertiary transition-colors w-fit text-sm" href="mailto:ddp@esimex.eb.mil.br">ddp@esimex.eb.mil.br</a>
                <span class="text-on-surface-variant text-sm">Local: SMU - Brasília, DF</span>
            </div>
        </div>
    </footer>

    <!-- MODAL DE BIOGRAFIA DOS PALESTRANTES -->
    <div id="bio-modal" class="bio-modal" onclick="closeModal()">
        <div class="bio-modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closeModal()">&times;</span>
            <div class="flex flex-col md:flex-row gap-6 items-center md:items-start">
                <img id="modal-img" class="w-32 h-32 rounded-full object-cover border-4 border-primary flex-shrink-0" src="" alt="">
                <div>
                    <h3 id="modal-name" class="font-headline-md text-headline-md font-bold text-primary mb-1"></h3>
                    <p id="modal-role" class="font-label-caps text-label-caps text-tertiary mb-4 uppercase tracking-wider"></p>
                    <p id="modal-bio" class="font-body-md text-body-md text-on-surface-variant leading-relaxed"></p>
                </div>
            </div>
        </div>
    </div>

    <!-- SCRIPTS DE INTERATIVIDADE -->
    <script>
        // Dados de Biografia dos Palestrantes para evitar escape de aspas no HTML
        const speakersData = {{
            "mourao": {{
                "name": "Senador Gen Ex Mourão",
                "role": "Membro do CCAI / Senador da República",
                "bio": "General de Exército da Reserva, ex-Vice-Presidente da República e atualmente Senador da República. Possui extensa carreira militar com atuação na área estratégica e operacional. Exerce papel fundamental como membro da Comissão Mista de Controle das Atividades de Inteligência (CCAI).",
                "image": "{img_mourao}"
            }},
            "anna": {{
                "name": "Anna Cruz",
                "role": "Instrutora da Escola de Inteligência (Esint)",
                "bio": "Pesquisadora sênior da Escola de Inteligência (Esint) da ABIN. Doutora em Segurança e Defesa, com mais de 15 anos de atuação dedicados ao estudo de diretrizes doutrinárias de inteligência civil e estatal, bem como dilemas éticos na atividade.",
                "image": ""
            }},
            "wellington": {{
                "name": "Prof. Dr. Wellington",
                "role": "Pesquisador da Escola Superior de Defesa (ESD)",
                "bio": "Doutor em Ciências Políticas e analista sênior da Escola Superior de Defesa. Suas pesquisas enfocam psicologia social aplicada e Defesa Cognitiva, desenvolvendo contramedidas contra guerra híbrida e ações de desinformação estratégica.",
                "image": "{img_wellington}"
            }},
            "brasil": {{
                "name": "Cel R1 Mario Brasil do Nascimento",
                "role": "Diretor do Curso de Defesa e Geopolítica – ESD",
                "bio": "Diretor do Curso de Defesa e Geopolítica da Escola Superior de Defesa. Possui mais de 10 anos de experiência no Exército Brasileiro, com atuação em inteligência estratégica, gestão de projetos e avaliação de políticas públicas. Tem formação em relações internacionais, resolução de conflitos e ciências militares, dedicando-se ao desenvolvimento de lideranças e à inovação no setor de defesa.",
                "image": "{_brasil_modal_img}"
            }},
            "mauricio": {{
                "name": "Maurício Viegas",
                "role": "Assessor de Tecnologia do STF",
                "bio": "Bacharel em Direito e Engenharia de Computação, assessora o STF em temas cibernéticos. Referência em Direito Digital, coordena grupos de estudo voltados para o combate à desinformação estruturada e o amparo constitucional da verdade pública.",
                "image": "{img_mauricio}",
                "objectPos": "top"
            }},
            "heitor": {{
                "name": "TC R1 Heitor",
                "role": "Consultor Sênior - Pluvia Inteligência",
                "bio": "Tenente-Coronel da Reserva da Arma de Comunicações do Exército. Mestre em Computação Aplicada, lidera projetos de Inteligência Artificial e processamento inteligente de ameaças na Pluvia Inteligência, colaborando ativamente com o SIEx.",
                "image": "{img_heitor}"
            }},
            "marcio": {{
                "name": "Márcio Lopes",
                "role": "Diretor de Defesa - Imagem / ArcGIS",
                "bio": "Geógrafo com especialização em sensoriamento remoto de alta resolução. Atua como Diretor de Soluções de Defesa e Inteligência na Imagem, sendo especialista no emprego de soluções ArcGIS para consciência situacional de teatros de operações modernos.",
                "image": "{img_marcio}"
            }}
        }};

        // Função para alternar abas da Timeline
        function switchTab(btn, tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.getElementById(tabId).classList.remove('hidden');
            
            document.querySelectorAll('.tab-btn').forEach(b => {{
                b.classList.remove('border-primary', 'text-primary', 'font-bold');
                b.classList.add('border-transparent', 'text-on-surface-variant', 'font-semibold');
            }});
            
            btn.classList.add('border-primary', 'text-primary', 'font-bold');
            btn.classList.remove('border-transparent', 'text-on-surface-variant', 'font-semibold');
        }}

        // Funções do Modal de Palestrantes
        function showBio(speakerId) {{
            const data = speakersData[speakerId];
            if (data) {{
                document.getElementById('modal-name').innerText = data.name;
                document.getElementById('modal-role').innerText = data.role;
                document.getElementById('modal-bio').innerText = data.bio;
                const img = document.getElementById('modal-img');
                img.src = data.image;
                img.style.objectPosition = data.objectPos || 'center';
                document.getElementById('bio-modal').classList.add('active');
            }}
        }}

        function closeModal() {{
            document.getElementById('bio-modal').classList.remove('active');
        }}

        // Fechar modal ao pressionar ESC
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                closeModal();
            }}
        }});
    </script>
"""

# Monta documento HTML completo (iframe do Streamlit — sem indentação em markdown)
def build_full_page():
    head = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=Inter:wght@600&display=swap" />
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>{tailwind_config_js}</script>
{css_content}
<style>
html {{ scroll-behavior: smooth; scrollbar-width: none; -ms-overflow-style: none; }}
html::-webkit-scrollbar {{ display: none; }}
body {{ margin: 0; padding: 0; overflow-x: hidden; min-height: 100vh; }}
@keyframes heroSlide1 {{
    0%, 38%  {{ opacity: 1; }}
    48%, 90% {{ opacity: 0; }}
    100%     {{ opacity: 1; }}
}}
@keyframes heroSlide2 {{
    0%, 38%  {{ opacity: 0; }}
    48%, 90% {{ opacity: 1; }}
    100%     {{ opacity: 0; }}
}}
</style>
</head>
<body class="bg-background text-on-surface antialiased">
"""
    footer = """
<script>
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
        var id = this.getAttribute('href').slice(1);
        if (!id) return;
        var el = document.getElementById(id);
        if (el) {
            e.preventDefault();
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
</script>
</body>
</html>
"""
    body = textwrap.dedent(html_body).strip()
    return head + body + footer

# Renderização final
page_html = build_full_page()

st.markdown(streamlit_overrides, unsafe_allow_html=True)
st.components.v1.html(page_html, height=900, scrolling=True)
