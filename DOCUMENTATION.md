# 📖 Documentação do Projeto — DIO Explorer + IBM Bob

> Guia completo para profissionais que desejam aprender com este projeto:
> arquitetura, prompts usados, modos do Bob, dicas e insights práticos.

---

## 📑 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Estrutura de Arquivos](#2-estrutura-de-arquivos)
3. [O Servidor MCP — dio-explorer](#3-o-servidor-mcp--dio-explorer)
4. [Ferramentas MCP Disponíveis](#4-ferramentas-mcp-disponíveis)
5. [Comandos Bob (.bob/commands) e Skills (.bob/skills)](#5-comandos-bob-bobcommands-e-skills-bobskills)
6. [Interface Web — DIO Explorer](#6-interface-web--dio-explorer)
7. [Configuração do Bob (.bob/mcp.json e .bobignore)](#7-configuração-do-bob-bobmcpjson-e-bobignore)
8. [Dataset — trilhas_dio.json](#8-dataset--trilhas_diojson)
9. [Testes — Cobertura e Resultados](#9-testes--cobertura-e-resultados)
10. [Todos os Prompts Usados na Construção](#10-todos-os-prompts-usados-na-construção)
11. [Modos do Bob e Quando Usar](#11-modos-do-bob-e-quando-usar)
12. [Dicas de Uso do Bob](#12-dicas-de-uso-do-bob)
13. [Insights para Futuros Profissionais](#13-insights-para-futuros-profissionais)

---

## 1. Visão Geral do Projeto

O **DIO Explorer** é um servidor MCP (*Model Context Protocol*) construído do zero
durante um bootcamp IBM Bob. Ele expõe **três ferramentas de IA** diretamente
dentro do assistente IBM Bob, além de uma **interface web** independente que replica
todas as funcionalidades sem depender do Bob:

| Componente | O que faz |
|---|---|
| Ferramenta MCP `trilha` | Retorna um plano de estudos formatado para qualquer tecnologia do catálogo |
| Ferramenta MCP `desafio` | Gera um desafio de código com nível configurável |
| Ferramenta MCP `certificado` | Emite um certificado fictício com código de verificação único |
| Slash `/desafio-nivel` | Versão aprimorada do desafio com nível Iniciante/Intermediário/Avançado |
| Interface Web | SPA estática em HTML/CSS/JS com todas as 4 funcionalidades acessíveis no navegador |

O projeto demonstra, na prática, como **estender o IBM Bob com capacidades customizadas**
via protocolo MCP sem depender de serviços externos — tudo roda localmente via `stdio`.

---

## 2. Estrutura de Arquivos

```
ibm_bob/
├── .bob/
│   ├── mcp.json                    ← Registro do servidor MCP no Bob
│   ├── commands/
│   │   ├── trilha.md               ← Slash /trilha
│   │   ├── desafio.md              ← Slash /desafio
│   │   ├── desafio-nivel.md        ← Slash /desafio-nivel (novo)
│   │   └── certificado.md          ← Slash /certificado
│   └── skills/
│       ├── trilha/SKILL.md         ← Skill encapsulada /trilha
│       ├── desafio/SKILL.md        ← Skill encapsulada /desafio
│       ├── desafio-nivel/SKILL.md  ← Skill encapsulada /desafio-nivel (novo)
│       └── certificado/SKILL.md    ← Skill encapsulada /certificado
│
├── .bobignore                      ← Arquivos excluídos do contexto do Bob
├── Hello_world.md                  ← Primeiro arquivo criado no projeto
├── DOCUMENTATION.md                ← Este arquivo
│
└── dio_explorer/
    ├── data/
    │   └── trilhas_dio.json        ← Dataset com 40 trilhas de formação
    ├── docs/
    │   └── resultado_testes.txt    ← Relatório de 84 testes (100% aprovados)
    ├── interface/
    │   └── index.html              ← Interface web estática (novo)
    ├── src/
    │   ├── dio_explorer.py         ← Módulo Python com as funções dos comandos
    │   └── test_dio_explorer.py    ← Suíte de 84 testes unitários
    └── mcp/
        ├── src/
        │   └── index.ts            ← Código-fonte TypeScript do servidor MCP
        ├── build/
        │   └── index.js            ← Build compilado (executado pelo Bob)
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
    ├── buscarTrilha()       ← busca case-insensitive por tecnologia ou nome
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

**Saída:** Markdown com tecnologia, nível, XP, módulos numerados, badges e próximos passos.

**Comportamento de erro:** Retorna `❌ Nenhuma trilha encontrada para "X"` quando a tecnologia não existe no dataset.

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

## 5. Comandos Bob (`.bob/commands`) e Skills (`.bob/skills`)

Os comandos slash ficam em `.bob/commands/` e ficam visíveis como `/nome-do-comando`
na interface do Bob. Cada comando possui uma **Skill** correspondente em `.bob/skills/`
que encapsula as instruções detalhadas de geração.

| Comando | Argumentos | Skill | Descrição |
|---|---|---|---|
| `/trilha` | `<tecnologia>` | `trilha/SKILL.md` | Plano de estudos da trilha |
| `/desafio` | `<tecnologia> <nivel>` | `desafio/SKILL.md` | Desafio simples de código |
| `/desafio-nivel` | `<tecnologia> <nivel>` | `desafio-nivel/SKILL.md` | Desafio completo com Iniciante/Intermediário/Avançado |
| `/certificado` | `<seu-nome> <trilha>` | `certificado/SKILL.md` | Certificado fictício de conclusão |

---

### `/trilha <tecnologia>`

```
Argument-hint: <tecnologia>
Exemplo: /trilha React
```

Lê `trilhas_dio.json`, localiza a trilha e gera:
- Metadados: tecnologia, nível, XP, acesso vitalício, lives
- Módulos numerados com títulos coerentes e progressão lógica
- Badges disponíveis
- Seção **🚀 Próximos Passos** com 3 dicas específicas

---

### `/desafio <tecnologia> <nivel>`

```
Argument-hint: <tecnologia> <nivel>
Exemplo: /desafio Python Básico
```

Gera um desafio simples. Se `$2` estiver vazio, assume **Intermediário**.

**Saída:** título, nível, tempo, XP, descrição de 1 linha, entrada esperada, saída esperada.

---

### `/desafio-nivel <tecnologia> <nivel>`

```
Argument-hint: <tecnologia> <nivel>
Exemplo: /desafio-nivel Kotlin Avançado
```

Versão aprimorada do `/desafio`. Diferenciais:

| Aspecto | `/desafio` | `/desafio-nivel` |
|---|---|---|
| Escala de níveis | Básico / Intermediário / Avançado | **Iniciante** / Intermediário / Avançado |
| Normalização de entrada | Sem normalização | Aceita variações livres ("basico", "AVANÇADO", "advanced") |
| Descrição | 1 linha | 4+ linhas com contexto de negócio e foco do nível |
| Exemplos | Nenhum | **2 pares** entrada/saída (caso normal + caso de borda) |
| Restrições | — | 3 a 5 itens técnicos |
| Critérios de avaliação | — | 4 a 6 itens |
| Dica | — | Específica para tecnologia e nível |
| Bônus | — | ✅ Seção **🚀 Bônus (opcional)** |

**Mapeamento XP / Tempo:**
| Nível | XP | Tempo |
|---|---|---|
| Iniciante | 300 XP | 30 min |
| Intermediário | 600 XP | 60 min |
| Avançado | 1000 XP | 120 min |

---

### `/certificado <seu-nome> <trilha>`

```
Argument-hint: <seu-nome> <trilha>
Exemplo: /certificado "João Silva" Java
```

Emite o certificado com:
- Frase de atestação com nome e trilha
- Data real de emissão e código único `DIO-XX-AAAA-NNNNNN`
- Tabela de informações da trilha (tecnologia, nível, módulos, XP, lives, acesso vitalício)
- Badges conquistadas
- Aviso de caráter fictício e link para `web.dio.me`

---

## 6. Interface Web — DIO Explorer

A interface web é um **Single Page Application** 100% estático localizado em
`dio_explorer/interface/index.html`. Abre diretamente no navegador com duplo clique —
sem servidor, sem dependências externas.

### Tecnologias

| Item | Detalhe |
|---|---|
| Linguagem | HTML5 + CSS3 + JavaScript (Vanilla ES6+) |
| Dependências | Nenhuma — tudo inline |
| Dados | Dataset das 40 trilhas embutido diretamente no JS |
| Markdown | Renderer próprio (sem biblioteca) |

### Abas Disponíveis

| Aba | Slash equivalente | O que faz |
|---|---|---|
| 📚 Trilhas | `/trilha` | Busca por tecnologia + grid clicável com filtro por nome e nível |
| 💻 Desafio | `/desafio` | Desafio simples com níveis Básico / Intermediário / Avançado |
| 🎯 Desafio Nível | `/desafio-nivel` | Desafio completo com níveis Iniciante / Intermediário / Avançado |
| 🎓 Certificado | `/certificado` | Emissão de certificado fictício |

### Detalhes por Aba

**📚 Trilhas**
- Campo de busca por tecnologia → exibe plano de estudos com módulos e badges
- Grid de cards com todas as 40 trilhas, filtráveis por nome/tecnologia e nível
- Clicar em um card preenche automaticamente o campo de busca e exibe o plano

**💻 Desafio**
- Select: Básico / Intermediário / Avançado
- Saída idêntica ao `cmd_desafio()` do módulo Python: descrição de 1 linha, entrada e saída esperadas

**🎯 Desafio Nível**
- Select: **Iniciante** / Intermediário / Avançado (escala diferente do `/desafio`)
- Saída completa: descrição com foco do nível, 2 pares de exemplo, restrições, critérios, dica específica, seção Bônus
- Normalização de texto livre via `normalizarNivel()`: aceita "basico", "AVANÇADO", "advanced" etc.

**🎓 Certificado**
- Campos: nome completo + tecnologia
- Saída idêntica ao `cmd_certificado()` do módulo Python: atestação, data, código, tabela de informações, badges

### Barra de Estatísticas

Exibida no topo da página, calculada dinamicamente:
- Total de trilhas (40)
- XP total acumulado (~210k XP)
- Contagem por nível (Básico, Intermediário, Avançado)

---

## 7. Configuração do Bob (`.bob/mcp.json` e `.bobignore`)

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

## 8. Dataset — trilhas_dio.json

O dataset contém **40 trilhas de formação** cobrindo as principais tecnologias do mercado.
O arquivo foi expandido de 30 para 40 trilhas durante o bootcamp (IDs 31–40).

| Categoria | Tecnologias |
|---|---|
| Linguagens Back-end | Python, Java, Node.js, PHP, C#, TypeScript, Go, Rust, Kotlin |
| Frameworks Back-end | Spring Boot, NestJS |
| Front-end | JavaScript, React, Angular, Vue.js, Next.js |
| Mobile | Flutter, Android, iOS |
| Cloud | AWS, Microsoft Azure, Google Cloud, Cloud Native |
| Dados & IA | Machine Learning, Data Science, Data Engineering, IA Generativa, IBM watsonx, Power BI |
| Infraestrutura | DevOps, Containers (Docker/K8s), Linux, RPA |
| Banco de Dados | SQL, MongoDB |
| Especialidades | Cybersecurity, Blockchain, Unity, QA, Prompt Engineering |

### Schema de Cada Trilha

```typescript
interface Trilha {
  id: number;                    // Identificador único (1–40)
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

## 9. Testes — Cobertura e Resultados

O projeto possui uma suíte completa de testes unitários em `dio_explorer/src/test_dio_explorer.py`.
A meta mínima foi elevada de **70%** para **80%** durante o bootcamp.

| Categoria | Testes | Resultado |
|---|---|---|
| `TestHelpers` | 19 testes | ✅ OK |
| `TestCmdTrilha` | 22 testes | ✅ OK |
| `TestCmdDesafio` | 13 testes | ✅ OK |
| `TestCmdCertificado` | 24 testes | ✅ OK |
| **TOTAL** | **84 testes** | **100% aprovados** |

**Relatório gerado em:** `dio_explorer/docs/resultado_testes.txt`

Para rodar os testes:
```bash
py dio_explorer/src/test_dio_explorer.py
```

### O que é testado

**TestHelpers (19 testes)**
- `_load_trilhas()` retorna lista não-vazia
- Dataset contém pelo menos 40 trilhas
- Todos os campos obrigatórios presentes em cada trilha
- IDs únicos e tecnologias únicas no dataset
- Nível válido (`Básico`, `Intermediário`, `Avançado`) em todas as trilhas
- `xp_total` inteiro positivo em todas as trilhas
- `badges_disponiveis` não-vazia em todas as trilhas
- `_vitalicio_label()` correto para `True` e `False`
- Busca case-insensitive (java, JAVA, Java), por substring, com espaços extras
- Busca por tecnologias das trilhas expandidas (Kotlin, Go, Power BI, Linux, Rust, Spring Boot)
- Retorno `None` para tecnologia inexistente

**TestCmdTrilha (22 testes)**
- Retorna string não-vazia
- Contém nome da formação, nível, XP, lives, vitalício, módulos, badges
- Número de módulos listados corresponde ao campo `numero_modulo`
- XP exibido bate com o JSON
- Todas as badges aparecem no resultado
- Mensagem de erro menciona a tecnologia informada
- Funciona para trilhas novas: Python, Kotlin, Go, Rust, Linux, Spring Boot

**TestCmdDesafio (13 testes)**
- Retorna string não-vazia
- Contém tecnologia, nível, tempo, XP, descrição, entrada/saída
- XP e tempo corretos para Básico (300/30), Intermediário (600/60), Avançado (1000/120)
- Nível padrão quando vazio → Intermediário
- Nível desconhecido assume 600 XP (Intermediário)
- Funciona para Python, Kotlin

**TestCmdCertificado (24 testes)**
- Retorna string não-vazia
- Contém nome do usuário, nome da trilha, título, XP, nível, módulos, lives, badges
- Título correto: `# 🎓 Certificação DIO`
- Frase de atestação presente
- Seção `## 📋 Informações da Trilha` presente
- Sufixos corretos: `N módulos`, `N lives`
- Data de emissão aparece **antes** das badges
- Código de verificação no formato `DIO-XX-AAAA-NNNNNN`
- Campo vitalício: "Sim" para trilhas vitalícias, "Não" para não-vitalícias
- Aviso de certificado fictício e link `web.dio.me`
- Mensagem de erro menciona a trilha informada
- Funciona para Python, Kotlin (trilha nova)

---

## 10. Todos os Prompts Usados na Construção

Esta seção registra os prompts-chave que guiaram a criação de cada componente.
São excelentes referências para quem quer aprender Engenharia de Prompts com o Bob.

---

### 10.1 Criação do Dataset

```
Crie um arquivo JSON com 30 trilhas de formação da plataforma DIO cobrindo
as principais tecnologias do mercado. Cada trilha deve ter: id, nome, tecnologia,
nivel (Básico/Intermediário/Avançado), numero_modulo, xp_total,
badges_disponiveis (array), vitalicio (boolean) e lives_ao_vivo.
Salve em dio_explorer/data/trilhas_dio.json.
```

---

### 10.2 Criação do Servidor MCP

```
Construa um servidor MCP em TypeScript usando @modelcontextprotocol/sdk.
O servidor deve expor três ferramentas: trilha, desafio e certificado.
Ele deve ler trilhas_dio.json para as ferramentas trilha e certificado,
e gerar desafios aleatórios para a ferramenta desafio.
Use transporte stdio. Salve em dio_explorer/mcp/src/index.ts.
```

---

### 10.3 Configuração do MCP no Bob

```
Configure o servidor MCP dio-explorer no arquivo .bob/mcp.json
para que o Bob possa chamar as ferramentas trilha, desafio e certificado.
O servidor deve ser executado com node apontando para o build compilado.
```

---

### 10.4 Criação dos Comandos Slash

```
Crie três comandos slash para o Bob em .bob/commands/:
- /trilha <tecnologia>: retorna plano de estudos formatado em Markdown
- /desafio <tecnologia> <nivel>: gera desafio de código com contexto realista
- /certificado <nome> <trilha>: emite certificado fictício com código de verificação
Cada comando deve ter description e argument-hint no frontmatter YAML.
```

---

### 10.5 Criação do .bobignore

```
Crie um arquivo .bobignore excluindo node_modules, .env,
cache de progresso, certificados emitidos e arquivos temporários
do contexto de leitura do Bob.
```

---

### 10.6 Criação dos Testes

```
Crie uma suíte de testes completa para o projeto DIO Explorer cobrindo:
os helpers (loadTrilhas, buscarTrilha, vitalicioLabel),
os três comandos (trilha, desafio, certificado) com casos de sucesso e erro.
Meta mínima de 70% de aprovação. Gere o relatório em resultado_testes.txt.
```

---

### 10.7 Documentação Inicial

```
Bob, documente todo o projeto feito até o momento, com todos os prompts usados,
modos de uso, dicas de uso e insights para futuros profissionais que vão
aprender com nosso projeto.
```

---

### 10.8 Refatoração dos Slash Commands com Skills

```
revise os arquivos de testes criados e o arquivo com os resultados após a
refatoração da criação dos slash commands
```

> **O que foi feito:**
> Os três slash commands foram revisados e complementados com Skills do Bob (`.bob/skills/`)
> que encapsulam as instruções de geração de resposta. O arquivo de testes `test_dio_explorer.py`
> teve seus caminhos corrigidos (`sys.path` e `output_dir`), e o relatório
> `resultado_testes.txt` foi regenerado — **49/49 testes aprovados (100%)**.

---

### 10.9 Expansão do Dataset e Testes

```
Expanda o dataset para 40 trilhas, adicionando as tecnologias:
Kotlin, Go, Power BI, Linux, Rust, NestJS, Next.js, Spring Boot, RPA, Cloud Native.
Atualize a suíte de testes para cobrir as novas trilhas e eleve a meta para 80%.
```

> **O que foi feito:**
> O arquivo `trilhas_dio.json` foi expandido de 30 para 40 trilhas (IDs 31–40).
> A suíte de testes foi ampliada de 49 para **84 testes**, cobrindo as novas trilhas,
> validações adicionais do dataset (IDs únicos, tecnologias únicas, nível válido,
> XP positivo, badges não-vazias) e novos casos para os três comandos.
> Meta elevada de 70% para **80%**. Resultado: **84/84 aprovados (100%)**.

---

### 10.10 Criação da Interface Web

```
Bob, crie uma interface para possibilitar o acesso ao projeto
```

> **O que foi feito:**
> Criado `dio_explorer/interface/index.html` — SPA estático com 4 abas mapeando
> os 4 slash commands do projeto. Dataset das 40 trilhas embutido no JS.
> Markdown renderer próprio, barra de estatísticas dinâmica, grid clicável com
> filtros, spinner de loading, suporte a Enter nos campos de texto.

---

### 10.11 Revisão do Certificado

```
Bob, revise o certificado considerando que as informações não foram atualizadas
com as mudanças solicitadas.
```

> **O que foi feito:**
> `.bob/commands/certificado.md` e `.bob/skills/certificado/SKILL.md` foram
> sincronizados com o formato atual do `cmd_certificado()` em `dio_explorer.py`:
> título `# 🎓 Certificação DIO`, frase de atestação, data/código antes das badges,
> tabela com cabeçalho `Campo | Valor`, sufixos `N módulos` / `N lives`,
> badges listadas como `- 🥇 **{nome}**` (sem invenção de descrições).

---

### 10.12 Revisão da Interface com Mudanças do Repositório

```
Bob, revise o projeto com as alterações criadas desde o último commit
para que as mudanças estejam disponíveis na interface criada.
```

> **O que foi feito:**
> A função `showCertificado()` da interface foi alinhada ao `cmd_certificado()`
> atual do Python (que havia sido revertido para o formato anterior ao MCP).
> As 10 trilhas adicionadas (IDs 31–40) já estavam na interface desde a criação.

---

### 10.13 Adição da Aba Desafio Nível

```
Bob, a slash /desafio-nivel não está disponível na interface criada
```

> **O que foi feito:**
> Adicionada a aba **🎯 Desafio Nível** na interface, mapeando o slash `/desafio-nivel`.
> Implementada a função `showDesafioNivel()` com escala Iniciante/Intermediário/Avançado,
> normalização de texto livre, 2 pares de exemplo, 6 critérios, dica específica e
> seção 🚀 Bônus.

---

### 10.14 Distinção Visual entre Abas Desafio e Desafio Nível

```
Bob, revise as abas "Desafio" e "Desafio Nível" considerando que estão
apresentando o mesmo comportamento.
```

> **O que foi feito:**
> `showDesafio()` foi restaurado ao conteúdo exato do `cmd_desafio()` do commit
> (sem seções extras). Títulos dos cards atualizados para identificar claramente
> o slash de cada aba. Subtítulos descritivos adicionados a cada card.

---

## 11. Modos do Bob e Quando Usar

O IBM Bob possui três modos principais. Entender quando usar cada um é fundamental
para obter o melhor resultado.

### 🤖 Agent (Padrão)

**Ideal para:** Escrever código, criar arquivos, instalar dependências, rodar comandos.

```
Exemplos usados neste projeto:
- Criar o servidor MCP em TypeScript
- Compilar o projeto com tsc
- Criar os comandos slash e skills
- Gerar o dataset JSON
- Criar a interface web
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

## 12. Dicas de Uso do Bob

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

### 💡 Interfaces web como documentação executável

A interface `dio_explorer/interface/index.html` é um artefato de documentação viva —
ela mostra exatamente o que cada slash command produz, sem depender do Bob estar
em execução. Use-a para demonstrações, onboarding e validação visual.

---

## 13. Insights para Futuros Profissionais

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

### 🔑 Skills encapsulam conhecimento reutilizável

As Skills (`.bob/skills/`) são instruções especializadas que o Bob carrega sob demanda.
Quando um slash command aciona uma skill, o Bob recebe instruções detalhadas sem
precisar de um prompt longo. É a forma mais eficiente de padronizar comportamentos.

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

Os 84 testes deste projeto documentam o comportamento esperado de cada ferramenta.
Quando um novo desenvolvedor entra no projeto, os testes explicam as regras de negócio
melhor do que qualquer comentário de código.

---

### 🔑 O .bobignore é tão importante quanto o .gitignore

Controlar o contexto do modelo é uma forma de **otimização de custo e qualidade**.
Menos arquivos irrelevantes = menos ruído = respostas mais precisas.

---

### 🔑 Interfaces web como ponte entre IA e usuário

A interface `index.html` demonstra um padrão importante: **desacoplar a lógica de negócio
da ferramenta de IA**. O módulo Python (`dio_explorer.py`) é a fonte da verdade;
o MCP, os slash commands e a interface web são apenas formas diferentes de expor
a mesma funcionalidade. Esse padrão facilita manutenção e testes.

---

### 🔑 Iterate rápido, documente cedo

Este projeto foi construído em ciclos curtos:
1. Dataset → 2. Servidor MCP → 3. Comandos slash → 4. Testes → 5. Interface Web → 6. Documentação

Cada etapa validou a anterior. Não espere o projeto estar "pronto" para documentar —
a documentação é parte do produto.

---

*Documentação gerada com IBM Bob · Projeto DIO Explorer Bootcamp*
