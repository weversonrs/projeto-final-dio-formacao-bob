---
description: Gera um certificado fictício em Markdown com nome do usuário e trilha concluída
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

Liste cada badge de `badges_disponiveis` com emoji de medalha e uma linha descrevendo a competência que ela representa.

---

**Data de Emissão:** {data atual no formato DD/MM/AAAA}
**Código de Verificação:** `DIO-{ID_TRILHA}-{ANO}-{número aleatório de 6 dígitos}`

---

*Este certificado é fictício e foi gerado para fins educacionais pelo projeto DIO Explorer.*
*Verifique certificados reais em: https://web.dio.me*

---

Se nenhuma trilha for encontrada para o valor informado em $2, responda com:
> ❌ Trilha "$2" não encontrada. Verifique o nome da tecnologia ou da formação e tente novamente.
