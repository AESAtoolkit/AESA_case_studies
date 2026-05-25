# AESA_case_studies

Open repository for reproducible Absolute Environmental Sustainability Assessment (AESA) case studies.

This repository is intended to help researchers and practitioners share AESA studies with the material needed to understand, inspect, and reproduce them. When available, each case study should indicate the source from which it originates, such as a scientific article, report, preprint, thesis, technical document, or other reference material.

## Relation to `pyaesa`

<img src="https://raw.githubusercontent.com/AESAtoolkit/pyaesa/main/images/fig-pyaesa-logo.png" alt="pyaesa" width="180">

This repository is designed to facilitate reproducible `pyaesa` case studies by encouraging contributors to report the `pyaesa` version, configuration files, workflow scripts, and external inputs needed to reproduce an AESA case study.

However, the repository is open to AESA case studies implemented with other tools, provided that the workflow and assumptions are sufficiently documented.

Resources for `pyaesa`: [GitHub](https://github.com/AESAtoolkit/pyaesa) and [Read the Docs](https://pyaesa.readthedocs.io/).

## Purpose

The repository aims to provide a common space for reproducible AESA studies, including:

- workflow scripts or notebooks;
- software(s), software versions, and computing environment information;
- input data references;
- configuration files;
- results and figures;
- documentation needed to reproduce the case study;
- a reference to the scientific article, report, preprint, thesis, or other source document where the case study can be found when available.

The goal is not only to store final outputs when available, but also to make clear how these outputs were produced and where the methodological basis of the case study is documented.

## Repository organization

Case studies are organized by AESA level:

```text
AESA_case_studies/
│
├── level_1_country/
├── level_2_sector/
├── level_3_company/
├── level_4_product/
├── level_5_person/
└── README.md
```

## Definition of the levels

| AESA level | Folder | Scope |
|---|---|---|
| L1 | [`level_1_country/`](level_1_country/) | Country level AESA studies |
| L2 | [`level_2_sector/`](level_2_sector/) | Sector or industry level AESA studies |
| L3 | [`level_3_company/`](level_3_company/) | Company or organization level AESA studies |
| L4 | [`level_4_product/`](level_4_product/) | Product, service, or technology level AESA studies |
| L5 | [`level_5_person/`](level_5_person/) | Person, household, or individual consumption level AESA studies |

## Adding a case study

Contributors should add case studies through a fork and pull request workflow:

1. Fork the repository.
2. Create a branch in the fork with a clear name, for example `case_study_level_2_electricity_france_2019_2060`.
3. Add the case study under the relevant AESA level folder using a clear, descriptive folder name.
4. Include the minimum case study information listed below.
5. Open a pull request from the fork branch to `main`.
6. Wait for maintainer review before the case study is merged.

For example:

```text
level_2_sector/
└── electricity_france_2019-2060/
```

or:

```text
level_4_product/
└── bicycle_belgium_2025/
```

## Minimum information for a case study

Each case study should include a local `README.md` with at least:

1. Study title.
2. Reference to the scientific article, report, preprint, thesis, or other source document where the case study can be found when available.
3. Authors and contact information.
4. Short description of the system assessed.
5. Software(s) used and software versions.
6. Input data sources.
7. Main workflow steps.
8. Instructions to reproduce the outputs.
9. License or reuse conditions for the case study material, when relevant.

## Optional case study folder template

Contributors may use the following folder structure for an individual case study:

```text
case_study_title/
├── README.md
├── environment/
├── input_references/
├── workflow/
├── outputs/
├── figures/
└── references/
```

Suggested contents:

| Folder | Content |
|---|---|
| `environment/` | Software(s), software versions, dependency files, environment export files, or installation instructions |
| `input_references/` | References to input datasets and instructions to access them |
| `workflow/` | Scripts, notebooks, configuration files, and execution instructions |
| `outputs/` | Result tables |
| `figures/` | Figures generated from the workflow |
| `references/` | Full citation, DOI, persistent link, or notes identifying the scientific article, report, preprint, thesis, or other source document where the case study can be found |

This structure is optional. Contributors may use another structure if the case study remains clear and reproducible.

Large datasets should generally not be committed directly to the repository unless their license and file size make this appropriate. Prefer references to official data sources or external archives, for example Zenodo.
