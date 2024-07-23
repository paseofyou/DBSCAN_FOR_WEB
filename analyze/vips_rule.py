"""
原VIPS规则：各个规则独自运行，根据不同的标签定制使用规则。
规则 1
如果当前结点不是文本结点，同时它又没有任何有效的孩子结点，那么该结点将不被分割，并且从结点集合中删除。
规则 2
如果当前结点只有一个有效的孩子结点，同时该孩子结点不是文本结点，那么当前结点将被分割。
规则 3
如果当前的DOM结点是整个子DOM树的根结点(与页面块对应)，同时只有一个子DOM树与当前的页面块关联，那么分割该结点。
规则 4
如果当前结点的所有的孩子结点都是文本结点或者是虚拟文本结点，那么不分割该节点。
如果当前所有孩子结点的字体大小和字体重量都是相同的，那么该页面块的DoC设置为10，否则设置为9。
规则 5
如果当前DOM结点的孩子结点中有一个line-break结点，那么该结点将被继续分割
规则 6
如果当前结点的孩子结点中存在<HR>结点，那么该结点将被继续分割
规则 7
如果当前结点的背景色与它的所有子结点中的某个的背景色不相同，那么该结点将被分割，同时具有不同颜色的子结点在本次迭代中不分割，分割在下轮迭代中进行。
与此同时，孩子结点的DoC的值根据标签和尺寸的不同设置为6-8。
规则 8
如果结点至少具有一个文本或者虚拟文本子结点，同时结点的相对大小小于门槛大小，那么这个结点不再分割，同时根据标签的不同，DoC的值设置为5-8。
规则 9
如果当前结点的所有子结点中最大的尺寸也小于门槛大小，那么该结点将不再分割，同时DoC值根据HTML标签和结点大小设置。
规则 10
如果前一个兄弟结点没有被分割，那么该结点也不会被继续分割
规则 11
分割该结点
规则12
不要分割该结点，同时基于当前结点的标签和大小设置DoC值
"""


class VIPSRule:

    @staticmethod
    def dividable(node):
        if node.nodeType == 3:
            return False
        name = node.tag

        if not VIPSRule.isnode(name):
            return VIPSRule.inlineRules(node)
        elif (name == 'table'):
            return VIPSRule.tableRules(node)
        elif (name == 'tr'):
            return VIPSRule.trRules(node)
        elif (name == 'td'):
            return VIPSRule.tdRules(node)
        elif (name == 'p'):
            return VIPSRule.pRules(node)
        else:
            return VIPSRule.otherRules(node)

    @staticmethod
    def otherRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule4(node):
            return True
        if VIPSRule.rule6(node):
            return True
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule12(node):
            return True
        return False

    @staticmethod
    def pRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule4(node):
            return True
        if VIPSRule.rule5(node):
            return True
        if VIPSRule.rule6(node):
            return True
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule12(node):
            return True
        return False

    @staticmethod
    def tdRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule4(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule11(node):
            return True
        if VIPSRule.rule13(node):
            return True
        return False

    @staticmethod
    def trRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule13(node):
            return True
        return False

    @staticmethod
    def tableRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule13(node):
            return True
        return False

    @staticmethod
    def inlineRules(node):
        if VIPSRule.rule1(node):
            return True
        if VIPSRule.rule2(node):
            return True
        if VIPSRule.rule3(node):
            return True
        if VIPSRule.rule4(node):
            return True
        if VIPSRule.rule5(node):
            return True
        if VIPSRule.rule6(node):
            return True
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule12(node):
            return True
        return False

    """
    Rule 1: 如果当前结点不是文本结点，同时它又没有任何有效的孩子结点，那么该结点将不被分割，并且从结点集合中删除。
    """

    @staticmethod
    def rule1(node):
        if not VIPSRule.isTextNode(node) and not VIPSRule.hasValidChildNode(node):
            # question
            node.parentNode.childNodes.remove(node)
            return False
        return True

    """ 
    Rule 2: 如果当前结点只有一个有效的孩子结点，同时该孩子结点不是文本结点，那么当前结点将被分割。
    """

    @staticmethod
    def rule2(node):
        if len(node.childNodes) == 1:
            node = node.childNodes[0]
            if VIPSRule.isValidNode(node) and not VIPSRule.isTextNode(node):
                return True
        return False

    """ 
    Rule 3: 如果当前的DOM结点是整个子DOM树的根结点(与页面块对应)，同时只有一个子DOM树与当前的页面块关联，那么分割该结点。
    """

    @staticmethod
    def rule3(node):
        cnt = 0
        for child in node.childNodes:
            if child.tag == node.tag:
                result = True
                VIPSRule.isOnlyOneDomSubTree(node, child, result)
                if result:
                    cnt += 1

        return True if cnt == 1 else False

    """
    Rule 4: 如果DOM节点的所有子节点都是文本节点或虚拟文本节点，不划分节点。
    如果所有子节点的字体大小和字体权重相同，将提取块的DoC设置为10。
    否则，将此提取块的DoC设置为9。
    
    如果当前结点的所有的孩子结点都是文本结点或者是虚拟文本结点，那么不分割该节点。
    如果当前所有孩子结点的字体大小和字体重量都是相同的，那么该页面块的DoC设置为10，否则设置为9。
    """

    @staticmethod
    def rule4(node):
        subBoxList = node.childNodes
        count = 0
        for box in subBoxList:
            if VIPSRule.isTextNode(box) or VIPSRule.isVirtualTextNode(box):
                count += 1
        if count == len(subBoxList):
            fontSize = 0
            for box in subBoxList:
                childSize = box.font_size
                if fontSize != 0:
                    if fontSize != childSize:
                        node.Doc = 9
                        return False
                    else:
                        fontSize = childSize

            fontWeight = None
            for box in subBoxList:
                childWeight = box.visual_cues['font-weight']
                if fontWeight != None:
                    if fontWeight != childWeight:
                        node.Doc = 9
                        return False
                    else:
                        fontWeight = childWeight

            node.Doc = 10
            return False
        return True

    """
    Rule 5:  如果DOM节点的子节点之一是换行节点，则划分该DOM节点
    """

    @staticmethod
    def rule5(node):

        subBoxList = node.childNodes
        for box in subBoxList:
            # question
            if not VIPSRule.isnode(box.nodeName):
                return True

        return False

    """
    Rule 6: 如果DOM节点的一个子节点有HTML标签<HR>，然后划分这个DOM节点
    """

    @staticmethod
    def rule6(node):

        subBoxList = node.childNodes

        for box in subBoxList:
            if box.nodeName == 'hr':
                return True

        return False

    """
    Rule 7: 如果所有子节点的大小总和大于这个DOM节点的大小，然后除以这个节点。
    """

    @staticmethod
    def rule7(node):

        x = node.visual_cues['bounds']['x']
        y = node.visual_cues['bounds']['y']
        width = node.visual_cues['bounds']['width']
        height = node.visual_cues['bounds']['height']

        subBoxList = node.childNodes
        # question
        for box in subBoxList:
            if (box.visual_cues['bounds']['x'] < x):
                return True
            if (box.visual_cues['bounds']['y'] < y):
                return True
            if ((x + width) < (box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width'])):
                return True
            if ((y + height) < (box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height'])):
                return True
        return False

    """
    Rule 8: 如果该节点的背景颜色与其子节点之一不同，除以这个节点，同时，背景颜色不同的子节点将不会在这一轮中被划分。
    根据子节点的html标签和子节点的大小设置子节点的DoC值(6 ~ 8)。
    """

    @staticmethod
    def rule8(node):
        ret = False

        bColor = node.visual_cues['background-color']
        for b in node.children:
            child = b.boxs[0]
            childColor = child.visual_cues['background-color']
            if bColor != childColor:
                b.isDividable = False
                b.Doc = VIPSRule.getDocByTagSize("", 0)
                ret = True
        return ret

    """
    Rule 9: 如果节点至少有一个文本节点子节点或至少有一个虚拟文本节点子节点，且节点的相对大小小于某一阈值，则该节点不能被分割
    根据节点的html标签设置DoC值，取值范围为5 ~ 8
    """

    @staticmethod
    def rule9(node):
        ret = True

        subBoxList = node.childNodes
        count = 0
        for box in subBoxList:
            if (VIPSRule.isTextNode(box) or VIPSRule.isVirtualTextNode(box)):
                count += 1
        if count > 0:
            if (node.visual_cues['bounds']['x'] * node.visual_cues['bounds']['y'] < VIPSRule.threshold):
                ret = False
                node.Doc = VIPSRule.getDocByTagSize("", 0)

        return ret

    """
    Rule 10: 如果最大大小节点的子节点小于阈值(相对大小)，不要分割该节点。根据该节点的html标签和大小设置DoC。
    """

    @staticmethod
    def rule10(node):

        subBoxList = node.childNodes
        maxSize = 0
        for box in subBoxList:
            childSize = box.visual_cues['bounds']['x'] * box.visual_cues['bounds']['y']
            maxSize = childSize if maxSize < childSize else maxSize
        if maxSize < VIPSRule.threshold:
            node.Doc = VIPSRule.getDocByTagSize("", 0)
            return False
        return True

    """
    Rule 11: 如果前一个兄弟节点未被划分，则不划分此节点
    """

    @staticmethod
    def rule11(node):
        children = node.parent.children
        index = children.index(node)
        count = 0
        for i in range(0, index):
            if not children[i].isDividable:
                count += 1
        return not count == index

    """
    Rule 12: Divide this node.
    """

    @staticmethod
    def rule12(node):
        return True

    """
    Rule 13: 不划分这个节点，根据该节点的html标签和大小设置DoC值。
    """

    @staticmethod
    def rule13(node):
        node.Doc = VIPSRule.getDocByTagSize("", 0)
        return False

    @staticmethod
    def hasValidChildNode(node):
        for box in node.childNodes:
            if VIPSRule.isValidNode(box):
                return True
        return False

    """
    a node that can be seen through the browser. 
     The node's width and height are not equal to zero.
    """

    @staticmethod
    def isValidNode(node):
        display = node.display
        visibility = node.visibility

        if display == 'none' or visibility == 'hidden':
            return False
        height = node.height
        width = node.width
        if height == 0 or width == 0:
            return False
        return True

    """
    the DOM node corresponding to free text, which does not have an html tag
    """

    @staticmethod
    def isTextNode(node):
        return node.nodeType == 3

    """
    Virtual text node (recursive definition):
     Inline node with only text node children is a virtual text node.
     Inline node with only text node and virtual text node children is a virtual text node.
     判断是否全是text虚拟节点
    """

    @staticmethod
    def isVirtualTextNode(node):
        count = 0
        for box in node.childNodes:
            if VIPSRule.isTextNode(box) or VIPSRule.isVirtualTextNode(box):
                count += 1
        if count == len(node.childNodes):
            return True
        return False

    @staticmethod
    def isnode(name):
        if (name == 'a' or
                name == 'abbr' or
                name == 'acronym' or
                name == 'b' or
                name == 'bdo' or
                name == 'big' or
                name == 'br' or
                name == 'button' or
                name == 'cite' or
                name == 'code' or
                name == 'dfn' or
                name == 'em' or
                name == 'i' or
                name == 'img' or
                name == 'input' or
                name == 'kbd' or
                name == 'label' or
                name == 'map' or
                name == 'object' or
                name == 'q' or
                name == 'samp' or
                name == 'script' or
                name == 'select' or
                name == 'small' or
                name == 'span' or
                name == 'strong' or
                name == 'sub' or
                name == 'sup' or
                name == 'textarea' or
                name == 'time' or
                name == 'tt' or
                name == 'var'):
            return False
        else:
            return True

    # 匹配单个dom树是否完全相同
    @staticmethod
    def isOnlyOneDomSubTree(pattern, node, result):
        if pattern.tag != node.tag:
            result = False
        pattern_child = pattern.childNodes
        node_child = node.childNodes
        if len(pattern_child) != len(node_child):
            result = False
        if not result:
            return
        for i in range(0, len(pattern_child)):
            VIPSRule.isOnlyOneDomSubTree(pattern_child[i], node_child[i], result)

    @staticmethod
    def getDocByTagSize(tag, size):
        return 7
