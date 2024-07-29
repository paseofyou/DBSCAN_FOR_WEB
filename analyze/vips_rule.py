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
from common.config import Config


class VIPSRule:
    @staticmethod
    def dividable(node):
        if node.nodeType == 3:
            return False
        name = node.tag
        #
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
        # return VIPSRule.testRules(node)
        # return True

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
        if VIPSRule.rule_tmp(node):
            return True
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule11(node):
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
        if VIPSRule.rule_tmp(node):
            return True
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule11(node):
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
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule10(node):
            return True
        if VIPSRule.rule12(node):
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
        if VIPSRule.rule_tmp(node):
            return True
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule12(node):
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
        if VIPSRule.rule7(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule12(node):
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
        if VIPSRule.rule_tmp(node):
            return True
        if VIPSRule.rule8(node):
            return True
        if VIPSRule.rule9(node):
            return True
        if VIPSRule.rule11(node):
            return True
        return False

    """
    Rule 1: 如果当前结点不是文本结点，同时它又没有任何有效的孩子结点，那么该结点将不被分割，并且从结点集合中删除。
    说明：此处不显示，即表示分割
    """

    @staticmethod
    def rule1(node):
        if not VIPSRule.isTextNode(node) and not VIPSRule.hasValidChildNode(node):
            # node.block.block_visual = False
            return True
        return False

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
    Rule 4: 如果当前结点的所有的孩子结点都是文本结点或者是虚拟文本结点，那么不分割该节点。
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
                        node.block.Doc = 9
                        return False
                    else:
                        fontSize = childSize
            fontWeight = None
            for box in subBoxList:
                childWeight = box.font_weight
                if fontWeight != None:
                    if fontWeight != childWeight:
                        node.block.Doc = 9
                        return False
                    else:
                        fontWeight = childWeight
            node.block.Doc = 10
            return False
        return True

    """
    Rule 5:  如果DOM节点的子节点之一是换行节点，则划分该DOM节点
        如果当前DOM结点的孩子结点中有一个line-break结点，那么该结点将被继续分割
        
        这里判断是不是包含除了最小子标签额外的标签，如果包含，则划分
    """

    @staticmethod
    def rule5(node):
        for box in node.childNodes:
            if not VIPSRule.isnode(box.tag):
                return True
        return False

    """
    Rule 6: 如果当前结点的孩子结点中存在<HR>结点，那么该结点将被继续分割
    """

    @staticmethod
    def rule6(node):
        for box in node.childNodes:
            if box.tag == 'hr':
                return True
        return False

    """
    Rule tmp: 如果所有子节点的大小总和大于这个DOM节点的大小，然后除以这个节点。
    """

    @staticmethod
    def rule_tmp(node):

        x = node.x
        y = node.y
        width = node.width
        height = node.height

        subBoxList = node.childNodes
        # question
        for box in subBoxList:
            if box.x < x:
                return True
            if box.y < y:
                return True
            if (x + width) < (box.x + box.width):
                return True
            if (y + height) < (box.y + box.height):
                return True
        return False

    """
    Rule 7: 如果该节点的背景颜色与其子节点之一不同，除以这个节点，同时，背景颜色不同的子节点将不会在这一轮中被划分。
    根据子节点的html标签和子节点的大小设置子节点的DoC值(6 ~ 8)。
    如果当前结点的背景色与它的所有子结点中的某个的背景色不相同，那么该结点将被分割，同时具有不同颜色的子结点在本次迭代中不分割，分割在下轮迭代中进行。
    与此同时，孩子结点的DoC的值根据标签和尺寸的不同设置为6-8。
    
    特殊
    """

    @staticmethod
    def rule7(node):
        ret = False
        bColor = node.background_color
        for child in node.childNodes:
            childColor = child.background_color
            if bColor != childColor:
                child.block.block_dividable = False
                # todo 设置不同doc值
                child.block.Doc = VIPSRule.getDocByTagSize("", 0)
                ret = True
        return ret

    """
    Rule 8: 如果结点至少具有一个文本或者虚拟文本子结点，同时结点的相对大小小于门槛大小，那么这个结点不再分割，同时根据标签的不同，DoC的值设置为5-8。
    """

    @staticmethod
    def rule8(node):
        ret = True
        count = 0
        for box in node.childNodes:
            if VIPSRule.isTextNode(box) or VIPSRule.isVirtualTextNode(box):
                count += 1
                break
        if count > 0:
            if node.x * node.y < Config.VIPS_threshold:
                ret = False
                # todo 设置不同doc值
                node.block.Doc = VIPSRule.getDocByTagSize("", 0)

        return ret

    """
    Rule 9: 如果当前结点的所有子结点中最大的尺寸也小于门槛大小，那么该结点将不再分割，同时DoC值根据HTML标签和结点大小设置。
    """

    @staticmethod
    def rule9(node):
        maxSize = 0
        for box in node.childNodes:
            childSize = box.x * box.y
            maxSize = childSize if maxSize < childSize else maxSize
        if maxSize < Config.VIPS_threshold:
            node.block.Doc = VIPSRule.getDocByTagSize("", 0)
            return False
        return True

    """
    Rule 10: 如果前一个兄弟结点没有被分割，那么该结点也不会被继续分割
    """

    @staticmethod
    def rule10(node):
        if (node.parentNode is None):
            return False
        children = node.parentNode.childNodes
        index = children.index(node)
        count = 0
        for i in range(0, index):
            if children[i].block.block_divide:
                count += 1
        return not count == index

    """
    Rule 11: 分割该结点
    """

    @staticmethod
    def rule11(node):
        return True

    """
    Rule 12: 不要分割该结点，同时基于当前结点的标签和大小设置DoC值
    """

    @staticmethod
    def rule12(node):
        node.Doc = VIPSRule.getDocByTagSize("", 0)
        return False

    @staticmethod
    def hasValidChildNode(node):
        # for box in node.childNodes:
        #     if VIPSRule.isValidNode(box):
        #         return True
        # return False
        return len(node.childNodes) != 0

    """
    判断该节点是否可见
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
    判断是不是核心点
    """

    @staticmethod
    def isTextNode(node):
        return node.nodeType == 3

    """
     判断子节点是否全是text虚拟节点
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

    # todo 是否覆盖完全，没有的会导致不再分割
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

    @staticmethod
    def isCoreNode(tag):
        if tag in ('#text', 'img'):
            return True
        return False

    @staticmethod
    def testRules(node):
        if VIPSRule.rule1(node):
            return True
        # if VIPSRule.rule2(node):
        #     return True
        # if VIPSRule.rule3(node):
        #     return True
        # if VIPSRule.rule4(node):
        #     return True
        # if VIPSRule.rule5(node):
        #     return True
        # if VIPSRule.rule6(node):
        #     return True
        # if VIPSRule.rule7(node):
        #     return True
        # if VIPSRule.rule_tmp(node):
        #     return True
        # if VIPSRule.rule8(node):
        #     return True
        # if VIPSRule.rule9(node):
        #     return True
        # if VIPSRule.rule10(node):
        #     return True
        # if VIPSRule.rule11(node):
        #     return True
        return False
