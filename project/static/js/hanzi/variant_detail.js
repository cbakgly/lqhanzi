// iframe高度自适应
function iFrameHeight(id) {
    var ifm = document.getElementById(id);
    ifm.height = document.getElementById('dictionary-content').clientHeight - 90;
}
