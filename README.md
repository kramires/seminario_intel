# Seminário de Inteligência — EsIMEx

Portal web do **Seminário de Inteligência** da Escola de Inteligência Militar do Exército (EsIMEx), realizado nos dias **01 e 02 de julho de 2026** em comemoração ao 32º aniversário da instituição.

---

## Sobre o Projeto

Aplicação web desenvolvida com **Streamlit** que gera uma página HTML completa e interativa para divulgação do evento. O HTML é gerado dinamicamente a partir de um arquivo JSON de configuração, sem dependência de banco de dados.

---

## Estrutura do Projeto

```
seminario_inteligencia/
├── app.py                  # Aplicação principal (Streamlit)
├── extrato_os.json         # Fonte de dados: agenda, textos e configurações
├── requirements.txt        # Dependências Python
│
├── assets/                 # CSS, JS e imagens auxiliares
│   ├── style.css
│   ├── streamlit-overrides.css
│   ├── tailwind.config.js
│   └── *.png               # Imagens de galeria e ícones
│
├── imagens/                # Imagens gerais do evento
│   ├── esimex_noturna.jpg
│   ├── banner.jpeg
│   ├── auditorio_seminario.jpeg
│   ├── qrcode.png
│   ├── simbolo_esimex1.png
│   ├── simbolo_cie.png
│   └── palestrantes/       # Fotos dos palestrantes
│       ├── genMourao.jpeg
│       ├── profWellington.jpeg
│       ├── mauriciuViegas.jpeg
│       ├── marcioLopes.jpeg
│       ├── Tc R1 Heitor.jpeg
│       └── cel_brasil.jpeg  # Inserir quando disponível
│
└── static/                 # Arquivos servidos pelo Streamlit (/app/static/)
    └── assets/             # Gerado automaticamente pelo app (não editar)
```

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- pip

### Instalação

```bash
pip install -r requirements.txt
```

### Iniciar o servidor

```bash
streamlit run app.py
```

Acesse em: **http://localhost:8501**

---

## Configuração do Evento

Toda a agenda e os textos do evento são controlados pelo arquivo `extrato_os.json`. Para atualizar datas, horários, palestrantes ou textos da programação, edite esse arquivo — o app recarrega automaticamente.

### Estrutura do JSON

```json
{
  "SEMINÁRIO DE INTELIGÊNCIA": "título do evento",
  "a. Concepção": "texto da seção Sobre",
  "ANEXO A – Programação Geral do Seminário": {
    "01 JUL 26 (4ª feira)": ["HHh-HHh: descrição da atividade."],
    "02 JUL 26 (5ª feira)": ["HHh-HHh: descrição da atividade."]
  }
}
```

Atividades com "Painel" no texto recebem destaque visual automático. Atividades com "INTERVALO" ou "ALMOÇO" recebem o estilo de pausa.

---

## Palestrantes

Para adicionar ou atualizar a foto de um palestrante:

1. Salve a imagem em `imagens/palestrantes/` (formato `.jpeg` ou `.png`)
2. No `app.py`, carregue a imagem com `b64("imagens/palestrantes/nome_arquivo.jpeg")`
3. Referencie nos blocos do card e no `speakersData` do JavaScript

> **Foto pendente:** Cel R1 Mario Brasil do Nascimento — salvar como `imagens/palestrantes/cel_brasil.jpeg`

---

## Link de Inscrição e Transmissão

No topo do `app.py`, altere as variáveis:

```python
LINK_INSCRICAO  = "https://..."   # formulário de inscrição
LINK_TRANSMISSAO = "https://..."  # link ao vivo (deixar vazio para ocultar)
```

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| [Streamlit](https://streamlit.io) | Servidor web e renderização |
| [Tailwind CSS](https://tailwindcss.com) | Estilização via CDN |
| [Material Symbols](https://fonts.google.com/icons) | Ícones |
| [Hanken Grotesk / Inter](https://fonts.google.com) | Tipografia |

---

## Organização

**Escola de Inteligência Militar do Exército (EsIMEx)**  
Centro de Inteligência do Exército (CIE) — SMU, Brasília – DF  
contato: `comsoc@esimex.eb.mil.br`
