# Electricity consumption ASR

*EU27, BRICS5, and USMCA, 1995–2022.*

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

- `pb_lcia`
- `gwp100_lcia`

## Study scope

This study evaluates electricity consumption for EU27, BRICS5, and USMCA using
FU `L2.c.b`. The aggregated production sector is `Electricity`, and the
consuming region axis is `r_c`.

The PB-LCIA route covers 1995 through 2022. The dynamic GWP100 CC route covers
2000 through 2022. Both routes use EXIOBASE 3.10.2 ixi for IO-LCA.
OECD v2025 is used with EXIOBASE to construct the inter-MRIO uncertainty source.

## Workflow

### Aggregation and disaggregation

The notebook uses custom mappings to aggregate EXIOBASE and OECD regions into
EU27, BRICS5, and USMCA, group the EXIOBASE electricity sectors, and align the
OECD aggregate sector `D` with the EXIOBASE `Electricity` sector. It computes
the deterministic aSoCCs required for the disaggregation and creates the
alternate source `oecd_electricity`.

Copy the five supplied aggregation mappings to these paths under the configured
pyaesa workspace before processing:

- `aggregation_csvs/exiobase_agg/agg_reg_elec_3regions_study.csv` to
  `<workspace>/data_raw/mrio/exiobase_3/aggregation/agg_reg_elec_3regions_study.csv`;
- `aggregation_csvs/exiobase_agg/agg_sec_elec_3regions_study.csv` to
  `<workspace>/data_raw/mrio/exiobase_3/aggregation/ixi/agg_sec_elec_3regions_study.csv`;
- `aggregation_csvs/exiobase_agg/agg_reg_oecd_d_3regions_study.csv` to
  `<workspace>/data_raw/mrio/exiobase_3/aggregation/agg_reg_oecd_d_3regions_study.csv`;
- `aggregation_csvs/exiobase_agg/agg_sec_oecd_d_3regions_study.csv` to
  `<workspace>/data_raw/mrio/exiobase_3/aggregation/ixi/agg_sec_oecd_d_3regions_study.csv`;
- `aggregation_csvs/oecd_v2025_agg/agg_reg_oecd_d_3regions_study.csv` to
  `<workspace>/data_raw/mrio/oecd_v2025/aggregation/agg_reg_oecd_d_3regions_study.csv`.

### ASR uncertainty analysis

`3regions_study_asr.ipynb` configures the pyaesa workspace, downloads and
processes the required population, GDP, AR6, EXIOBASE, and OECD data, builds the
inter-MRIO disaggregated source, and runs both ASR uncertainty routes.

The aSoCC uncertainty sources cover inter-MRIO uncertainty, the acquired rights
allocation method reference year unertainty, and inter-method uncertainty. The
GWP100 route uses dynamic IPCC AR6 CC for SSP2, including uncertainty across the
available IAMs and climate pathway categories C1 through C4.

Pyaesa writes the native results under the `3regions_study` project in the
configured workspace.

## Reproduce the study

1. Open `3regions_study_asr.ipynb`.
2. Replace the `/path/to/pyaesa_workspace` placeholder assigned to
   `WORKSPACE_ROOT` in the configuration cell.
3. Copy the five aggregation CSV files to the workspace paths listed above.
4. Run the notebook from top to bottom.
5. Allow the download and processing cells to complete before running
   deterministic aSoCC and disaggregation.
6. Run the PB-LCIA ASR uncertainty cell.
7. Run the GWP100 ASR uncertainty cell with dynamic AR6 CC.

## Folder inventory

```text
README.md
3regions_study_asr.ipynb
aggregation_csvs/
    exiobase_agg/
        agg_reg_elec_3regions_study.csv
        agg_reg_oecd_d_3regions_study.csv
        agg_sec_elec_3regions_study.csv
        agg_sec_oecd_d_3regions_study.csv
    oecd_v2025_agg/
        agg_reg_oecd_d_3regions_study.csv
im_sp_Electricity_rc_EU27_BRICS5_USMCA_ft.pdf
im_sp_Electricity_rc_EU27_BRICS5_USMCA_ft.svg
im_sp_Electricity_rc_EU27_BRICS5_USMCA_p5_p95_mean_only.pdf
im_sp_Electricity_rc_EU27_BRICS5_USMCA_p5_p95_mean_only.svg
```

## Retained outputs

### Workspace outputs

Pyaesa writes the native deterministic and uncertainty outputs below:

`<workspace>/3regions_study/`

### PB-LCIA inter-method figures

`im_sp_Electricity_rc_EU27_BRICS5_USMCA_p5_p95_mean_only.svg` and
`im_sp_Electricity_rc_EU27_BRICS5_USMCA_p5_p95_mean_only.pdf` are vector
versions of the ASR trajectory figure for the ten PB control variables. Each
panel combines EU27, BRICS5, and USMCA; color identifies the region, the line
shows the regional mean, and the band spans P5 to P95.

`im_sp_Electricity_rc_EU27_BRICS5_USMCA_ft.svg` and
`im_sp_Electricity_rc_EU27_BRICS5_USMCA_ft.pdf` are vector versions of the
frequency of transgression (`f^T`) trajectory figure for the same control
variables and regions. The frequency is the share of evaluated uncertainty
outcomes above the Min SOS threshold, which corresponds to ASR greater than 1.
