---
name: certificado
description: >-
  Gera um certificado fictício em Markdown com nome do usuário e trilha
  concluída
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <seu-nome> <trilha>
---

O usuário quer gerar um certificado fictício para o nome **$1** na trilha **$2**.

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja `tecnologia` ou `nome` corresponda (de forma aproximada, ignorando maiúsculas/minúsculas) ao valor informado em $2.

Gere o certificado em Markdown seguindo exatamente este modelo:

---

# 🎓 Certificado de Conclusão

---

> *A plataforma **DIO — Digital Innovation One** certifica que*

## $1

*concluiu com êxito a trilha de formação:*

# 🏆 {nome da trilha}

---

| | |
|---|---|
| **Tecnologia** | {tecnologia} |
| **Nível** | {nivel} |
| **Módulos Concluídos** | {numero_modulo} |
| **XP Conquistado** | {xp_total} XP |
| **Lives Assistidas** | {lives_ao_vivo} |
| **Acesso Vitalício** | {Sim ou Não} |

---

## 🏅 Badges Conquistadas

Para cada item do array `badges_disponiveis`, gere uma linha no formato:
`- 🥇 **{nome do badge}**`

---

**Data de Emissão:** {data atual no formato DD/MM/AAAA}
**Código de Verificação:** `DIO-{ID_TRILHA com zero à esquerda, ex: 01}-{ANO}-{número aleatório de 6 dígitos}`

---

*Este certificado é fictício e foi gerado para fins educacionais pelo projeto DIO Explorer.*
*Verifique certificados reais em: https://web.dio.me*

---

Se nenhuma trilha for encontrada para o valor informado em $2, responda com:
> ❌ Trilha "$2" não encontrada. Verifique o nome da tecnologia ou da formação e tente novamente.
