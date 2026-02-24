# Pyrl Examples Test Report

**Generated:** 2026-02-24 02:39:03

## Summary

| Metric | Count |
|--------|-------|
| Total | 127 |
| Passed | 25 |
| Failed | 102 |
| Timeout | 0 |
| Success Rate | 19.7% |

## Category Breakdown

| Category | Total | Passed | Failed | Rate |
|----------|-------|--------|--------|------|
| root | 127 | 25 | 102 | 19.7% |

## Failed Examples

### COMPREHENSIVE_EXAMPLES.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 222, Column 5
[93mUnexpected token:[0m 'return' (type: RETURN)
[93mExpected one of:[0m newline, else, }, SEMICOLON

[93mContext:[0m
219 |     if $x < 0 {
220 |         return -$x
221 |     }
222 |     return $x
[91m          ^^^^^^[0m
223 | }
224 | 
225 | # Анонимная функция с циклом

[91m================...
```

### examples_00001_00100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 31, Column 57
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, @variable, &variable, %variable, R, {, (, boolean, string, [, ... and 3 more

[93mContext:[0m
28 |     %condition["value"] = true
29 |     # Process data
30 | def configure($j, $force):
31 |     &parse($min, $expone...
```

### examples_00101_00200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.58s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 123, Column 312
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, @variable, number, &variable, boolean, [, (, string, R, None, ... and 3 more

[93mContext:[0m
120 | 
121 | # Example 110
122 | # ==================================================
123 | class Transformer {init($ra...
```

### examples_00201_00300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 17, Column 874
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m None, string, &variable, identifier, @variable, [, {, %variable, R, $variable, ... and 3 more

[93mContext:[0m
14 | # Example 202
15 | # ==================================================
16 | &transform($left) = {print(468); ...
```

### examples_00301_00400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 78, Column 7
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m number, None, {, boolean, identifier, [, &variable, R, $variable, (, ... and 3 more

[93mContext:[0m
75 | $current = 'source'
76 | $a = false
77 | $counter = false
78 | $n = --56
[91m           ^[0m
79 | $end = any([-44.36, -8...
```

### examples_00401_00500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 72, Column 318
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, {, [, $variable, identifier, string, number, boolean, &variable, R, ... and 3 more

[93mContext:[0m
69 | 
70 | # Example 407
71 | # ==================================================
72 | class Thread extends Converter {ini...
```

### examples_00501_00600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 122, Column 649
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, identifier, boolean, number, None, {, (, @variable, %variable, string, ... and 3 more

[93mContext:[0m
119 | 
120 | # Example 511
121 | # ==================================================
122 | class Publisher {init($heig...
```

### examples_00601_00700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.58s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 165, Column 58
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, R, None, boolean, string, {, [, %variable, &variable, (, ... and 3 more

[93mContext:[0m
162 | $key = None
163 | $limit = 'link'
164 | $parent = 'demo' % 'enabled' + ! -213 < 960
165 | $center = %database - [$item,...
```

### examples_00701_00800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 85, Column 292
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m &variable, %variable, boolean, @variable, (, R, identifier, string, [, {, ... and 3 more

[93mContext:[0m
82 | 
83 | # Example 707
84 | # ==================================================
85 | class Subscriber {init($a, $end)...
```

### examples_00801_00900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.59s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 598, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m string, :

[93mContext:[0m
595 |     $margin = "warning"
596 |     return verify({"input": $element, "error": $rate})
597 |     return execute(%plan, $phase) < "hello" < "world" < $velocity
598 | test({"warning": $period, "email"...
```

### examples_00901_01000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 104, Column 1053
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m newline, }, SEMICOLON

[93mContext:[0m
101 | 
102 | # Example 906
103 | # ==================================================
104 | class Profile {init($difference, $remainder, $pos) = {@logs[3] = {"message": none, "info":...
```

### examples_01001_01100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.60s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 129, Column 72
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m R, %variable, (, [, boolean, number, $variable, identifier, string, &variable, ... and 3 more

[93mContext:[0m
126 | # ==================================================
127 | $result = (%table)
128 | $quotient = &write
129 | ...
```

### examples_01101_01200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** Runtime Error: Undefined variable: $distance
- **Line:** None
- **Execution Time:** 0.65s

**Stderr:**
```text
Runtime Error: Undefined variable: $distance

```

### examples_01201_01300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 185, Column 50
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m &variable, boolean, R, $variable, identifier, string, %variable, @variable, None, [, ... and 3 more

[93mContext:[0m
182 |     # Initialize variables
183 |     $age = run(%feature, @ids) % ["no", "info", True, $i, 16.50, 801] ...
```

### examples_01301_01400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 391, Column 10
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m &variable, {, R, boolean, None, number, [, %variable, string, identifier, ... and 3 more

[93mContext:[0m
388 | 
389 | # Example 1333
390 | # ==================================================
391 | $line = --None - validate()...
```

### examples_01401_01500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 203, Column 14
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, @variable, string, (, R, None, {, &variable, number, identifier, ... and 3 more

[93mContext:[0m
200 | # Example 1416
201 | # ==================================================
202 | $power = $z
203 | $momentum = --None
[9...
```

### examples_01501_01600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 29, Column 52
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m %variable, &variable, @variable, None, identifier, [, boolean, $variable, (, number, ... and 3 more

[93mContext:[0m
26 | $angle = $head / $val
27 | $input = $max
28 | $first = -initialize()
29 | $element = %record != $accelera...
```

### examples_01601_01700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 360, Column 387
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m newline, SEMICOLON, }

[93mContext:[0m
357 | 
358 | # Example 1627
359 | # ==================================================
360 | &check($score, $mass, $output) = {for $key in @rows {print(float(true, %map, false) and @s...
```

### examples_01701_01800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 79, Column 134
[93mUnexpected token:[0m "'target'" (type: STRING)
[93mExpected one of:[0m }, newline, SEMICOLON

[93mContext:[0m
76 | # Example 1706
77 | # ==================================================
78 | class Queue {prop score prop z prop item method join($amount) = {$numerator = "info"; $ratio; $ph...
```

### examples_01801_01900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 121, Column 9
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m string, :

[93mContext:[0m
118 |     assert ["input", -20.97, None] == @columns
119 | elif -49 != None * %data < 985 - $result >= ["link", false, -30.12]:
120 |     %access["result"] = $momentum
121 |     test() == @messages
[91...
```

### examples_01901_02000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 106, Column 372
[93mUnexpected token:[0m '%font' (type: HASH_VAR)
[93mExpected one of:[0m ), ,

[93mContext:[0m
103 | # Example 1910
104 | # ==================================================
105 | class List {init() = {print($pressure + [False, 757, $value, 700, 188, $energy, none, none] < @kinds - -800 or ...
```

### examples_02001_02100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.61s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 807, Column 7
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m {, &variable, string, R, number, [, %variable, @variable, (, None, ... and 3 more

[93mContext:[0m
804 | # Example 2063
805 | # ==================================================
806 | $parent = -&trace
807 | $m = --14.06 <= "l...
```

### examples_02101_02200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.61s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 364, Column 18
[93mUnexpected token:[0m ')' (type: RPAR)
[93mExpected one of:[0m number, NOT, {, &variable, @variable, $variable, (, string, +/-, None, ... and 6 more

[93mContext:[0m
361 |     print(none != verify($range, "city", {"output": $error}))
362 |     # Clean up
363 |     # Calculate result
364 |  ...
```

### examples_02201_02300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 203, Column 11
[93mUnexpected token:[0m ',' (type: COMMA)
[93mExpected one of:[0m )

[93mContext:[0m
200 |     print(items(@products, -898))
201 |     return ({"name": none, "value": none, "error": "type", "address": $amplitude, "key": 227}) - [true, -47.92, 543] < -20.17 + not -141
202 | len('info', 20.60, ...
```

### examples_02301_02400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.58s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 493, Column 436
[93mUnexpected token:[0m ':' (type: COLON)
[93mExpected one of:[0m SEMICOLON, }, newline

[93mContext:[0m
490 | 
491 | # Example 2341
492 | # ==================================================
493 | class Graph extends Response {prop c = %data method refresh($last) = {@outputs = [$line, "outp...
```

### examples_02401_02500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 280, Column 568
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m R, {, %variable, identifier, [, string, number, boolean, $variable, (, ... and 3 more

[93mContext:[0m
277 | # Example 2426
278 | # ==================================================
279 | class Session {init() = {@types; $i ...
```

### examples_02501_02600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 435, Column 97
[93mUnexpected token:[0m ',' (type: COMMA)
[93mExpected one of:[0m )

[93mContext:[0m
432 |     @values = [None, 37.77, None]
433 |     print([false, 720, null, $char, $name, False])
434 | configure("link", "password")
435 | print({"id": $pos, "type": $quantity, "value": $border, "name": $acce...
```

### examples_02601_02700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 255, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m string, :

[93mContext:[0m
252 |     assert false != @messages or -124 / -40 and "label"
253 | load()
254 | range()
255 | test([-225, false], true)
[91m          ^[0m
256 | 
257 | # Example 2619
258 | # ========================...
```

### examples_02701_02800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 240, Column 7
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m $variable, [, {, (, &variable, %variable, number, @variable, identifier, None, ... and 3 more

[93mContext:[0m
237 |     print(-678 < @records != $rate)
238 |     &evaluate($val, $head, $phase) = {print(["dest", True] or {"city...
```

### examples_02801_02900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 47, Column 15
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m None, $variable, string, @variable, boolean, [, &variable, (, %variable, number, ... and 3 more

[93mContext:[0m
44 |     print(-806 * true < 733)
45 |     # Clean up
46 |     $limit = ! True / ["enabled"] < $val
47 |     retur...
```

### examples_02901_03000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 92, Column 54
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m number, [, R, (, {, %variable, None, &variable, string, @variable, ... and 3 more

[93mContext:[0m
89 | 
90 | # Example 2909
91 | # ==================================================
92 | $density = ["label", null] == &connect ...
```

### examples_03001_03100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 160, Column 11
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, None, boolean, %variable, $variable, @variable, string, number, R, {, ... and 3 more

[93mContext:[0m
157 | # Example 3011
158 | # ==================================================
159 | $error = "key" // [null, "...
```

### examples_03101_03200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 75, Column 1422
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m number, [, identifier, None, string, &variable, @variable, (, $variable, boolean, ... and 3 more

[93mContext:[0m
72 | # Example 3106
73 | # ==================================================
74 | class Database extends Audio...
```

### examples_03201_03300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 27, Column 433
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, $variable, &variable, R, {, None, %variable, string, boolean, number, ... and 3 more

[93mContext:[0m
24 | # ==================================================
25 | &process() = {for $root in range(1) {$quotient = len(@user...
```

### examples_03301_03400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 436, Column 171
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m }, SEMICOLON, newline

[93mContext:[0m
433 | # Example 3335
434 | # ==================================================
435 | &read($prev) = {print(%context <= 'file'); (validate(@vector, True)); while -517 > 949 or %data {...
```

### examples_03401_03500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.52s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 17, Column 105
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m number, {, boolean, &variable, @variable, identifier, $variable, %variable, (, R, ... and 3 more

[93mContext:[0m
14 | # Example 3402
15 | # ==================================================
16 | def disable($amplitude, $a):
...
```

### examples_03501_03600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 78, Column 6
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m number, identifier, string, (, [, &variable, %variable, None, {, boolean, ... and 3 more

[93mContext:[0m
75 |     # Calculate result
76 |     $temp = 958
77 |     return &store
78 |     --41
[91m          ^[0m
79 |     return...
```

### examples_03601_03700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 106, Column 79
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m {, %variable, R, [, None, identifier, number, @variable, string, $variable, ... and 3 more

[93mContext:[0m
103 | # ==================================================
104 | &evaluate($factor) = {if (all()) {$last = None <= "re...
```

### examples_03701_03800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.60s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 555, Column 283
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m }, newline, SEMICOLON

[93mContext:[0m
552 |     assert load($pos, @block)
553 |     $x = "tag"
554 | def verify($product, $power):
555 |     &init() = {if -384 * $median % {"hello": $energy, "status": $pivot, "value": "er...
```

### examples_03801_03900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 255, Column 9
[93mUnexpected token:[0m '&authenticate' (type: FUNC_VAR)
[93mExpected one of:[0m :

[93mContext:[0m
252 | $m = ! "message" >= @strings and {"message": False, "name": $capacity, "test": -574}
253 | $weight = "left"
254 | $power = -28.37 or [null, 'username', 421, False, None, $momentum, $densit...
```

### examples_03901_04000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 309, Column 9
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m {, [, @variable, (, identifier, None, boolean, number, string, %variable, ... and 3 more

[93mContext:[0m
306 | # ==================================================
307 | $pivot = &navigate
308 | $factor = (false)
309 | $key = ...
```

### examples_04001_04100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 296, Column 488
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m R, $variable, string, [, &variable, {, number, (, boolean, @variable, ... and 3 more

[93mContext:[0m
293 | 
294 | # Example 4022
295 | # ==================================================
296 | class Audio {init($right, $spe...
```

### examples_04101_04200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.63s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 939, Column 63
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m None, string, {, R, (, identifier, number, [, @variable, &variable, ... and 3 more

[93mContext:[0m
936 | 
937 | # Example 4177
938 | # ==================================================
939 | class Client {init($energy, $scor...
```

### examples_04201_04300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 86, Column 725
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m SEMICOLON, newline, }

[93mContext:[0m
83 | 
84 | # Example 4210
85 | # ==================================================
86 | class Service {init($node, $z) = {print([403] >= %database - join()); while -$difference and cl...
```

### examples_04301_04400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.61s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 601, Column 20
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, &variable, %variable, None, $variable, number, boolean, {, @variable, R, ... and 3 more

[93mContext:[0m
598 | $amplitude = "open"
599 | $sum = (-300) % $x % ($difference)
600 | $left = ['inactive', 921, -52.80, nu...
```

### examples_04401_04500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 288, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m :, string

[93mContext:[0m
285 |     return -&stop != none == [-357, true, null]
286 | check(&join)
287 | clean(@pool, "chapter", 'password')
288 | test([true, null, 'input', -342, -267, False, True], 29)
[91m          ^[0m
289...
```

### examples_04501_04600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 159, Column 99
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, boolean, &variable, None, $variable, {, number, %variable, R, @variable, ... and 3 more

[93mContext:[0m
156 | 
157 | # Example 4515
158 | # ==================================================
159 | &close($pressure...
```

### examples_04601_04700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 34, Column 137
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, string, %variable, @variable, $variable, &variable, identifier, [, None, R, ... and 3 more

[93mContext:[0m
31 | for $swap in range(6):
32 |     # Calculate result
33 |     # Initialize variables
34 | class Container {prop ...
```

### examples_04701_04800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 343, Column 413
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m %variable, R, [, {, boolean, &variable, number, None, string, @variable, ... and 3 more

[93mContext:[0m
340 | # Example 4725
341 | # ==================================================
342 | &receive() = {convert(%storage); r...
```

### examples_04801_04900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 116, Column 94
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m $variable, identifier, [, number, %variable, R, (, &variable, string, None, ... and 3 more

[93mContext:[0m
113 | # ==================================================
114 | $x = %request < None + 693 != $tmp
115 | $circumferen...
```

### examples_04901_05000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 189, Column 158
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m @variable, &variable, {, identifier, (, boolean, [, number, None, R, ... and 3 more

[93mContext:[0m
186 |     print((False))
187 |     %state["message"] = [616, True, -62.14]
188 |     return
189 | &verify($temperature, $nex...
```

### examples_05001_05100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 23, Column 75
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m &variable, %variable, boolean, string, {, identifier, @variable, R, $variable, None, ... and 3 more

[93mContext:[0m
20 | # Example 5002
21 | # ==================================================
22 | &reset($amplitude) = {@user...
```

### examples_05101_05200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 93, Column 131
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, identifier, number, string, @variable, &variable, R, None, %variable, $variable, ... and 3 more

[93mContext:[0m
90 | # ==================================================
91 | &store($difference, $rate) = {@fields[1] = [$pr...
```

### examples_05201_05300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 248, Column 73
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, string, $variable, R, &variable, (, %variable, @variable, number, boolean, ... and 3 more

[93mContext:[0m
245 | for $interval in [$value, -163, 'ready']:
246 |     @configs = [none, -13.59, 46, -67.02, -326, -10, ...
```

### examples_05301_05400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 66, Column 34
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m boolean, string, number, @variable, &variable, [, {, %variable, $variable, (, ... and 3 more

[93mContext:[0m
63 | $quantity = initialize($min, [$remainder]) == enumerate($limit) > (-386)
64 | $force = 'disabled' // True / form...
```

### examples_05401_05500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 176, Column 252
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m [, string, $variable, {, &variable, %variable, identifier, R, @variable, None, ... and 3 more

[93mContext:[0m
173 | # Example 5414
174 | # ==================================================
175 | class Client {init($index, $...
```

### examples_05501_05600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 476, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m :, string

[93mContext:[0m
473 |     return
474 |     return [-335, 'description', False, 5.86, 398, -410] - -18.26 or [-550, False] <= [-619]
475 | configure(&init, None, 'demo')
476 | test({"email": $size, "input": true}, [95.3...
```

### examples_05601_05700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 76, Column 207
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m R, None, (, number, [, identifier, {, %variable, boolean, &variable, ... and 3 more

[93mContext:[0m
73 | 
74 | # Example 5607
75 | # ==================================================
76 | &initialize() = {print($token); $sum...
```

### examples_05701_05800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 67, Column 7
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m [, number, &variable, boolean, R, $variable, (, @variable, %variable, string, ... and 3 more

[93mContext:[0m
64 | # ==================================================
65 | $n = @bytes > [814, false, 'city'] > False // ("pending...
```

### examples_05801_05900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 251, Column 122
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m string, {, boolean, $variable, @variable, &variable, [, %variable, None, R, ... and 3 more

[93mContext:[0m
248 |     return {"value": -611, "id": $index, "warning": $phase} - {"data": True, "email": $token, "output": $speed,...
```

### examples_05901_06000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.59s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 608, Column 171
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, None, {, %variable, $variable, number, @variable, &variable, boolean, string, ... and 3 more

[93mContext:[0m
605 | 
606 | # Example 5956
607 | # ==================================================
608 | class Handler {init...
```

### examples_06001_06100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** Runtime Error: Undefined variable: %state
- **Line:** None
- **Execution Time:** 0.65s

**Stderr:**
```text
Runtime Error: Undefined variable: %state

```

### examples_06101_06200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 109, Column 11
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m $variable, %variable, string, None, number, identifier, R, {, @variable, boolean, ... and 3 more

[93mContext:[0m
106 | $child = 'no'
107 | $numerator = @headers <= 801 - ! 180
108 | $status = @bytes <= ["text"] and ['off', Fa...
```

### examples_06201_06300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 519, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m string, :

[93mContext:[0m
516 |     &init($pivot, $rate, $leaf) = {{"username": -88.02, "input": 'category', "key": $line} // &forward != @columns; while ($m * %validation * {"success": 39.50} + {"success": $message, "phone": -1...
```

### examples_06301_06400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.62s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 846, Column 122
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m {, [, None, (, &variable, number, boolean, $variable, identifier, string, ... and 3 more

[93mContext:[0m
843 | # ==================================================
844 | class Observer {init($price, $previous) = {for $diamet...
```

### examples_06401_06500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 71, Column 41
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, %variable, $variable, boolean, None, number, identifier, string, &variable, R, ... and 3 more

[93mContext:[0m
68 |     print([none, -6, -829, -131, $sum, $current])
69 |     %theme = {"example": "section", "country": true}
...
```

### examples_06501_06600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 29, Column 33
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m &variable, boolean, {, %variable, $variable, identifier, string, None, number, @variable, ... and 3 more

[93mContext:[0m
26 | $key = &setup * (['target', 52, true, -275, -878, 36.44])
27 | $percentage = 956
28 | $phase = -3.08...
```

### examples_06601_06700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.61s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 725, Column 215
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, $variable, None, %variable, R, @variable, &variable, [, string, identifier, ... and 3 more

[93mContext:[0m
722 | 
723 | # Example 6657
724 | # ==================================================
725 | class Entity {init($l...
```

### examples_06701_06800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 266, Column 118
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m identifier, string, (, boolean, {, R, None, &variable, $variable, number, ... and 3 more

[93mContext:[0m
263 |     $swap = (None) != ! %settings > %font
264 |     return (('disabled' / %attributes))
265 | def flush($accumula...
```

### examples_06801_06900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 12
[93mUnexpected token:[0m 'true' (type: IDENT)
[93mExpected one of:[0m )

[93mContext:[0m
 4 | 
 5 | # Example 6801
 6 | # ==================================================
 7 | print(-not true <= {"warning": "password", "phone": $score, "input": None, "token": -97})
[91m                ^^^^[0...
```

### examples_06901_07000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 184, Column 1507
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m @variable, [, identifier, R, boolean, &variable, number, %variable, {, None, ... and 3 more

[93mContext:[0m
181 | # Example 6917
182 | # ==================================================
183 | &parse($factor, $median, $lea...
```

### examples_07001_07100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 64, Column 15
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, string, $variable, @variable, {, R, &variable, number, [, %variable, ... and 3 more

[93mContext:[0m
61 | class Consumer {init($message, $difference, $offset) = {@schemas[4] = &trace; $range = -621 // %data // ['sta...
```

### examples_07101_07200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 148, Column 13
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m boolean, %variable, &variable, {, string, [, None, $variable, number, (, ... and 3 more

[93mContext:[0m
145 | $end = null < [-46.47]
146 | if {"status": $min}:
147 |     # Validate input
148 |     print((--452 > none / %condi...
```

### examples_07201_07300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 534, Column 5
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m @variable, $variable, boolean, number, &variable, R, None, [, {, string, ... and 3 more

[93mContext:[0m
531 | $prev = $base
532 | $text = $padding
533 | $item = 283
534 | if -! -76.47 <= [-580, "begin", true, "password", $age]...
```

### examples_07301_07400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 246, Column 848
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m identifier, None, %variable, &variable, string, [, number, $variable, boolean, @variable, ... and 3 more

[93mContext:[0m
243 | # Example 7320
244 | # ==================================================
245 | class Builder {pr...
```

### examples_07401_07500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 14, Column 66
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, None, %variable, {, string, R, identifier, (, number, @variable, ... and 3 more

[93mContext:[0m
11 |     @columns = [12.78, -763, $result]
12 |     (not ! 729)
13 | else:
14 |     print(True + [88.68, false, None, 'username...
```

### examples_07501_07600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 215, Column 6
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m (, &variable, $variable, @variable, identifier, {, string, boolean, number, [, ... and 3 more

[93mContext:[0m
212 | $previous = %payload <= $center == [None, true]
213 | $quotient = (339) - process(False, none, $ratio) or {"he...
```

### examples_07601_07700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 174, Column 346
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m @variable, {, [, identifier, &variable, string, $variable, boolean, %variable, (, ... and 3 more

[93mContext:[0m
171 | 
172 | # Example 7612
173 | # ==================================================
174 | class Formatter {i...
```

### examples_07701_07800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 378, Column 834
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m None, string, boolean, [, &variable, {, R, identifier, number, $variable, ... and 3 more

[93mContext:[0m
375 | # Example 7734
376 | # ==================================================
377 | class Stack {init($quantity, $rem...
```

### examples_07801_07900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 667, Column 97
[93mUnexpected token:[0m 'None' (type: IDENT)
[93mExpected one of:[0m }, SEMICOLON, newline

[93mContext:[0m
664 | # Example 7854
665 | # ==================================================
666 | class Graph {init($margin, $n, $period) = {%fields; return ([-28.18, -20.18, -66.85, true, -601, 14...
```

### examples_07901_08000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 113, Column 439
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m R, %variable, $variable, string, &variable, {, None, boolean, @variable, number, ... and 3 more

[93mContext:[0m
110 | &convert($remainder) = {return; return}
111 | &compute($threshold, $element, $entry) = {print(({"id": $pro...
```

### examples_08001_08100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 115, Column 602
[93mUnexpected token:[0m 'print' (type: PRINT)
[93mExpected one of:[0m newline, }, SEMICOLON

[93mContext:[0m
112 | # Example 8011
113 | # ==================================================
114 | class Tester {init($entry, $remainder, $a) = {map(&login); ("disabled" - 838 or "category"); @mem...
```

### examples_08101_08200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 260, Column 12
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m boolean, number, None, R, {, identifier, %variable, (, string, $variable, ... and 3 more

[93mContext:[0m
257 |     return str(none, "no")
258 | def shrink($mode, $power, $total, $input):
259 |     print(true or ["section"] or...
```

### examples_08201_08300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.52s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 59, Column 5
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m :, string

[93mContext:[0m
56 |     ('demo')
57 |     $output = (format())
58 |     # Check condition
59 | test(@data)
[91m         ^[0m
60 | sum()
61 | find(false, False, null)
62 | 

[91m======================================...
```

### examples_08301_08400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 142, Column 2407
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m &variable, [, None, $variable, identifier, number, boolean, @variable, {, %variable, ... and 3 more

[93mContext:[0m
139 | # ==================================================
140 | class Gateway {prop m prop index prop i = ...
```

### examples_08401_08500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.57s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 481, Column 13
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m %variable, string, @variable, identifier, $variable, boolean, &variable, None, [, (, ... and 3 more

[93mContext:[0m
478 |     assert $c != -48.89
479 |     assert %product
480 |     # Log message
481 |     assert --110 == 'pa...
```

### examples_08501_08600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.54s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 162, Column 147
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m identifier, %variable, (, @variable, number, &variable, None, R, {, $variable, ... and 3 more

[93mContext:[0m
159 | 
160 | # Example 8512
161 | # ==================================================
162 | class Controller exte...
```

### examples_08601_08700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.52s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 23, Column 6
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m $variable, (, R, {, [, None, @variable, boolean, &variable, %variable, ... and 3 more

[93mContext:[0m
20 | def increment($width):
21 |     return -665 % "close" / ["start", true, False, none, "status", -84.11, true]
22 |     @i...
```

### examples_08701_08800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.63s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 803, Column 175
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m %variable, &variable, $variable, @variable, identifier, [, (, string, R, boolean, ... and 3 more

[93mContext:[0m
800 |     %cache["output"] = &route
801 |     assert [$output, 'city', $word, True, -305, true]
802 |     # Han...
```

### examples_08801_08900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.56s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 295, Column 169
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m string, identifier, &variable, @variable, [, {, R, %variable, boolean, $variable, ... and 3 more

[93mContext:[0m
292 |     @elements = [$avg, -467, True, 16.34, -81.59, none, "message"]
293 |     print(! {"demo": -85.03, "me...
```

### examples_08901_09000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 66, Column 13
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m $variable, (, R, None, [, boolean, {, string, @variable, &variable, ... and 3 more

[93mContext:[0m
63 | 
64 | # Example 8905
65 | # ==================================================
66 | $counter = -! ['note'] or $c
[91m    ...
```

### examples_09001_09100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 72, Column 17
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m %variable, number, (, {, None, [, R, string, $variable, @variable, ... and 3 more

[93mContext:[0m
69 | if $z:
70 |     @points[0] = 'name'
71 |     # Clean up
72 |     $current = -! 73.94 <= -"world"
[91m                     ...
```

### examples_09101_09200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.52s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 8, Column 796
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m %variable, number, None, {, $variable, R, boolean, [, &variable, identifier, ... and 3 more

[93mContext:[0m
 5 | # Example 9101
 6 | # ==================================================
 7 | &write() = {@attributes = [none, 94...
```

### examples_09201_09300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.62s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 945, Column 232
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m $variable, boolean, (, @variable, %variable, {, number, [, string, R, ... and 3 more

[93mContext:[0m
942 | # Example 9280
943 | # ==================================================
944 | &setup($price, $first, $entry) = {! (...
```

### examples_09301_09400.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.51s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 39, Column 15
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m @variable, identifier, $variable, &variable, [, %variable, {, (, boolean, R, ... and 3 more

[93mContext:[0m
36 | # ==================================================
37 | $pressure = ('enabled')
38 | $message = (@transactions)...
```

### examples_09401_09500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 286, Column 264
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m @variable, identifier, &variable, %variable, (, R, None, {, string, [, ... and 3 more

[93mContext:[0m
283 |     @piece[10] = "data"
284 |     &write($accumulator, $time, $margin) = {if [$phase, $denominator, -8.74, "type", $...
```

### examples_09501_09600.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 213, Column 1073
[93mUnexpected token:[0m '!' (type: NOT_OP)
[93mExpected one of:[0m {, R, %variable, None, [, string, number, (, &variable, identifier, ... and 3 more

[93mContext:[0m
210 | # Example 9518
211 | # ==================================================
212 | class Provider {prop b prop value = $p...
```

### examples_09601_09700.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.51s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 10
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m &variable, (, {, @variable, number, boolean, None, $variable, string, [, ... and 3 more

[93mContext:[0m
 4 | 
 5 | # Example 9601
 6 | # ==================================================
 7 | $pos = (--1.47 // @requests)
[91m...
```

### examples_09701_09800.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 246, Column 9
[93mUnexpected token:[0m '(' (type: LPAR)
[93mExpected one of:[0m :, string

[93mContext:[0m
243 | # Example 9723
244 | # ==================================================
245 | def open($circumference, $left, $force, $range):
246 |     test({"code": $last, "id": $amount, "hello": "page", "cou...
```

### examples_09801_09900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.55s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 227, Column 14
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m None, (, [, identifier, string, @variable, &variable, number, R, $variable, ... and 3 more

[93mContext:[0m
224 | # ==================================================
225 | $b = @kinds
226 | $temperature = &handle
227 | $expon...
```

### examples_09901_10000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.53s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 206, Column 126
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m R, string, %variable, &variable, {, None, [, identifier, $variable, number, ... and 3 more

[93mContext:[0m
203 |     @jobs[1] = @tasks
204 |     return 710
205 | for $price in ["dest", False, -793, none, 51.86, None, 567]:
2...
```

### web_server_auth.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.51s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 546, Column 20
[93mUnexpected token:[0m '=' (type: EQUAL)
[93mExpected one of:[0m (

[93mContext:[0m
543 | # Pyrl HTTP Server class
544 | class PyrlServer:
545 |     def __init__($self, %config):
546 |         $self.host = %config["host"]
[91m                         ^[0m
547 |         $self.port = %config...
```


## Error Types

### PYRL RUNTIME ERROR (102 occurrences)

- COMPREHENSIVE_EXAMPLES.pyrl
- examples_00001_00100.pyrl
- examples_00101_00200.pyrl
- examples_00201_00300.pyrl
- examples_00301_00400.pyrl
- examples_00401_00500.pyrl
- examples_00501_00600.pyrl
- examples_00601_00700.pyrl
- examples_00701_00800.pyrl
- examples_00801_00900.pyrl
- examples_00901_01000.pyrl
- examples_01001_01100.pyrl
- examples_01101_01200.pyrl
- examples_01201_01300.pyrl
- examples_01301_01400.pyrl
- examples_01401_01500.pyrl
- examples_01501_01600.pyrl
- examples_01601_01700.pyrl
- examples_01701_01800.pyrl
- examples_01801_01900.pyrl
- examples_01901_02000.pyrl
- examples_02001_02100.pyrl
- examples_02101_02200.pyrl
- examples_02201_02300.pyrl
- examples_02301_02400.pyrl
- examples_02401_02500.pyrl
- examples_02501_02600.pyrl
- examples_02601_02700.pyrl
- examples_02701_02800.pyrl
- examples_02801_02900.pyrl
- examples_02901_03000.pyrl
- examples_03001_03100.pyrl
- examples_03101_03200.pyrl
- examples_03201_03300.pyrl
- examples_03301_03400.pyrl
- examples_03401_03500.pyrl
- examples_03501_03600.pyrl
- examples_03601_03700.pyrl
- examples_03701_03800.pyrl
- examples_03801_03900.pyrl
- examples_03901_04000.pyrl
- examples_04001_04100.pyrl
- examples_04101_04200.pyrl
- examples_04201_04300.pyrl
- examples_04301_04400.pyrl
- examples_04401_04500.pyrl
- examples_04501_04600.pyrl
- examples_04601_04700.pyrl
- examples_04701_04800.pyrl
- examples_04801_04900.pyrl
- examples_04901_05000.pyrl
- examples_05001_05100.pyrl
- examples_05101_05200.pyrl
- examples_05201_05300.pyrl
- examples_05301_05400.pyrl
- examples_05401_05500.pyrl
- examples_05501_05600.pyrl
- examples_05601_05700.pyrl
- examples_05701_05800.pyrl
- examples_05801_05900.pyrl
- examples_05901_06000.pyrl
- examples_06001_06100.pyrl
- examples_06101_06200.pyrl
- examples_06201_06300.pyrl
- examples_06301_06400.pyrl
- examples_06401_06500.pyrl
- examples_06501_06600.pyrl
- examples_06601_06700.pyrl
- examples_06701_06800.pyrl
- examples_06801_06900.pyrl
- examples_06901_07000.pyrl
- examples_07001_07100.pyrl
- examples_07101_07200.pyrl
- examples_07201_07300.pyrl
- examples_07301_07400.pyrl
- examples_07401_07500.pyrl
- examples_07501_07600.pyrl
- examples_07601_07700.pyrl
- examples_07701_07800.pyrl
- examples_07801_07900.pyrl
- examples_07901_08000.pyrl
- examples_08001_08100.pyrl
- examples_08101_08200.pyrl
- examples_08201_08300.pyrl
- examples_08301_08400.pyrl
- examples_08401_08500.pyrl
- examples_08501_08600.pyrl
- examples_08601_08700.pyrl
- examples_08701_08800.pyrl
- examples_08801_08900.pyrl
- examples_08901_09000.pyrl
- examples_09001_09100.pyrl
- examples_09101_09200.pyrl
- examples_09201_09300.pyrl
- examples_09301_09400.pyrl
- examples_09401_09500.pyrl
- examples_09501_09600.pyrl
- examples_09601_09700.pyrl
- examples_09701_09800.pyrl
- examples_09801_09900.pyrl
- examples_09901_10000.pyrl
- web_server_auth.pyrl
