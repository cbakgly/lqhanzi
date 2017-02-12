// 全局变量
var base_url = 'https://s3.cn-north-1.amazonaws.com.cn/lqhanzi-images/dictionaries/zh-dict/';
var max_page = 5727;
var cur_page;

// 点击目录索引
$(document).on('click', '.catalog-panel .treeview a', function () {
    var page = $(this).attr('alt');
    set_page(page);
});


// 点击检索结果集
$(document).on('click', '.strokes-item .hanzi-item', function () {
    $(".popup").hide("normal");
    var page = $(this).attr('title').split('-')[0];
    set_page(page);
});

// 设置浏览页面
function set_page(page) {
    page = page + '';
    var padding_page = page;
    var suffix = '.png';
    if (padding_page.match(/^\d+$/) != null) {
        var pad = "0000"
        padding_page = pad.substring(0, pad.length - page.length) + page;
    } else if (page.match(/Z\d\d/) != null) {
        suffix = '.jpg';
    }
    var url = base_url + padding_page + suffix;
    $('#image-page').attr('src', url);
    // 设置当前页面
    cur_page = page;
}

// 放大/缩小
var o_time;
function changeSize(id, action) {
    var obj = document.getElementById(id);
    obj.style.width = parseInt(obj.style.width) + (action == '+' ? +10 : -10) + '%';
    o_time = window.setTimeout('changeSize(\'' + id + '\',\'' + action + '\')', 100);
}

document.onmouseup = function () {
    window.clearTimeout(o_time);
}

// 后一页
$(document).on('click', '#page-backward', function () {
    var last_page = parseInt(cur_page) > 1 ? parseInt(cur_page) - 1 : 1;
    set_page(last_page);
});

// 前一页
$(document).on('click', '#page-forward', function () {
    var next_page = parseInt(cur_page) + 1 < max_page ? parseInt(cur_page) + 1 : max_page;
    set_page(next_page);
});

