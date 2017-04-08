// 全局变量
var base_url = 'http://s3.cn-north-1.amazonaws.com.cn/lqhanzi-images/dictionaries/dh-dict/';
var cur_page = 'A01';

// 点击目录索引
$(document).on('click', '.catalog-panel .treeview a', function () {
    var page = $(this).attr('alt');
    set_page(page);
});


// 点击检索结果集
$(document).on('click', '.strokes-item .hanzi-item', function () {
    $(".popup").hide("normal");
    var page = $(this).attr('alt');
    set_page(page);
});

// 设置浏览页面
function set_page(page) {
    page = page + '';
    var padding_page = page;
    var suffix = '.png';
    if (padding_page.match(/^\d+$/) != null) {
        var pad = "000"
        padding_page = pad.substring(0, pad.length - page.length) + page;
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
//    o_time = window.setTimeout('changeSize(\'' + id + '\',\'' + action + '\')', 100);
}

document.onmouseup = function () {
    window.clearTimeout(o_time);
}


// 后一页
$(document).on('click', '#page-backward', function () {
    var page = cur_page;
    var type = '';
    var matches = page.match(/(A)(\d+)/);
    if (matches != null) {
        type = matches[1];
        page = matches[2];
    }
    var last_page = parseInt(page) > 1 ? parseInt(page) - 1 : 1;
    if (type == 'A' && last_page < 10) {
        last_page = '0' + last_page;
    }
    last_page = '' + type + last_page;
    if (last_page == '1') {
        last_page = 'A91';
    }
    set_page(last_page);
});

// 前一页
$(document).on('click', '#page-forward', function () {
    var page = cur_page;
    var type = '';
    var matches = page.match(/(A)(\d+)/);
    if (matches != null) {
        type = matches[1];
        page = matches[2];
    }
    var max_page_map = {'A': 91, '': 770};
    var max_page = max_page_map[type];
    var next_page = parseInt(page) + 1 < max_page ? parseInt(page) + 1 : max_page;
    if (type == 'A' && next_page < 10) {
        next_page = '0' + next_page;
    }
    next_page = '' + type + next_page;
    if (next_page == 'A91')
        next_page = 1;
    set_page(next_page);
});

