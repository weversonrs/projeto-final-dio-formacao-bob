"""
Testes unitários — DIO Explorer
Cobre os slash commands /trilha, /desafio e /certificado com foco em Java.
Meta: >= 70% de aprovação nos casos de teste.
"""

import sys
import os
import unittest
import json
import re

# Garante que o módulo src seja encontrado independente de onde o teste rode
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dio_explorer import (
    _load_trilhas,
    _buscar_trilha,
    _vitalicio_label,
    cmd_trilha,
    cmd_desafio,
    cmd_certificado,
)


# ===========================================================================
# Testes auxiliares / helpers
# ===========================================================================

class TestHelpers(unittest.TestCase):

    def test_load_trilhas_retorna_lista(self):
        """_load_trilhas deve retornar uma lista não-vazia."""
        trilhas = _load_trilhas()
        self.assertIsInstance(trilhas, list)
        self.assertGreater(len(trilhas), 0)

    def test_load_trilhas_quantidade_minima(self):
        """O arquivo deve conter pelo menos 30 trilhas."""
        trilhas = _load_trilhas()
        self.assertGreaterEqual(len(trilhas), 30)

    def test_load_trilhas_campos_obrigatorios(self):
        """Cada trilha deve ter todos os campos obrigatórios."""
        campos = {"id", "nome", "tecnologia", "nivel", "numero_modulo",
                  "xp_total", "badges_disponiveis", "vitalicio", "lives_ao_vivo"}
        for trilha in _load_trilhas():
            for campo in campos:
                self.assertIn(campo, trilha, f"Campo '{campo}' ausente na trilha id={trilha.get('id')}")

    def test_vitalicio_label_true(self):
        self.assertEqual(_vitalicio_label(True), "Sim")

    def test_vitalicio_label_false(self):
        self.assertEqual(_vitalicio_label(False), "Não")

    def test_buscar_trilha_java_exato(self):
        """Deve encontrar a trilha Java por correspondência exata (case-insensitive)."""
        trilha = _buscar_trilha("Java")
        self.assertIsNotNone(trilha)
        self.assertIn("Java", trilha["tecnologia"])

    def test_buscar_trilha_java_minusculo(self):
        """Deve encontrar a trilha Java mesmo com entrada em minúsculas."""
        trilha = _buscar_trilha("java")
        self.assertIsNotNone(trilha)

    def test_buscar_trilha_java_maiusculo(self):
        """Deve encontrar a trilha Java com entrada em maiúsculas."""
        trilha = _buscar_trilha("JAVA")
        self.assertIsNotNone(trilha)

    def test_buscar_trilha_inexistente(self):
        """Deve retornar None para tecnologia inexistente."""
        trilha = _buscar_trilha("COBOL_XYZ_INEXISTENTE")
        self.assertIsNone(trilha)


# ===========================================================================
# Testes do /trilha
# ===========================================================================

class TestCmdTrilha(unittest.TestCase):

    def setUp(self):
        self.resultado_java = cmd_trilha("Java")

    def test_trilha_java_retorna_string(self):
        """Deve retornar uma string não-vazia."""
        self.assertIsInstance(self.resultado_java, str)
        self.assertGreater(len(self.resultado_java), 0)

    def test_trilha_java_contem_nome_formacao(self):
        """O resultado deve conter o nome da formação Java."""
        self.assertIn("Java", self.resultado_java)

    def test_trilha_java_contem_nivel(self):
        """O resultado deve conter o campo Nível."""
        self.assertIn("Nível", self.resultado_java)

    def test_trilha_java_contem_xp(self):
        """O resultado deve conter XP Total."""
        self.assertIn("XP", self.resultado_java)

    def test_trilha_java_contem_vitalicio(self):
        """O resultado deve informar acesso vitalício."""
        self.assertIn("Vitalício", self.resultado_java)

    def test_trilha_java_contem_lives(self):
        """O resultado deve informar lives ao vivo."""
        self.assertIn("Lives", self.resultado_java)

    def test_trilha_java_contem_modulos(self):
        """O resultado deve listar os módulos."""
        self.assertIn("Módulos", self.resultado_java)

    def test_trilha_java_contem_badges(self):
        """O resultado deve listar as badges."""
        self.assertIn("Badges", self.resultado_java)

    def test_trilha_java_numero_modulos_correto(self):
        """O número de módulos listados deve corresponder ao campo numero_modulo."""
        trilha = _buscar_trilha("Java")
        # Conta ocorrências de linhas no formato "N. Módulo"
        modulos_encontrados = re.findall(r"^\d+\. Módulo", self.resultado_java, re.MULTILINE)
        self.assertEqual(len(modulos_encontrados), trilha["numero_modulo"])

    def test_trilha_java_xp_correto(self):
        """O XP exibido deve ser o mesmo do JSON."""
        trilha = _buscar_trilha("Java")
        self.assertIn(str(trilha["xp_total"]), self.resultado_java)

    def test_trilha_java_badges_corretas(self):
        """Todas as badges da trilha Java devem aparecer no resultado."""
        trilha = _buscar_trilha("Java")
        for badge in trilha["badges_disponiveis"]:
            self.assertIn(badge, self.resultado_java)

    def test_trilha_tecnologia_inexistente(self):
        """Para tecnologia inexistente deve retornar mensagem de erro."""
        resultado = cmd_trilha("COBOL_XYZ_INEXISTENTE")
        self.assertIn("❌", resultado)
        self.assertIn("Nenhuma trilha encontrada", resultado)

    def test_trilha_case_insensitive(self):
        """A busca deve ser case-insensitive."""
        resultado_lower = cmd_trilha("java")
        resultado_upper = cmd_trilha("JAVA")
        self.assertNotIn("❌", resultado_lower)
        self.assertNotIn("❌", resultado_upper)


# ===========================================================================
# Testes do /desafio
# ===========================================================================

class TestCmdDesafio(unittest.TestCase):

    def setUp(self):
        self.resultado = cmd_desafio("Java", "Intermediário")

    def test_desafio_retorna_string(self):
        """Deve retornar uma string não-vazia."""
        self.assertIsInstance(self.resultado, str)
        self.assertGreater(len(self.resultado), 0)

    def test_desafio_contem_tecnologia(self):
        """O resultado deve mencionar a tecnologia Java."""
        self.assertIn("Java", self.resultado)

    def test_desafio_contem_nivel(self):
        """O resultado deve mencionar o nível."""
        self.assertIn("Intermediário", self.resultado)

    def test_desafio_contem_xp(self):
        """O resultado deve conter XP ao concluir."""
        self.assertIn("XP", self.resultado)

    def test_desafio_contem_tempo(self):
        """O resultado deve conter tempo estimado."""
        self.assertIn("minutos", self.resultado)

    def test_desafio_contem_descricao(self):
        """O resultado deve conter seção de descrição."""
        self.assertIn("Descrição", self.resultado)

    def test_desafio_contem_entrada_saida(self):
        """O resultado deve conter entrada e saída esperadas."""
        self.assertIn("Entrada", self.resultado)
        self.assertIn("Saída", self.resultado)

    def test_desafio_nivel_basico_xp_correto(self):
        """Nível Básico deve gerar 300 XP."""
        resultado = cmd_desafio("Java", "Básico")
        self.assertIn("300", resultado)

    def test_desafio_nivel_avancado_xp_correto(self):
        """Nível Avançado deve gerar 1000 XP."""
        resultado = cmd_desafio("Java", "Avançado")
        self.assertIn("1000", resultado)

    def test_desafio_nivel_padrao_quando_vazio(self):
        """Sem nível, deve assumir Intermediário."""
        resultado = cmd_desafio("Java", "")
        self.assertIn("Intermediário", resultado)

    def test_desafio_tempo_basico(self):
        """Nível Básico deve ter 30 minutos."""
        resultado = cmd_desafio("Java", "Básico")
        self.assertIn("30", resultado)

    def test_desafio_tempo_avancado(self):
        """Nível Avançado deve ter 120 minutos."""
        resultado = cmd_desafio("Java", "Avançado")
        self.assertIn("120", resultado)


# ===========================================================================
# Testes do /certificado
# ===========================================================================

class TestCmdCertificado(unittest.TestCase):

    def setUp(self):
        self.nome = "Weverson RS"
        self.resultado = cmd_certificado(self.nome, "Java")

    def test_certificado_retorna_string(self):
        """Deve retornar uma string não-vazia."""
        self.assertIsInstance(self.resultado, str)
        self.assertGreater(len(self.resultado), 0)

    def test_certificado_contem_nome_usuario(self):
        """O certificado deve conter o nome do usuário."""
        self.assertIn(self.nome, self.resultado)

    def test_certificado_contem_nome_trilha(self):
        """O certificado deve conter o nome da trilha Java."""
        self.assertIn("Java", self.resultado)

    def test_certificado_contem_titulo(self):
        """O certificado deve conter o título 'Certificado de Conclusão'."""
        self.assertIn("Certificado de Conclusão", self.resultado)

    def test_certificado_contem_xp(self):
        """O certificado deve conter o XP conquistado."""
        trilha = _buscar_trilha("Java")
        self.assertIn(str(trilha["xp_total"]), self.resultado)

    def test_certificado_contem_nivel(self):
        """O certificado deve conter o nível da trilha."""
        self.assertIn("Intermediário", self.resultado)

    def test_certificado_contem_modulos(self):
        """O certificado deve conter a quantidade de módulos."""
        trilha = _buscar_trilha("Java")
        self.assertIn(str(trilha["numero_modulo"]), self.resultado)

    def test_certificado_contem_badges(self):
        """O certificado deve conter as badges da trilha Java."""
        trilha = _buscar_trilha("Java")
        for badge in trilha["badges_disponiveis"]:
            self.assertIn(badge, self.resultado)

    def test_certificado_contem_codigo_verificacao(self):
        """O certificado deve conter um código de verificação DIO."""
        self.assertIn("DIO-", self.resultado)

    def test_certificado_contem_data_emissao(self):
        """O certificado deve conter a data de emissão."""
        self.assertIn("Data de Emissão", self.resultado)

    def test_certificado_contem_aviso_ficticio(self):
        """O certificado deve conter aviso de que é fictício."""
        self.assertIn("fictício", self.resultado)

    def test_certificado_contem_link_dio(self):
        """O certificado deve conter link para web.dio.me."""
        self.assertIn("web.dio.me", self.resultado)

    def test_certificado_trilha_inexistente(self):
        """Para trilha inexistente deve retornar mensagem de erro."""
        resultado = cmd_certificado("Weverson RS", "COBOL_XYZ_INEXISTENTE")
        self.assertIn("❌", resultado)
        self.assertIn("não encontrada", resultado)

    def test_certificado_vitalicio_java(self):
        """A trilha Java é vitalícia — deve aparecer 'Sim' no certificado."""
        self.assertIn("Sim", self.resultado)

    def test_certificado_codigo_formato_correto(self):
        """O código de verificação deve seguir o padrão DIO-XX-AAAA-NNNNNN."""
        padrao = r"DIO-\d{2}-\d{4}-\d{6}"
        self.assertRegex(self.resultado, padrao)


# ===========================================================================
# Runner com relatório em .txt
# ===========================================================================

if __name__ == "__main__":
    import io
    from datetime import datetime

    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "dio_explorer", "docs")
    os.makedirs(output_dir, exist_ok=True)
    resultado_path = os.path.join(output_dir, "resultado_testes.txt")

    # Captura saída do runner
    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    resultado = runner.run(suite)

    total = resultado.testsRun
    falhas = len(resultado.failures)
    erros = len(resultado.errors)
    aprovados = total - falhas - erros
    cobertura = (aprovados / total * 100) if total > 0 else 0
    status_geral = "[APROVADO]" if cobertura >= 70 else "[REPROVADO]"

    relatorio = []
    relatorio.append("=" * 70)
    relatorio.append("  RELATÓRIO DE TESTES — DIO EXPLORER")
    relatorio.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    relatorio.append("=" * 70)
    relatorio.append("")
    relatorio.append("DETALHAMENTO DOS TESTES")
    relatorio.append("-" * 70)
    relatorio.append(buffer.getvalue())
    relatorio.append("-" * 70)
    relatorio.append("RESUMO")
    relatorio.append("-" * 70)
    relatorio.append(f"  Total de testes executados : {total}")
    relatorio.append(f"  Aprovados                  : {aprovados}")
    relatorio.append(f"  Falhas                     : {falhas}")
    relatorio.append(f"  Erros                      : {erros}")
    relatorio.append(f"  Taxa de aprovação          : {cobertura:.1f}%")
    relatorio.append(f"  Meta mínima                : 70.0%")
    relatorio.append(f"  Status geral               : {status_geral}")
    relatorio.append("")

    if resultado.failures:
        relatorio.append("FALHAS DETALHADAS")
        relatorio.append("-" * 70)
        for test, msg in resultado.failures:
            relatorio.append(f"FALHA: {test}")
            relatorio.append(msg.encode("ascii", "replace").decode("ascii"))
            relatorio.append("")

    if resultado.errors:
        relatorio.append("ERROS DETALHADOS")
        relatorio.append("-" * 70)
        for test, msg in resultado.errors:
            relatorio.append(f"ERRO: {test}")
            relatorio.append(msg.encode("ascii", "replace").decode("ascii"))
            relatorio.append("")

    relatorio.append("=" * 70)
    conteudo = "\n".join(relatorio)

    with open(resultado_path, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(conteudo.encode("ascii", "replace").decode("ascii"))
    print(f"\nResultados gravados em: {resultado_path}")
    sys.exit(0 if cobertura >= 70 else 1)
