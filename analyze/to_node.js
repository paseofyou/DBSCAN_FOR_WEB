let elements = [];
// let element_one = null
function toJSON(element) {
    if (element === null) return;
    if (element.nodeType !== 1) return;
    // console.log(element)
    // element_one = element
    // if (element.nodeType === 3 && isEmpty(element.nodeValue)) return;
    let rect = element.getBoundingClientRect();
    let style = window.getComputedStyle(element);
    let tagName = element.tagName.toLowerCase();
    // 初始化过滤---特殊无用标签
    if (style.getPropertyValue("visibility") === 'hidden' || style.getPropertyValue("display") === 'none') return;
    if (tagName === 'html' || tagName === 'script' || tagName === 'noscript' || tagName === 'style') return;
    if (tagName === 'hr' || tagName === 'br') return;
    if (rect.width > 0 && rect.height > 0) {
        let childNodes = [];
        if (element.childNodes !== null) {
            let length = element.childNodes.length;
            for (let i = 0; i < length; i++) {
                let it = toJSON(element.childNodes[i]);
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
            'text': element.innerText,
            'nodeType': element.nodeType,
            // 'parentNode': element.parentNode.tagName.toLowerCase(),
        };
        elements.push(item);
        return item;
    }
}


function isEmpty(obj) {
    return obj == null || obj === '';
}

function main() {
    let directChildren = document.body.children;
    for (let i = 0; i < directChildren.length; i++) {
        toJSON(directChildren[i]);
    }
    return elements;
}