# One net. Three rulers.

Voice: en-US-JennyNeural; duration 349.77 s.

## 00:00:00.000 · One net. Three rulers.
How can the same set of pins have three different wirelengths? In this lesson, we use three different rulers to understand net models in chip placement.

## 00:00:10.467 · Connections first. Positions next.
A net on a chip can connect several pins at once. The connections are already specified; placement chooses their positions. Before estimating wirelength, we must also choose a measurement model.

## 00:00:24.767 · Four pins we can check by hand
Start with four pins at the corners of a square of side two. We use these same coordinates throughout, comparing a bounding box, a clique, and a star.

## 00:00:35.733 · Horizontal plus vertical
We use Manhattan distance, rather than straight-line distance. Add the absolute horizontal difference to the absolute vertical difference. The bent lines in our drawings illustrate that measurement.

## 00:00:49.533 · From A to D: two plus two
From A at the lower left to D at the upper right, move two units horizontally and two vertically. Their Manhattan distance is four. Every model here uses this same basic distance.

## 00:01:02.833 · Ruler one: measure the boundary
The first model finds the smallest box containing all pins. The leftmost and rightmost pins determine its width. The lowest and highest determine its height. Add width and height.

## 00:01:17.067 · Half the perimeter, not all of it
For our square, width and height are both two, giving a half-perimeter wirelength of four. Walking around all four sides gives eight. That is the full perimeter, not this metric.

## 00:01:30.967 · A single scan is enough
The bounding box needs only four extreme coordinates. Scan each pin once to find them, so the computation grows linearly with the number of pins. It is a cheap wirelength estimate.

## 00:01:44.433 · Ruler two: measure every pair
The second model is a clique: connect every pair of distinct pins and add their Manhattan distances. Four pins give six unordered pairs. Count each pair exactly once.

## 00:01:57.967 · Every term names a pair
In alphabetical order, measure A to B, A to C, and A to D; then B to C, B to D, and C to D. The six distances are two, two, four, four, two, and two.

## 00:02:13.067 · Six distances add up to sixteen
Adding these six terms gives sixteen. Do not count both A to B and B to A. Those names describe the same unordered pair; double counting would incorrectly produce thirty-two.

## 00:02:26.200 · The edge count grows quadratically
With p pins, a clique has p times p minus one, divided by two edges. Here we sum unnormalized Manhattan distances. This is not the squared-distance objective used in quadratic placement.

## 00:02:40.767 · Ruler three: choose a hub
The third model is a star. Choose one existing pin as a hub and connect it to every other pin. Our example uses A. We do not introduce a virtual center.

## 00:02:53.867 · Measure only three spokes
With A as the hub, the spokes are A to B, A to C, and A to D. Their lengths are two, two, and four, totaling eight. Other pin pairs do not enter this sum.

## 00:03:07.500 · The hub is part of the definition
A star has only p minus one spokes, so its computation is linear in the pin count. But the hub is part of the model definition. Always name it when reporting the result.

## 00:03:20.367 · Same pins. Three readings.
The same pins now give four, sixteen, and eight. Neither their coordinates nor their connections changed. Only the measurement changed. These numbers alone cannot rank which model is better.

## 00:03:35.267 · Break the symmetry
For the square, choosing any corner as the star hub happens to give the same answer. That is a consequence of symmetry. An asymmetric example reveals why the hub matters.

## 00:03:48.200 · Change the hub. Change the result.
Using A, B, C, and D as hubs now gives sixteen, twenty-two, fourteen, and twenty. C has the smallest value here. This shows hub dependence; it does not prove a placement algorithm is optimal.

## 00:04:04.267 · An interior move can stay hidden
Next, A, B, and C support an eight by eight bounding box. Move the interior pin D from four, four to two, two. Watch the three rulers: which readings change?

## 00:04:18.767 · One move. Different sensitivities.
The half-perimeter stays sixteen because the outer boundaries did not change. The clique decreases from fifty-six to fifty-two, and the star from twenty-four to twenty. Different models respond differently to the same move.

## 00:04:33.867 · Zero wirelength is not a legal layout
Place every pin at one position and all three wirelengths become zero. Real cells have area and cannot freely overlap. These measurements have not checked density, overlap, or timing.

## 00:04:47.933 · A model drawing is not routed wire
The bent lines illustrate measurement relationships, not final shared routing paths. Before comparing two placement candidates, align the model, the distance, the weights, and the constraints. Small numbers need a clear definition.

## 00:05:04.433 · Measure a spread and a compact square
On the website, load the spread square and then the compact reference square. The readings change from sixteen, sixty-four, thirty-two to four, sixteen, eight. Drag a pin to investigate your own placement.

## 00:05:20.033 · Predict first. Then check.
Change the star hub, move the interior pin, and try the six experiment tasks. Write down your prediction first. Then inspect each computed contribution and explain where the change came from.

## 00:05:34.600 · Take the definitions with you
Finally, implement the three functions in the downloadable Python exercise and compare with the independent reference. More important than remembering four, sixteen, and eight is explaining exactly what each number measures.
