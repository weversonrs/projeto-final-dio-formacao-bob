# 🚀 DIO Explorer

Projeto desenvolvido durante o **Bootcamp IBM** em parceria com a **Digital Innovation One (DIO)**, utilizando a ferramenta **IBM Bob** como assistente de IA.

---

## 📌 O que é o DIO Explorer

O **DIO Explorer** é um servidor MCP (*Model Context Protocol*) integrado ao **IBM Bob** que simula funcionalidades da plataforma **Digital Innovation One (DIO)**. Por meio de ferramentas MCP, comandos slash e skills, é possível consultar trilhas de estudos, gerar desafios de código e emitir certificados fictícios diretamente no chat do Bob — sem sair da ferramenta.

O projeto nasceu como exercício prático do Bootcamp IBM e demonstra, na prática, como estender as capacidades de um assistente de IA com ferramentas externas via protocolo MCP.

---

### 🔧 Arquitetura do Projeto

O projeto é composto por seis camadas integradas:

#### 1. Servidor MCP — `dio_explorer/mcp/`
Escrito em **TypeScript/Node.js** com o SDK oficial `@modelcontextprotocol/sdk`, o servidor expõe três ferramentas ao Bob via transporte **stdio**:

| Ferramenta | Descrição |
|---|---|
| `trilha` | Consulta o dataset e retorna o plano de estudos completo da tecnologia |
| `desafio` | Gera um enunciado de desafio de código com nível, XP, tempo e critérios de avaliação |
| `certificado` | Emite um certificado fictício em Markdown com dados reais da trilha e código de verificação único |

Os parâmetros são validados com **Zod** antes de serem processados, garantindo tipagem segura em tempo de execução. A busca por tecnologia é **case-insensitive** e suporta correspondências parciais.

#### 2. Módulo Python — `dio_explorer/src/dio_explorer.py`
Implementa as mesmas três funções (`cmd_trilha`, `cmd_desafio`, `cmd_certificado`) de forma **independente do Bob**, tornando a lógica de negócio unitariamente testável. Inclui helpers internos para carregamento do dataset (`_load_trilhas`), busca por tecnologia (`_buscar_trilha`) e formatação de saída.

#### 3. Dataset — `dio_explorer/data/trilhas_dio.json`
Arquivo JSON com **mais de 40 trilhas** de tecnologias, cada uma contendo: `id`, `nome`, `tecnologia`, `nivel`, `numero_modulo`, `xp_total`, `badges_disponiveis`, `vitalicio` e `lives_ao_vivo`. Cobre desde linguagens de programação (Python, Java, Kotlin, Rust, Go) até temas avançados (IA Generativa, IBM watsonx, Cloud Native, Blockchain).

#### 4. Interface Web — `dio_explorer/interface/index.html`
Painel HTML estático (sem dependência de servidor) com **quatro abas** — Trilha, Desafio, Desafio Nível e Certificado — barra de estatísticas do projeto e distinção visual entre os dois comandos de desafio. Abre diretamente no navegador.

#### 5. Comandos Slash — `.bob/commands/`
Quatro atalhos de prompt disponíveis no chat do Bob:

| Comando | Arquivo |
|---|---|
| `/trilha` | `.bob/commands/trilha.md` |
| `/desafio` | `.bob/commands/desafio.md` |
| `/desafio-nivel` | `.bob/commands/desafio-nivel.md` |
| `/certificado` | `.bob/commands/certificado.md` |

Cada arquivo define o prompt que o Bob executa ao receber o respectivo slash command.

#### 6. Skills — `.bob/skills/`
Quatro skills reutilizáveis (uma por comando) que encapsulam as instruções de formatação e comportamento esperado. As skills são carregadas pelo Bob sob demanda, padronizando as respostas independentemente de como a ferramenta for invocada — via slash command ou chamada direta à ferramenta MCP.

---

## ▶️ Como executar o projeto

### Pré-requisitos

- [Node.js](https://nodejs.org/) v18 ou superior
- [Python](https://www.python.org/) 3.10 ou superior
- [IBM Bob](https://www.ibm.com/bob) instalado e configurado

### 1. Instalar dependências do servidor MCP

```bash
cd dio_explorer/mcp
npm install
```

### 2. Compilar o servidor TypeScript

```bash
npm run build
```

### 3. Registrar o servidor no Bob

O arquivo `.bob/mcp.json` já está configurado. Certifique-se de que o caminho absoluto aponta para o arquivo compilado:

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["<caminho-absoluto>/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

Reinicie o Bob após qualquer alteração no `mcp.json`.

### 4. Abrir a interface web (opcional)

Abra o arquivo `dio_explorer/interface/index.html` diretamente no navegador — não requer servidor web.

---

## 💬 Como usar os comandos

Os comandos estão disponíveis como **slash commands** no chat do IBM Bob.

### `/trilha <tecnologia>`

Retorna o plano de estudos completo para a tecnologia informada, incluindo módulos, badges, XP e lives ao vivo.

```
/trilha Java
/trilha Python
/trilha React
```

### `/desafio <tecnologia> <nivel>`

Gera um desafio de código original para a tecnologia e nível escolhidos. O nível pode ser `Básico`, `Intermediário` ou `Avançado`. Se omitido, assume `Intermediário`.

```
/desafio Java Avançado
/desafio Python Básico
/desafio JavaScript
```

### `/desafio-nivel <tecnologia> <nivel>`

Versão aprimorada do comando `/desafio`, com enunciados mais detalhados, dois exemplos de entrada/saída e uma seção de bônus. Aceita variações de grafia no nível (ex: `avancado`, `ADVANCED`).

```
/desafio-nivel Kotlin Intermediário
/desafio-nivel Go Avançado
```

### `/certificado <seu-nome> <trilha>`

Emite um certificado fictício em Markdown com dados reais da trilha (XP, módulos, badges, lives) e um código de verificação no formato `DIO-XX-AAAA-NNNNNN`.

```
/certificado "Ana Lima" Python
/certificado "Carlos Dev" React
```

> **Tecnologias disponíveis:** Python, Java, JavaScript, React, Angular, Node.js, AWS, Microsoft Azure, Google Cloud, Machine Learning, Data Science, Data Engineering, DevOps, Containers, TypeScript, Vue.js, Flutter, Android, iOS, C#, PHP, Segurança da Informação, SQL, MongoDB, IA Generativa, Prompt Engineering, Unity, Blockchain, Quality Assurance, IBM watsonx, Kotlin, Go, Power BI, Linux, Rust, NestJS, Next.js, Spring Boot, RPA, Cloud Native.

---

## 🧪 Como executar os testes

Os testes unitários estão em [`dio_explorer/src/test_dio_explorer.py`](dio_explorer/src/test_dio_explorer.py) e cobrem os três comandos principais (`/trilha`, `/desafio`, `/certificado`) além dos helpers internos.

### Executar os testes com relatório

```bash
cd dio_explorer/src
python test_dio_explorer.py
```

O relatório é gerado automaticamente em `dio_explorer/docs/resultado_testes.txt`.

### Executar via pytest (sem relatório)

```bash
cd dio_explorer/src
python -m pytest test_dio_explorer.py -v
```

### Resultado atual

| Métrica | Valor |
|---|---|
| Total de testes | 84 |
| Aprovados | 84 |
| Falhas | 0 |
| Erros | 0 |
| Taxa de aprovação | **100%** |
| Meta mínima | 80% |
| Status | ✅ APROVADO |

---

## ✨ Melhorias implementadas desde o último commit

As seguintes melhorias foram implementadas em relação ao commit anterior (`feat: projeto DIO Explorer completo`):

### 📦 Expansão do Dataset
Adicionadas **10 novas trilhas** ao arquivo `trilhas_dio.json`, totalizando mais de 40 trilhas disponíveis:
- Kotlin, Go, Power BI, Linux, Rust, NestJS, Next.js, Spring Boot, RPA e Cloud Native.

### 🐍 Refatoração do Módulo Python
- O arquivo `dio_explorer.py` foi refatorado para separar a lógica de negócio dos comandos slash, tornando-o independentemente testável sem dependência do Bob.

### 🧪 Expansão da Suíte de Testes
- Testes aumentados de zero para **84 casos**, com cobertura de 100%.
- Adicionadas classes `TestHelpers`, `TestCmdTrilha`, `TestCmdDesafio` e `TestCmdCertificado`.
- Runner com geração automática de relatório em `.txt`.

### 📜 Refatoração dos Comandos Slash com Skills
- Os comandos `/trilha`, `/desafio` e `/certificado` foram aprimorados com instruções mais detalhadas e precisas.
- Criado o novo comando `/desafio-nivel` com suporte a variações de grafia e dois exemplos de entrada/saída.
- Criadas **Skills** (`.bob/skills/`) para encapsular o conhecimento de cada comando de forma reutilizável.

### 🖥️ Interface Web
- Criada a interface visual `dio_explorer/interface/index.html` com abas para Trilha, Desafio, Desafio Nível e Certificado, além de barra de estatísticas e distinção visual entre as abas de desafio.

### 📖 Documentação Atualizada
- `DOCUMENTATION.md` atualizado com todos os novos prompts utilizados, modos do Bob, dicas de uso e insights para futuros profissionais.

---

## 🎓 Aprendizado

O desenvolvimento do projeto possibilitou colocar em prática os conceitos aprendidos da ferramenta IBM Bob.
Foi possível praticar a conexão com repositórios remotos, clonagem de projetos, inclusão e alteração de arquivos, geração de documentação, criação e execução de testes, criação de servidor MCP, além de realizar as entregas das alterações realizadas.
