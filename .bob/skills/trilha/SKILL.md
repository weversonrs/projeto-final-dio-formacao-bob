---
name: trilha
description: Retorna um plano de estudos formatado para uma tecnologia da DIO
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <tecnologia>
---

O usuário quer consultar a trilha de estudos para a tecnologia: **$1**

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize o objeto dentro do array `trilhas` cuja propriedade `tecnologia` corresponda (de forma aproximada, ignorando maiúsculas/minúsculas) ao valor informado em **$1**. Tente também comparar com a propriedade `nome` caso a correspondência por `tecnologia` não seja encontrada.

Com os dados encontrados, gere a resposta em Markdown seguindo **exatamente** este modelo — substitua cada `{campo}` pelo valor real do JSON:

---

# 📚 Plano de Estudos — {nome}

**Tecnologia:** {tecnologia}
**Nível:** {nivel}
**XP Total:** {xp_total} XP
**Acesso Vitalício:** {Sim se vitalicio=true, Não se vitalicio=false}
**Lives ao Vivo:** {lives_ao_vivo}

---

## 🗂️ Módulos da Trilha

Gere exatamente {numero_modulo} módulos numerados de 1 até {numero_modulo}. Cada módulo deve ter um **título coerente com a tecnologia** e uma breve descrição de uma linha. Os títulos devem representar uma progressão lógica de aprendizado (fundamentos → intermediário → avançado).

Exemplo de formato:
1. **Introdução à {tecnologia}** — Conceitos fundamentais e configuração do ambiente.
2. **{Tópico 2}** — Descrição breve.
...

---

## 🏅 Badges Disponíveis

Liste cada badge presente no array `badges_disponiveis` como um item com emoji de medalha 🏅.

---

## 🚀 Próximos Passos

Sugira 3 dicas práticas e específicas para o aluno continuar evoluindo após concluir essa trilha.

---

Se nenhuma trilha for encontrada para **$1**, responda com:
> ❌ Nenhuma trilha encontrada para "$1". Verifique o nome da tecnologia e tente novamente.
>
> Tecnologias disponíveis: Python, Java, JavaScript, React, Angular, Node.js, AWS, Microsoft Azure, Google Cloud, Machine Learning, Data Science, Data Engineering, DevOps, Containers, TypeScript, Vue.js, Flutter, Android, iOS, C#, PHP, Segurança da Informação, SQL, MongoDB, IA Generativa, Prompt Engineering, Unity, Blockchain, Quality Assurance, IBM watsonx, Kotlin, Go, Power BI, Linux, Rust, NestJS, Next.js, Spring Boot, RPA, Cloud Native.
