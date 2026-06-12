<table style="width: 600px; border: none;" cellpadding="10" align="center">
  <tr>
    <td align="center">
      <img src="images/iPOP-up_logo.png" alt="iPOP-up" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/U-Paris-Cite-logo.png" alt="Université Paris-Cité" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/IFB-logo.png" alt="IFB" style="height: 65px; width: auto;">
    </td>
    <td align="center">
      <img src="images/ELIXIR-France_logo.png" alt="ELIXIR-FR" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/MERIT-logo.png" alt="MERIT" style="height: 50px; width: auto;">
    </td>
  </tr>
</table>

# Reproduction de la Figure 2A — *Cell-Cycle-Regulated Transcription*

Ce dépôt reproduit la **Figure 2A** de Kelliher *et al.* 2016 (*PLOS Genetics*,
[10.1371/journal.pgen.1006453](https://doi.org/10.1371/journal.pgen.1006453)) :
une **heatmap des gènes périodiques du cycle cellulaire** de *Saccharomyces
cerevisiae*. La figure est reconstruite **à partir des données brutes**, puis le
code est mis aux normes de développement logiciel et de science ouverte.

> Réalisé dans le cadre de l'atelier *« Utilisation des IA génératives comme appui
> à la programmation et au scripting pour la biologie »* (IFB / Université Paris
> Cité / MERIT) — **groupe XX, reverse engineering**. Le sujet d'origine est le
> dépôt [IFB-ElixirFr/IA-BioSoftware-Workshop](https://github.com/IFB-ElixirFr/IA-BioSoftware-Workshop).

<p align="center">
  <img src="tp_python/figure_2a.png" alt="Figure 2A reproduite (Python)" height="320">
</p>

## Ce qui a été fait

La même figure a été reproduite **deux fois**, en **Python** et en **R**, chaque
version étant accompagnée d'une mise aux normes complète (environnement
reproductible, qualité, sécurité, tests, documentation, CI).

### La démarche scientifique (rétro-ingénierie de la figure)

1. **Chargement** des profils d'expression RNA-seq (`data/oscillating-genes_1705_normalized-profiles.tsv`) : 1705 gènes × 50 points temporels (1 prélèvement / 5 min, accession GEO **GSE80474**).
2. **Normalisation z-score** par gène : `(x − moyenne) / écart-type`.
3. **Tri des gènes par phase du pic** d'expression, extraite de la composante de Fourier à la période du cycle cellulaire (~75 min) → fait apparaître les vagues diagonales de transcription successives.
4. **Heatmap** : colormap cyan → noir → jaune, bornée à [−1.5, +1.5], comme dans l'article.

## Les deux implémentations

| | Python — [`tp_python/`](tp_python) | R — [`tp_r/cellcyclefig2a/`](tp_r/cellcyclefig2a) |
|---|---|---|
| Environnement | **Pixi** (`pixi.toml`) | **renv** (`renv.lock`) |
| Qualité / style | **ruff** | **styler** + **lintr** (0 warning) |
| Typage / doc | **pyright** (0 erreur) | **roxygen2** (package R documenté) |
| Sécurité | **safety** + **trivy** (0 vuln) | **oysteR** (voir note ci-dessous) |
| Tests | **pytest** — 12 tests | **testthat** — 18 tests |
| Couverture | **99 %** | **100 %** |
| Vérification | CI verte | `R CMD check` : **0 error / 0 warning / 0 note** |

### Démarrage rapide

**Python**
```bash
cd tp_python
pixi install
pixi run python figure_2a.py        # génère figure_2a.png
pixi run all-checks                 # lint + typecheck + tests
```

**R**
```bash
cd tp_r/cellcyclefig2a
Rscript -e 'renv::restore()'
Rscript run.R                       # génère figure_2a.png
Rscript -e 'devtools::check()'      # vérification complète du package
```

## Science ouverte

Le dépôt suit les recommandations de
[`instruction_bonne_pratique.md`](instruction_bonne_pratique.md) :

- **Licence** : code sous **MIT** (matériel pédagogique d'origine sous CC BY-SA 4.0).
- **Citabilité** : [`CITATION.cff`](tp_python/CITATION.cff) + [`codemeta.json`](tp_python/codemeta.json) (auteur, ORCID, affiliation).
- **Communauté** : [`CONTRIBUTING`](.github/CONTRIBUTING.md), templates d'issues et de Pull Request.
- **Intégration continue** : [`.github/workflows/`](.github/workflows) — CI qualité (lint, types, sécurité, tests) + CI de release (changelog automatique via git-cliff).
- **Pre-commit** : `.pre-commit-config.yaml` (whitespace, secrets, ruff…).

> **Note — audit `oysteR` (R)** : l'audit des dépendances R interroge l'API
> Sonatype OSS Index, qui requiert désormais une authentification (un compte
> gratuit suffit). Sans identifiants l'API renvoie HTTP 401 ; la marche à suivre
> est documentée dans le [README du package R](tp_r/cellcyclefig2a/README.md).

## Structure du dépôt

```
.
├── data/                       # Article (PDF) + données d'expression
├── tp_python/                  # Implémentation Python (Pixi)
│   ├── figure_2a.py            #   pipeline de reproduction
│   ├── tests/                  #   tests pytest
│   ├── pixi.toml / pyproject.toml
│   ├── CITATION.cff / codemeta.json
│   └── README.md
├── tp_r/cellcyclefig2a/        # Implémentation R (package + renv)
│   ├── R/                      #   fonctions (load_data, process_data, visualize)
│   ├── tests/testthat/         #   tests testthat
│   ├── DESCRIPTION / NAMESPACE / renv.lock
│   └── README.md
└── .github/workflows/          # CI qualité + release
```

## Traçabilité de l'assistance IA

| | |
|---|---|
| **Groupe** | XX — reverse engineering |
| **Outil** | Claude Code |
| **Modèle** | Claude Opus 4.8 (`claude-opus-4-8`, confirmé via `/model`) |
| **Requêtes** | ~30 (prompts utilisateur de la session) |
| **Tokens** | ~248,9k au total (117,9k en entrée + 131,0k en sortie) |

## Licence

Le code de ce dépôt est distribué sous licence **MIT** (voir les fichiers
`LICENSE` dans `tp_python/` et `tp_r/cellcyclefig2a/`). Le matériel pédagogique
d'origine reste sous [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
Voir aussi le [Code de conduite](code_of_conduct.md).

## Référence

Kelliher CM, Leman AR, Sierra CS, Haase SB (2016) *Investigating Conservation of
the Cell-Cycle-Regulated Transcriptional Program in the Fungal Pathogen,
Cryptococcus neoformans.* PLOS Genetics 12(12): e1006453.
<https://doi.org/10.1371/journal.pgen.1006453>
