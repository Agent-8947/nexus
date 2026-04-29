如果 $\textit{nums}$ 每个数的出现次数都一样，那么无解。

如果有两个出现次数不同的元素，那么直接把 $\min(\textit{nums})$ 作为 $x$，即可满足题目要求。由于 $x$ 是最小值，另一个出现次数不同的数必然大于 $x$，题目的第一个要求 $x<y$ 自动成立。

对于 $y$，选择 $\textit{nums}$ 中的出现次数不等于 $x$ 的出现次数的最小元素。

统计元素出现次数可以用哈希表（或者数组）。

[本题视频讲解](https://www.bilibili.com/video/BV1VvABz9EGz/)，欢迎点赞关注~

```py [sol-Python3]
class Solution:
    def minDistinctFreqPair(self, nums: List[int]) -> List[int]:
        cnt = Counter(nums)
        mn = min(nums)

        cnt_min = cnt[mn]
        min_y = min((y for y, c in cnt.items() if c != cnt_min), default=None)

        if min_y is None:
            return [-1, -1]
        return [mn, min_y]
```

```java [sol-Java]
class Solution {
    public int[] minDistinctFreqPair(int[] nums) {
        Map<Integer, Integer> cnt = new HashMap<>();
        int mn = Integer.MAX_VALUE;
        for (int x : nums) {
            cnt.merge(x, 1, Integer::sum); // cnt[x]++
            mn = Math.min(mn, x);
        }

        int cntMin = cnt.get(mn);
        int minY = Integer.MAX_VALUE;
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            if (e.getValue() != cntMin) {
                minY = Math.min(minY, e.getKey());
            }
        }

        if (minY == Integer.MAX_VALUE) {
            return new int[]{-1, -1};
        }
        return new int[]{mn, minY};
    }
}
```

```cpp [sol-C++]
class Solution {
public:
    vector<int> minDistinctFreqPair(vector<int>& nums) {
        unordered_map<int, int> cnt;
        int mn = INT_MAX;
        for (int x : nums) {
            cnt[x]++;
            mn = min(mn, x);
        }

        int cnt_min = cnt[mn];
        int min_y = INT_MAX;
        for (auto& [y, c] : cnt) {
            if (c != cnt_min) {
                min_y = min(min_y, y);
            }
        }

        if (min_y == INT_MAX) {
            return {-1, -1};
        }
        return {mn, min_y};
    }
};
```

```go [sol-Go]
func minDistinctFreqPair(nums []int) []int {
	cnt := map[int]int{}
	mn := math.MaxInt
	for _, x := range nums {
		cnt[x]++
		mn = min(mn, x)
	}

	cntMin := cnt[mn]
	minY := math.MaxInt
	for y, c := range cnt {
		if c != cntMin {
			minY = min(minY, y)
		}
	}

	if minY == math.MaxInt {
		return []int{-1, -1}
	}
	return []int{mn, minY}
}
```

#### 复杂度分析

- 时间复杂度：$\mathcal{O}(n)$，其中 $n$ 是 $\textit{nums}$ 的长度。
- 空间复杂度：$\mathcal{O}(n)$。

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
