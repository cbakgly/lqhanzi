// 点击检索结果集
$(document).on('click', '.strokes-item .hanzi-item', function () {
    $(".popup").hide("normal");
    var alt = $(this).attr('alt');

    $.get('/dicts/korean/detail', {"title": alt}, function (data) {
        // 渲染数据
        var trans_hash = {0:'正字', 1:'狭义异体字', 2:'广义且正字', 3:'广义异体字'};
        var str = '';
        for (item in data) {
            // 正字
            var std_hanzi = data[item].std_hanzi;
            var cls = std_hanzi.target == true ? "hanzi-normal keyword" : "hanzi-normal";
            var title = std_hanzi.hanzi_pic_id + "&#xa;" + trans_hash[std_hanzi.variant_type];
            str += '<p class="hanzi-normal"><a>[<span class="' + cls + '" title="' + title + '"><img src="' + std_hanzi.pic_url + '" alt="' + std_hanzi.hanzi_pic_id + '"></span>]</a></p>';
            // 异体字列表
            var variants = data[item].variants;
            str += '<div class="hanzi-variants">';
            for (var i = 0; i < variants.length; i++) {
                var variant = variants[i];
                var cls = variant.variant_type == 3 ? 'variant' : ''; // 广义异体字
                if (variant.target = true)
                    cls += ' keyword';
                title = variant.hanzi_pic_id + "&#xa;" + trans_hash[variant.variant_type];
                str += '<a><span class="' + cls + '" title="' + title + '"><img src="' + variant.pic_url + '" alt="' + variant.hanzi_pic_id + '"></span></a>';
            }
            str += '</div>';
        }
        $('#korean-hanzi-set').css('text-align', 'left');
        $('#korean-hanzi-set').html(str);
    });

});
