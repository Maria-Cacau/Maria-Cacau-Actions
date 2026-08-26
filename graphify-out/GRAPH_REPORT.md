# Graph Report - Maria-Cacau-Actions  (2026-08-26)

## Corpus Check
- 4 files · ~1,147 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 23 nodes · 23 edges · 5 communities (3 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `32e364e7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Maria-Cacau-Actions
- update_graph.py
- run_isort.py
- summary_row
- finish.sh

## God Nodes (most connected - your core abstractions)
1. `Maria-Cacau-Actions` - 7 edges
2. `force_rebuild()` - 4 edges
3. `main()` - 4 edges
4. `changed_files()` - 2 edges
5. `summary_row()` - 2 edges
6. `changed_files()` - 2 edges
7. `summary_row()` - 2 edges
8. `main()` - 2 edges
9. `Fallback quando `graphify update` recusa sobrescrever o grafo (guard-rail…` - 1 edges
10. `Linha de tabela pro summary combinado (isort + graphify), montado num step…` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (5 total, 2 thin omitted)

### Community 0 - "Maria-Cacau-Actions"
Cohesion: 0.25
Nodes (7): Como consumir, Estrutura, Maria-Cacau-Actions, Padrões, Requerimentos, Testar localmente, Versionamento

### Community 1 - "update_graph.py"
Cohesion: 0.53
Nodes (5): changed_files(), force_rebuild(), main(), Fallback quando `graphify update` recusa sobrescrever o grafo (guard-rail…, Path

### Community 2 - "run_isort.py"
Cohesion: 0.50
Nodes (4): changed_files(), main(), Linha de tabela pro summary combinado (isort + graphify), montado num step…, summary_row()

## Knowledge Gaps
- **7 isolated node(s):** `finish.sh script`, `Requerimentos`, `Estrutura`, `Padrões`, `Como consumir` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `summary_row()` connect `summary_row` to `update_graph.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **What connects `finish.sh script`, `Requerimentos`, `Estrutura` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._