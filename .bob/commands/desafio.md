---
description: Gera um desafio de código aleatório para uma tecnologia e nível escolhidos
argument-hint: <tecnologia> <nivel>
---

O usuário quer um desafio de código para a tecnologia **$1** no nível **$2**.

Regras de geração:
- **Nível Básico**: problemas simples de lógica, estruturas de dados elementares, funções básicas da linguagem, laços e condicionais.
- **Nível Intermediário**: problemas com orientação a objetos, manipulação de arquivos, consumo de APIs, estruturas de dados mais complexas.
- **Nível Avançado**: problemas de performance, concorrência, design patterns, arquitetura de sistemas ou integração de múltiplos componentes.
- Se **$2** não for informado ou estiver em branco, assuma o nível **Intermediário**.
- O desafio deve ser **100% original e diferente a cada execução** — varie o tema do domínio (e-commerce, fintech, saúde, jogos, logística, etc.).
- O enunciado deve usar linguagem clara e tom educativo, como em plataformas de coding challenge.

Gere o desafio em Markdown seguindo **exatamente** este modelo:

---

# 💻 Desafio de Código — $1

**Nível:** $2
**Tempo estimado:** {X} minutos
**XP ao concluir:** {XP} XP

---

## 📋 Descrição do Desafio

Descreva um problema prático e realista com contexto de negócio claro (ex: sistema de delivery, plataforma de streaming, app bancário). O enunciado deve ter no mínimo 3 linhas e deixar claro o que o programa deve fazer.

---

## 📥 Entrada Esperada

Descreva o formato exato da entrada que o programa deve receber (tipos, estrutura, exemplos de valores válidos).

## 📤 Saída Esperada

Descreva o formato exato da saída que o programa deve produzir.

---

## 💡 Exemplo

Mostre pelo menos um par de entrada/saída concreto em bloco de código.

```
Entrada:
{exemplo de entrada}

Saída:
{exemplo de saída}
```

---

## 🔒 Restrições

Liste de 2 a 4 restrições técnicas do desafio (ex: não usar biblioteca X, limite de complexidade, tamanho da entrada).

---

## 🏆 Critérios de Avaliação

Liste de 3 a 5 critérios que serão avaliados na solução (ex: clareza do código, tratamento de erros, cobertura de casos extremos, performance).

---

## 💬 Dica

Forneça uma dica sutil que oriente o raciocínio do aluno sem entregar a solução.

---
