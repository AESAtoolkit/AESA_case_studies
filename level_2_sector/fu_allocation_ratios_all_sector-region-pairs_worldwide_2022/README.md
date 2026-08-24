# FU allocation ratios and deterministic ASR

*EXIOBASE 3.10.2, GWP100, studied year 2022.*

## Reference

de Bantel, E. I., Pirson, T., Puig-Samper, G., Hartmann, J. M., Bouillass, G.,
Yannou, B., Jankovic, M., Bol, D., & Hauschild, M. Z. *UNCASExt: A Systematic
Computational Framework for Uncertainty Propagation and Scope Consistency in
Absolute Environmental Sustainability Assessments (AESA).* Manuscript submitted
for publication.

## Software requirements

Install pyaesa v1.2.8:

```bash
pip install pyaesa==1.2.8
```

LCIA:

- `gwp100_lcia

(possible to switch/add pb_lcia)

## Study scope

This folder contains two deterministic analyses for all EXIOBASE 3.10.2 ixi
MRIO sector and region pairs represented by the pyaesa `elec` sector
aggregation. This aggregation groups the EXIOBASE electricity sectors and
retains 150 sector groups across 49 EXIOBASE regions, giving 7,350 sector and
region pairs.

Both analyses use:

- MRIO source `exiobase_3102_ixi`;
- studied year 2022;
- aggregation version `elec`;
- deterministic calculations only.

## Workflow

### Allocation ratio analysis

`compute_allocation_ratios.py` quantifies how the allocation FU changes the
aSoCC in Phase B.

The reference denominator is `L2.c.b`, CBA impacts of total demand. The tested
numerators are:

- `L2.c.a`, CBA impacts of final demand;
- `L2.a.c`, PBA impacts of total output.

A ratio greater than 1 means that the numerator FU produces a larger aSoCC than
the `L2.c.b` reference for the same allocation method, sector, and region. A
ratio below 1 means that it produces a smaller aSoCC.

The analysis uses acquired rights reference year 1995. Its detailed table has
88,200 rows: 12 allocation method ratio definitions for each of the 7,350
sector and region pairs.

### Deterministic ASR analysis

`compute_deterministic_asr_all_fus.ipynb` computes Phase C deterministic ASR
for five FUs:

- `L2.a.a` with axes `r_p` and `s_p`;
- `L2.a.b` with axes `r_p` and `s_p`;
- `L2.a.c` with axes `r_p` and `s_p`;
- `L2.c.a` with axes `r_f` and `s_p`;
- `L2.c.b` with axes `r_c` and `s_p`.

Each FU has a separate pyaesa project. No region, sector, or allocation method
selector is passed to `deterministic_asr`, so every valid pair and every default
pyaesa allocation method for that FU are evaluated.

The ASR workflow uses retrospective MRIO years 1995 through 2022, acquired
rights reference years 1995 and 2022, deterministic IO LCA as the numerator, and
the static GWP100 CC with `cc_bound = min_cc`.

## Reproduce the study

### Allocation ratio analysis

1. Replace the `/path/to/pyaesa_workspace` placeholder assigned to
   `WORKSPACE_PATH` in `compute_allocation_ratios.py`.
2. Run `python compute_allocation_ratios.py` from this folder.
3. Inspect the generated CSV files under
   `<workspace>/uncasext_fu_ratio__ratio/csv/`.

### Deterministic ASR analysis

1. Open `compute_deterministic_asr_all_fus.ipynb`.
2. Replace the `/path/to/pyaesa_workspace` placeholder assigned to
   `WORKSPACE_ROOT` in the configuration cell.
3. Run the notebook from top to bottom.
4. Allow the download and processing cells to complete before starting the five
   ASR projects. Processing 28 EXIOBASE years is resource intensive.
5. Run the synthesis cells after all five project runs have completed.

Neither workflow requests `refresh=True`. Existing valid pyaesa downloads and
processed assets are reused.

## Folder inventory

```text
README.md
compute_allocation_ratios.py
compute_deterministic_asr_all_fus.ipynb
fu_ratios_results_2022/
    allocation_ratio_distribution.csv
    allocation_ratio_stats_by_sector_country.csv
    allocation_ratio_stats_world.csv
    fig-allocation-ratios-fus.pdf
    fig-allocation-ratios-fus.svg
fu_asr_results_2022/
    asr_fu_L2_a_a_results_2022.csv
    asr_fu_L2_a_b_results_2022.csv
    asr_fu_L2_a_c_results_2022.csv
    asr_fu_L2_c_a_results_2022.csv
    asr_fu_L2_c_b_results_2022.csv
    asr_fu_ridgelines.pdf
    asr_fu_ridgelines.svg
```

## Retained outputs

### Allocation ratio outputs

- `fu_ratios_results_2022/allocation_ratio_distribution.csv`: detailed
  numerator, denominator, and ratio values;
- `fu_ratios_results_2022/allocation_ratio_stats_world.csv`: world summary
  statistics for every allocation method and FU ratio;
- `fu_ratios_results_2022/allocation_ratio_stats_by_sector_country.csv`:
  summary statistics for all 7,350 sector and region pairs;
- `fu_ratios_results_2022/fig-allocation-ratios-fus.svg` and
  `fu_ratios_results_2022/fig-allocation-ratios-fus.pdf`: vector versions of
  the three panel publication figure comparing `L2.c.a` and `L2.a.c` with the
  `L2.c.b` reference.

### Deterministic ASR outputs

Native pyaesa Parquet outputs are written below each workspace project:

- `<workspace>/<fu_code>/A_lca/...` for IO LCA;
- `<workspace>/<fu_code>/B1_asocc/...` for aSoCC;
- `<workspace>/<fu_code>/B2_acc/...` for aCC;
- `<workspace>/<fu_code>/C_asr/...` for ASR.

The notebook writes the combined CSV to:

`<workspace>/synthesis_fus/deterministic_asr_all_fus_2022.csv`

The distributed results are split into one CSV per FU so that each file remains
below GitHub's single file size limit:

- `fu_asr_results_2022/asr_fu_L2_a_a_results_2022.csv`;
- `fu_asr_results_2022/asr_fu_L2_a_b_results_2022.csv`;
- `fu_asr_results_2022/asr_fu_L2_a_c_results_2022.csv`;
- `fu_asr_results_2022/asr_fu_L2_c_a_results_2022.csv`;
- `fu_asr_results_2022/asr_fu_L2_c_b_results_2022.csv`.

Every CSV uses the columns `fu_code`, `source`, `agg_version`, `lcia_method`,
`impact`, `impact_unit`, `cc_type`, `cc_bound`, `l1_l2_method`,
`reference_year`, `r_p`, `r_c`, `r_f`, `s_p`, `year`, `io_lca`, `asocc`, `cc`,
`acc`, and `asr`.

`fu_asr_results_2022/asr_fu_ridgelines.svg` and
`fu_asr_results_2022/asr_fu_ridgelines.pdf` are vector versions of the
deterministic ASR ridgeline figure for the five FUs.
