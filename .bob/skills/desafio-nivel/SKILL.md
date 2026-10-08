---
name: desafio-nivel
description: Gera um desafio de código personalizado para uma tecnologia e nível (Iniciante, Intermediário ou Avançado)
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <tecnologia> <nivel>
---

O usuário quer um desafio de código para a tecnologia **$1** no nível **$2**.

Normalize o nível informado:
- Qualquer variação de "iniciante", "basico", "básico", "beginner" → **Iniciante**
- Qualquer variação de "intermediario", "intermediário", "intermediate" → **Intermediário**
- Qualquer variação de "avancado", "avançado", "advanced" → **Avançado**
- Se vazio ou não reconhecido → **Intermediário**

Parâmetros por nível:
| Nível | Tempo | XP |
|---|---|---|
| Iniciante | 30 min | 300 XP |
| Intermediário | 60 min | 600 XP |
| Avançado | 120 min | 1000 XP |

Perfil de cada nível:
- **Iniciante**: lógica simples, variáveis, condicionais, laços e funções básicas. Sem bibliotecas externas.
- **Intermediário**: orientação a objetos, coleções, APIs REST, arquivos ou estruturas de dados intermediárias.
- **Avançado**: concorrência, design patterns, arquitetura, otimização de algoritmos ou integração de múltiplos componentes.

Gere um desafio 100% original, variando o domínio de negócio a cada execução (e-commerce, fintech, saúde, logística, jogos, educação, etc.), seguindo **exatamente** este modelo em Markdown:

---

# 💻 Desafio de Código — {tecnologia}

**Nível:** {nivel normalizado}
**Tempo estimado:** {X} minutos
**XP ao concluir:** {XP} XP

---

## 📋 Descrição do Desafio

Descreva um problema prático com contexto de negócio claro (mínimo 4 linhas), detalhando o que o programa deve fazer e por que esse problema existe no contexto escolhido.

---

## 📥 Entrada Esperada

Descreva o formato exato da entrada (tipos, estrutura, exemplos e limites).

## 📤 Saída Esperada

Descreva o formato exato da saída, incluindo formatação e casos de borda.

---

## 💡 Exemplo

Mostre pelo menos dois pares de entrada/saída — um caso comum e um caso de borda.

```
Entrada 1:
{exemplo normal}

Saída 1:
{saída esperada}

Entrada 2 (caso de borda):
{exemplo limite}

Saída 2:
{saída para o caso de borda}
```

---

## 🔒 Restrições

Liste de 3 a 5 restrições técnicas do desafio.

---

## 🏆 Critérios de Avaliação

Liste de 4 a 6 critérios avaliados na solução, incluindo clareza, cobertura de casos de borda, tratamento de erros, performance e uso adequado dos recursos da linguagem.

---

## 💬 Dica

Forneça uma dica sutil específica para {tecnologia} e para o nível {nivel}, sem entregar a solução.

---

## 🚀 Bônus (opcional)

Sugira uma extensão do desafio para quem quiser ir além.

---
