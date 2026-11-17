# One set of pins, three different rulers

Placement · Lesson 03 · FanqinZeng

## Goals and conventions

Compute BBox/HPWL, Clique, and Star from coordinates, explain every contribution, and recognize the limitations of each model. We use a single net with unit weights and two-dimensional Manhattan distance. All four pins can move: this is a measurement experiment, rather than a placement optimizer with fixed-cell constraints.

The origin is at bottom left, with y pointing up. The Manhattan distance between two pins is |xᵢ−xⱼ|+|yᵢ−yⱼ|. The bent lines illustrate this distance; they are not actual shared routing.

## Three models

1. **BBox / HPWL**: find the minimum and maximum coordinates on each axis. The result is (max x−min x)+(max y−min y). This is the bounding box’s half-perimeter, rather than its full perimeter. A single scan of p pins takes O(p) time.
2. **Clique**: sum the Manhattan distance of every unordered pair i<j. There are p(p−1)/2 pairs, giving O(p²) time. This lesson uses neither normalization nor squared distances.
3. **Star-from-h**: choose an existing pin h as the hub and sum its distances to the other p−1 pins. This takes O(p) time. The choice of h is part of the definition; a virtual hub is a separate convention.

## A standard example you can calculate by hand

| Pin | x | y |
|---|---:|---:|
| A | 2 | 2 |
| B | 4 | 2 |
| C | 2 | 4 |
| D | 4 | 4 |

HPWL = 2+2 = **4**.

The six Clique pairs are AB=2, AC=2, AD=4, BC=4, BD=2, and CD=2, for a total of **16**. Count AB and BA as one pair.

Star-from-A = AB+AC+AD = 2+2+4 = **8**.

## Three counterexamples

**Hub dependence.** For A(0,0), B(6,0), C(1,2), and D(2,5), HPWL=11 and Clique=36. Using hubs A/B/C/D gives Star values of 16/22/14/20. The four equal hub values in the symmetric square do not imply that changing hubs preserves the value for every input.

**The interior blind spot.** Start with A(0,0), B(8,0), C(0,8), and D(4,4). Move D to (2,2). HPWL stays at 16, while Clique drops from 56 to 52 and Star-from-A from 24 to 20. An unchanged boundary does not imply unchanged values in the other models.

**Zero is not a legality certificate.** If all pins overlap, all three values are zero. These models do not check physical cell area, overlap, density, or timing, so the result does not certify a completed placement.

## Compare like with like

The values 4, 16, and 8 measure different quantities on the same diagram. Their relative sizes cannot tell us which model is “best.” Before comparing two candidate placements, align the model, distance metric, weights, and constraints. HPWL is an estimate, rather than exact routed wirelength.

The main experiment measures only ABCD. Across the teacher’s six nets, total unweighted HPWL changes 52→14; with weights [1,1,1,1,5,1], it changes 116→30. Do not mix these all-net values with single-net ABCD’s 16→4 in the same comparison column.

## Implementation and verification

Complete the three functions in exercise.py, then compare with reference.py. Input is a list of pins, each with id, x, and y. IDs must be unique and coordinates finite. Empty or single-pin nets give zero; for a nonempty net the hub must be present. With two pins, all three models agree.

Check translation invariance and uniform positive scaling. Also check that the sum of Star values over every existing pin as hub equals twice the Clique value. Reject missing coordinates, NaN, duplicate IDs, and invalid hubs.

## Sources and licenses

This material follows Yongfu Li’s eda-learning / module01-03-net-models and placement-core.js. The mapping follows course order; issue #26 has an empty body. New explanations and exercises are CC BY 4.0; new code is MIT. See THIRD_PARTY_NOTICES.md in the repository for individual lesson references, fonts, and other third-party sources.
