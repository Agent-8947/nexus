按题意模拟：

1. 从左到右遍历 $s$。
2. 只要最近相同字母的下标差大于 $k$，任意相同字母的下标差都大于 $k$。因此，设 $s[i]$ 在**答案**中的最后一次出现的下标是 $j$。如果 $i-j\le k$，那么删除 $s[i]$（跳过 $s[i]$），否则把 $s[i]$ 添加到答案中。
3. 为了快速找到字母 $c$ 在答案中的最后一次出现的下标，我们可以用一个数组（或者哈希表）记录每个字母在答案中最后一次出现的下标。

[本题视频讲解](https://www.bilibili.com/video/BV1VvABz9EGz/?t=4m52s)，欢迎点赞关注~

```py [sol-Python3]
class Solution:
    def mergeCharacters(self, s: str, k: int) -> str:
        last = defaultdict(lambda: -inf)
        ans = []
        for ch in s:
            # ch 在 ans 中的下标是 len(ans)
            if len(ans) - last[ch] > k:
                last[ch] = len(ans)
                ans.append(ch)
        return ''.join(ans)
```

```java [sol-Java]
class Solution {
    public String mergeCharacters(String s, int k) {
        int[] last = new int[26];
        // 保证首次遇到字母 i 时，ans.length() - last[i] > k 是 true
        Arrays.fill(last, -k - 1);

        StringBuilder ans = new StringBuilder();
        for (char ch : s.toCharArray()) {
            // ch 在 ans 中的下标是 ans.length()
            if (ans.length() - last[ch - 'a'] > k) {
                last[ch - 'a'] = ans.length();
                ans.append(ch);
            }
        }
        return ans.toString();
    }
}
```

```cpp [sol-C++]
class Solution {
public:
    string mergeCharacters(string s, int k) {
        // 保证首次遇到字母 i 时，ans.size() - last[i] > k 是 true
        vector<int> last(26, -k - 1);
        string ans;
        for (char ch : s) {
            // ch 在 ans 中的下标是 ans.size()
            if (ans.size() - last[ch - 'a'] > k) {
                last[ch - 'a'] = ans.size();
                ans += ch;
            }
        }
        return ans;
    }
};
```

```go [sol-Go]
func mergeCharacters(s string, k int) string {
	last := [26]int{}
	for i := range last {
		last[i] = -k - 1 // 保证首次遇到字母 i 时，len(ans)-last[i] > k 是 true
	}

	ans := []byte{}
	for _, ch := range s {
		// ch 在 ans 中的下标是 len(ans)
		if len(ans)-last[ch-'a'] > k {
			last[ch-'a'] = len(ans)
			ans = append(ans, byte(ch))
		}
	}
	return string(ans)
}
```

#### 复杂度分析

- 时间复杂度：$\mathcal{O}(n)$ 或 $\mathcal{O}(n + |\Sigma|)$，其中 $n$ 是 $s$ 的长度，$|\Sigma|=26$ 是字符集合的大小。注意创建大小为 $|\Sigma|$ 的数组需要 $\mathcal{O}(|\Sigma|)$ 的时间。
- 空间复杂度：$\mathcal{O}(|\Sigma|)$。返回值不计入。

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
