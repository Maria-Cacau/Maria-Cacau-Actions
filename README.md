# Maria-Cacau-Actions

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Language](https://img.shields.io/badge/language-Python-blue?logo=python)
![Language](https://img.shields.io/badge/language-Bash-4EAA25?logo=gnubash&logoColor=white)

</br>

Repositório central de GitHub Actions da organização [Maria Cacau](https://github.com/Maria-Cacau):
Composite Actions e Reusable Workflows consumidos pelos demais repositórios 

- [Requerimentos](#requerimentos)
- [Estrutura](#estrutura)
- [Padrões](#padrões)
- [Como consumir](#como-consumir)
- [Versionamento](#versionamento)
- [Testar localmente](#testar-localmente)

## Requerimentos

| Linguagem | Versão |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | 3.13.x |

## Estrutura

| Pasta | O que é |
|---|---|
| `.github/workflows/` | Reusable Workflows (`on: workflow_call`) — orquestram as Composite Actions |
| `actions/` | Composite Actions, uma pasta por action — cada uma com `action.yml` + script próprio |

## Padrões

| Linguagem | Quando usar |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | Padrão (recomendado) |
| ![Bash](https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=white) | Cenários curtos |

> ![NOTE]
> Scripts nunca ficam inline no YAML — sempre em arquivo separado dentro da pasta da action.

## Como consumir

Cada repo consumidor declara seu próprio gatilho (`on: push`, `paths`, etc.) e chama o Reusable
Workflow daqui — este repositório não sabe *quando* deve rodar, só *o que* faz.

```yaml
# ex: Maria-Cacau-App/.github/workflows/develop.yml
on:
  push:
    branches: [develop]
    paths: ['maria_cacau/**/*.py']

jobs:
  standardize:
    uses: Maria-Cacau/Maria-Cacau-Actions/.github/workflows/code-standardize.yml@v1
```

## Versionamento

Repositório **trunk-based** — sem branch `develop`, tudo flui direto pra `main` via PR. Releases
são marcadas por tag (`v1`, `v1.2.0`), nunca referenciadas por `@main` em produção.

## Testar localmente

Workflows e actions podem ser testados antes do push com [`act`](https://github.com/nektos/act)
(roda os jobs num container Docker simulando o runner da GitHub).

```bash
act -l              # lista os jobs disponíveis
act -j <job>        # roda um job específico
```
