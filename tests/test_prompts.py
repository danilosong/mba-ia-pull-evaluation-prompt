"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @classmethod
    def setup_class(cls):
        """Carrega o arquivo YAML otimizado uma única vez para todos os testes."""
        yaml_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        
        # Carrega o YAML e isola os dados do prompt v2
        data = load_prompts(str(yaml_path))
        cls.prompt_data = data.get("bug_to_user_story_v2", {})
        cls.system_prompt = cls.prompt_data.get("system_prompt", "")
        cls.metadata = cls.prompt_data.get("metadata", {})

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "A chave 'system_prompt' não existe no YAML."
        assert self.system_prompt is not None, "O 'system_prompt' está nulo."
        assert len(self.system_prompt.strip()) > 0, "O 'system_prompt' está vazio."

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_lower = self.system_prompt.lower()
        role_keywords = ["você é", "product manager", "product owner", "atua como", "sua função é"]
        
        # O teste passa se pelo menos uma das palavras-chave estiver no texto
        has_role = any(keyword in prompt_lower for keyword in role_keywords)
        assert has_role, "Nenhuma definição de persona clara foi encontrada no system_prompt."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_lower = self.system_prompt.lower()
        format_keywords = ["markdown", "user story", "formato", "critérios de aceitação"]
        
        has_format = any(keyword in prompt_lower for keyword in format_keywords)
        assert has_format, "O prompt não exige de forma explícita o formato (Markdown ou User Story)."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_lower = self.system_prompt.lower()
        
        # Garante que as palavras de estrutura de exemplos existam
        assert "exemplo" in prompt_lower, "A palavra 'exemplo' não foi encontrada."
        assert "entrada:" in prompt_lower or "entrada" in prompt_lower, "A indicação da 'entrada' do exemplo está ausente."
        assert "saída:" in prompt_lower or "saída" in prompt_lower, "A indicação da 'saída' do exemplo está ausente."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        # Procurando a tag literal de TODO que costuma vir em templates
        assert "[todo]" not in self.system_prompt.lower(), "Atenção: Você esqueceu a tag [TODO] no system_prompt."
        assert "<todo>" not in self.system_prompt.lower(), "Atenção: Você esqueceu a tag <TODO> no system_prompt."

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert "techniques" in self.metadata, "A chave 'techniques' não foi encontrada dentro de 'metadata'."
        
        techniques = self.metadata["techniques"]
        assert isinstance(techniques, list), "As técnicas nos metadados devem ser uma lista."
        assert len(techniques) >= 2, f"Foram listadas apenas {len(techniques)} técnicas. O mínimo exigido são 2."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])