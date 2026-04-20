# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Projeto desenvolvido para a atividade de pull, otimização, push e avaliação de prompts usando LangChain, LangSmith Prompt Hub e métricas customizadas.

O caso trabalhado é a conversão de relatórios de bug em User Stories estruturadas.

## Objetivo

O software implementa o fluxo solicitado na atividade:

1. Fazer pull do prompt inicial de baixa qualidade no LangSmith Prompt Hub.
2. Salvar o prompt localmente em YAML.
3. Criar uma versão otimizada do prompt com técnicas de Prompt Engineering.
4. Fazer push da versão otimizada para o LangSmith Prompt Hub.
5. Avaliar o prompt com as métricas Helpfulness, Correctness, F1-Score, Clarity e Precision.
6. Validar a estrutura do prompt otimizado com testes automatizados.

## Estrutura do Projeto

```text
mba-ia-pull-evaluation-prompt/
├── .env.example
├── requirements.txt
├── README.md
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
└── tests/
    └── test_prompts.py
```

## Técnicas Aplicadas (Fase 2)

### Few-shot Learning

Usei Few-shot Learning porque a tarefa exige um padrão de saída específico: transformar um bug report em User Story com critérios de aceitação. Os exemplos ajudam o modelo a reproduzir a estrutura esperada.

No arquivo `prompts/bug_to_user_story_v2.yml`, o prompt contém exemplos com entrada e saída para diferentes tipos de bug, como validação de e-mail, problema de layout em iOS, métrica incorreta em dashboard, imagens não carregando no Safari, webhook de pagamento, relatório lento, falha de autorização em API, cálculo incorreto de desconto e travamento no Android.

Exemplo de aplicação no prompt:

```text
Entrada:
Campo de email aceita texto sem @, permitindo cadastros inválidos.

Saída:
Como um usuário criando uma conta, eu quero que o sistema valide meu email corretamente, para que eu não insira um endereço inválido por engano.

Critérios de Aceitação:
- Dado que estou no formulário de cadastro
- Quando digito um email sem o caractere @
- Então devo ver uma mensagem de erro
- E não devo conseguir prosseguir com o cadastro
- E a mensagem deve explicar o formato correto
```

### Chain of Thought (CoT)

Usei Chain of Thought como raciocínio interno. O prompt orienta o modelo a classificar a complexidade do bug, identificar fatos importantes e revisar se os dados foram preservados antes de gerar a resposta final.

O prompt também instrui o modelo a não escrever esse raciocínio na resposta final. Assim, a saída permanece objetiva e no formato solicitado.

Exemplo de aplicação no prompt:

```text
1) Classifique: simples, médio ou complexo.
2) Liste fatos do bug a preservar.
3) Escolha o template.
4) Revise se cada fato aparece na história ou nos critérios.
```

### Role Prompting

Usei Role Prompting para definir uma persona clara para o modelo. O prompt informa que o modelo deve atuar como Product Owner / Product Manager ágil experiente.

Essa técnica foi escolhida porque a saída esperada não é apenas uma reescrita do bug, mas uma User Story com linguagem de produto, critérios de aceitação e contexto útil para desenvolvimento.

Exemplo de aplicação no prompt:

```text
Você é um Product Owner / Product Manager ágil experiente.
```

### Skeleton of Thought

Usei Skeleton of Thought por meio de templates por complexidade. O prompt diferencia bugs simples, médios e complexos, indicando quais blocos devem aparecer em cada caso.

Essa técnica foi escolhida para evitar respostas desorganizadas e para manter consistência entre exemplos diferentes do dataset.

Exemplo de aplicação no prompt:

```text
Bug simples: só história + critérios.
Bug médio: critérios + blocos nomeados conforme o contexto.
Bug complexo: seções USER STORY PRINCIPAL, CRITÉRIOS DE ACEITAÇÃO, CRITÉRIOS TÉCNICOS, CONTEXTO DO BUG e TASKS.
```

## Prompt Otimizado

O prompt otimizado está em:

```text
prompts/bug_to_user_story_v2.yml
```

Ele contém:

- `system_prompt` com persona, regras, formato, tratamento de casos e exemplos.
- `user_prompt` recebendo o campo `{bug_report}`.
- `metadata` com versão e técnicas utilizadas.

As técnicas listadas no YAML são:

- Few-shot Learning.
- Chain of Thought (CoT).
- Role Prompting.
- Skeleton of Thought.

## Pull do Prompt Inicial

O script `src/pull_prompts.py` faz pull do prompt:

```text
leonanluppi/bug_to_user_story_v1
```

E salva o resultado em:

```text
prompts/bug_to_user_story_v1.yml
```

Comando:

```bash
python src/pull_prompts.py
```

## Push do Prompt Otimizado

O script `src/push_prompts.py` lê:

```text
prompts/bug_to_user_story_v2.yml
```

E publica o prompt otimizado no LangSmith Prompt Hub com o nome:

```text
bug_to_user_story_v2
```

O username do LangSmith é lido pela variável:

```text
USERNAME_LANGSMITH_HUB
```

Comando:

```bash
python src/push_prompts.py
```

## Resultados Finais

### Link do LangSmith

Projeto de avaliação no LangSmith:

```text
https://smith.langchain.com/public/1000ca55-68c6-4350-8d27-ed39d22b80fa/d
```

### Resultado da Última Execução

Última avaliação executada com:

```text
Provider: openai
Modelo Principal: gpt-4o
Modelo de Avaliação: gpt-4o
Dataset: prompt-optimization-challenge-resolved-eval
Exemplos carregados: 15
Prompt avaliado: bug_to_user_story_v2
```

Resultado agregado:

| Métrica | Resultado | Status |
| --- | ---: | :---: |
| Helpfulness | 0.94 | Atingiu 0.9 |
| Correctness | 0.93 | Atingiu 0.9 |
| F1-Score | 0.92 | Atingiu 0.9 |
| Clarity | 0.94 | Atingiu 0.9 |
| Precision | 0.94 | Atingiu 0.9 |
| Média geral | 0.9340 | Atingiu 0.9 |

### Status Final

O prompt `bug_to_user_story_v2` atingiu todas as 5 métricas com pontuação maior ou igual a 0.9. A média geral final foi `0.9340`.

URL pública do prompt publicado:

```text
https://smith.langchain.com/hub/danilosong/bug_to_user_story_v2
```

### Comparativo v1 vs v2

| Prompt | Helpfulness | Correctness | F1-Score | Clarity | Precision | Observação |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `bug_to_user_story_v1` | Não registrado neste README | Não registrado neste README | Não registrado neste README | Não registrado neste README | Não registrado neste README | Prompt inicial de baixa qualidade puxado do LangSmith |
| `bug_to_user_story_v2` | 0.94 | 0.93 | 0.92 | 0.94 | 0.94 | Prompt otimizado aprovado, com média geral 0.9340 |

### Screenshots e Evidências

Evidências a anexar ou manter no repositório/entrega:

- Screenshot do dashboard com as avaliações.
- Screenshot mostrando o dataset com 15 exemplos.
- Screenshot de pelo menos 3 traces detalhados.
- Screenshot da avaliação final com todas as métricas acima de 0.9.

## Testes de Validação

O arquivo `tests/test_prompts.py` implementa os testes solicitados:

- `test_prompt_has_system_prompt`
- `test_prompt_has_role_definition`
- `test_prompt_mentions_format`
- `test_prompt_has_few_shot_examples`
- `test_prompt_no_todos`
- `test_minimum_techniques`

Comando para executar:

```bash
pytest tests/test_prompts.py
```

## Como Executar

### 1. Criar e ativar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows:

```bash
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`.

Variáveis principais:

```text
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
USERNAME_LANGSMITH_HUB=

LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
EVAL_MODEL=gpt-4o
OPENAI_API_KEY=
```

Também é possível usar Gemini, conforme o `.env.example`.

### 4. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

### 5. Revisar ou editar o prompt otimizado

Arquivo:

```text
prompts/bug_to_user_story_v2.yml
```

### 6. Fazer push para o LangSmith Prompt Hub

```bash
python src/push_prompts.py
```

### 7. Executar avaliação

```bash
python src/evaluate.py
```

### 8. Executar testes

```bash
pytest tests/test_prompts.py
```

## Iterações Realizadas

O processo de otimização seguiu o ciclo:

1. Avaliar o prompt atual.
2. Identificar métricas abaixo de 0.9.
3. Ajustar o prompt em `prompts/bug_to_user_story_v2.yml`.
4. Fazer push novamente para o LangSmith.
5. Reexecutar `python src/evaluate.py`.

Durante as iterações, o principal ponto de melhoria foi o F1-Score. A análise mostrou que alguns exemplos retornados primeiro pelo LangSmith exigiam mais detalhes em casos médios e complexos, especialmente:

- Validação de estoque no checkout.
- Modal de confirmação em telas pequenas.
- Critérios técnicos e de prevenção em bugs complexos.

O prompt final adicionou regras específicas para esses casos, preservando a estrutura geral e os few-shots que já estavam funcionando.

## Evidências no LangSmith

As evidências esperadas para entrega são:

- Link público do dashboard do LangSmith.
- Dataset de avaliação com 15 exemplos.
- Execuções do prompt `bug_to_user_story_v2`.
- Notas das 5 métricas de avaliação acima de 0.9.
- Tracing detalhado de pelo menos 3 exemplos.

Links registrados:

```text
Dashboard:
https://smith.langchain.com/public/1000ca55-68c6-4350-8d27-ed39d22b80fa/d

Prompt publicado:
https://smith.langchain.com/hub/danilosong/bug_to_user_story_v2
```
