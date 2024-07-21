function toJSON(node) {
    node = node || this;
    var obj = {
        nodeType: node.nodeType
    };
    if (node.tagName) {
        obj.tagName = node.tagName.toLowerCase();
    }
    // else if (node.nodeName) {
    //     obj.nodeName = node.nodeName;
    // }
    if (node.nodeValue) {
        obj.nodeValue = node.nodeValue;
    }
    if (node.nodeType == 1) {
        obj.visual_cues = getCSS(node);
    }

    var attrs = node.attributes;
    if (attrs) {
        var length = attrs.length;
        var arr = obj.attributes = new Array(length);
        for (var i = 0; i < length; i++) {
            arr[i] = attrs[i];
        }
    }
    var childNodes = node.childNodes;
    if (childNodes) {
        length = childNodes.length;
        arr = obj.childNodes = new Array(length);
        for (i = 0; i < length; i++) {
            if (childNodes[i].tagName != 'script') {
                arr[i] = toJSON(childNodes[i]);
            }
        }
    }
    return obj;
}

function getCSS(node) {
    var visual_cues = {};
    style = window.getComputedStyle(node);
    visual_cues["bounds"] = node.getBoundingClientRect();
    visual_cues["font-size"] = style.getPropertyValue("font-size");
    visual_cues["font-weight"] = style.getPropertyValue("font-weight");
    visual_cues["background-color"] = style.getPropertyValue("background-color");
    visual_cues["display"] = style.getPropertyValue("display");
    visual_cues["visibility"] = style.getPropertyValue("visibility");
    visual_cues["text"] = node.innerText
    visual_cues["className"] = node.className
    return visual_cues;
}