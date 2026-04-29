由于无论如何排列 $n$ 中的数位，这些数位的阶乘之和是不变的。

设 $n$ 的各个数位的阶乘之和为 $s$。问题变成：

- 能否把 $n$ 重新排列，变成 $s$？

只要 $n$ 和 $s$ 中的 $0,1,2,\ldots,9$ 的个数都相等，$n$ 就可以重排成 $s$。

如何遍历 $n$ 的每个数位？可以把 $n$ 转成字符串。也可以不断地把 $n$ 除以 $10$（下取整）直到 $0$，例如 $123\to 12\to 1\to 0$。在这个过程中的 $n\bmod 10$，即为每个数位。

**注**：题目不允许 $n$ 重排后有前导零。当 $n$ 和 $s$ 重排相同时，二者十进制**长度相等**，由于 $s$ 没有前导零，所以 $n$ 重排成 $s$ 后也没有前导零。

[本题视频讲解](https://www.bilibili.com/video/BV1HeZfB7EBt/?t=5m45s)，欢迎点赞关注~

```py [sol-Python3]
# 预处理阶乘
fac = [1] * 10
for i in range(1, 10):
    fac[i] = fac[i - 1] * i

class Solution:
    def isDigitorialPermutation(self, n: int) -> bool:
        sum_fac = 0
        cnt = [0] * 10
        while n > 0:
            n, d = divmod(n, 10)
            sum_fac += fac[d]
            cnt[d] += 1

        while sum_fac > 0:
            sum_fac, d = divmod(sum_fac, 10)
            cnt[d] -= 1

        return cnt == [0] * 10
```

```java [sol-Java]
class Solution {
    private static final int[] fac = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880};

    public boolean isDigitorialPermutation(int n) {
        int sumFac = 0;
        int[] cnt = new int[10];
        for (; n > 0; n /= 10) {
            int d = n % 10;
            sumFac += fac[d];
            cnt[d]++;
        }

        for (; sumFac > 0; sumFac /= 10) {
            cnt[sumFac % 10]--;
        }

        for (int i = 0; i < 10; i++) {
            if (cnt[i] != 0) {
                return false;
            }
        }
        return true;
    }
}
```

```cpp [sol-C++]
class Solution {
    static constexpr int fac[] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880};

public:
    bool isDigitorialPermutation(int n) {
        int sum_fac = 0;
        array<int, 10> cnt{};
        for (; n > 0; n /= 10) {
            int d = n % 10;
            sum_fac += fac[d];
            cnt[d]++;
        }

        for (; sum_fac > 0; sum_fac /= 10) {
            cnt[sum_fac % 10]--;
        }

        // cnt[i] == 0
        return cnt == array<int, 10>();
    }
};
```

```go [sol-Go]
var fac = [10]int{1}

func init() {
	// 预处理阶乘
	for i := 1; i < len(fac); i++ {
		fac[i] = fac[i-1] * i
	}
}

func isDigitorialPermutation(n int) bool {
	sumFac := 0
	cnt := [10]int{}
	for ; n > 0; n /= 10 {
		d := n % 10
		sumFac += fac[d]
		cnt[d]++
	}

	for ; sumFac > 0; sumFac /= 10 {
		cnt[sumFac%10]--
	}

	// cnt[i] == 0
	return cnt == [10]int{}
}
```

#### 复杂度分析

不计入预处理阶乘的时间和空间。

- 时间复杂度：$\mathcal{O}(\log n + D)$。其中 $D=10$。创建大小为 $D$ 的数组需要 $\mathcal{O}(D)$ 的时间和空间。
- 空间复杂度：$\mathcal{O}(D)$。

## 注

$9! = 362880$，所以 $7$ 个 $9!$ 之和小于 $9999999$，后续 $99\ldots9$ 的增长速度比十进制长度乘以 $9!$ 更快，所以只需考虑 $n<9999999$ 的解。

暴力枚举后发现，去掉重排后等价的解，只有 $4$ 个本质不同的解：

$$
1,2,145,40558
$$

```py
class Solution:
    def isDigitorialPermutation(self, n: int) -> bool:
        s = ''.join(sorted(str(n)))
        return s in ('1', '2', '145', '04558')
```

## 相似题目

[49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/)

## 分类题单

[如何科学刷题？](https://leetcode.cn/circle/discuss/RvFUtj/)

1. [滑动窗口与双指针（定长/不定长/单序列/双序列/三指针/分组循环）](https://leetcode.cn/circle/discuss/0viNMK/)
2. [二分算法（二分答案/最小化最大值/最大化最小值/第K小）](https://leetcode.cn/circle/discuss/SqopEo/)
3. [单调栈（基础/矩形面积/贡献法/最小字典序）](https://leetcode.cn/circle/discuss/9oZFK9/)
4. [网格图（DFS/BFS/综合应用）](https://leetcode.cn/circle/discuss/YiXPXW/)
5. [位运算（基础/性质/拆位/试填/恒等式/思维）](https://leetcode.cn/circle/discuss/dHn9Vk/)
6. [图论算法（DFS/BFS/拓扑排序/基环树/最短路/最小生成树/网络流）](https://leetcode.cn/circle/discuss/01LUak/)
7. [动态规划（入门/背包/划分/状态机/区间/状压/数位/数据结构优化/树形/博弈/概率期望）](https://leetcode.cn/circle/discuss/tXLS3i/)
8. [常用数据结构（前缀和/差分/栈/队列/堆/字典树/并查集/树状数组/线段树）](https://leetcode.cn/circle/discuss/mOr1u6/)
9. [数学算法（数论/组合/概率期望/博弈/计算几何/随机算法）](https://leetcode.cn/circle/discuss/IYT3ss/)
10. [贪心与思维（基本贪心策略/反悔/区间/字典序/数学/思维/脑筋急转弯/构造）](https://leetcode.cn/circle/discuss/g6KTKL/)
11. [链表、树与回溯（前后指针/快慢指针/DFS/BFS/直径/LCA）](https://leetcode.cn/circle/discuss/K0n2gO/)
12. [字符串（KMP/Z函数/Manacher/字符串哈希/AC自动机/后缀数组/子序列自动机）](https://leetcode.cn/circle/discuss/SJFwQI/)

[我的题解精选（已分类）](https://github.com/EndlessCheng/codeforces-go/blob/master/leetcode/SOLUTIONS.md)
