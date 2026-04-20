"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.
"""

import os
import sys
import yaml
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, print_section_header

load_dotenv()

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """Valida estrutura básica de um prompt."""
    errors = []
    if "system_prompt" not in prompt_data or not prompt_data["system_prompt"].strip():
        errors.append("Falta o 'system_prompt'.")
    if "user_prompt" not in prompt_data or not prompt_data["user_prompt"].strip():
        errors.append("Falta o 'user_prompt'.")
        
    return len(errors) == 0, errors

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """Faz push do prompt otimizado para o LangSmith Hub."""
    
    # 1. Pega o Handle (Username) do LangSmith a partir do .env
    langsmith_handle = os.getenv("USERNAME_LANGSMITH_HUB")
    
    if not langsmith_handle:
        print("\n⚠️ ALERTA: Variável USERNAME_LANGSMITH_HUB não encontrada no .env.")
        print("Para enviar ao Hub, precisamos do seu username do LangSmith (ex: danilosong).")
        langsmith_handle = input("Digite seu Username do LangSmith agora: ").strip()
        
        if not langsmith_handle:
            print("❌ Push cancelado. Username é obrigatório.")
            return False

    repo_full_name = f"{langsmith_handle}/{prompt_name}"
    
    # 2. Converte as strings do YAML em um objeto oficial do LangChain
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"])
        ])
    except Exception as e:
        print(f"❌ Erro ao converter o template do LangChain: {e}")
        return False

    # 3. Faz o push real para a nuvem
    print(f"Enviando para o repositório: {repo_full_name}...")
    try:
        url = hub.push(repo_full_name, prompt_template)
        print(f"\n✅ PUSH REALIZADO COM SUCESSO!")
        print(f"🔗 URL Pública: {url}")
        return True
    except Exception as e:
        err = str(e)
        if "409" in err or "Nothing to commit" in err or "prompt has not changed" in err.lower():
            print("\n⚠️  Hub recusou: o prompt é idêntico ao último commit (409 Conflict).")
            print("   Nada foi publicado de novo — a avaliação já usa essa versão no LangSmith.")
            print("   Para forçar novo commit: altere o YAML (ex.: metadata.iteration ou uma linha no system_prompt).")
            return True
        print(f"\n❌ ERRO FATAL AO FAZER PUSH:")
        print(f"{e}")
        print("\nDica: Verifique se sua LANGSMITH_API_KEY tem permissão de escrita no Hub.")
        return False

def main():
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")
    
    # Checa se a chave API está configurada
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    yaml_path = "prompts/bug_to_user_story_v2.yml"
    prompt_name = "bug_to_user_story_v2"

    print(f"Lendo arquivo: {yaml_path}")
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo YAML: {e}")
        return 1

    if prompt_name not in data:
        print(f"❌ Chave '{prompt_name}' não encontrada dentro do arquivo YAML.")
        return 1

    prompt_data = data[prompt_name]

    # Validação
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Erros de validação encontrados no YAML:")
        for erro in errors:
            print(f"  - {erro}")
        return 1

    print("✓ Arquivo YAML validado com sucesso.")

    # Executa o Push
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())