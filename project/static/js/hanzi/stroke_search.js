// string必须是"source=unicode;code=;variant_type=null;std_hanzi=;as_std_hanzi="这样的格式
function FindPropertyValue(string, property) {
    var rex = new RegExp(property + "=(.*?)\\|");
    m = string.match(rex);
    if (m != null && m[1] != "undefined") return m[1];
    else return '';
}

// 用户输入检索表达式，然后点击enter查询
$(function () {
    document.onkeydown = function (e) {
        var ev = document.all ? window.event : e;
        if (ev.keyCode == 13 && document.activeElement.id == 'searchinput') {
            $('#strock_search_btn').click();
        }
    }
});

$(document).ready(function () {
    // 检索结果汉字集，鼠标悬停时显示提示框
    $(document).on('mouseover', '.hanzi-item', function () {
        var options = $.extend({position: "t", value: 15}, {position: "b", value: 35});
        offset = $(this).offset();
        h = $(this).height();
        w = $(this).width();

        var value = $(this).attr("data-value");
        // $('#bline1').html($(this).html());
        $('#bline2').html(FindPropertyValue(value, "source"));
        if (FindPropertyValue(value, "code") == '') {
            $('#line2').hide();
        } else {
            $('#line2').show();
            $('#bline3').html(FindPropertyValue(value, "code"));
        }
        $('#bline4').html(FindPropertyValue(value, "radical"));
        $('#bline5').html(FindPropertyValue(value, "max_strokes"));
        if (FindPropertyValue(value, "std_hanzi") == '') {
            $('#std_hanzi').hide();
            $('#bline6').hide();
        } else {
            $('#std_hanzi').show();
            $('#bline6').show();
            $('#bline6').html(FindPropertyValue(value, "std_hanzi"));
        }
        $('#bline7').html(FindPropertyValue(value, "min_split"));

        // 设置"异体字检索"链接的属性值
        // 设置"反查编码"链接的属性值
        var code = FindPropertyValue(value, "code");
        if (code != '') {
            $('#search1').attr("data-value", code);
            $('#search2').attr("data-value", code);
        } else {
            $('#search1').attr("data-value", $(this).html());
            $('#search2').attr("data-value", $(this).html());
        }

        var btip_width = $("#btip").width();
        var btip_height = $("#btip").height();
        var new_left_offset = (btip_width - w) / 2;

        $("#btip").css({
            "left": offset.left - new_left_offset - 5,
            "top": offset.top - btip_height - 5
        });

        // 显示bubble
        btip_timer = setTimeout('$("#btip").fadeIn(100)', 600);

    });

    var btip_timer;
    // 检索结果汉字集，鼠标离开时隐藏提示框
    $(document).on('mouseout', '.hanzi-item', function () {
        clearTimeout(btip_timer);
        $("#btip").hide();
    });

    $(document).on('mouseover', '#btip', function () {
        $("#btip").show();
    });

    $(document).on('mouseout', '#btip', function () {
        $("#btip").hide();
    });

    // 点击bubble中的“异体字检索”时的响应函数
    $(document).on('click', '#search1', function () {
        var attr = $('#search2').attr("data-value");
        var url = '/variant_search?q=' + attr;
        window.open(url);
    });

    // 点击bubble中的“反查编码”时的响应函数
    $(document).on('click', '#search2', function () {
        var attr = $('#search2').attr("data-value");
        $("#searchinput").val(attr);
        // 设置最后一个单选按纽为选中状态
        $('.search-bottom input:last').click();
        // 触发按纽的点击事件
        $("#strock_search_btn").trigger("click");
    });

    // 点击笔画数的响应函数
    $(document).on('click', '#stroke > span', function () {
        var stroke = $(this).html();
        $("#radical_input").val(stroke);
        strokes_filter3();
    });

    // 点击笔顺时的响应函数
    $(document).on('click', '#stroke-order > span', function () {
        var value = $(this).attr("data-value");
        $("#radical_input").val($("#radical_input").val() + value);
        strokes_filter3();
    });

    // 点击重置时的响应函数
    $(document).on('click', '#clearitem', function () {
        $("#radical_input").val("");
        $(".parts-results span").show();
        $("#searcherror").text("");
    });

    // 输入框有输入时的响应
    $(document).on('input propertychange', '#radical_input', function () {
        strokes_filter3();
    });

    // 点击部件时的响应函数
    $(document).on('click', '.result-item', function () {
        var text = $("#searchinput").val() + $(this).html();
        $("#searchinput").val(text);
    });

    // 点击结构时的响应函数
    $(document).on('click', '.compontent-item', function () {
        var text = $("#searchinput").val() + $(this).attr("data-value");
        $("#searchinput").val(text);
    });

    // 点击反查编码/返回
    var reverse_query = null;
    $("#reverse-back-btn").on('click', function() {
        $('.search-bottom input:first').click();
        $.get(reverse_query, function (data) {
            render_stroke_result(data);
            $('#reverse-back-btn').hide();
        });
        $("#btip").hide();
        $("#btip").css("visibility", "visible");    // 打开提示框的开关
    });

    // 点击搜索按钮时的响应函数
    $("#strock_search_btn").click(function () {
        $('.no-result').hide();
        // 获取输入并去除空格
        var q = $(".ser-input").val().replace(/\s/g, '');
        if (q == '') return;

        // 如果有超过两个结构符，则应为正则检索
        if (q.match(/[⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]/g) !== null && q.match(/[⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]/g).length > 1) {
            //$('.search-bottom input[name="r"][value="2"]').attr('checked', true);
            $('.search-bottom input[name="r"][value="2"]').click();

        }

        // 获取当前查询模式，并存储在隐藏元素中以备后用
        var mode = $('.search-bottom input[name="r"]:checked').val();
        $("#current_mode").text(mode);

        if (mode == '1' || mode == '2') { // 一般检索&正则检索
            $("#btip").css("visibility", "visible");    // 打开提示框的开关
            reverse_query =location.origin + '/ajax_stroke_search?q=' + q + '&mode=' + mode;
            $.get("ajax_stroke_search", {"q": q, "mode": mode}, function (data) {
                render_stroke_result(data);
            });
            $('#reverse-back-btn').hide();
        } else if (mode == '3') {  // 反查编码
            $("#btip").css("visibility", "hidden");    // 关闭提示框的开关
            $.get("inverse_search", {"q": $(".ser-input").val()}, function (data) {
                render_inverse_result(data);
                $('#reverse-back-btn').show();
            });
        }
        $("#btip").hide();
    });

    // 结果页面中点击上一页、下一页时的响应函数
    $(document).on('click', '.stroke_page', function () {
        var url = 'ajax_stroke_search?' + $(this).attr("data-url");
        $.get(url, function (data) {
            render_stroke_result(data);
        });
    });

    // 点击跳页按钮时的响应函数
    $("#stroke_page_btn").click(function () {
        var new_page = $('#new_page').val();
        var regex = /^[1-9]{1}[0-9]*$/;
        var pages = parseInt($("#total").html() / $("#perpage").html())
        if ($("#total").html() % $("#perpage").html() != 0)
            ++pages;

        if (new_page.match(regex) == null) {
            // $("#search_tip").html("格式不对。");
            return;
        } else if (new_page > pages) {
            $('#new_page').val(pages)
            new_page = pages;
        }

        var url = 'ajax_stroke_search?' + $(this).attr("data-url") + '&page_num=' + new_page;
        $.get(url, function (data) {
            render_stroke_result(data);
        });
    });

});

// 笔画数字映射关系
var g_stroke_alias = {
    "h": "1",
    "s": "2",
    "p": "3",
    "n": "4",
    "d": "4",
    "z": "5"
};

function letters_to_numbers(string) {
    var ret = '';
    var len = string.length;
    for (var i = 0; i < len; i++) {
        ret += g_stroke_alias[string[i]];
    }
    return ret;
}


function strokes_filter3() {
    // 判断输入内容所符合的模式
    // 1、hs3-5，表示前两画为横、竖，剩余3-5画；
    // 2、3-5hs，表示总笔画为3-5，前两画为横、竖。
    // 又细分为以下5种

    $("#searcherror").text("");
    var regex1 = /^(\d{1,2})([hspndz]*)$/;
    var regex2 = /^(\d{1,2}-\d{1,2})([hspndz]*)$/;
    var regex3 = /^([hspndz]+)(\d{1,2})$/;
    var regex4 = /^([hspndz]+)(\d{1,2}-\d{1,2})$/;
    var regex5 = /^([hspndz]+)$/;

    // 去除空格
    var input = $("#radical_input").val();
    input = input.replace(/\s/g, '');
    if (input == '') {
        $(".parts-results span").show();
        $("#searcherror").text("");
        return;
    }

    // 经检查无问题
    if (m = input.match(regex1)) {
        var num = m[1];
        var strokes = letters_to_numbers(m[2]);
        var fliter = num + '-' + strokes;

        $(".parts-results span").hide();
        var array = $(".parts-results span[data-stroke^=" + fliter + "]");
        if (array.length > 0) {
            $(".parts-results span[data-stroke^=" + fliter + "]").show();

            $(".result-stoke[data-stroke^=" + num + '-' + "]").show();
        }
    } else if (m = input.match(regex2)) {
        var strokes = letters_to_numbers(m[2]);
        var array = m[1].split('-');
        var small = parseInt(array[0]);
        var large = parseInt(array[1]);

        if (small >= large) {
            $("#searcherror").text("笔画范围有误。");
            return;
        }

        $(".parts-results span").hide();
        for (var i = small; i <= large; i++) {
            var fliter = i + '-' + strokes;
            var array = $(".parts-results span[data-stroke^=" + fliter + "]");
            if (array.length > 0) {
                $(".parts-results span[data-stroke^=" + fliter + "]").show();
            }
        }

        for (var i = small; i <= large; i++) {
            $(".result-stoke[data-stroke^=" + i + '-' + "]").show();
        }

    } else if (m = input.match(regex3)) {
        var strokes = letters_to_numbers(m[1]);
        var left = parseInt(m[2]);
        var total = strokes.length + left;
        var fliter = total + '-' + strokes;

        $(".parts-results span").hide();
        var array = $(".parts-results span[data-stroke^=" + fliter + "]");
        if (array.length > 0) {
            $(".parts-results span[data-stroke^=" + fliter + "]").show();
            $(".result-stoke[data-stroke^=" + total + '-' + "]").show();
        }
    } else if (m = input.match(regex4)) {
        var strokes = letters_to_numbers(m[1]);
        var array = m[2].split('-');

        var small = parseInt(array[0]);
        var large = parseInt(array[1]);

        if (small >= large) {
            $("#searcherror").text("剩余笔画范围有误。");
            return;
        }

        $(".parts-results span").hide();
        for (var i = small; i <= large; i++) {
            var total = strokes.length + i;
            var fliter = total + '-' + strokes;

            var array = $(".parts-results span[data-stroke^=" + fliter + "]");
            if (array.length > 0) {
                $(".parts-results span[data-stroke^=" + fliter + "]").show();
                $(".result-stoke[data-stroke^=" + total + '-' + "]").show();
            }
        }
    } else if (m = input.match(regex5)) {
        var strokes = letters_to_numbers(m[1]);
        $(".parts-results span").hide();
        for (var i = 1; i <= 22; i++) {
            var fliter = i + '-' + strokes;
            var array = $(".parts-results span[data-stroke^=" + fliter + "]");
            if (array.length > 0) {
                $(".parts-results span[data-stroke^=" + fliter + "]").show();
                $(".result-stoke[data-stroke^=" + i + '-' + "]").show();
            }
        }
    } else {
        $("#searcherror").text("格式错误。");
    }
}


// 渲染部件笔画检字法结果集
function render_stroke_result(dataset) {
    // 查询到的字对象的集合
    var q = dataset.q;
    var total = dataset.total;
    var data = dataset.result;
    var mode = dataset.mode;
    var page_num = dataset.page_num;
    var page_size = dataset.page_size;
    var pages = parseInt(total / page_size);
    if (total % page_size != 0)
        ++pages;

    $("#result-tips").show();
    // $(".con-right").addClass("con-right-new");
    
    // 如果没有检索到数据
    if ( total == 0 || data === undefined) {
        $('#hanzi-wrap').html('');
        $('#pages-box').hide();
        $("#total").html(0);
        $("#perpage").html(0);
        $("#con-left").fadeIn(600);
        // $("#con-right").addClass("con-right-new");
        return;
    }

    // 显示符合要求的条目数
    if (total > page_size)
        $('#pages-box').show();
    else
        $('#pages-box').hide();

    $("#total").html(total);
    $("#perpage").html(page_size);
    $('#hanzi-wrap').html('');
    $('#pagination').html('');


    // 本次查询到的字对象的个数
    len = data.length;
    for (var i = 0; i < len; i++) {
        var char = "";
        if (data[i].source == 1) { // 如果是unicode
            var data_value = 'source=unicode|code=' + data[i].remark + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
            char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
            char += data[i].hanzi_char;
            char += '" data-value="';
            char += data_value + '">';
            char += data[i].hanzi_char;
            char += '</a></li>';
        } else if (data[i].source == 2) { // 如果是台湾异体字
            var data_value = 'source=台湾异体字|code=' + data[i].seq_id + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
            if (data[i].hanzi_char != "") {
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            } else {
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_pic_id;
                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        } else if (data[i].source == 3) {  // 如果是汉字大字典
            if (data[i].hanzi_char != "") {
                var data_value = 'source=汉字大字典|code=' + data[i].hanzi_char + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            } else {
                var data_value = 'source=汉字大字典|code=' + data[i].hanzi_pic_id + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_pic_id;
                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        } else if (data[i].source == 4) {  // 如果是高丽异体字
            if (data[i].hanzi_char != "") {
                var data_value = 'source=高丽异体字|code=' + data[i].hanzi_char + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            } else {
                var data_value = 'source=高丽异体字|code=' + data[i].hanzi_pic_id + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_pic_id;
                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        } else if (data[i].source == 5) {  // 如果是敦煌俗字典
            if (data[i].hanzi_char != "") {
                var data_value = 'source=敦煌俗字典|code=' + data[i].hanzi_char + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            } else {
                var data_value = 'source=敦煌俗字典|code=' + data[i].hanzi_pic_id + '|radical=' + data[i].radical + '|max_strokes=' + data[i].max_strokes + '|std_hanzi=' + data[i].std_hanzi + '|min_split=' + data[i].min_split + '|';
                char = '<li><a class="hanzi-item" target="_blank" href="/variant_detail?q=';
                char += data[i].hanzi_pic_id;
                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        }
        // 把字填到左侧结果面板
        $('.hanzi-wrap').append(char);
    }

    // 分页导航
    var str = '';
    if (page_num > 1) {
        var url = 'q=' + q + '&mode=' + mode + '&page_num=' + parseInt(page_num - 1);
        str += '<li class="stroke_page" data-url="' + url + '"><</li>';
    }
    str += '<li>' + page_num + '</li>';
    if (page_num < pages) {
        var url = 'q=' + q + '&mode=' + mode + '&page_num=' + parseInt(page_num + 1);
        str += '<li class="stroke_page" data-url="' + url + '">></li>';
    }
    $('#pagination').append(str);
    $('#pages').html(pages);

    // 给Go按纽增加data-url属性， 以便单击时利用
    var new_url = 'q=' + q + '&mode=' + mode;
    $('#stroke_page_btn').attr("data-url", new_url);

    // 让隐藏的左面板显示出来
    $("#con-left").fadeIn(600);
    // $(".con-right").addClass("con-right-new");
}

// 渲染反查编码的结果
function render_inverse_result(data) {
    $('.pages-box').empty();
    $('.hanzi-wrap').html('');

    if ($.isEmptyObject(data)) {
        $("#total").html(0);
        $("#perpage").html(0);
        // $('.hanzi-wrap').html('没有检索到数据。');
        $("#con-left").fadeIn(600);
        // $(".con-right").addClass("con-right-new");
        return;
    }
    $("#result-tips").hide();

    var str = '<table class="reverse">';
    if (data.hanzi_pic_id != "") {
        str += '<tr><td><a target="_blank" href="/variant_detail?q=' + data.hanzi_pic_id + '"><img src="' + data.pic_url + '"></a></td></tr>';
    } else {
        str += '<tr><td style="font-size:35px;"><a target="_blank" href="/variant_detail?q=' + data.hanzi_char + '">' + data.hanzi_char + '</a></td></tr>';
    }
    str += '<tr><td>初步拆分</td><td>' + data.min_split + '</td></tr>';
    str += '<tr><td>混合拆分</td><td>' + data.mix_split + '</td></tr>';
    str += '<tr><td>部件序列</td><td>' + data.stroke_serial + '</td></tr>';
    str += '<tr><td>相似部件</td><td>' + data.similar_parts + '</td></tr>';
    str += '</table>';
    $('.hanzi-wrap').append(str);

    $("#con-left").fadeIn(600);
    // $(".con-right").addClass("con-right-new");
}
