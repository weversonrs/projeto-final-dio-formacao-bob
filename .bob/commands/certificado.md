---
description: Gera um certificado fictício em Markdown com o nome do usuário e a trilha concluída
argument-hint: <seu-nome> <trilha>
---

O usuário quer gerar um certificado fictício para o nome **$1** na trilha **$2**.

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize o objeto dentro do array `trilhas` cuja propriedade `tecnologia` ou `nome` corresponda (de forma aproximada, ignorando maiúsculas/minúsculas) ao valor informado em **$2**.

Com os dados encontrados, gere o certificado em Markdown substituindo cada `{campo}` pelo valor real do JSON:

---

# 🎓 Certificado de Conclusão

---

> *A plataforma **DIO — Digital Innovation One** certifica que*

## $1

*concluiu com êxito a trilha de formação:*

# 🏆 {nome}

---

| | |
|---|---|
| **Tecnologia** | {tecnologia} |
| **Nível** | {nivel} |
| **Módulos Concluídos** | {numero_modulo} |
| **XP Conquistado** | {xp_total} XP |
| **Lives Assistidas** | {lives_ao_vivo} |
| **Acesso Vitalício** | {Sim se vitalicio=true, Não se vitalicio=false} |

---

## 🏅 Badges Conquistadas

Para cada item do array `badges_disponiveis`, gere uma linha no formato:
`- 🥇 **{nome do badge}**`

---

**Data de Emissão:** {data atual no formato DD/MM/AAAA}
**Código de Verificação:** `DIO-{id com dois dígitos, ex: 01}-{ano atual}-{número aleatório de 6 dígitos}`

---

*Este certificado é fictício e foi gerado para fins educacionais pelo projeto DIO Explorer.*
*Verifique certificados reais em: https://web.dio.me*

---

Se nenhuma trilha for encontrada para **$2**, responda com:
> ❌ Trilha "$2" não encontrada. Verifique o nome da tecnologia ou da formação e tente novamente.
>
> Trilhas disponíveis: Python, Java, JavaScript, React, Angular, Node.js, AWS, Microsoft Azure, Google Cloud, Machine Learning, Data Science, Data Engineering, DevOps, Containers, TypeScript, Vue.js, Flutter, Android, iOS, C#, PHP, Segurança da Informação, SQL, MongoDB, IA Generativa, Prompt Engineering, Unity, Blockchain, Quality Assurance, IBM watsonx, Kotlin, Go, Power BI, Linux, Rust, NestJS, Next.js, Spring Boot, RPA, Cloud Native.
