#!/usr/bin/env node
/**
 * DIO Explorer MCP Server
 * Expõe as ferramentas trilha, desafio e certificado via protocolo MCP.
 * Transporte: stdio (padrão para uso local com o Bob).
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve, join } from "path";

// ---------------------------------------------------------------------------
// Localização do arquivo de dados
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// build/index.js → ../../data/trilhas_dio.json
const DATA_FILE = resolve(__dirname, "..", "..", "data", "trilhas_dio.json");

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: string;
  numero_modulo: number;
  xp_total: number;
  badges_disponiveis: string[];
  vitalicio: boolean;
  lives_ao_vivo: number;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function loadTrilhas(): Trilha[] {
  const raw = readFileSync(DATA_FILE, "utf-8");
  return JSON.parse(raw).trilhas as Trilha[];
}

function buscarTrilha(tecnologia: string): Trilha | undefined {
  const termo = tecnologia.trim().toLowerCase();
  return loadTrilhas().find(
    (t) =>
      termo.includes(t.tecnologia.toLowerCase()) ||
      t.tecnologia.toLowerCase().includes(termo)
  );
}

function vitalicioLabel(v: boolean): string {
  return v ? "Sim" : "Não";
}

function hoje(): string {
  return new Date().toLocaleDateString("pt-BR");
}

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

const TEMAS = [
  "sistema de biblioteca",
  "API de e-commerce",
  "jogo da memória",
  "gerenciador de tarefas",
  "sistema bancário",
  "analisador de logs",
  "agenda de contatos",
  "conversor de moedas",
  "buscador de CEP",
];

// ---------------------------------------------------------------------------
// Servidor MCP
// ---------------------------------------------------------------------------
const server = new McpServer({
  name: "dio-explorer",
  version: "1.0.0",
});

// ── Ferramenta: trilha ──────────────────────────────────────────────────────
server.registerTool(
  "trilha",
  {
    description:
      "Consulta o arquivo trilhas_dio.json e retorna um plano de estudos formatado para a tecnologia informada.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe("Nome da tecnologia a buscar (ex: Java, Python, React)"),
    }),
  },
  async ({ tecnologia }) => {
    const trilha = buscarTrilha(tecnologia);

    if (!trilha) {
      return {
        content: [
          {
            type: "text",
            text: `❌ Nenhuma trilha encontrada para "${tecnologia}". Verifique o nome da tecnologia e tente novamente.`,
          },
        ],
        isError: true,
      };
    }

    const modulos = Array.from(
      { length: trilha.numero_modulo },
      (_, i) =>
        `${i + 1}. Módulo ${i + 1} — Conteúdo programático do módulo ${i + 1} da trilha ${trilha.tecnologia}.`
    ).join("\n");

    const badges = trilha.badges_disponiveis
      .map((b) => `- 🥇 **${b}**`)
      .join("\n");

    const texto = [
      `# 📚 Plano de Estudos — ${trilha.nome}`,
      "",
      `**Tecnologia:** ${trilha.tecnologia}`,
      `**Nível:** ${trilha.nivel}`,
      `**XP Total:** ${trilha.xp_total} XP`,
      `**Acesso Vitalício:** ${vitalicioLabel(trilha.vitalicio)}`,
      `**Lives ao Vivo:** ${trilha.lives_ao_vivo}`,
      "",
      "---",
      "",
      "## 🗂️ Módulos da Trilha",
      "",
      modulos,
      "",
      "---",
      "",
      "## 🏅 Badges Disponíveis",
      "",
      badges,
    ].join("\n");

    return { content: [{ type: "text", text: texto }] };
  }
);

// ── Ferramenta: desafio ─────────────────────────────────────────────────────
server.registerTool(
  "desafio",
  {
    description:
      "Gera um desafio de código para a tecnologia e nível informados.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe("Tecnologia do desafio (ex: Java, Python, JavaScript)"),
      nivel: z
        .enum(["Básico", "Intermediário", "Avançado"])
        .optional()
        .describe("Nível do desafio. Padrão: Intermediário"),
    }),
  },
  async ({ tecnologia, nivel }) => {
    const lvl = nivel ?? "Intermediário";
    const xpMap: Record<string, number> = {
      Básico: 300,
      Intermediário: 600,
      Avançado: 1000,
    };
    const tempoMap: Record<string, number> = {
      Básico: 30,
      Intermediário: 60,
      Avançado: 120,
    };
    const tema = TEMAS[randomInt(0, TEMAS.length - 1)];

    const texto = [
      `# 💻 Desafio de Código — ${tecnologia}`,
      "",
      `**Nível:** ${lvl}`,
      `**Tempo estimado:** ${tempoMap[lvl]} minutos`,
      `**XP ao concluir:** ${xpMap[lvl]} XP`,
      "",
      "---",
      "",
      "## 📋 Descrição do Desafio",
      "",
      `Implemente um **${tema}** utilizando **${tecnologia}**. O sistema deve contemplar as operações básicas de CRUD com validação de dados e tratamento de erros.`,
      "",
      "## 📥 Entrada Esperada",
      "Comandos via chamadas de função ou requisições HTTP com os dados necessários.",
      "",
      "## 📤 Saída Esperada",
      "Resultados formatados em texto ou JSON conforme a operação executada.",
      "",
      "---",
      "",
      "## 🔒 Restrições",
      "- Não utilizar frameworks externos além dos permitidos pela trilha.",
      "- A solução deve cobrir ao menos 3 casos de erro.",
      "",
      "## 🏆 Critérios de Avaliação",
      "- Clareza e organização do código",
      "- Tratamento adequado de exceções",
      "- Cobertura dos requisitos funcionais",
      "",
      "## 💬 Dica",
      `Comece modelando as entidades do ${tema} antes de escrever qualquer lógica de negócio.`,
    ].join("\n");

    return { content: [{ type: "text", text: texto }] };
  }
);

// ── Ferramenta: certificado ─────────────────────────────────────────────────
server.registerTool(
  "certificado",
  {
    description:
      "Gera um certificado fictício em Markdown para o nome do usuário e a trilha concluída.",
    inputSchema: z.object({
      nome_usuario: z
        .string()
        .describe("Nome completo do aluno que receberá o certificado"),
      tecnologia: z
        .string()
        .describe("Tecnologia ou nome da formação concluída (ex: Java, React)"),
    }),
  },
  async ({ nome_usuario, tecnologia }) => {
    const trilha = buscarTrilha(tecnologia);

    if (!trilha) {
      return {
        content: [
          {
            type: "text",
            text: `❌ Trilha "${tecnologia}" não encontrada. Verifique o nome da tecnologia ou da formação e tente novamente.`,
          },
        ],
        isError: true,
      };
    }

    const codigo = `DIO-${String(trilha.id).padStart(2, "0")}-${new Date().getFullYear()}-${randomInt(100000, 999999)}`;

    const badges = trilha.badges_disponiveis
      .map((b) => `- 🥇 **${b}**`)
      .join("\n");

    const texto = [
      "# 🎓 Certificado de Conclusão",
      "",
      "---",
      "",
      "> *A plataforma **DIO — Digital Innovation One** certifica que*",
      "",
      `## ${nome_usuario}`,
      "",
      "*concluiu com êxito a trilha de formação:*",
      "",
      `# 🏆 ${trilha.nome}`,
      "",
      "---",
      "",
      "| | |",
      "|---|---|",
      `| **Tecnologia** | ${trilha.tecnologia} |`,
      `| **Nível** | ${trilha.nivel} |`,
      `| **Módulos Concluídos** | ${trilha.numero_modulo} |`,
      `| **XP Conquistado** | ${trilha.xp_total} XP |`,
      `| **Lives Assistidas** | ${trilha.lives_ao_vivo} |`,
      `| **Acesso Vitalício** | ${vitalicioLabel(trilha.vitalicio)} |`,
      "",
      "---",
      "",
      "## 🏅 Badges Conquistadas",
      "",
      badges,
      "",
      "---",
      "",
      `**Data de Emissão:** ${hoje()}`,
      `**Código de Verificação:** \`${codigo}\``,
      "",
      "---",
      "",
      "*Este certificado é fictício e foi gerado para fins educacionais pelo projeto DIO Explorer.*",
      "*Verifique certificados reais em: https://web.dio.me*",
    ].join("\n");

    return { content: [{ type: "text", text: texto }] };
  }
);

// ---------------------------------------------------------------------------
// Inicialização
// ---------------------------------------------------------------------------
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("dio-explorer MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
