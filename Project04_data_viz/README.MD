# 设计目标
意在呈现球员表现与身体素质哪一项挂钩

# 设计决策
数据集中球员表现以 avg 和 HR 体现，既然选择 x 轴为 height，y 轴为weight，那么再增加另外的分类数据 handedness 以颜色区分，avg 和 HR 以气泡的大小区分

# Demo1
思路：根据惯用手查看远动员的身高体重分布

同学反馈：数据太多，能否做个分类

# Demo2
思路：进行数据分类

同学反馈：分类有了，那么还是没有关联到其他数据，比如 avg 和 HR


# Demo3
思路：HR 和 avg 不可同时参与，所以选择加一个分类选择

# Demo4
以 d3.js 重写一遍，改善了每个起泡的透明度，及过滤了部分数据，增加了动画效果

# 结论
数据集对于身体素质的可参考项有体重、身高和惯用手，可以看到 Home Run 次数多集中于体重、身高中位数的地方，惯用手为右手的最为突出，
而场均得分这一项因为差距过小，实在难以得出明显的结论

**参考：**
[D3.js Step by Step: Adding a Legend](http://zeroviscosity.com/d3-js-step-by-step/step-3-adding-a-legend)
[dimple advanced examples](http://dimplejs.org/advanced_examples_viewer.html?id=advanced_interactive_legends)
[dimple](https://github.com/PMSI-AlignAlytics/dimple)
[w3cschool](http://www.w3school.com.cn/)
[d3教程](http://d3.decembercafe.org/pages/lessons/11.html)
[MDN](https://developer.mozilla.org/)


