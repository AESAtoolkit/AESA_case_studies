# Functional Unit Allocation Ratios, EXIOBASE 3.10.2, GWP100, 2022

Reference article:

de Bantel, E. I., Pirson, T., Puig-Samper, G., Hartmann, J. M., Bouillass, G.,
Yannou, B., Jankovic, M., Bol, D., & Hauschild, M. Z.
UNCASExt -- A Systematic Computational Framework for Uncertainty Propagation and
Scope Consistency in Absolute Environmental Sustainability Assessments (AESA)
[Manuscript submitted for publication].

Software:

- pyaesa v1.2.4

LCIA method:

- GWP100

## Scope

This case study quantifies how the choice of allocation functional unit changes
allocated shares of carrying capacities (aSoCCs) in Phase B of AESA. The comparison
is computed for all EXIOBASE 3.10.2 ixi sector-region pairs in 2022.

The code can be adapted to other years, functional units, MRIO sources, LCIA methods
covered by pyaesa.

For the ratios, the reference denominator is `L2.c.b`, CBA impacts of total demand.
The two tested numerator functional units are:
- `L2.c.a`, CBA impacts of final demand.
- `L2.a.c`, PBA impacts of total output.

Ratios greater than 1 indicate that using the tested numerator functional unit would
produce a larger allocated share than the `L2.c.b` reference for the same
allocation method and sector-region pair. Ratios below 1 indicate a smaller
allocated share.

The computation uses by default (but can be updated):

- MRIO source: `exiobase_3102_ixi`.
- Year: 2022.
- LCIA method: `gwp100_lcia`.
- Impact category: `GWP_100`.
- Reference year for acquired rights methods: 1995.
- pyaesa sector aggregation: `elec`, with all EXIOBASE electricity sectors
  grouped together.

The result table contains 88 200 allocation ratio rows, corresponding to 12
allocation method ratio definitions across 7 350 sector-region pairs.

## Files

`compute_allocation_ratios.py`

Workflow script that prepares the pyaesa inputs, runs deterministic aSoCC for
the required L2 functional units, and computes the allocation ratio CSV files.

`fu_ratios_results_2022/allocation_ratio_distribution.csv`

Detailed allocation ratio distribution table. Each row corresponds to one
functional unit ratio, allocation method ratio, country, sector, and year.
Columns include the numerator value, denominator value, and ratio value.

`fu_ratios_results_2022/allocation_ratio_stats_world.csv`

World-level summary statistics for the allocation ratio distributions. It includes
summary rows for each allocation method ratio and each functional unit ratio..

`fu_ratios_results_2022/allocation_ratio_stats_by_sector_country.csv`

Summary statistics for all 7 350 sector-region pairs.
