# Finite-bath transport model

This is a fully synthetic, dimensionless passive-tracer experiment on eight idealized porous replica slabs. It is not measured archaeological material or a validated dating method. All definitions below are part of the task, not parameters that participants must discover from external sources.

## Shared experiment

Each slab has unit half-thickness and unit cross-sectional area. We follow one half, initially symmetric about its middle plane. Each has its own supplied uniform initial tracer concentration. Its original exterior exchanges tracer with a common, well-mixed reservoir throughout the experiment. Its middle plane is sealed before its opening event and exchanges with the same reservoir afterward.

The reservoir has supplied volume V and constant volumetric inflow/outflow rate Q. Incoming liquid has the supplied feed concentration; outgoing liquid has the current reservoir concentration. Tracer gained by any slab is removed from the bath, and tracer released by any slab enters the bath. The bath concentration therefore depends on all eight opening events and diffusivities. It is not the feed concentration. Only its final measured concentration is provided; no intermediate bath or slab measurements are supplied.

## Discrete equations

The authoritative model has 24 equal finite-volume cells per half-slab and 240 updates over normalized time 0 to 1. Cell centers are x_k=(k+0.5)/24 for k=0..23. Cell volume is h=1/24 and time step is dt=1/240. Each slab has a constant diffusivity D_i. Let u_i,k be its cell concentration and b the common bath concentration before an update.

Internal flux from cell k to cell k+1 is F_i,k=D_i*(u_i,k-u_i,k+1)/h. Left boundary influx is L_i=2*D_i*(b-u_i,0)/h. Right boundary influx is R_i=a_i*2*D_i*(b-u_i,23)/h, where a_i=0 before opening and 1 afterward. Fluxes may be negative: a slab may release tracer into the bath.

For update j=0..239, a_i=1 if j>=t_i and 0 otherwise. Each internal face removes dt*F_i,k/h from its left cell and adds the same amount to its right cell. Add dt*L_i/h to cell 0 and dt*R_i/h to cell 23. Simultaneously update the bath by:

`b_new = b + dt/V * (Q*(feed_j-b) - sum_i(L_i+R_i))`.

Every flux uses the previous state. This conserves total tracer apart from the explicitly recorded net inlet/outlet flux: the change in `V*b + h*sum_i,k(u_i,k)` equals `dt*Q*(feed_j-b)`. The specified parameter ranges make all concentration-update weights nonnegative. This model does not include chemical reactions or irreversible adsorption.

The six feed knots lie at times 0, 0.2, 0.4, 0.6, 0.8 and 1. Linear interpolation at `(j+0.5)/240` gives feed_j. The initial bath concentration is feed_0, the first interpolated midpoint value. All slabs start with their own supplied uniform concentration. Eight distinct integer opening steps are drawn without replacement from 1 through 235. Rank 0 is the earliest and rank 7 the latest. Ranks are returned in input slab order, not chronological list order.

## Distributions and observations

Feed knots and the eight initial concentrations are independent Uniform(0.08,0.92) draws. Reservoir volume is Uniform(0.35,1.2), and exchange rate is Uniform(0.3,1.0). These supplied quantities are rounded to six decimals before simulation. Diffusivities are independent Uniform(0.004,0.035) draws. All these draws are independent of the opening-step assignment.

`diffusivity_assays[i] = D_i*exp(e_i)`, with independent normal e_i of mean 0 and standard deviation 0.2, rounded to six decimals. Final profiles sample cell indices `[0,1,2,4,7,10,13,16,19,21,23]`. Independent Gaussian measurement error with standard deviation 0.004 is added to each profile value and to the final bath measurement; values are clipped to [0,1] and rounded to three decimals. Noise settings are declared simulation assumptions, not empirically calibrated instrument specifications.

Each record is one independently generated complete reservoir experiment. All eight slabs stay together for splitting, validation and grading. Training and evaluation come from the same stated generative family, using new experiments. The input does not identify a physical museum object or excavation site.

## Intended use and limitations

The intended use is comparison of CPU numerical and learned methods for uncertain chronology under shared material exchange. A candidate event sequence must be consistent with both local profiles and the bath balance. Solvers may model each specimen approximately or jointly model the experiment; no particular algorithm is required.

The half-slabs are one-dimensional, equally sized and immobile. The model omits reactions, adsorption, advection within slabs, spatially varying diffusivity, irregular fracture geometry and changes in bath volume. Perfect mixing is assumed. Profiles are final observations; diffusion and noisy assays can make multiple event orders plausible. Labels record simulated events exactly but do not guarantee unique recoverability. Results do not establish performance on real archaeological materials or different transport physics. No personal, biological or sensitive site records are included.
