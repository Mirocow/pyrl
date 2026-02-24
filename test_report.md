# Pyrl Examples Test Report

**Generated:** 2026-02-24 02:43:39

## Summary

| Metric | Count |
|--------|-------|
| Total | 127 |
| Passed | 22 |
| Failed | 105 |
| Timeout | 0 |
| Success Rate | 17.3% |

## Category Breakdown

| Category | Total | Passed | Failed | Rate |
|----------|-------|--------|--------|------|
| root | 127 | 22 | 105 | 17.3% |

## Failed Examples

### 06_anonymous_functions.pyrl

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
[93mLocation:[0m Line 22, Column 15
[93mExpected one of:[0m Unknown

[93mContext:[0m
19 | 
20 | print("=== Anonymous Function with Loop ===")
21 | &sum_range($start, $end) = {
22 |     $total = 0;
[91m                   ^[0m
23 |     for $i in range($start, $end + 1) {
24 |         $total = $total + $i
25 |     };

[91m=========...
```

### 06_classes.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 13, Column 22
[93mExpected one of:[0m Unknown

[93mContext:[0m
10 |     prop age = 0
11 |     
12 |     init($name, $age) = {
13 |         $name = $name;
[91m                          ^[0m
14 |         $age = $age
15 |     }
16 |     

[91m============================================================[0m

```

### 07_classes.pyrl

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
[93mLocation:[0m Line 12, Column 19
[93mExpected one of:[0m Unknown

[93mContext:[0m
 9 |     prop age
10 |     
11 |     init($n, $a) = {
12 |         $name = $n;
[91m                       ^[0m
13 |         $age = $a
14 |     }
15 |     

[91m============================================================[0m

```

### COMPREHENSIVE_EXAMPLES.pyrl

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
[93mLocation:[0m Line 472, Column 5
[93mUnexpected token:[0m '$temp' (type: SCALAR_VAR)
[93mExpected one of:[0m string, newline, ,, }, identifier

[93mContext:[0m
469 | 
470 | # Простой блок
471 | $block_result = {
472 |     $temp = 10
[91m          ^^^^^[0m
473 |     $temp = $temp * 2
474 |     return $temp
475 | }

[91m=====...
```

### examples_00001_00100.pyrl

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
[93mLocation:[0m Line 7, Column 67
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 1
 6 | # ==================================================
 7 | &configure($quantity) = {while ([149]) > $last {print(%privilege)}; none >= [45.95, none, 813, -90.84, -524, $parent]}
[91m                                       ...
```

### examples_00101_00200.pyrl

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
[93mLocation:[0m Line 7, Column 75
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 101
 6 | # ==================================================
 7 | class File extends Profile {init($word) = {! not %rule / null // (%header); return ["phone", None] and not [$mode, -371, 9.54, $accumulator, $size] * $phase; ret...
```

### examples_00201_00300.pyrl

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
[93mLocation:[0m Line 16, Column 32
[93mExpected one of:[0m Unknown

[93mContext:[0m
13 | 
14 | # Example 202
15 | # ==================================================
16 | &transform($left) = {print(468); print($message); verify({"address": $swap, "city": $avg, "address": false}); return}
[91m                                    ^...
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
[93mLocation:[0m Line 63, Column 115
[93mExpected one of:[0m Unknown

[93mContext:[0m
60 |     print({"data": $score, "error": $output, "username": false})
61 |     556
62 | else:
63 |     &read() = {print(process(-25.19, %rule) - @configs and {"address": null, "info": none, "city": $age} or False); print(%request)}
[91m          ...
```

### examples_00401_00500.pyrl

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
[93mLocation:[0m Line 31, Column 135
[93mExpected one of:[0m Unknown

[93mContext:[0m
28 | $char = null % 'end'
29 | $end = {"test": $tmp, "info": 'open', "password": False, "country": $tail} <= $factor / @segment == -316
30 | $line = %validation
31 | &delete() = {print(%subscription < $output == $factor < -{"key": $status, "name":...
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
[93mLocation:[0m Line 38, Column 56
[93mExpected one of:[0m Unknown

[93mContext:[0m
35 | 
36 | # Example 503
37 | # ==================================================
38 | class Factory extends Extension {init() = {print(&hide); $pos = 'pending' - @classes or "left" or $amplitude; 'tag'; return true} prop amount = $bound prop outp...
```

### examples_00601_00700.pyrl

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
[93mLocation:[0m Line 36, Column 95
[93mExpected one of:[0m Unknown

[93mContext:[0m
33 | 
34 | # Example 603
35 | # ==================================================
36 | class Matrix {prop data = [True] prop m method filter() = {if ['label', true] {{"info": None}}; %dict["sample"] = $percentage; @models[0] = @attributes; return}...
```

### examples_00701_00800.pyrl

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
[93mLocation:[0m Line 46, Column 35
[93mExpected one of:[0m Unknown

[93mContext:[0m
43 | $base = join($j, %payload, 'error') / True and @teams
44 | if execute($momentum) or {"code": $interval, "test": null, "status": $element, "key": -509, "code": True} - [466, -615, $phase, -27] and "email":
45 |     # Clean up
46 |     &close($i...
```

### examples_00801_00900.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 182
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 801
 6 | # ==================================================
 7 | class Runner extends Store {init($head, $phase) = {for $base in range(5) {if True <= -16.17 + %info // 12.08 {for $x in range(7) {if [$end, 806, True] {print([T...
```

### examples_00901_01000.pyrl

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
[93mLocation:[0m Line 36, Column 127
[93mExpected one of:[0m Unknown

[93mContext:[0m
33 |     %access = {"output": $head, "phone": $margin}
34 |     print((None))
35 |     # Process data
36 |     &transform($total) = {$width != 'begin' < false or %condition / $head == -4.40 <= [false, $avg, $n, 'message', -392, -293]; if @features...
```

### examples_01001_01100.pyrl

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
[93mLocation:[0m Line 15, Column 42
[93mExpected one of:[0m Unknown

[93mContext:[0m
12 | 
13 | # Example 1002
14 | # ==================================================
15 | &save($word) = {%policy["value"] = %theme; %entry = {"example": $area}; if [9.28, false, False, True, true, "on", 595] {$time = clear('on', {"result": -790}) =...
```

### examples_01101_01200.pyrl

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
[93mLocation:[0m Line 117, Column 109
[93mExpected one of:[0m Unknown

[93mContext:[0m
114 | 
115 | # Example 1108
116 | # ==================================================
117 | &disconnect() = {for $capacity in @collection {@tags = ["file", 216, $median, 'status', $parent, -584, 954]}; $speed = {"test": $width, "warning": $total...
```

### examples_01201_01300.pyrl

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
[93mLocation:[0m Line 10, Column 78
[93mExpected one of:[0m Unknown

[93mContext:[0m
 7 | $offset = -939
 8 | $pos = 'result' + none * [$error, True, -190, $next, 554, true, "type"] >= ["id", -8, -474, 'body', 305, $z, $threshold] // {"test": $density, "demo": True, "password": $interval, "name": $pos, "email": $val}
 9 | for $swap...
```

### examples_01301_01400.pyrl

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
[93mLocation:[0m Line 7, Column 67
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 1301
 6 | # ==================================================
 7 | &evaluate() = {print(compute({"phone": $temperature}, -266, True)); for $range in @indices {@data = [$limit, 3.22, 24.90, none, false, "off", -42.86]}; print(@c...
```

### examples_01401_01500.pyrl

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
[93mLocation:[0m Line 33, Column 70
[93mExpected one of:[0m Unknown

[93mContext:[0m
30 | # Example 1403
31 | # ==================================================
32 | &init($power, $velocity) = {$c = 'page'}
33 | &delete($c, $flag) = {for $ratio in @cache {@warnings[4] = [True, 30]; %access["error"] = True; %constraint["status"] =...
```

### examples_01501_01600.pyrl

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
[93mLocation:[0m Line 7, Column 223
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 1501
 6 | # ==================================================
 7 | &process($next_val, $frequency, $last) = {if %document and None * false or ['yes'] == -17.90 / {"city": $duration} {$sum = [545, false, "info", $min, true, 915...
```

### examples_01601_01700.pyrl

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
[93mLocation:[0m Line 121, Column 147
[93mExpected one of:[0m Unknown

[93mContext:[0m
118 | 
119 | # Example 1610
120 | # ==================================================
121 | &reset($angle, $z, $border) = {print((['right', none, "text", false, 'message', -335, "pending", 486] % %condition) > (-710) or 'disabled' % None); @head...
```

### examples_01701_01800.pyrl

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
[93mLocation:[0m Line 17, Column 35
[93mExpected one of:[0m Unknown

[93mContext:[0m
14 |     return
15 |     @words[4] = {"demo": False, "city": $mode, "password": 939}
16 |     return
17 | &clean() = {if [none, 626] {return; for $tail in range(5) {$min - {"phone": $total, "phone": true, "token": True, "code": $age, "data": "categ...
```

### examples_01801_01900.pyrl

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
[93mLocation:[0m Line 25, Column 112
[93mExpected one of:[0m Unknown

[93mContext:[0m
22 | # Example 1802
23 | # ==================================================
24 | def warn():
25 |     &configure($root, $j, $margin) = {@fragments = [-63.70, 903, True, -69.00, false, false, $remainder, 18.29]; print(&backup); @tokens[3] = %dict...
```

### examples_01901_02000.pyrl

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
[93mLocation:[0m Line 53, Column 114
[93mExpected one of:[0m Unknown

[93mContext:[0m
50 | if 'username' / {"token": 996, "error": $length, "phone": -491, "country": false}:
51 |     # Initialize variables
52 |     # Calculate result
53 | class Job extends Checker {init($next, $output) = {$next = @list >= -68.63 > True > min($head,...
```

### examples_02001_02100.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 10, Column 155
[93mExpected one of:[0m Unknown

[93mContext:[0m
 7 | def test():
 8 |     @categories[9] = $temperature
 9 |     # Validate input
10 |     &run($count, $previous) = {if -{"country": True, "country": null, "code": -787} // @options <= $angle + null and $name {$error or $tmp < $text or $end; retu...
```

### examples_02101_02200.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 18
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 2101
 6 | # ==================================================
 7 | &test() = {return; $child = %order - @fragments < 69 + %header; print(@products); return}
[91m                      ^[0m
 8 | &configure($first, $force, $rate...
```

### examples_02201_02300.pyrl

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
[93mLocation:[0m Line 7, Column 40
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 2201
 6 | # ==================================================
 7 | &execute($temperature) = {print("info"); for $amount in @chunk {if (none - $coefficient) * (329) {for $i in range(5) {%session["test"] = {"email": $avg, "info":...
```

### examples_02301_02400.pyrl

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
[93mLocation:[0m Line 39, Column 55
[93mExpected one of:[0m Unknown

[93mContext:[0m
36 |     %environment["data"] = "yes"
37 |     @block = [-442, 580, False, $circumference, 2.71]
38 |     return
39 | &convert($n) = {if "note" {return [$left, "key", none]; @configs[9] = {"success": 'password', "email": 883}; print(-null)} else {i...
```

### examples_02401_02500.pyrl

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
[93mLocation:[0m Line 25, Column 167
[93mExpected one of:[0m Unknown

[93mContext:[0m
22 |     @strings = [$time, 'link']
23 |     $count = &insert >= @section
24 |     @rows[10] = {"input": "end", "id": $area, "result": 329, "input": $current}
25 | class Runner extends Stream {prop result = %response prop total = {"info": $speed} ...
```

### examples_02501_02600.pyrl

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
[93mLocation:[0m Line 21, Column 76
[93mExpected one of:[0m Unknown

[93mContext:[0m
18 | # Example 2502
19 | # ==================================================
20 | # Initialize variables
21 | &connect($padding, $load, $height) = {return [None, 58, 965, False, -33.79]; &verify; return {"phone": false} / $node and @types and true...
```

### examples_02601_02700.pyrl

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
[93mLocation:[0m Line 17, Column 72
[93mExpected one of:[0m Unknown

[93mContext:[0m
14 |     # Check condition
15 | for $start in range(12):
16 |     print(keys())
17 |     &reset($result) = {print(True - @elements <= @products + "success"); print("chapter"); return}
[91m                                                           ...
```

### examples_02701_02800.pyrl

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
[93mLocation:[0m Line 47, Column 36
[93mExpected one of:[0m Unknown

[93mContext:[0m
44 | 
45 | # Example 2704
46 | # ==================================================
47 | &load($median) = {@numbers[10] = $j; print((find($max, $acceleration, True)) - %order); $tail = ! %customer; return ({"error": $m, "data": "pending", "key": 16...
```

### examples_02801_02900.pyrl

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
[93mLocation:[0m Line 7, Column 67
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 2801
 6 | # ==================================================
 7 | class Clock {init() = {for $rate in @properties {-599 or 'enabled'; while strip($median, "right") != [727, 45.86, -83.14, -160] == None % items() < @ids and 'do...
```

### examples_02901_03000.pyrl

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
[93mLocation:[0m Line 44, Column 64
[93mExpected one of:[0m Unknown

[93mContext:[0m
41 | 
42 | # Example 2904
43 | # ==================================================
44 | &transform($percentage, $size, $parent) = {@issues[10] = 'link'; return -30.83 + print(-346) > None // @units}
[91m                                           ...
```

### examples_03001_03100.pyrl

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
[93mLocation:[0m Line 7, Column 33
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 3001
 6 | # ==================================================
 7 | &send() = {@inputs[10] = @groups; print($min); print(%mapping * $z / "address" + not -957 <= None - {"error": "title", "country": false}); print((! false > true...
```

### examples_03101_03200.pyrl

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
[93mLocation:[0m Line 38, Column 78
[93mExpected one of:[0m Unknown

[93mContext:[0m
35 | for $difference in range(7):
36 |     %context = {"value": 34.89, "code": "type"}
37 |     # Format output
38 |     &test($magnitude, $pressure) = {not (@units <= [18.56, -202, true, None]); %info["sample"] = 'category'; return; print(str([nul...
```

### examples_03201_03300.pyrl

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
[93mLocation:[0m Line 9, Column 42
[93mExpected one of:[0m Unknown

[93mContext:[0m
 6 | # ==================================================
 7 | $root = @tasks > %fields >= ["category", 'city', -641]
 8 | $ratio = %subscription
 9 | &check($speed, $error) = {{"result": -58}; $pos = false == @segment; return}
[91m                ...
```

### examples_03301_03400.pyrl

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
[93mLocation:[0m Line 7, Column 44
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 3301
 6 | # ==================================================
 7 | class Database {init() = {return 'password'; return 66.94 * (@items) / 'test' < {"test": $leaf} < 'link'; return (-12.54 < @headers <= $age or %account)} prop r...
```

### examples_03401_03500.pyrl

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
[93mLocation:[0m Line 17, Column 105
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m [, boolean, number, $variable, %variable, R, (, None, @variable, {, ... and 3 more

[93mContext:[0m
14 | # Example 3402
15 | # ==================================================
16 | def disable($amplitude, $a):
17 |     asser...
```

### examples_03501_03600.pyrl

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
[93mLocation:[0m Line 45, Column 46
[93mExpected one of:[0m Unknown

[93mContext:[0m
42 |     print(load($threshold, 'group'))
43 |     %table["warning"] = $width
44 |     print(True)
45 |     &test($k, $text) = {%map["key"] = &format; $end = -51.63 / -400; if -42.79 {@items and True and 657 == (@properties); for $counter in @sessi...
```

### examples_03601_03700.pyrl

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
[93mLocation:[0m Line 7, Column 151
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 3601
 6 | # ==================================================
 7 | class Response {prop data method get() = {return max($interval) or &log + -67.66 and 'example' <= {"error": -573, "password": 'target', "error": none}; @sectio...
```

### examples_03701_03800.pyrl

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
[93mLocation:[0m Line 7, Column 36
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 3701
 6 | # ==================================================
 7 | &clear($name, $offset) = {('group'); return "key" - None // %context // list() == abs([true, $capacity, "file", false], {"country": false, "info": $direction, "...
```

### examples_03801_03900.pyrl

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
[93mLocation:[0m Line 23, Column 139
[93mExpected one of:[0m Unknown

[93mContext:[0m
20 |     $k = ($capacity)
21 | for $size in range(12):
22 |     $swap = $z
23 |     &delete() = {$counter = verify($pos, {"city": $acceleration, "key": $y, "data": true, "email": 'complete', "message": 546}, "comment"); while 329 >= @array {%entry...
```

### examples_03901_04000.pyrl

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
[93mLocation:[0m Line 121, Column 137
[93mExpected one of:[0m Unknown

[93mContext:[0m
118 | 
119 | # Example 3909
120 | # ==================================================
121 | &load($counter, $text, $quantity) = {while 'title' or @pool // 'link' or ["output", None, $quantity, null, $interval] {$volume = @series; if keys() < flo...
```

### examples_04001_04100.pyrl

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
[93mLocation:[0m Line 147, Column 29
[93mExpected one of:[0m Unknown

[93mContext:[0m
144 | 
145 | # Example 4010
146 | # ==================================================
147 | &validate($exponent) = {-855; range(False, $volume); %color = {"country": $z, "value": $i, "email": -16.85, "demo": "body"}; return {"country": $accelerat...
```

### examples_04101_04200.pyrl

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
[93mLocation:[0m Line 15, Column 155
[93mExpected one of:[0m Unknown

[93mContext:[0m
12 |     # Calculate result
13 |     $min = convert()
14 |     ($node - [-629, -732, none, -70.77, 139, 539, $pivot] or 64)
15 |     &insert($angle) = {if ["yes", None, -803, false, 310] or %payload {$node = True <= ["result", null, 87.10, 'output...
```

### examples_04201_04300.pyrl

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
[93mLocation:[0m Line 12, Column 51
[93mExpected one of:[0m Unknown

[93mContext:[0m
 9 | $remainder = 544 + True <= ["phone", 10.21, true, False, 729, -315] or ('done')
10 | $key = parse(%order, ["city", $val, -977, "country", null, 124, 'enabled', $quantity])
11 | if %meta:
12 |     &init($threshold, $swap, $mode) = {return True;...
```

### examples_04301_04400.pyrl

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
[93mLocation:[0m Line 35, Column 82
[93mExpected one of:[0m Unknown

[93mContext:[0m
32 | def handle():
33 |     # Initialize variables
34 |     # Update state
35 |     &receive() = {return {"info": $pressure, "value": $exponent, "hello": "data"}; @chars = [null, "title", -5.88, False, -83.24, -37.27, True]; $b = true; print(null <...
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
[93mLocation:[0m Line 53, Column 103
[93mExpected one of:[0m Unknown

[93mContext:[0m
50 | 
51 | # Example 4404
52 | # ==================================================
53 | &fetch($end, $speed, $y) = {print(['yes', 979, False, -939, -558] and 'on' + $key >= -258 - not int()); [-221, 173]; $denominator = @processes; for $next in @...
```

### examples_04501_04600.pyrl

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
[93mLocation:[0m Line 23, Column 35
[93mExpected one of:[0m Unknown

[93mContext:[0m
20 | $token = run(%result)
21 | $time = "done"
22 | $frequency = -47.29 or False or &receive - 71.32 and "url"
23 | &save($tmp, $size) = {print($flag); return (-713) - &test <= ([False, "false", "active", $text, True, -73, False])}
[91m           ...
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
[93mLocation:[0m Line 34, Column 128
[93mExpected one of:[0m Unknown

[93mContext:[0m
31 | for $swap in range(6):
32 |     # Calculate result
33 |     # Initialize variables
34 | class Container {prop price = true prop j prop data = 'link' prop score = $price method slice($height) = {%product["name"] = 76; while --55.88 + false == ...
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
[93mLocation:[0m Line 17, Column 59
[93mExpected one of:[0m Unknown

[93mContext:[0m
14 | # ==================================================
15 | def test($margin, $total, $momentum, $buffer):
16 |     $previous = $threshold
17 |     &fetch($difference, $width) = {@messages[10] = &insert; print(@types); $interval = (! -52) / (map...
```

### examples_04801_04900.pyrl

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
[93mLocation:[0m Line 42, Column 114
[93mExpected one of:[0m Unknown

[93mContext:[0m
39 | 
40 | # Example 4804
41 | # ==================================================
42 | &evaluate($first, $right) = {return [$val, -31.42, 506, none, 'true'] % 'complete' and 'begin' + 756 < not -95.73; print(strip(@tags, &refresh, @alerts)); if ...
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
[93mLocation:[0m Line 18, Column 102
[93mExpected one of:[0m Unknown

[93mContext:[0m
15 | 
16 | # Example 4902
17 | # ==================================================
18 | class Adapter {prop count = %settings prop score prop output method join($last) = {return calculate(); if (convert([29.09, 478, -418, null])) + {"password": "...
```

### examples_05001_05100.pyrl

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
[93mLocation:[0m Line 22, Column 63
[93mExpected one of:[0m Unknown

[93mContext:[0m
19 | 
20 | # Example 5002
21 | # ==================================================
22 | &reset($amplitude) = {@users = [$char, false, -74.48, $center]; [617, 'demo', "city", -889, $next_val, True, 977] > sum(); print(%properties // {"test": 'demo'...
```

### examples_05101_05200.pyrl

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
[93mLocation:[0m Line 14, Column 38
[93mExpected one of:[0m Unknown

[93mContext:[0m
11 |     print((846 // {"status": 'link', "key": 'inactive', "data": $b, "username": $word} == $phase))
12 |     # Log message
13 |     return
14 | &calculate($force, $node) = {&restart; $density; calculate(-59.08) and @array * not 'test' != $age; ...
```

### examples_05201_05300.pyrl

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
[93mLocation:[0m Line 34, Column 69
[93mExpected one of:[0m Unknown

[93mContext:[0m
31 |     # Update state
32 |     # Log message
33 |     # Update state
34 | &open($force) = {$base = [True, "note", 13] >= save() <= -711 + True; return ([None, $quantity, 782, -703, True, -501] - [null]) != ! {"country": 29, "sample": -558}; test(...
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
[93mLocation:[0m Line 12, Column 140
[93mExpected one of:[0m Unknown

[93mContext:[0m
 9 | def forward($tail, $temperature, $remainder):
10 |     # Validate input
11 |     print([$diameter, -985, $sum, -253, True] < "demo" * 'phone' == &increase)
12 |     &configure($exponent, $tail) = {$duration = convert([429], [-45.08, 210, Fals...
```

### examples_05401_05500.pyrl

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
[93mLocation:[0m Line 7, Column 135
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 5401
 6 | # ==================================================
 7 | &test($magnitude, $element) = {print(["username", $word, 481, 'section', "content", -60] < -{"data": false, "error": $score} % "city"); @properties[7] = [none,...
```

### examples_05501_05600.pyrl

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
[93mLocation:[0m Line 7, Column 65
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 5501
 6 | # ==================================================
 7 | class Module {init() = {return [$m, "section", "text", 276, 501]; return} prop quantity prop age = false prop name = %storage prop score method join() = {for $a...
```

### examples_05601_05700.pyrl

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
[93mLocation:[0m Line 62, Column 29
[93mExpected one of:[0m Unknown

[93mContext:[0m
59 | def divide($height, $word):
60 |     %session = {"demo": $a, "code": $denominator, "message": 118}
61 |     print(items() * @events % {"warning": True, "type": $start})
62 |     &save() = {print($ratio); return}
[91m                          ...
```

### examples_05701_05800.pyrl

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
[93mLocation:[0m Line 9, Column 61
[93mExpected one of:[0m Unknown

[93mContext:[0m
 6 | # ==================================================
 7 | @bytes = [True, -34.56, -871, False]
 8 | $x = True <= (None and {"result": $previous})
 9 | &retrieve($count, $line, $b) = {[-970, 192, none, 'enabled']; return}
[91m                  ...
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
[93mLocation:[0m Line 63, Column 55
[93mExpected one of:[0m Unknown

[93mContext:[0m
60 | 
61 | # Example 5806
62 | # ==================================================
63 | class Plugin {init($rate, $y) = {@collection[6] = True; return [False]} prop value prop x prop result = -440 method reload() = {while -@piece {return {"output"...
```

### examples_05901_06000.pyrl

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
[93mLocation:[0m Line 19, Column 58
[93mExpected one of:[0m Unknown

[93mContext:[0m
16 | # ==================================================
17 | %response["result"] = $center
18 | assert ! &expand % 786 > close(@logs, 413)
19 | &clean() = {$child = [655, None, -731, -41.44] > $counter; [True, None, 75, 50.69, 429]}
[91m        ...
```

### examples_06001_06100.pyrl

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
[93mLocation:[0m Line 139, Column 184
[93mExpected one of:[0m Unknown

[93mContext:[0m
136 | 
137 | # Example 6011
138 | # ==================================================
139 | &run($z, $head, $z) = {if @numbers or -848 // None - none {@types = [None, -816, $flag, "group"]} else {if $phase {$limit = (find(885, &merge)) > [$momen...
```

### examples_06101_06200.pyrl

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
[93mLocation:[0m Line 56, Column 152
[93mExpected one of:[0m Unknown

[93mContext:[0m
53 | # ==================================================
54 | &compute() = {($avg and {"address": none, "hello": True, "key": $mode, "id": $text, "key": -615})}
55 | &run() = {$offset = $result}
56 | &clear($length, $pivot, $avg) = {if [-318] {pr...
```

### examples_06201_06300.pyrl

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
[93mLocation:[0m Line 77, Column 174
[93mExpected one of:[0m Unknown

[93mContext:[0m
74 | 
75 | # Example 6208
76 | # ==================================================
77 | class Observer {prop z method reset($z, $previous) = {@rows - [None, 871, 84.85, none, -517, "body", 949, none] - null < [$force] and $threshold == $magnitude...
```

### examples_06301_06400.pyrl

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
[93mLocation:[0m Line 7, Column 112
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 6301
 6 | # ==================================================
 7 | class Checker {init($phase) = {%header = {"username": $status, "city": False, "city": $message, "world": $prev}; ! ['category'] or 'country'; for $coefficient ...
```

### examples_06401_06500.pyrl

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
[93mLocation:[0m Line 9, Column 64
[93mExpected one of:[0m Unknown

[93mContext:[0m
 6 | # ==================================================
 7 | test "input":
 8 |     print(784)
 9 |     &execute() = {@jobs = ["tag", 289, True, $quotient, 'text']; $velocity; $element > {"id": $size}; calculate($denominator, none); return 265}
[...
```

### examples_06501_06600.pyrl

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
[93mLocation:[0m Line 16, Column 45
[93mExpected one of:[0m Unknown

[93mContext:[0m
13 | 
14 | # Example 6502
15 | # ==================================================
16 | &remove($speed, $node) = {$total = "chapter"; 83.74; print([$acceleration, none, $counter, 842, True]); return}
[91m                                          ...
```

### examples_06601_06700.pyrl

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
[93mLocation:[0m Line 8, Column 87
[93mExpected one of:[0m Unknown

[93mContext:[0m
 5 | # Example 6601
 6 | # ==================================================
 7 | &write($data) = {print(%storage)}
 8 | &compute($volume, $child, $amount) = {for $duration in range(3) {@elements = [-89.63]}; return; for $power in @rows {-calculate...
```

### examples_06701_06800.pyrl

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
[93mLocation:[0m Line 14, Column 125
[93mExpected one of:[0m Unknown

[93mContext:[0m
11 | # Example 6702
12 | # ==================================================
13 | class Point {prop score = $element prop score prop c method remove($percentage, $mass) = {%item = {"error": $y}}}
14 | class Processor extends Component {prop data ...
```

### examples_06801_06900.pyrl

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
[93mLocation:[0m Line 57, Column 108
[93mExpected one of:[0m Unknown

[93mContext:[0m
54 |     # Initialize variables
55 |     $score = save($age, -77.11) < load({"demo": "output"}, [-961, -44.01, 972, $head, 'test', $next_val, 748, 303], @elements)
56 |     # Handle error
57 |     &compute($base, $left, $node) = {print(["section",...
```

### examples_07001_07100.pyrl

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
[93mLocation:[0m Line 7, Column 226
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 7001
 6 | # ==================================================
 7 | class Reporter {prop n = $limit prop a prop j = $mode method delete($result) = {@inputs = [90.66, 25, $padding, $output]} method merge($amplitude, $temp) = {%m...
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
[93mLocation:[0m Line 16, Column 46
[93mExpected one of:[0m Unknown

[93mContext:[0m
13 | 
14 | # Example 7102
15 | # ==================================================
16 | class Image {init() = {@bytes[10] = $capacity; $text = replace() + False > $child; return} prop y prop value method append() = {$min and "done"; %role["status"...
```

### examples_07201_07300.pyrl

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
[93mLocation:[0m Line 53, Column 62
[93mExpected one of:[0m Unknown

[93mContext:[0m
50 | 
51 | # Example 7205
52 | # ==================================================
53 | class Scheduler {init($load, $y) = {%state = {"info": $token}; 'page' != [-794, 74.08, null, $quotient]; $magnitude; return} prop value = {"warning": 221, "cod...
```

### examples_07301_07400.pyrl

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
[93mLocation:[0m Line 9, Column 23
[93mExpected one of:[0m Unknown

[93mContext:[0m
 6 | # ==================================================
 7 | # Handle error
 8 | @points = [636, -45.44, $token, True, "begin", 704, none, -11.94]
 9 | &initialize() = {$data; return load(%font) or $rate == &sign; return}
[91m                    ...
```

### examples_07401_07500.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 14, Column 66
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m {, boolean, (, identifier, %variable, string, &variable, $variable, None, @variable, ... and 3 more

[93mContext:[0m
11 |     @columns = [12.78, -763, $result]
12 |     (not ! 729)
13 | else:
14 |     print(True + [88.68, false...
```

### examples_07501_07600.pyrl

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
[93mLocation:[0m Line 7, Column 58
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 7501
 6 | # ==================================================
 7 | class Runner {init() = {%result = {"test": 'description'}; print(@types - (True) and %subscription); return ((-423) <= false)} prop age = null prop total prop q...
```

### examples_07601_07700.pyrl

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
[93mLocation:[0m Line 45, Column 145
[93mExpected one of:[0m Unknown

[93mContext:[0m
42 | def encode($mass, $next):
43 |     # Handle error
44 |     # Update state
45 | &format($base, $mass, $density) = {return &add != None or %meta == %fields or (values(&unsubscribe, 'country', [-35.54, -707, "sample", $next])); %profile["sample"...
```

### examples_07701_07800.pyrl

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
[93mLocation:[0m Line 73, Column 172
[93mExpected one of:[0m Unknown

[93mContext:[0m
70 | 
71 | # Example 7706
72 | # ==================================================
73 | class Logger {prop data prop b = 557 prop temp = {"example": -412} prop item = 48.74 method refresh($duration, $tail) = {while 800 % {"message": false} {$quot...
```

### examples_07801_07900.pyrl

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
[93mLocation:[0m Line 7, Column 56
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 7801
 6 | # ==================================================
 7 | &delete($n, $acceleration) = {if $angle or $end {! None; print(({"country": 29.39, "username": $energy})); while {"address": $input} >= {"demo": $error, "id": $...
```

### examples_07901_08000.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 50
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 7901
 6 | # ==================================================
 7 | class Image {init($tmp) = {while %profile {return; return $numerator}; return &load and format(27.87, [none, 420, 862, $name, False, -68, 'description']) < @seq...
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
[93mLocation:[0m Line 81, Column 34
[93mExpected one of:[0m Unknown

[93mContext:[0m
78 | 
79 | # Example 8007
80 | # ==================================================
81 | &test() = {%item = {"test": $max}; if %plan <= -147 == $input or [-46.10, $error, none, $buffer, True, -13.09, 'content'] {$power = 94.44}; if None {%output["s...
```

### examples_08101_08200.pyrl

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
[93mLocation:[0m Line 38, Column 66
[93mExpected one of:[0m Unknown

[93mContext:[0m
35 | 
36 | # Example 8102
37 | # ==================================================
38 | class Monitor extends Matrix {init() = {print([-612, none, -308]); $angle = ($base) * strip({"email": "group"}) >= %response // ("no"); return "active" == fals...
```

### examples_08201_08300.pyrl

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
[93mLocation:[0m Line 10, Column 29
[93mExpected one of:[0m Unknown

[93mContext:[0m
 7 | test "country":
 8 |     @vector[4] = ["waiting", 991, -935, $limit]
 9 |     @rows = [$max, $first, "message", null, 'end', 89]
10 |     &parse($ratio) = {return; if (transform($b, [76.64, "start", 781, -263])) {@args[10] = {"info": $diameter...
```

### examples_08301_08400.pyrl

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
[93mLocation:[0m Line 29, Column 84
[93mExpected one of:[0m Unknown

[93mContext:[0m
26 | $rate = 'success' and %person
27 | if ['file', None, 896, True, none, 899, null] / ! [false, "start", $base, false, 972, 'ready'] and initialize(-507):
28 |     print(execute("country"))
29 |     &clean($swap, $circumference, $total) = {return...
```

### examples_08401_08500.pyrl

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
[93mLocation:[0m Line 19, Column 153
[93mExpected one of:[0m Unknown

[93mContext:[0m
16 |     print(771)
17 |     $y = null
18 | while "section":
19 |     &clean($y, $entry) = {while (&error // &init) + None {[41.27, -80, "begin", $median, False] and -82.57 != [-483, -137, $start] / ['warning', $width]; %session and 34.39 or $mode...
```

### examples_08501_08600.pyrl

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
[93mLocation:[0m Line 36, Column 61
[93mExpected one of:[0m Unknown

[93mContext:[0m
33 |     $border = 485
34 |     assert convert(@series, 288) >= {"message": null} < &validate
35 |     # Initialize variables
36 |     &delete($max, $area, $current) = {@numbers[2] = @options; for $coefficient in range(6) {91.34 or "url" <= %respon...
```

### examples_08601_08700.pyrl

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
[93mLocation:[0m Line 23, Column 6
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m {, string, boolean, &variable, None, R, (, $variable, number, @variable, ... and 3 more

[93mContext:[0m
20 | def increment($width):
21 |     return -665 % "close" / ["start", true, False, none, "status", -84.11, true]
22 |     ...
```

### examples_08701_08800.pyrl

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
[93mLocation:[0m Line 43, Column 52
[93mExpected one of:[0m Unknown

[93mContext:[0m
40 | while ! [16.86, 305, 432, $min, 43, 'section', -32.83, False] % {"city": 742, "result": $buffer, "country": 623, "sample": True, "name": $volume} % %membership / 388:
41 |     assert not (%context <= $power) != ! %item
42 |     # Initialize va...
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
[93mLocation:[0m Line 25, Column 56
[93mExpected one of:[0m Unknown

[93mContext:[0m
22 | # ==================================================
23 | print({"output": 911, "sample": $threshold})
24 | 113
25 | &update() = {@settings = [-528, 510, $leaf, -420, None]; -41.39 != compute() * false // $i; @bytes = [$previous, $swap, 'right...
```

### examples_08901_09000.pyrl

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
[93mLocation:[0m Line 7, Column 96
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 8901
 6 | # ==================================================
 7 | &store($amount, $message, $mode) = {%entry = {"country": "right", "email": true, "input": true}; @batch = [274, 373, 3.71, "start", none, $name]}
[91m         ...
```

### examples_09001_09100.pyrl

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
[93mLocation:[0m Line 19, Column 39
[93mExpected one of:[0m Unknown

[93mContext:[0m
16 | 
17 | # Example 9002
18 | # ==================================================
19 | &receive($i, $swap, $b) = {%attributes; if verify(@bits, [902, 'result', true, "inactive", -912, -50, 72, false]) {%font = {"message": None, "city": $head, "sa...
```

### examples_09101_09200.pyrl

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
[93mLocation:[0m Line 7, Column 79
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 9101
 6 | # ==================================================
 7 | &write() = {@attributes = [none, 942, $distance, -44.73, "key", "sample", -77]; return}
[91m                                                                   ...
```

### examples_09201_09300.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 7, Column 154
[93mExpected one of:[0m Unknown

[93mContext:[0m
 4 | 
 5 | # Example 9201
 6 | # ==================================================
 7 | class Checker {prop y prop count = false method remove($min) = {print(&unsubscribe - "demo" // (@notifications))} method splice() = {$last or dict(%meta); init...
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
[93mLocation:[0m Line 33, Column 34
[93mExpected one of:[0m Unknown

[93mContext:[0m
30 | # Handle error
31 | # Initialize variables
32 | print(not False * [$total, True, True, -291, 'input', 'inactive'] >= [78.14, 'finish', $result, "body"] - 82.83 != ['file', $pos, $first, $border, -803, 'group', "href", 44.56] + $percentage)
33 ...
```

### examples_09401_09500.pyrl

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
[93mLocation:[0m Line 56, Column 18
[93mExpected one of:[0m Unknown

[93mContext:[0m
53 | @entries = ['demo', -619, $element, none, -687, 72.26, -315]
54 | len(-60.65) < $interval == [false, $data, 436, $child, True, False] + True
55 | $value = True == float("no", {"error": $mass, "type": $quotient, "output": -767}, %environment)
5...
```

### examples_09501_09600.pyrl

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
[93mLocation:[0m Line 77, Column 210
[93mExpected one of:[0m Unknown

[93mContext:[0m
74 | 
75 | # Example 9506
76 | # ==================================================
77 | &insert($duration, $max, $bound) = {while "phone" + %cache + items(@sessions, @records) and any(%fields, %theme, 'path') > %state {clean([$y, -39.15, $token, ...
```

### examples_09601_09700.pyrl

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
[93mLocation:[0m Line 7, Column 10
[93mUnexpected token:[0m '-' (type: ADD_OP)
[93mExpected one of:[0m string, boolean, R, %variable, {, number, @variable, [, $variable, identifier, ... and 3 more

[93mContext:[0m
 4 | 
 5 | # Example 9601
 6 | # ==================================================
 7 | $pos = (--1.47 // @requests)...
```

### examples_09701_09800.pyrl

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
[93mLocation:[0m Line 16, Column 107
[93mExpected one of:[0m Unknown

[93mContext:[0m
13 |     $temperature = {"example": $interval, "key": $j} or $median or -42.99 + [347]
14 |     print(&expand)
15 | elif {"error": $power}:
16 |     &read($element) = {$b = [none, false, -589] or False and {"token": $velocity} <= ['label'] >= &res...
```

### examples_09801_09900.pyrl

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
[93mLocation:[0m Line 141, Column 41
[93mExpected one of:[0m Unknown

[93mContext:[0m
138 | if -(%settings > &revert):
139 |     assert ! close(-522) != ['pending', 36.15, $k, False, false, None, $avg]
140 | for $node in @elements:
141 |     &format($mass, $pos) = {print($size); return}
[91m                                        ...
```

### examples_09901_10000.pyrl

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
[93mLocation:[0m Line 70, Column 80
[93mExpected one of:[0m Unknown

[93mContext:[0m
67 | def read():
68 |     return @configs
69 |     $pivot = "error"
70 |     &process($width, $tail, $percentage) = {handle(@columns, $height, @entries); while ! 'body' and %rule // (@customers) {if None {return ! "sample"; $length or 577 or %privi...
```

### web_server_auth.pyrl

- **Category:** root
- **Error Type:** PYRL RUNTIME ERROR
- **Error Message:** [91m============================================================[0m
- **Line:** None
- **Execution Time:** 0.50s

**Stderr:**
```text
[91m============================================================[0m
[91mPARSE ERROR[0m
[91m============================================================[0m
[93mLocation:[0m Line 563, Column 17
[93mUnexpected token:[0m 'in' (type: IDENT)
[93mExpected one of:[0m :

[93mContext:[0m
560 |         # Find matching route
561 |         $key = $method + ":" + $path
562 |         
563 |         if $key in $self.routes:
[91m                      ^^[0m
564 |             $handler = $self.route...
```


## Error Types

### PYRL RUNTIME ERROR (105 occurrences)

- 06_anonymous_functions.pyrl
- 06_classes.pyrl
- 07_classes.pyrl
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
