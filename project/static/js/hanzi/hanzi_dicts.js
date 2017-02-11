$(document).ready(function () {

    //当剩余笔画数变化时的响应函数
    $(document).on('click', '#search_by_left', function () {

        var left_stroke = $('.input-ser').val();
        // 校验
        var regex = /^[1-9]?[0-9]*$/;
        if (left_stroke.match(regex) == null) {
            // $("#search_tip").html("格式不对");
            return;
        }
        // 当前激活的字典
        var trans_hash = {
            '台湾异体字字典': 2,
            '高丽异体字字典': 4,
            '汉语大字典': 3,
            '敦煌俗字典': 5,
        };
        var dict = $(".dict-tabs .active").html();
        var source = trans_hash[dict];
        // 当前部首
        var radical = $('#search_item').html();

        $.get('/dicts/dicts_search', {"q": radical, "source": source, "left_stroke": left_stroke}, function (data) {
            // 渲染数据
            render_dicts_panel(data);
        });

    });


    // 导航上一页、下一页
    $(document).on('click', '.stroke_page', function () {
        var url = $(this).attr("data-url");
        $.get(url, function (data) {
            // 渲染数据
            render_dicts_panel(data);
        });

    });


    // 导航跳页
    $(document).on('click', '#dict_page_btn', function () {
        var new_page = $('#new_page').val();

        var regex = /^[1-9]?[0-9]*$/;
        if (new_page.match(regex) == null) {
            // $("#search_tip2").html("页码格式不对");
            return;
        }

        var url = $(this).attr("data-url");
        url += '&page_num=' + new_page;

        $.get(url, function (data) {
            // 渲染数据
            render_dicts_panel(data);
        });
    });

    // 点击检索结果集
    $(document).on('click', '.strokes-item .hanzi-item', function () {
        $(".popup").hide("normal");
        var seq_id = $(this).attr('alt');
        $('#iframe-content').attr('src', '/dicts/taiwan/detail?seq_id=' + seq_id);
    });

    // 点击目录索引
    $(document).on('click', '.treeview a.inner', function () {
        $('#iframe-content').attr('src', $(this).attr("href"));
        return false;
    });

});


// 点击部首时的响应函数
function clickRadical(radical) {
    if ($('#search_item').html() == radical)
        return;

    // 当前激活的字典
    var trans_hash = {
        '台湾异体字字典': 2,
        '高丽异体字字典': 4,
        '汉语大字典': 3,
        '敦煌俗字典': 5,
    };
    var dict = $(".dict-tabs .active").html();
    var source = trans_hash[dict];

    $.get('/dicts/dicts_search', {"q": radical, "source": source}, function (data) {
        // 设置检索结果面板提示信息
        $('#search_item').html(radical);
        // 渲染数据
        render_dicts_panel(data);
    });
}


function render_dicts_panel(data) {
    var q = data.q;
    var source = data.source;
    var left_stroke = data.left_stroke;
    var page_size = data.page_size;
    var page_num = data.page_num;
    var total_count = data.total_count;
    var pages = data.pages;

    var stroke_map = new Array(
        '零画', '一画', '二画', '三画', '四画', '五画', '六画', '七画', '八画', '九画',
        '十画', '十一画', '十二画', '十三画', '十四画', '十五画', '十六画', '十七画', '十八画', '十九画',
        '二十画', '二十一画', '二十二画', '二十三画', '二十四画', '二十五画', '二十六画', '二十七画', '二十八画', '二十九画',
        '三十画', '三十一画', '三十二画', '三十三画', '三十四画', '三十五画', '三十六画', '三十七画', '三十八画', '三十九画',
        '四十画', '四十一画', '四十二画', '四十三画', '四十四画', '四十五画', '四十六画', '四十七画', '四十八画', '四十九画',
        '五十画', '五十一画', '五十二画', '五十三画', '五十四画', '五十五画', '五十六画', '五十七画', '五十八画', '五十九画',
        '六十画', '六十一画', '六十二画', '六十三画', '六十四画'
    );

    // 清空历史
    $('#search_result .strokes-lists').empty();
    $('#search_result .pagination').empty();

    // 设置提示信息
    $('#search_count').html(total_count);

    // 显示检索结果汉字集
    var hanzi_set = data.result;
    var len = hanzi_set.length;
    var cur_remain_strokes_num = -1;
    for (var i = 0; i < len; i++) {
        if (cur_remain_strokes_num != hanzi_set[i].remain_strokes_num) {
            cur_remain_strokes_num = hanzi_set[i].remain_strokes_num;

            var str = '<li class="strokes-item"><span class="num">' + stroke_map[cur_remain_strokes_num] + '</span>';
            str += '<div class="strokes-item-bd clearfix">';

            for (var j = i; j < len; j++) {
                if (source == 4 && hanzi_set[j].hanzi_pic_id != '') {     // 如果是高丽异体字，优先显示图片
                    str += '<span class="hanzi-item" alt="' + hanzi_set[j].seq_id + '"><img src="' + hanzi_set[j].pic_url + '" alt="' + hanzi_set[j].hanzi_pic_id + '"></span>';
                } else if (hanzi_set[j].hanzi_char != '') {
                    str += '<span class="hanzi-item" alt="' + hanzi_set[j].seq_id + '">' + hanzi_set[j].hanzi_char + '</span>';
                } else {
                    str += '<span class="hanzi-item" alt="' + hanzi_set[j].seq_id + '"><img src="' + hanzi_set[j].pic_url + '" alt="' + hanzi_set[j].hanzi_pic_id + '"></span>';
                }

                // 如果下一个字的剩余笔划数有变化，就跳出
                if ((j + 1 < len) && (cur_remain_strokes_num != hanzi_set[j + 1].remain_strokes_num)) {
                    i = j;
                    break;
                }
            }

            str += '</div></li>';
            $('.strokes-lists').append(str);
        }
    }

    // 设置导航条
    if (pages > 1) {
        var str = '';
        var url = '/dicts/dicts_search?q=' + q + '&source=' + source + '&page_size=' + page_size + '&left_stroke=' + left_stroke;
        if (page_num != 1) {
            var pre_url = url + '&page_num=' + parseInt(page_num - 1);
            str += '<li class="stroke_page" data-url="' + pre_url + '">上一页</li>';
        }
        str += '<li>当前第' + page_num + '页</li>';
        if (page_num != pages) {
            var next_url = url + '&page_num=' + parseInt(page_num + 1);
            str += '<li class="stroke_page" data-url="' + next_url + '">下一页</li>';
        }
        $('.pagination').append(str);
        $('#pages').html(pages);
        $('#dict_page_btn').attr("data-url", url);
        $('.pages-box').show();
    } else {
        $('.pages-box').hide();
    }
}
