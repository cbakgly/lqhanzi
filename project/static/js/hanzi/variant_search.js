// 常量
var TAIWAN = 2;
var HANYU = 3;
var KOREAN = 4;
var DUNHUANG = 5;

// 获取url参数
function get_query_string(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)  return unescape(r[2]);
    return null;
}

// 用户输入检索表达式，然后点击enter查询
$(function () {
    document.onkeydown = function (e) {
        var ev = document.all ? window.event : e;
        if (ev.keyCode == 13 && document.activeElement.id == 'variant_searchinput') {
            $('#variant_search_btn').click();
        }
    }
});

$(document).ready(function () {
    // 如果url中有参数，则点击查询
    var q = $("#q").text();
    if (q != "None" && q.toString().length > 0) {
        $("#variant_searchinput").val(q);
        $(".tip").text("正在查询中...");
        $.get("ajax_variant_search", {"q": $(".ser-input").val()}, function (data) {
            render_variant_result(data);
        });
    }

    // 点击异体字搜索按钮时的响应函数
    $("#variant_search_btn").click(function () {
        $.get("ajax_variant_search", {"q": $(".ser-input").val()}, function (data) {
            render_variant_result(data);
        });
    });

});


// 渲染异体字检字法结果集的函数
function render_variant_result(res) {
    if (res.empty == true || res === undefined) {
        $(".tip").text("检索到0条数据。");
        return;
    }

    // 清空结果面板
    $('.dict-result-lists').html('');

    var char = "";
    var data = res.data;
    var hanzi_codes = data.hanzi_codes;

    if (data[TAIWAN].length > 0) {  // 台湾异体字
        var source = TAIWAN;
        char += '<li class="dict-result-item">';
        char += '<h3 class="dict-title">《台湾异体字字典》</h3>';
        var hanzi_set = data[source];
        for (var j = 0; j < hanzi_set.length; j++) {
            // 正字
            if (hanzi_set[j].hanzi_char != '') {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_char + '">';
                char += '[<span>' + hanzi_set[j].hanzi_char + '</span>]</a></p>';
            } else {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_pic_id + '">';
                char += '[<span><img src="' + hanzi_set[j].pic_url + '"></span>]</a></p>';
            }
            // 异体字
            char += '<div class="hanzi-variants">';
            if (hanzi_set[j].variants === undefined) continue;
            var variants = hanzi_set[j].variants;
            for (var k = 0; k < variants.length; k++) {
                if (variants[k].hanzi_char != '') {
                    char += '<a target="_blank" href="/variant_detail?q=' + variants[k].hanzi_char + '">';
                    char += '<span class="normal ';
                    if (variants[k].variant_type == 3) char += 'instruction-generic-variant-char';
                    else if (variants[k].variant_type == 2) char += 'instruction-generic-variant-std-char';
                    char += '">';
                    char += variants[k].hanzi_char;
                    char += '</span></a>';
                } else {
                    char += '<a target="_blank" href="/variant_detail?q=' + variants[k].hanzi_pic_id + '">';
                    char += '<span ';
                    if (variants[k].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                    else if (variants[k].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                    char += '>';
                    char += '<img src="' + variants[k].pic_url + '">';
                    char += '</span></a>';
                }
            }
            char += '</div></li>';
        }
    }

    if (data[KOREAN].length > 0) {  // 高丽异体字
        var source = KOREAN;
        char += '<li class="dict-result-item">';
        char += '<h3 class="dict-title">《高丽异体字字典》</h3>';
        var hanzi_set = data[source];
        for (var j = 0; j < hanzi_set.length; j++) {
            // 正字
            if (hanzi_set[j].hanzi_char != '') {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_char + '">';
                char += '[<span>' + hanzi_set[j].hanzi_char + '</span>]</a></p>';
            } else {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_pic_id + '">';
                char += '[<span><img src="' + hanzi_set[j].pic_url + '"></span>]</a></p>';
            }
            // 异体字
            char += '<div class="hanzi-variants">';
            if (hanzi_set[j].variants === undefined) continue;
            var variants = hanzi_set[j].variants;
            for (var k = 0; k < variants.length; k++) {
                if (variants[k].hanzi_char != '') {
                    char += '<a target="_blank" href="/variant_detail?q=' + variants[k].hanzi_char + '">';
                    char += '<span class="normal ';
                    if (hanzi_set[j].variant_type == 3) char += 'instruction-generic-variant-char';
                    else if (hanzi_set[j].variant_type == 2) char += 'instruction-generic-variant-std-char';
                    char += '">' + variants[k].hanzi_char + '</span></a>';
                } else {
                    char += '<a target="_blank" href="/variant_detail?q=' + variants[k].hanzi_pic_id + '">';
                    char += '<span ';
                    if (hanzi_set[j].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                    else if (hanzi_set[j].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                    char +='><img src="' + variants[k].pic_url + '"></span></a>';
                }
            }
            char += '</div></li>';
        }
    }

    if (data[HANYU].length > 0) {  // 汉语大字典
        var source = HANYU;
        char += '<li class="dict-result-item">';
        char += '<h3 class="dict-title">《汉语大字典》</h3>';
        var hanzi_set = data[source];
        for (var j = 0; j < hanzi_set.length; j++) {
            if (hanzi_set[j].hanzi_char != '') {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_char + '">';
                char += '[<span ';
                if (hanzi_set[j].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                else if (hanzi_set[j].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                char += '>' + hanzi_set[j].hanzi_char + '</span>]</a></p>';
            } else {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_pic_id + '">';
                char += '[<span ';
                if (hanzi_set[j].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                else if (hanzi_set[j].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                char +='><img src="' + hanzi_set[j].pic_url + '"></span>]</a></p>';
            }
        }
    }

    if (data[DUNHUANG].length > 0) {  // 敦煌俗字典
        var source = DUNHUANG;
        char += '<li class="dict-result-item">';
        char += '<h3 class="dict-title">《敦煌俗字典》</h3>';
        var hanzi_set = data[source];
        for (var j = 0; j < hanzi_set.length; j++) {
            if (hanzi_set[j].hanzi_char != '') {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_char + '">';
                char += '[<span ';
                if (hanzi_set[j].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                else if (hanzi_set[j].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                char += '>' + hanzi_set[j].hanzi_char + '</span>]</a></p>';
            } else {
                char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?q=' + hanzi_set[j].hanzi_pic_id + '">';
                char += '[<span ';
                if (hanzi_set[j].variant_type == 3) char += 'class="instruction-generic-variant-char"';
                else if (hanzi_set[j].variant_type == 2) char += 'class="instruction-generic-variant-std-char"';
                char += '><img src="' + hanzi_set[j].pic_url + '"></span>]</a></p>';
            }
        }
    }

    $('.dict-result-lists').append(char);

    $('.no-result').hide();
    $('.dict-results').show();

}


