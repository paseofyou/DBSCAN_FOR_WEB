from analyze.vips_rule import VIPSRule

'''
    吐槽：
    被坑了，原来不是把所有的node节点全权交给这里处理的，而是VIPS只是优化一小部分，核心过滤却只是保留下文本框（把上一级的大小长度保存到文本节点中）。
    这里VIPS最大的作用就是优化一点小节点堆的合并，就是地图那些的节点合并起来了
    麻了，害得我把自己创新出来的规则都写出来之后发现跑都是过滤效果不好。
    心态搞炸了，害得我甚至把我自己写了一天的算法规则全部给删了，照着原项目重写了，还是实现不了好的过滤效果，最后debug后才发现VIPS的作用没那么大。害我走了很多冤枉路
'''


class VIPSAnalyze:
    node_list = []
    divide_list = []
    # 计数器 for test
    count = 0

    def service(self, node_list):
        print("VIPS过滤中...")
        self.node_list = node_list
        # self.filterTextList()
        self.divideList()
        self.fillList()
        self.filterNoDisplayList()
        return self.divide_list

    # 去除第一层的#text节点
    def filterTextList(self):
        for i in range(len(self.node_list) - 1, -1, -1):
            if self.node_list[i].tag != '#text':
                pass
            else:
                self.node_list.remove(self.node_list[i])

    def filterNoDisplayList(self):
        for i in range(len(self.divide_list) - 1, -1, -1):
            if self.divide_list[i].block.block_visual is True:
                pass
            else:
                self.divide_list.remove(self.divide_list[i])

    def divideList(self):
        for node in self.node_list:
            self.divideNode(node)

    def divideNode(self, node):
        self.count += 1
        if node.block.block_dividable and VIPSRule.dividable(node):
            node.block.block_visual = False
            # node.block.block_divide = True
            for b in node.childNodes:
                self.divideNode(b)

    def fillList(self):
        for node in self.node_list:
            # if(node.block.block_visual is True):
            self.fill(node)

    def fill(self, node):
        self.divide_list.append(node)
        for i in node.childNodes:
            self.fill(i)
