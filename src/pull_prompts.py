"""
Script para fazer pull de prompts do LangSmith Prompt Hub.
"""

import os
import sys
import yaml
from dotenv import load_dotenv
from langchain import hub
from utils import check_env_vars, print_section_header

load_dotenv()

def pull_prompts_from_langsmith():
    # Repositório original do desafio
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    yaml_path = "prompts/bug_to_user_story_v1.yml"
    
    print(f"Puxando prompt '{prompt_name}' do LangSmith Hub...")
    
    try:
        # 1. Faz o pull do objeto no Hub
        prompt_template = hub.pull(prompt_name)
        
        # 2. Extrai as mensagens (System e Human) do objeto LangChain
        system_prompt = ""
        user_prompt = ""
        
        for msg in prompt_template.messages:
            prompt_type = msg.__class__.__name__
            if "System" in prompt_type:
                system_prompt = msg.prompt.template
            elif "Human" in prompt_type:
                user_prompt = msg.prompt.template
        
        # 3. Monta a estrutura de dicionário para virar um YAML limpo
        yaml_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt inicial (ruim) puxado do repositório base.",
                "system_prompt": system_prompt.strip(),
                "user_prompt": user_prompt.strip(),
                "metadata": {
                    "version": "v1",
                    "tags": ["bug-analysis", "user-story"]
                }
            }
        }
        
        # 4. Cria a pasta prompts caso ela não exista
        os.makedirs("prompts", exist_ok=True)
        
        # 5. Salva no arquivo YAML
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
        print(f"\n✅ PULL REALIZADO COM SUCESSO!")
        print(f"O prompt ruim original foi salvo em: {yaml_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO AO FAZER PULL DO PROMPT: {e}")
        print("Dica: Verifique se sua LANGSMITH_API_KEY está configurada no .env e se tem acesso à internet.")
        return False

def main():
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")
    
    # Checa se a chave API está configurada (obrigatório para o pull)
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
        
    success = pull_prompts_from_langsmith()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())