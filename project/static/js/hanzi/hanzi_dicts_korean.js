// 点击检索结果集
$(document).on('click', '.strokes-item .hanzi-item', function () {
    $(".popup").hide("normal");
    var q = $(this).attr('alt');
    $('#iframe-content').attr('src', '/dicts/korean/detail?q=' + q);
});


// iframe高度自适应
function iFrameHeight(id) {
    var ifm = document.getElementById(id);
    ifm.height = document.getElementById('dictionary-content').clientHeight - 90;
}
