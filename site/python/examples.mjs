/** Python source is executed by CPython/Pyodide in a dedicated worker. */
export const REFERENCE = `# Edit pins or functions, then Run. 修改坐标或函数，然后运行。
from itertools import combinations

pins = [(2, 2), (4, 2), (2, 4), (4, 4)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bbox(pins):
    if not pins:
        return 0
    xs, ys = zip(*pins)
    return max(xs) - min(xs) + max(ys) - min(ys)

def clique(pins):
    return sum(manhattan(a, b) for a, b in combinations(pins, 2))

def star(pins, hub=0):
    if not pins:
        return 0
    return sum(manhattan(pins[hub], pin) for pin in pins)

print("BBox =", bbox(pins))
print("Clique =", clique(pins))
print("Star =", star(pins))
`;
export const EXAMPLES = {
 reference: REFERENCE,
 asymmetric: REFERENCE.replace('[(2, 2), (4, 2), (2, 4), (4, 4)]', '[(0, 0), (6, 0), (1, 2), (2, 5)]'),
 exercise: `# Exercise / 练习：complete the three functions, then check the assertions.
from itertools import combinations
pins = [(2, 2), (4, 2), (2, 4), (4, 4)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bbox(pins):
    # TODO: return width + height / 宽 + 高
    raise NotImplementedError("Implement bbox / 请实现 bbox")

def clique(pins):
    # TODO: sum over every unordered pair / 每个无序点对
    raise NotImplementedError("Implement clique / 请实现 clique")

def star(pins, hub=0):
    # TODO: sum distances to hub / 到中心引脚的距离之和
    raise NotImplementedError("Implement star / 请实现 star")

assert bbox(pins) == 4
assert clique(pins) == 16
assert star(pins) == 8
print("All checks passed! / 全部通过！")
`
};
export const RUN_TIMEOUT_MS = 5000;
export const LIVE_DEBOUNCE_MS = 700;
export const MAX_OUTPUT_CHARS = 40000;
