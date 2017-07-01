// iframe高度自适应
function iFrameHeightByClass(classname) {
    var ifms = document.getElementsByClassName(classname);
    for(var i = 0; i < ifms.length; i++) {
        ifms[i].height = document.getElementsByClassName('hanzi-sets-content')[0].clientHeight + 90;
    }
}

function iFrameHeightByObject(obj) {
    obj.height = document.getElementsByClassName('hanzi-sets-content')[0].clientHeight;
}

// 全局变量
var base_url = 'http://s3.cn-north-1.amazonaws.com.cn/lqhanzi-images/dictionaries';


// 设置浏览页面
function hy_set_page(page) {
    page = page + '';
    var padding_page = page;
    var suffix = '.png';
    if (padding_page.match(/^\d+$/) != null) {
        var pad = "0000"
        padding_page = pad.substring(0, pad.length - page.length) + page;
    } else if (page.match(/A0[12]/) != null) {
        suffix = '.jpg';
    }
    var url = base_url + '/zh-dict/' + padding_page + suffix;
    $('#hy-image-page').attr('src', url);
    // 设置当前页面
    hy_cur_page = page;
}


// 设置浏览页面
function dh_set_page(page) {
    page = page + '';
    var padding_page = page;
    var suffix = '.png';
    if (padding_page.match(/^\d+$/) != null) {
        var pad = "000"
        padding_page = pad.substring(0, pad.length - page.length) + page;
    }
    var url = base_url + '/dh-dict/' + padding_page + suffix;
    $('#dh-image-page').attr('src', url);
    // 设置当前页面
    dh_cur_page = page;
}


function changeSize(id, action) {
    var obj = document.getElementById(id);
    obj.style.width = parseInt(obj.style.width) + (action == '+' ? +10 : -10) + '%';
}


// 后一页
$(document).on('click', '#hy-page-backward', function () {
    var page = hy_cur_page;
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
        last_page = 'A25';
    }
    hy_set_page(last_page);
});

// 前一页
$(document).on('click', '#hy-page-forward', function () {
    var page = hy_cur_page;
    var type = '';
    var matches = page.match(/(A)(\d+)/);
    if (matches != null) {
        type = matches[1];
        page = matches[2];
    }
    var max_page_map = {'A': 25, '': 5727};
    var max_page = max_page_map[type];
    var next_page = parseInt(page) + 1 < max_page ? parseInt(page) + 1 : max_page;
    if (type == 'A' && next_page < 10) {
        next_page = '0' + next_page;
    }
    next_page = '' + type + next_page;
    if (next_page == 'A25')
        next_page = 1;
    hy_set_page(next_page);
});

// 前一页
$(document).on('click', '#dh-page-forward', function () {
    var page = dh_cur_page;
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
    dh_set_page(next_page);
});

// 后一页
$(document).on('click', '#dh-page-backward', function () {
    var page = dh_cur_page;
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
    dh_set_page(last_page);
});