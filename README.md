# Shared Bath Fragment Records

Original synthetic source, version 2.0.0, for the finite-bath revision of Fracture Exposure Ordering. The source implements eight porous replica half-slabs exchanging a passive tracer with a single finite, replenished bath. Unknown opening events change exchange surfaces and consequently the bath encountered by all other slabs.

The supplied feed schedule is not the unknown bath trajectory. Inputs contain final slab profiles and one final bath measurement, known initial slab concentrations, bath volume, inflow/outflow rate and noisy diffusivity assays. The label is the vector of eight chronological opening ranks. Each record is a complete independent experiment; related slabs must remain in one split and grading row.

## Reproduction

Use Python 3.12 with requirements.txt. Run `python generate.py --count 32 --output demo_records.jsonl` for independent examples. The default demonstration key is public and is not the private key used for a frozen challenge corpus. A fixed count/key and pinned dependency version produce the same records. Frozen records, private creation keys and evaluation answers are not published in this repository. The raw challenge upload supplies frozen records and the pinned generator/dependency/release metadata for deterministic preparation.

Fields: case_id, feed_history(6), initial_concentrations(8), bath_volume, exchange_rate, bath_final, diffusivity_assays(8), profiles(8x11), fracture_ranks(8). MODEL.md specifies the exact finite-volume equations, observation conventions and distributions. The raw label field is excluded from public evaluation features during challenge preparation.

## Scope and rights

This is a dimensionless computational analogue, not measured archaeological data, an experimentally validated conservation model or a method for dating excavated objects. Synthetic framing, ambiguity and omitted physical processes are documented in MODEL.md. No third-party data, images or implementations are incorporated. Generated records and documentation are dedicated under CC0-1.0; original code is MIT licensed. Dependencies retain their own licences.

## Research context

Existing diffusion chronometry includes DiffSim (https://doi.org/10.3389/feart.2024.1431516), and inverse porewater history work includes Miller et al.2015 (https://simons.caltech.edu/publications/pdfs/Miller_etal_2015.pdf). Finite-reservoir diffusion and conservation laws are established mathematics. The proposed benchmark contribution is reconstruction of discrete opening chronology in a physically coupled experiment: one slab's exchange alters the boundary concentration at the others. Neither a new diffusion law nor absence of all related work is claimed. The source does not claim platform novelty or approval.
