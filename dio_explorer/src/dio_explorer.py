"""
DIO Explorer — Módulo principal com as funções dos slash commands.
Testável de forma unitária independente do Bob.
"""

import json
import os
import random
import re
from datetime import date


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "trilhas_dio.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_trilhas() -> list:
    """Carrega a lista de trilhas do arquivo JSON."""
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)["trilhas"]


def _buscar_trilha(tecnologia: str) -> dict | None:
    """Retorna a trilha cujo campo 'tecnologia' bate com o argumento (case-insensitive)."""
    termo = tecnologia.strip().lower()
    for trilha in _load_trilhas():
        if termo in trilha["tecnologia"].lower() or trilha["tecnologia"].lower() in termo:
            return trilha
    return None


def _vitalicio_label(valor: bool) -> str:
    return "Sim" if valor else "Não"


# ---------------------------------------------------------------------------
# /trilha
# ---------------------------------------------------------------------------

def cmd_trilha(tecnologia: str) -> str:
    """Gera o plano de estudos para uma tecnologia."""
    trilha = _buscar_trilha(tecnologia)

    if trilha is None:
        return f'❌ Nenhuma trilha encontrada para "{tecnologia}". Verifique o nome da tecnologia e tente novamente.'

    linhas = [
        f"# 📚 Plano de Estudos — {trilha['nome']}",
        "",
        f"**Tecnologia:** {trilha['tecnologia']}",
        f"**Nível:** {trilha['nivel']}",
        f"**XP Total:** {trilha['xp_total']} XP",
        f"**Acesso Vitalício:** {_vitalicio_label(trilha['vitalicio'])}",
        f"**Lives ao Vivo:** {trilha['lives_ao_vivo']}",
        "",
        "---",
        "",
        "## 🗂️ Módulos da Trilha",
        "",
    ]

    for i in range(1, trilha["numero_modulo"] + 1):
        linhas.append(f"{i}. Módulo {i} — Conteúdo programático do módulo {i} da trilha {trilha['tecnologia']}.")

    linhas += ["", "---", "", "## 🏅 Badges Disponíveis", ""]
    for badge in trilha["badges_disponiveis"]:
        linhas.append(f"- 🥇 **{badge}**")

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# /desafio
# ---------------------------------------------------------------------------

_TEMAS = [
    "sistema de biblioteca", "API de e-commerce", "jogo da memória",
    "gerenciador de tarefas", "sistema bancário", "analisador de logs",
    "agenda de contatos", "conversor de moedas", "buscador de CEP",
]

def cmd_desafio(tecnologia: str, nivel: str = "Intermediário") -> str:
    """Gera um desafio de código para a tecnologia e nível informados."""
    nivel = nivel.strip() or "Intermediário"
    tema = random.choice(_TEMAS)
    xp = {"Básico": 300, "Intermediário": 600, "Avançado": 1000}.get(nivel, 600)
    tempo = {"Básico": 30, "Intermediário": 60, "Avançado": 120}.get(nivel, 60)

    return "\n".join([
        f"# 💻 Desafio de Código — {tecnologia}",
        "",
        f"**Nível:** {nivel}",
        f"**Tempo estimado:** {tempo} minutos",
        f"**XP ao concluir:** {xp} XP",
        "",
        "---",
        "",
        f"## 📋 Descrição do Desafio",
        "",
        f"Implemente um {tema} usando {tecnologia}. O sistema deve contemplar as operações básicas de CRUD.",
        "",
        "## 📥 Entrada Esperada",
        "Comandos via linha de comando ou chamadas de função com os dados necessários.",
        "",
        "## 📤 Saída Esperada",
        "Resultados formatados em texto ou JSON conforme o comando executado.",
    ])


# ---------------------------------------------------------------------------
# /certificado
# ---------------------------------------------------------------------------

def cmd_certificado(nome_usuario: str, tecnologia: str) -> str:
    """Gera um certificado fictício em Markdown."""
    trilha = _buscar_trilha(tecnologia)

    if trilha is None:
        return f'❌ Trilha "{tecnologia}" não encontrada. Verifique o nome da tecnologia ou da formação e tente novamente.'

    hoje = date.today().strftime("%d/%m/%Y")
    codigo = f"DIO-{trilha['id']:02d}-{date.today().year}-{random.randint(100000, 999999)}"

    linhas = [
        "# 🎓 Certificação DIO",
        "",
        "---",
        "",
        f"Atestamos que o **{nome_usuario}** completou com sucesso a formação na **{trilha['nome']}**.",
        "",
        f"**Data de Emissão:** {hoje}",
        f"**Código de Verificação:** `{codigo}`",
        "",
        "---",
        "",
        "## 📋 Informações da Trilha",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| **Tecnologia** | {trilha['tecnologia']} |",
        f"| **Nível** | {trilha['nivel']} |",
        f"| **Módulos Concluídos** | {trilha['numero_modulo']} módulos |",
        f"| **XP Conquistado** | {trilha['xp_total']} XP |",
        f"| **Lives Assistidas** | {trilha['lives_ao_vivo']} lives |",
        f"| **Acesso Vitalício** | {_vitalicio_label(trilha['vitalicio'])} |",
        "",
        "---",
        "",
        "## 🏅 Badges Conquistadas",
        "",
    ]

    for badge in trilha["badges_disponiveis"]:
        linhas.append(f"- 🥇 **{badge}**")

    linhas += [
        "",
        "---",
        "",
        "*Este certificado é fictício e foi gerado para fins educacionais pelo projeto DIO Explorer.*",
        "*Verifique certificados reais em: https://web.dio.me*",
    ]

    return "\n".join(linhas)
