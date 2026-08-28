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
- [Validação](#validação)
- [Workflows & Actions](#workflows--actions)

## Requerimentos

| Linguagem | Versão |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | 3.13.x |

## Estrutura

| Pasta | O que é |
|---|---|
| `.github/workflows/` | Reusable Workflows (`on: workflow_call`) — orquestram as Composite Actions |
| `actions/` | Composite Actions, uma pasta por action — cada uma com `action.yml` + script próprio |
| `actions/git/` | Composite Actions ligadas a operações de git/GitHub (branch, tag, commit, PR, release) |

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

## Validação

Workflows e actions podem ser testados localmente antes do push com
[`act`](https://github.com/nektos/act) (roda os jobs num container Docker simulando o runner da
GitHub):

```bash
act -l              # lista os jobs disponíveis
act -j <job>        # roda um job específico
```

Fluxos que criam artefatos reais (release, tag, `.exe`) são arriscados de testar direto num repo
de produção — para esses, a validação acontece via
[`Maria-Cacau-App-Sandbox`](https://github.com/Maria-Cacau/Maria-Cacau-App-Sandbox), um fork do
`Maria-Cacau-App` isolado só pra esse propósito.

## Workflows & Actions

### Workflows

<table>
  <tr>
    <th>Nome</th>
    <th>Descrição</th>
  </tr>
  <tr>
    <td><a href=".github/workflows/code-standardize.yml">code-standardize</a></td>
    <td>Ajusta imports (isort) e atualiza o grafo de conhecimento (graphify) do repo consumidor.</td>
  </tr>
  <tr>
    <td><a href=".github/workflows/app-distribution.yml">app-distribution</a></td>
    <td>Valida versão/branch, gera o <code>.exe</code> via Nuitka e publica a release com o asset.</td>
  </tr>
  <tr>
    <td><a href=".github/workflows/publish-release.yml">publish-release</a></td>
    <td>Valida versão/branch e publica a release — sem etapa de build, pra repos sem app distribuível.</td>
  </tr>
  <tr>
    <td><a href=".github/workflows/pr-release.yml">pr-release</a></td>
    <td>Cria a branch de release, faz o bump de versão e abre o PR pra main.</td>
  </tr>
</table>

### Actions

<table>
  <tr>
    <th>Nome</th>
    <th>Descrição</th>
  </tr>
  <tr>
    <td><a href="actions/build/action.yml">build</a></td>
    <td>Roda o script de build do próprio repo consumidor (build.bat/build.sh) e expõe o Python resultante.</td>
  </tr>
  <tr>
    <td><a href="actions/nuitka/action.yml">nuitka</a></td>
    <td>Descobre o módulo de entrada, valida a metadata exigida e gera o <code>.exe</code> via Nuitka.</td>
  </tr>
  <tr>
    <td><a href="actions/check-version/action.yml">check-version</a></td>
    <td>Compara a versão do pyproject.toml contra a última release já publicada.</td>
  </tr>
  <tr>
    <td><a href="actions/isort-fix/action.yml">isort-fix</a></td>
    <td>Ajusta a ordenação dos imports Python com isort.</td>
  </tr>
  <tr>
    <td><a href="actions/graphify-update/action.yml">graphify-update</a></td>
    <td>Atualiza o grafo de conhecimento do projeto com graphify.</td>
  </tr>
  <tr>
    <td><a href="actions/git/branch-check/action.yml">git/branch-check</a></td>
    <td>Valida que o workflow está rodando a partir da branch esperada.</td>
  </tr>
  <tr>
    <td><a href="actions/git/commit-bot/action.yml">git/commit-bot</a></td>
    <td>Configura a identidade do bot, comita o que estiver alterado e dá push.</td>
  </tr>
  <tr>
    <td><a href="actions/git/branch-release/action.yml">git/branch-release</a></td>
    <td>Calcula a nova versão, cria a branch release/&lt;versão&gt; e bumpa o pyproject.toml.</td>
  </tr>
  <tr>
    <td><a href="actions/git/badge-update/action.yml">git/badge-update</a></td>
    <td>Atualiza o badge de versão e o link de release no README.md do repo.</td>
  </tr>
  <tr>
    <td><a href="actions/git/pr-ensure/action.yml">git/pr-ensure</a></td>
    <td>Cria (ou reaproveita/reabre) o PR de uma branch pra uma branch de destino.</td>
  </tr>
  <tr>
    <td><a href="actions/git/release-publish/action.yml">git/release-publish</a></td>
    <td>Cria/reaproveita a release, preenche a descrição a partir do PR e sobe um asset opcional.</td>
  </tr>
  <tr>
    <td><a href="actions/git/tag-create/action.yml">git/tag-create</a></td>
    <td>Cria (ou move) uma tag apontando pro commit atual.</td>
  </tr>
  <tr>
    <td><a href="actions/git/tag-delete/action.yml">git/tag-delete</a></td>
    <td>Remove a tag de teste correspondente a uma versão publicada.</td>
  </tr>
  <tr>
    <td><a href="actions/git/actions-notice/action.yml">git/actions-notice</a></td>
    <td>Emite uma annotation de notice no run.</td>
  </tr>
  <tr>
    <td><a href="actions/git/actions-cache-clear/action.yml">git/actions-cache-clear</a></td>
    <td>Apaga uma entrada de cache do Actions por chave.</td>
  </tr>
</table>
