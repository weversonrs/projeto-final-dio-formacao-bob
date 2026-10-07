---
description: Gera um desafio de código aleatório baseado em uma tecnologia e nível
argument-hint: <tecnologia> <nivel>
---

O usuário quer um desafio de código para a tecnologia **$1** no nível **$2**.

Gere um desafio de código fictício, criativo e educativo seguindo exatamente este modelo em Markdown:

---

# 💻 Desafio de Código — {tecnologia}

**Nível:** {nivel}
**Tempo estimado:** {X} minutos
**XP ao concluir:** {XP} XP

---

## 📋 Descrição do Desafio

Descreva um problema prático e coerente com a tecnologia e nível informados. O enunciado deve ser claro, com contexto realista (ex: sistema de e-commerce, API de banco, jogo, etc.).

---

## 📥 Entrada Esperada

Descreva o formato da entrada que o programa deve receber.

## 📤 Saída Esperada

Descreva o formato da saída que o programa deve produzir.

---

## 💡 Exemplo

Mostre um exemplo concreto de entrada e saída esperada em bloco de código.

---

## 🔒 Restrições

Liste de 2 a 4 restrições técnicas do desafio (ex: não usar biblioteca X, complexidade máxima, etc.).

---

## 🏆 Critérios de Avaliação

Liste de 3 a 5 critérios que serão avaliados na solução (ex: clareza do código, tratamento de erros, performance).

---

## 💬 Dica

Forneça uma dica sutil que ajude o aluno sem entregar a solução.

---

Regras para geração do desafio:
- Nível **Básico**: problemas simples de lógica, estruturas de dados elementares, funções básicas da linguagem.
- Nível **Intermediário**: problemas com estruturas mais complexas, APIs, orientação a objetos, manipulação de arquivos.
- Nível **Avançado**: problemas de performance, arquitetura, design patterns, concorrência ou integração de sistemas.
- O desafio deve ser 100% original e diferente a cada execução (use aleatoriedade no tema).
- Se o nível não for informado ($2 estiver vazio), assuma **Intermediário**.
