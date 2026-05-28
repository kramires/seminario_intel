# Contexto do projeto — Seminário de Inteligência (EsIMEx)

Documento para continuidade em outra sessão de IA ou por outro desenvolvedor.

---

## Objetivo

Landing page institucional do **Seminário de Inteligência** (32º aniversário da EsIMEx), convertida de um template HTML (design Stitch/Material) para **Streamlit**, mantendo visual premium (Tailwind, glassmorphism, paleta verde militar `#3e5338` / fundo `#fcf9f2`).

Referência visual: `imagens/design_seminario.png`

---

## Como rodar

```bash
cd /Users/kramires/Desktop/seminario_inteligencia
source .venv/bin/activate
streamlit run app.py
```

Abrir: **http://localhost:8501**

Se a porta estiver ocupada ou `ERR_CONNECTION_REFUSED`, matar processos e subir de novo:

```bash
lsof -ti :8501 | xargs kill -9 2>/dev/null
streamlit run app.py
```

---

## Estrutura do repositório

| Caminho | Função |
|---------|--------|
| `app.py` | App Streamlit: monta HTML, gera `static/seminario.html`, renderiza via `st.iframe()` |
| `extrato_os.json` | Dados do evento (título, concepção, agenda por dia) |
| `assets/` | CSS, Tailwind config, imagens geradas (palestrantes, galeria, qrcode antigo) |
| `imagens/` | **Assets institucionais reais** (prioridade na sincronização) |
| `static/seminario.html` | HTML gerado automaticamente (não editar manualmente; regenera ao rodar app) |
| `static/assets/` | Cópia servida em `/app/static/assets/*` |
| `.streamlit/config.toml` | Tema claro, `enableStaticServing = true` |

### `imagens/` (fonte de verdade para branding)

- `esimex_noturna.jpg` — **hero** (foto aérea noturna da EsIMEx com bandeira)
- `simbolo_esimex1.png` — logo navbar esquerda
- `simbolo_cie.png` — logo navbar direita
- `qrcode.png` — QR do formulário Survey123
- `banner.jpeg` — seção “Sobre” (lado direito)
- `design_seminario.png` — mockup do template alvo

---

## Arquitetura de renderização (importante)

### Por que não é `st.markdown(html)` puro?

1. HTML indentado em `st.markdown` virava **bloco de código** (Markdown interpreta 4 espaços como `<pre>`).
2. HTML com imagens em **base64 (~17 MB)** quebrava altura do iframe e performance.

### Solução atual

1. `sync_static_assets()` copia `assets/` + `imagens/` → `static/assets/`.
2. `build_full_page()` monta documento HTML completo com Tailwind CDN + `assets/tailwind.config.js` + `assets/style.css`.
3. `ensure_static_page()` grava `static/seminario.html` se `app.py` ou assets mudaram.
4. Streamlit pai: `st.markdown(streamlit_overrides)` esconde chrome do Streamlit.
5. Conteúdo: `st.iframe("/app/static/seminario.html", height="content", width="stretch")`.

URLs de imagens no HTML: `/app/static/assets/{arquivo}` via `static_asset_url()`.

---

## O que já foi implementado

- [x] Conversão do template para Streamlit
- [x] Timeline dinâmica a partir de `extrato_os.json`
- [x] 6 palestrantes + modal de biografia (JS)
- [x] Abas da agenda (01/02 JUL 26)
- [x] Galeria (4 imagens em `assets/gallery_*.png`)
- [x] Seções extras mantidas: destaques, objetivos, logística, ticker, footer
- [x] Link de inscrição: `https://survey123.arcgis.com/share/cee3256c9e044b688c79aa28ff2aab1f`
- [x] Símbolos locais na navbar (não mais URLs Google)
- [x] Botão **“Inscreva-se” removido do menu** (só link “Inscrições” + seção completa em `#inscricoes`)
- [x] Hero com `hero-backdrop` (CSS background) + `<img>` + overlay em `assets/style.css`

---

## Problemas em aberto (prioridade)

### 1. Hero: `esimex_noturna.jpg` NÃO aparece no navegador

**Sintoma:** área do hero fica branca/creme (`#fcf9f2`); navbar com logos funciona; demais seções carregam.

**O que já foi tentado:**

- Trocar URL externa por `/app/static/assets/esimex_noturna.jpg`
- `background-image` em `.hero-backdrop` no CSS
- Tag `<img>` com `loading="eager"`
- Ajuste de gradiente (`.hero-overlay`) para não cobrir 100% da foto
- `curl http://127.0.0.1:8501/app/static/assets/esimex_noturna.jpg` retorna **HTTP 200** (arquivo existe no servidor)

**Hipóteses para investigar:**

1. **Iframe `st.iframe` + altura `content`**: medição de altura falha; hero colapsa visualmente.
2. **Caminho no iframe**: testar URL relativa `assets/esimex_noturna.jpg` (base = `/app/static/seminario.html`).
3. **Embed base64 só do hero** (~460 KB) como fallback dentro do HTML gerado.
4. **Servir hero fora do iframe**: `st.image` ou bloco HTML só do hero no documento pai Streamlit.
5. **DevTools → Network**: ver se `esimex_noturna.jpg` retorna 404/403 dentro do iframe.
6. **Regenerar HTML**: apagar `static/seminario.html` e rodar `streamlit run app.py` + hard refresh (`Cmd+Shift+R`).

**Trecho atual do hero** (`app.py` ~linha 180):

```html
<header id="inicio" class="hero-section ...">
  <div class="hero-backdrop absolute inset-0 z-0" ...></div>
  <img class="hero-bg-img ..." src="/app/static/assets/esimex_noturna.jpg">
  <div class="hero-overlay absolute inset-0 z-[1]"></div>
  ...
</header>
```

**CSS** (`assets/style.css`):

```css
.hero-section .hero-backdrop {
  background-image: url("/app/static/assets/esimex_noturna.jpg");
  ...
}
```

### 2. Card do QR Code — simplificar (pedido do usuário)

**Pedido:** no card do QR, **somente** a imagem `imagens/qrcode.png` e a legenda abaixo:

> Aponte a câmera para se inscrever

**Estado atual** (`app.py` seção `#inscricoes`): card com `p-6 bg-white shadow-inner` + img 48x48 + span — mas a seção inteira ainda tem texto longo, botão e grid 8+4 colunas à esquerda. O usuário quer o **card lateral** minimalista (só QR + legenda), não remover a seção de inscrições.

**Alteração sugerida** no bloco `lg:col-span-4`:

```html
<div class="lg:col-span-4 flex flex-col items-center justify-center p-6 bg-white rounded-xl border border-outline-variant/20">
  <img src="{img_qrcode}" alt="QR Code inscrição" class="w-48 h-48 object-contain">
  <p class="mt-4 text-sm text-on-surface-variant text-center">Aponte a câmera para se inscrever</p>
</div>
```

Remover `shadow-inner` e classes extras se quiser card mais limpo. Garantir `img_qrcode` = `static_asset_url("qrcode.png")` após sync de `imagens/qrcode.png`.

### 3. Alinhar mais ao template (`design_seminario.png`)

- Hero: foto noturna full-width, título verde sobre gradiente inferior
- Navbar: logos nas pontas, links centrais, **sem** CTA “Inscreva-se”
- Paleta Material (já em `assets/tailwind.config.js`)
- Tipografia: Hanken Grotesk + Inter (label caps)

---

## Configurações fixas

```python
LINK_INSCRICAO = "https://survey123.arcgis.com/share/cee3256c9e044b688c79aa28ff2aab1f"
```

Palestrantes (paths em `assets/`): `mourao.png`, `anna.png`, `wellington.png`, `mauricio.png`, `heitor.png`, `marcio.png`

---

## Avisos do console (podem ignorar em dev)

- `Unrecognized feature: 'ambient-light-sensor'` etc. → scripts internos do **Streamlit** (`isLength.*.js`), não do app.
- `cdn.tailwindcss.com should not be used in production` → informativo; para produção considerar Tailwind build estático.
- `iframe sandbox allow-scripts allow-same-origin` → comportamento do `st.iframe`.

---

## Fluxo ao editar

1. Alterar `app.py` e/ou `assets/style.css`
2. Rodar `streamlit run app.py` (regenera `static/seminario.html` se mtime dos sources > HTML)
3. Ou: `rm static/seminario.html && streamlit run app.py`
4. Hard refresh no browser

**Não commitar** `static/seminario.html` se for gerado (opcional: adicionar ao `.gitignore`).

---

## Checklist para a próxima IA

- [ ] Corrigir exibição de `imagens/esimex_noturna.jpg` no hero (bloqueador principal)
- [ ] Simplificar card QR: só imagem + legenda “Aponte a câmera para se inscrever”
- [ ] Validar QR aponta para Survey123 (imagem `imagens/qrcode.png` já é desse link)
- [ ] Comparar resultado com `imagens/design_seminario.png`
- [ ] Testar mobile (473px) e desktop
- [ ] Não remover seções extras já aprovadas pelo usuário (destaques, galeria, palestrantes, etc.)

---

## Comandos úteis

```bash
# Verificar assets sincronizados
ls -la static/assets/esimex_noturna.jpg static/assets/qrcode.png

# Testar URL da imagem
curl -I http://127.0.0.1:8501/app/static/assets/esimex_noturna.jpg

# Regenerar HTML sem Streamlit UI
rm -f static/seminario.html && python app.py
```

---

## Histórico resumido da conversa

1. Usuário pediu rodar `app.py` → site mostrava **código HTML** em vez da página.
2. Causa: `st.markdown` + indentação; fix: `st.iframe` + HTML document completo.
3. HTML 17 MB (base64) → iframe minúsculo; fix: URLs estáticas `/app/static/assets/`.
4. `ERR_CONNECTION_REFUSED` → Streamlit não estava rodando.
5. Alinhar ao template: imagens locais `imagens/`, remover botão menu Inscreva-se, link Survey123.
6. Hero ainda em branco; QR card deve ser minimalista — **pendente**.

---

*Última atualização: 27/05/2026 — workspace `seminario_inteligencia`*
