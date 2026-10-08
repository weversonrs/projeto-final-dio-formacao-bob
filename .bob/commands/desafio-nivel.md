---
description: Gera um desafio de código personalizado para uma tecnologia e nível específicos
argument-hint: <tecnologia> <nivel>
---

O usuário quer um desafio de código para a tecnologia **$1** no nível **$2**.

Regras de geração:
- **Iniciante**: problemas simples de lógica, variáveis, condicionais, laços e funções básicas da linguagem. Sem bibliotecas externas.
- **Intermediário**: problemas com orientação a objetos, manipulação de coleções, consumo de APIs REST, leitura/escrita de arquivos ou estruturas de dados intermediárias.
- **Avançado**: problemas de performance, concorrência, design patterns avançados, arquitetura de sistemas, integração de múltiplos componentes ou otimização de algoritmos.
- Se **$2** não for informado ou estiver em branco, assuma o nível **Intermediário**.
- Se **$2** for informado com grafia diferente (ex: "avancado", "AVANÇADO", "advanced"), normalize para o nível mais próximo.
- O desafio deve ser **100% original e diferente a cada execução** — varie o domínio de negócio (e-commerce, fintech, saúde, logística, jogos, educação, etc.).
- XP e tempo estimado conforme o nível:
  - Iniciante → 30 min / 300 XP
  - Intermediário → 60 min / 600 XP
  - Avançado → 120 min / 1000 XP

Gere o desafio em Markdown seguindo **exatamente** este modelo:

---

# 💻 Desafio de Código — $1

**Nível:** $2
**Tempo estimado:** {X} minutos
**XP ao concluir:** {XP} XP

---

## 📋 Descrição do Desafio

Descreva um problema prático e realista com contexto de negócio claro. O enunciado deve ter no mínimo 4 linhas, detalhar **o que** o programa deve fazer e **por que** esse problema existe no contexto escolhido.

---

## 📥 Entrada Esperada

Descreva o formato exato da entrada (tipos, estrutura, exemplos de valores válidos e limites aceitáveis).

## 📤 Saída Esperada

Descreva o formato exato da saída que o programa deve produzir, incluindo formatação e casos de borda.

---

## 💡 Exemplo

Mostre pelo menos **dois** pares de entrada/saída concretos em bloco de código — um caso comum e um caso de borda.

```
Entrada 1:
{exemplo de entrada normal}

Saída 1:
{exemplo de saída normal}

Entrada 2 (caso de borda):
{exemplo de entrada limite}

Saída 2:
{saída esperada para o caso de borda}
```

---

## 🔒 Restrições

Liste de 3 a 5 restrições técnicas do desafio (ex: complexidade máxima O(n log n), não usar biblioteca X, tamanho máximo da entrada, tratamento obrigatório de erros).

---

## 🏆 Critérios de Avaliação

Liste de 4 a 6 critérios que serão avaliados na solução:
- Clareza e organização do código
- Cobertura dos casos de borda
- Tratamento de erros
- Performance e eficiência
- Uso adequado dos recursos da linguagem $1

---

## 💬 Dica

Forneça uma dica sutil que oriente o raciocínio do aluno sem entregar a solução. A dica deve ser específica para $1 e para o nível $2.

---

## 🚀 Bônus (opcional)

Sugira uma extensão do desafio para quem quiser ir além — uma funcionalidade extra, uma otimização ou uma integração com outro serviço.

---
