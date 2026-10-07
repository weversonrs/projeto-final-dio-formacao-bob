# 📖 Documentação do Projeto — DIO Explorer + IBM Bob

> Guia completo para profissionais que desejam aprender com este projeto:
> arquitetura, prompts usados, modos do Bob, dicas e insights práticos.

---

## 📑 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Estrutura de Arquivos](#2-estrutura-de-arquivos)
3. [O Servidor MCP — dio-explorer](#3-o-servidor-mcp--dio-explorer)
4. [Ferramentas MCP Disponíveis](#4-ferramentas-mcp-disponíveis)
5. [Comandos Bob (/.bob/commands)](#5-comandos-bob-bobcommands)
6. [Configuração do Bob (.bob/mcp.json e .bobignore)](#6-configuração-do-bob-bobmcpjson-e-bobignore)
7. [Dataset — trilhas_dio.json](#7-dataset--trilhas_diojson)
8. [Testes — Cobertura e Resultados](#8-testes--cobertura-e-resultados)
9. [Todos os Prompts Usados na Construção](#9-todos-os-prompts-usados-na-construção)
10. [Modos do Bob e Quando Usar](#10-modos-do-bob-e-quando-usar)
11. [Dicas de Uso do Bob](#11-dicas-de-uso-do-bob)
12. [Insights para Futuros Profissionais](#12-insights-para-futuros-profissionais)

---

## 1. Visão Geral do Projeto

O **DIO Explorer** é um servidor MCP (*Model Context Protocol*) construído do zero
durante um bootcamp IBM Bob. Ele expõe **três ferramentas de IA** diretamente
dentro do assistente IBM Bob:

| Ferramenta | O que faz |
|---|---|
| `trilha` | Retorna um plano de estudos formatado para qualquer tecnologia do catálogo |
| `desafio` | Gera um desafio de código criativo com nível configurável |
| `certificado` | Emite um certificado fictício com código de verificação único |

O projeto demonstra, na prática, como **estender o IBM Bob com capacidades customizadas**
via protocolo MCP sem depender de serviços externos — tudo roda localmente via `stdio`.

---

## 2. Estrutura de Arquivos

```
ibm_bob/
├── .bob/
│   ├── mcp.json                  ← Registro do servidor MCP no Bob
│   └── commands/
│       ├── trilha.md             ← Comando slash /trilha
│       ├── desafio.md            ← Comando slash /desafio
│       └── certificado.md        ← Comando slash /certificado
│
├── .bobignore                    ← Arquivos excluídos do contexto do Bob
├── Hello_world.md                ← Primeiro arquivo criado no projeto
│
└── dio_explorer/
    ├── data/
    │   └── trilhas_dio.json      ← Dataset com 30 trilhas de formação
    ├── docs/
    │   └── resultado_testes.txt  ← Relatório de 49 testes (100% aprovados)
    └── mcp/
        ├── src/
        │   └── index.ts          ← Código-fonte TypeScript do servidor MCP
        ├── build/
        │   └── index.js          ← Build compilado (executado pelo Bob)
        ├── package.json
        └── tsconfig.json
```

---

## 3. O Servidor MCP — dio-explorer

### Stack Tecnológica

| Item | Valor |
|---|---|
| Runtime | Node.js (ESM) |
| Linguagem | TypeScript 5.5 |
| SDK MCP | `@modelcontextprotocol/sdk` v1.x |
| Validação de schemas | `zod` v3.23 |
| Transporte | `stdio` (padrão local) |
| Build | `tsc` → `build/index.js` |

### Como o Servidor é Iniciado

O Bob lê o arquivo `.bob/mcp.json` ao iniciar e executa:

```bash
node C:\treinamento\bootcamp\ibm_bob\dio_explorer\mcp\build\index.js
```

A comunicação acontece via `stdin`/`stdout` usando o protocolo MCP —
o Bob envia chamadas de ferramenta em JSON e o servidor responde com o resultado.

### Fluxo Interno

```
Bob (cliente MCP)
    │
    │  JSON-RPC over stdio
    ▼
dio-explorer MCP Server (index.js)
    │
    ├── loadTrilhas()        ← lê trilhas_dio.json
    ├── buscarTrilha()       ← busca case-insensitive
    ├── vitalicioLabel()     ← boolean → "Sim"/"Não"
    ├── hoje()               ← data formatada pt-BR
    └── randomInt()          ← aleatoriedade nos certificados e desafios
```

---

## 4. Ferramentas MCP Disponíveis

### 4.1 `trilha`

**Descrição:** Consulta o dataset e retorna um plano de estudos completo.

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `tecnologia` | `string` | ✅ | Nome da tecnologia (ex: `Java`, `Python`, `React`) |

**Exemplo de uso no Bob:**
```
Mostre a trilha de estudos para Python
```

**Saída:** Markdown estruturado com tecnologia, nível, XP, módulos numerados e badges.

**Comportamento de erro:** Retorna mensagem `❌ Nenhuma trilha encontrada para "X"` quando a tecnologia não existe no dataset.

---

### 4.2 `desafio`

**Descrição:** Gera um desafio de código com tema aleatório para a tecnologia e nível informados.

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `tecnologia` | `string` | ✅ | Tecnologia do desafio (ex: `JavaScript`, `Java`) |
| `nivel` | `enum` | ❌ | `Básico`, `Intermediário` ou `Avançado`. Padrão: `Intermediário` |

**Mapeamento XP / Tempo:**
| Nível | XP | Tempo |
|---|---|---|
| Básico | 300 XP | 30 min |
| Intermediário | 600 XP | 60 min |
| Avançado | 1000 XP | 120 min |

**Exemplo de uso no Bob:**
```
Gere um desafio Avançado de TypeScript
```

---

### 4.3 `certificado`

**Descrição:** Emite um certificado fictício com código de verificação único por execução.

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome_usuario` | `string` | ✅ | Nome completo do aluno |
| `tecnologia` | `string` | ✅ | Tecnologia ou nome da formação |

**Formato do Código de Verificação:**
```
DIO-{ID_TRILHA_ZERO_PADDED}-{ANO}-{6 dígitos aleatórios}
Exemplo: DIO-02-2025-847291
```

**Exemplo de uso no Bob:**
```
Gere um certificado para Maria Silva na trilha de Java
```

---

## 5. Comandos Bob (`.bob/commands`)

Os comandos slash permitem chamar as ferramentas MCP diretamente pelo nome,
com argumentos posicionais (`$1`, `$2`).

### `/trilha <tecnologia>`

```markdown
Argument-hint: <tecnologia>
Exemplo: /trilha React
```

O comando lê `trilhas_dio.json`, localiza a trilha e gera o plano de estudos
com módulos fictícios numerados e badges listadas.

### `/desafio <tecnologia> <nivel>`

```markdown
Argument-hint: <tecnologia> <nivel>
Exemplo: /desafio Python Básico
```

Gera um desafio com contexto realista (e-commerce, banco, jogo etc.).
Se `$2` estiver vazio, assume **Intermediário**.

### `/certificado <seu-nome> <trilha>`

```markdown
Argument-hint: <seu-nome> <trilha>
Exemplo: /certificado "João Silva" Java
```

Emite o certificado com data real de emissão e código único.
Busca a trilha de forma aproximada (case-insensitive).

---

## 6. Configuração do Bob (`.bob/mcp.json` e `.bobignore`)

### `.bob/mcp.json`

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": [
        "C:\\treinamento\\bootcamp\\ibm_bob\\dio_explorer\\mcp\\build\\index.js"
      ]
    }
  }
}
```

> **Atenção:** O caminho é absoluto. Ao clonar o projeto em outra máquina,
> atualize o `args` com o caminho correto.

### `.bobignore`

```
node_modules/          ← Exclui dependências do contexto do Bob
.env                   ← Protege variáveis de ambiente
data/cache-progresso/  ← Cache transitório
docs/certificados-emitidos/
*.tmp
```

O `.bobignore` funciona como `.gitignore`, mas para o contexto de leitura do Bob —
evita que arquivos desnecessários consumam tokens do modelo.

---

## 7. Dataset — trilhas_dio.json

O dataset contém **30 trilhas de formação** cobrindo as principais tecnologias do mercado:

| Categoria | Tecnologias |
|---|---|
| Linguagens Back-end | Python, Java, Node.js, PHP, C#, TypeScript |
| Front-end | JavaScript, React, Angular, Vue.js |
| Mobile | Flutter, Android, iOS |
| Cloud | AWS, Microsoft Azure, Google Cloud |
| Dados & IA | Machine Learning, Data Science, Data Engineering, IA Generativa, IBM watsonx |
| Infraestrutura | DevOps, Containers (Docker/K8s) |
| Banco de Dados | SQL, MongoDB |
| Especialidades | Cybersecurity, Blockchain, Unity, QA, Prompt Engineering |

### Schema de Cada Trilha

```typescript
interface Trilha {
  id: number;                    // Identificador único (1–30)
  nome: string;                  // "Formação Java Developer"
  tecnologia: string;            // "Java"
  nivel: string;                 // "Básico" | "Intermediário" | "Avançado"
  numero_modulo: number;         // Quantidade de módulos (5–15)
  xp_total: number;              // XP total da trilha
  badges_disponiveis: string[];  // Lista de badges conquistáveis
  vitalicio: boolean;            // true = acesso permanente
  lives_ao_vivo: number;         // Quantidade de lives inclusas
}
```

---

## 8. Testes — Cobertura e Resultados

O projeto possui uma suíte completa de testes unitários e de integração:

| Categoria | Testes | Resultado |
|---|---|---|
| `TestHelpers` | 9 testes | ✅ OK |
| `TestCmdTrilha` | 13 testes | ✅ OK |
| `TestCmdDesafio` | 12 testes | ✅ OK |
| `TestCmdCertificado` | 15 testes | ✅ OK |
| **TOTAL** | **49 testes** | **100% aprovados** |

**Relatório gerado em:** `dio_explorer/docs/resultado_testes.txt`

### O que é testado

- Busca case-insensitive de trilhas
- Campos obrigatórios no JSON
- XP e tempo corretos por nível
- Formato do código de verificação (`DIO-XX-AAAA-NNNNNN`)
- Comportamento para tecnologias inexistentes
- Presença de badges, módulos, nível, XP nos outputs
- Aviso de certificado fictício e link para `web.dio.me`

---

## 9. Todos os Prompts Usados na Construção

Esta seção registra os prompts-chave que guiaram a criação de cada componente.
São excelentes referências para quem quer aprender Engenharia de Prompts com o Bob.

---

### 9.1 Criação do Dataset

```
Crie um arquivo JSON com 30 trilhas de formação da plataforma DIO cobrindo
as principais tecnologias do mercado. Cada trilha deve ter: id, nome, tecnologia,
nivel (Básico/Intermediário/Avançado), numero_modulo, xp_total,
badges_disponiveis (array), vitalicio (boolean) e lives_ao_vivo.
Salve em dio_explorer/data/trilhas_dio.json.
```

---

### 9.2 Criação do Servidor MCP

```
Construa um servidor MCP em TypeScript usando @modelcontextprotocol/sdk.
O servidor deve expor três ferramentas: trilha, desafio e certificado.
Ele deve ler trilhas_dio.json para as ferramentas trilha e certificado,
e gerar desafios aleatórios para a ferramenta desafio.
Use transporte stdio. Salve em dio_explorer/mcp/src/index.ts.
```

---

### 9.3 Configuração do MCP no Bob

```
Configure o servidor MCP dio-explorer no arquivo .bob/mcp.json
para que o Bob possa chamar as ferramentas trilha, desafio e certificado.
O servidor deve ser executado com node apontando para o build compilado.
```

---

### 9.4 Criação dos Comandos Slash

```
Crie três comandos slash para o Bob em .bob/commands/:
- /trilha <tecnologia>: retorna plano de estudos formatado em Markdown
- /desafio <tecnologia> <nivel>: gera desafio de código com contexto realista
- /certificado <nome> <trilha>: emite certificado fictício com código de verificação
Cada comando deve ter description e argument-hint no frontmatter YAML.
```

---

### 9.5 Criação do .bobignore

```
Crie um arquivo .bobignore excluindo node_modules, .env,
cache de progresso, certificados emitidos e arquivos temporários
do contexto de leitura do Bob.
```

---

### 9.6 Criação dos Testes

```
Crie uma suíte de testes completa para o projeto DIO Explorer cobrindo:
os helpers (loadTrilhas, buscarTrilha, vitalicioLabel),
os três comandos (trilha, desafio, certificado) com casos de sucesso e erro.
Meta mínima de 70% de aprovação. Gere o relatório em resultado_testes.txt.
```

---

### 9.7 Documentação Final

```
Bob, documente todo o projeto feito até o momento, com todos os prompts usados,
modos de uso, dicas de uso e insights para futuros profissionais que vão
aprender com nosso projeto.
```

---

## 10. Modos do Bob e Quando Usar

O IBM Bob possui três modos principais. Entender quando usar cada um é fundamental
para obter o melhor resultado.

### 🤖 Agent (Padrão)

**Ideal para:** Escrever código, criar arquivos, instalar dependências, rodar comandos.

```
Exemplos usados neste projeto:
- Criar o servidor MCP em TypeScript
- Compilar o projeto com tsc
- Criar os comandos slash
- Gerar o dataset JSON
```

**Ferramentas disponíveis:** Todas (leitura, escrita, execução de comandos, MCP, charts).

---

### 📋 Plan

**Ideal para:** Planejar arquitetura, escrever especificações técnicas, decompor problemas complexos antes de implementar.

```
Exemplos de uso:
- "Planeje a arquitetura do servidor MCP antes de implementar"
- "Quais arquivos precisarei criar para este projeto?"
- "Descreva o schema ideal para o dataset de trilhas"
```

**Importante:** No modo Plan, comandos de execução (`execute_command`) não estão disponíveis.

---

### ❓ Ask

**Ideal para:** Perguntas sobre o próprio Bob, conceitos técnicos, documentação IBM.

```
Exemplos de uso:
- "Como funciona o protocolo MCP?"
- "Quais são os modos disponíveis no Bob?"
- "Como configurar um servidor MCP remoto?"
```

---

## 11. Dicas de Uso do Bob

### 💡 Seja específico nos prompts

❌ Ruim:
```
Crie um servidor MCP
```

✅ Bom:
```
Crie um servidor MCP em TypeScript usando @modelcontextprotocol/sdk com
transporte stdio que exponha as ferramentas trilha, desafio e certificado.
Leia os dados de dio_explorer/data/trilhas_dio.json.
```

---

### 💡 Use o .bobignore para controlar o contexto

Arquivos muito grandes ou irrelevantes (como `node_modules`) consomem tokens
desnecessariamente. Sempre adicione ao `.bobignore` tudo que o Bob não precisa
ler para executar as tarefas.

---

### 💡 Prefira comandos slash para tarefas repetitivas

Em vez de digitar um prompt longo toda vez, crie um comando slash em `.bob/commands/`.
O Bob executará o template preenchendo `$1`, `$2` etc. com os argumentos fornecidos.

---

### 💡 Peça ao Bob para investigar antes de editar

O Bob segue a regra: *nunca especule sobre código que não abriu*.
Se pedir para "corrigir um bug", mencione o arquivo. O Bob vai ler o código
antes de qualquer edição — isso evita alterações erradas.

---

### 💡 Use o modo Plan para projetos grandes

Antes de implementar algo complexo, ative o modo Plan e peça um plano detalhado.
Isso evita retrabalho e garante que a arquitetura seja decidida antes do código.

---

### 💡 Compile antes de registrar o MCP

O arquivo `.bob/mcp.json` aponta para o `build/index.js`. Se o código TypeScript
for alterado sem recompilar (`npm run build`), o Bob continuará usando a versão antiga.

```bash
cd dio_explorer/mcp
npm run build
```

---

### 💡 Teste o servidor MCP manualmente

Antes de confiar que o servidor está funcionando, valide com:

```bash
node dio_explorer/mcp/build/index.js
# Deve exibir: dio-explorer MCP server running on stdio
```

---

## 12. Insights para Futuros Profissionais

### 🔑 O MCP é a nova forma de estender assistentes de IA

O *Model Context Protocol* permite que qualquer desenvolvedor crie ferramentas
customizadas que o assistente pode invocar. Isso vai muito além de "chatbots" —
você pode integrar bancos de dados, APIs internas, sistemas legados e qualquer
fonte de dados que sua empresa utilize.

---

### 🔑 stdio vs HTTP — escolha consciente

Este projeto usa `stdio` (transporte local), que é **simples, seguro e sem latência de rede**.
Para servidores MCP que precisam atender múltiplos clientes ou rodar em cloud,
use o transporte `HTTP + SSE` (Server-Sent Events).

---

### 🔑 Zod é seu aliado na validação de schemas MCP

O SDK MCP usa `zod` para validar os `inputSchema` das ferramentas.
Isso garante que o Bob sempre passe os parâmetros corretos e que erros de tipo
sejam capturados antes da lógica de negócio.

---

### 🔑 Comandos slash são prompts com superpoderes

Os arquivos em `.bob/commands/` são templates de prompt com frontmatter YAML.
Eles transformam fluxos complexos de múltiplos passos em um único comando simples.
Invista tempo em criar bons comandos slash — eles multiplicam a produtividade.

---

### 🔑 Engenharia de Prompts é uma habilidade técnica

Os prompts usados neste projeto não foram aleatórios. Cada um especificou:
- **O que** criar (artefato, arquivo, função)
- **Como** criar (tecnologia, padrão, formato)
- **Onde** salvar (caminho do arquivo)
- **Critérios de qualidade** (cobertura de testes, formato de saída)

Um prompt bem estruturado economiza várias iterações de correção.

---

### 🔑 Testes são documentação viva

Os 49 testes deste projeto documentam o comportamento esperado de cada ferramenta.
Quando um novo desenvolvedor entra no projeto, os testes explicam as regras de negócio
melhor do que qualquer comentário de código.

---

### 🔑 O .bobignore é tão importante quanto o .gitignore

Controlar o contexto do modelo é uma forma de **otimização de custo e qualidade**.
Menos arquivos irrelevantes = menos ruído = respostas mais precisas.

---

### 🔑 Iterate rápido, documente cedo

Este projeto foi construído em ciclos curtos:
1. Dataset → 2. Servidor MCP → 3. Comandos slash → 4. Testes → 5. Documentação

Cada etapa validou a anterior. Não espere o projeto estar "pronto" para documentar —
a documentação é parte do produto.

---

*Documentação gerada com IBM Bob · Projeto DIO Explorer Bootcamp*
