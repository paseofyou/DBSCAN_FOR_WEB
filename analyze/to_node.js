let elements = [];
// let element_one = null

// 树先序遍历，保证dom顺序，此处算法顺序与dom顺序一致
function toJSON(element, rect_parent = null) {
    if (element === null) return;
    if (element.nodeType !== 1 && element.nodeType !== 3) return;
    let tagName = element.tagName === undefined ? element.nodeName : element.tagName.toLowerCase();
    // console.log(element)
    // element_one = element
    if (element.nodeType === 3) {
        if (isEmpty(element.nodeValue)) {
            return;
        } else {
            let text = getItem(element);
            if (rect_parent !== null) {
                text.x = rect_parent.left;
                text.y = rect_parent.top;
                text.width = rect_parent.width;
                text.height = rect_parent.height;
            }
            return text;
        }
    }
    if (tagName === 'hr' || tagName === 'br') return getItem(element);
    let rect = element.getBoundingClientRect();
    let style = window.getComputedStyle(element);
    // 初始化过滤---特殊无用标签
    if (style.getPropertyValue("visibility") === 'hidden' || style.getPropertyValue("display") === 'none') return;
    if (tagName === 'script' || tagName === 'noscript' || tagName === 'style') return;
    // 初始化有效节点
    if (rect.width > 0 && rect.height > 0) {
        let childNodes = [];
        if (element.childNodes !== null) {
            let length = element.childNodes.length;
            for (let i = 0; i < length; i++) {
                let it = toJSON(element.childNodes[i], rect);
                if (it !== undefined && it !== null) {
                    childNodes.push(it);
                }
            }
        }
        let item = {
            'tag': tagName,
            'x': rect.left,
            'y': rect.top,
            'width': rect.width,
            'height': rect.height,
            'childNodes': childNodes,
            'display': style.getPropertyValue("display"),
            'visibility': style.getPropertyValue("visibility"),
            "background_color": style.getPropertyValue("background-color"),
            'text': element.innerText,
            'nodeType': element.nodeType,
            "font_size": style.getPropertyValue("font-size"),
            "font_weight": style.getPropertyValue("font-weight"),
        };
        elements.push(item);
        return item;
    }
}

function getItem(element) {
    let tagName = element.tagName === undefined ? element.nodeName : element.tagName.toLowerCase();
    return {
        'tag': tagName,
        'x': 0,
        'y': 0,
        'width': 0,
        'height': 0,
        'text': element.innerText,
        'nodeType': element.nodeType
    }
}


function isEmpty(obj) {
    return obj == null || obj === '';
}

function main() {
    let body = document.getElementsByTagName("BODY")[0];
    elements.unshift(toJSON(body));
    return elements;
}