---
description: Retorna um plano de estudos formatado para uma tecnologia da DIO
argument-hint: <tecnologia>
---

O usuário quer consultar a trilha de estudos da tecnologia: **$1**

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja `tecnologia` corresponda (de forma aproximada, ignorando maiúsculas/minúsculas) ao valor informado.

Com os dados encontrados, gere um plano de estudos formatado em Markdown seguindo exatamente este modelo:

---

# 📚 Plano de Estudos — {nome}

**Tecnologia:** {tecnologia}
**Nível:** {nivel}
**XP Total:** {xp_total} XP
**Acesso Vitalício:** {Sim ou Não}
**Lives ao Vivo:** {lives_ao_vivo}

---

## 🗂️ Módulos da Trilha

Liste {numero_modulo} módulos fictícios e coerentes com a tecnologia, numerados de 1 até {numero_modulo}, com título e uma breve descrição de cada módulo (1 linha).

---

## 🏅 Badges Disponíveis

Liste cada badge de `badges_disponiveis` como um item com emoji de medalha.

---

## 🚀 Próximos Passos

Sugira 3 dicas práticas para o aluno avançar nessa trilha após concluí-la.

---

Se nenhuma trilha for encontrada para a tecnologia informada, responda com:
> ❌ Nenhuma trilha encontrada para "$1". Verifique o nome da tecnologia e tente novamente.
