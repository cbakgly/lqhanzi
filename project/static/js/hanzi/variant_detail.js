// iframe高度自适应
function iFrameHeightByClass(classname) {
    var ifms = document.getElementsByClassName(classname);
    for(var i = 0; i < ifms.length; i++) {
        ifms[i].height = document.getElementsByClassName('hanzi-sets-content')[0].clientHeight + 90;
    }

}
