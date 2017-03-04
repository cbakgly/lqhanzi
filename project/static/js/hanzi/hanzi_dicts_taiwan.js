// 点击目录索引/正字字表/(常用字、次常用字、罕用字、新增正字)
$(document).on('click', '.treeview-menu .tw-std-hanzi', function () {
    // 弹出结果面板
    $(".popup").show("slow");

    if ($(this).text() == $(".treeview-menu .tw-std-hanzi.active").text()) {
        return false;
    }

    $(".treeview-menu .tw-std-hanzi.active").removeClass("active");
    $(this).addClass("active");

    // 清空部首输入框
    $('#input-strokes').val('');

    var url = $(this).attr("href");
    $.get(url, function (data) {
        // 渲染数据
        render_dicts_panel(data);
    });
    return false;
});


// 点击检索结果集
$(document).on('click', '.strokes-item .hanzi-item', function () {
    $(".popup").hide("normal");
    var q = $(this).attr('alt');
    $('#iframe-content').attr('src', '/dicts/taiwan/detail?q=' + q);
});


// iframe高度自适应
function iFrameHeight(id) {
    var ifm = document.getElementById(id);
    ifm.height = document.getElementById('dictionary-content').clientHeight - 90;
}