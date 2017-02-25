
//string必须是"source=unicode;code=;variant_type=null;std_hanzi=;as_std_hanzi="这样的格式
function FindPropertyValue(string,property)
{
    var rex = new RegExp( property+"=(.*?)\\|");
    m = string.match(rex);
    if(m != null && m[1]!="undefined") return m[1];
    else return '';
}


$(document).ready(function()
{

    $(document).on('mouseover', '.hanzi-item', function()
    {
        var options = $.extend({position:"t", value:15},{position:"b",value:35});

        offset = $(this).offset();
        h = $(this).height();
        w = $(this).width();

        var value = $(this).attr("data-value");

        $('#bline1').html( $(this).html()  );
        $('#bline2').html( FindPropertyValue(value,"source") );
        $('#bline3').html( FindPropertyValue(value,"code") );
        $('#bline4').html( FindPropertyValue(value,"radical") );
        $('#bline5').html( FindPropertyValue(value,"max_strokes") );
        $('#bline6').html( FindPropertyValue(value,"std_hanzi") );
        $('#bline7').html( FindPropertyValue(value,"min_split") );

        //设置"异体字检索"链接的属性值
        //设置”反查编码“链接的属性值
        var code = FindPropertyValue(value,"code");
        if(code!='')
        {
            $('#search1').attr("data-value",code);
            $('#search2').attr("data-value",code);
        }
        else
        {
            $('#search1').attr("data-value",$(this).html() );
            $('#search2').attr("data-value",$(this).html() );
        }


        var btip_width = $("#btip").width();
        var btip_height = $("#btip").height();
        var new_left_offset = (btip_width - w)/2;

        $("#btip").css({ "visibility":"visible","left":offset.left-new_left_offset-5,"top":offset.top-btip_height-5});

        //显示bubble
        $("#btip").show();

    });

    $(document).on('mouseout', '.hanzi-item', function()
    {
        $("#btip").hide();
    });


    $(document).on('mouseover', '#btip', function()
    {
        $("#btip").show();
    });


    $(document).on('mouseout', '#btip', function()
    {
        $("#btip").hide();
    });



    //点击bubble中的“异体字检索”时的响应函数
    $(document).on('click', '#search1', function()
    {
        var attr = $('#search2').attr("data-value");
        var url = 'variant_search?mark=ext&q=' + attr;
        window.open (url);
    });


    //点击bubble中的“反查编码”时的响应函数
    $(document).on('click', '#search2', function()
    {
        var attr = $('#search2').attr("data-value");
        $("#searchinput").val(attr);

        //设置最后一个单选按纽为选中状态
        $('.search-bottom input:last').click();

        //触发按纽的点击事件
        $("#strock_search_btn").trigger("click");

    });


    //点击笔画数的响应函数
    $(document).on('click', '#strokes > span', function()
    {
        var stroke = $(this).html();
        $("#radical_input").val(stroke);
        strokes_filter3();
    });


    //点击笔顺时的响应函数
    $(document).on('click', '#stroke-order > span', function()
    {
        var value = $(this).attr("data-value");
        $("#radical_input").val( $("#radical_input").val() + value);
        strokes_filter3();
    });


    //点击重置时的响应函数
    $(document).on('click', '#clearitem', function()
    {
        $("#radical_input").val("");
        $(".parts-results span").show();
        $("#searcherror").text("");
    });


    //输入框有输入时的响应
    $(document).on('input propertychange', '#radical_input', function()
    {
        strokes_filter3();
    });

    //点击部件时的响应函数
    $(document).on('click', '.result-item', function()
    {
        var text = $("#searchinput").val() + $(this).html();
        $("#searchinput").val(text);
    });

    //点击结构时的响应函数
    $(document).on('click', '.compontent-item', function()
    {
        var text = $("#searchinput").val() + $(this).attr("data-value");
        $("#searchinput").val(text);
    });

    //点击部件笔画搜索按钮时的响应函数
    $("#strock_search_btn").click( function ()
    {
        //获取当前查询模式，并存储在隐藏元素中以备后用
        var order = $('.search-bottom input[name="r"]:checked').val();
        $("#current_order").text(order);

        //获取输入并去除空格
        var q = $(".ser-input").val();
        q=q.replace(/\s/g,'');
        if(q=='')return;

        if(order=='1')
        {
            var regex1 = /^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([^\w,;:`%?&.+*^(){}@!|]+)(\d{1,3}-\d{1,3})$/;
            var regex2 = /^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([^\w,;:`%?&.+*^(){}@!|]+)(\d{1,3})$/;
            var regex3 = /^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([^\w,;:`%?&.+*^(){}@!|]+)$/;

            //检验输入数据
            var m = new Array;
            if(  (m=q.match(regex1))||(m=q.match(regex2))||(m=q.match(regex3)) )
            {
                if(m[3])
                {
                    var array = m[3].split('-');
                    var small = parseInt(array[0]);
                    var large = parseInt(array[1]);
                    if(small>=large){alert("格式不对");return;}
                }
            }
            else
            {alert("格式不对");return;}

            $.get(
              "stroke_normal_search",
              {"q":q,"page_num":1,"page_size":100,},
              function (data)
              {
                //渲染数据
                render_stroke_result(data);
              });
        }
        else if(order=='2')
        {
            var regex1 = /^([^a-zA-Z]+?)(\d{1,3}-\d{1,3})$/;
            var regex2 = /^([^a-zA-Z]+?)(\d{1,3})$/;
            var regex3 = /^([^a-zA-Z]+)$/;

            //检验输入数据
            var m = new Array;
            if(  (m=q.match(regex1))||(m=q.match(regex2))||(m=q.match(regex3)) )
            {
                if(m[3])
                {
                    var array = m[3].split('-');
                    var small = parseInt(array[0]);
                    var large = parseInt(array[1]);
                    if(small>=large){alert("格式不对1");return;}
                }
            }
            else
            {alert("格式不对2");return;}

            $.get(
              "stroke_advanced_search",
              {"q":q,"page_num":1,"page_size":100,},
              function (data)
              {
                  //渲染数据
                  render_stroke_result(data);
              });
        }
        else if(order=='3')
        {

            //检验输入数据

            $.get(
              "inverse_search",
              {"q":$(".ser-input").val()},
              function (data)
              {
                  //渲染数据
                  render_inverse_result(data);
              });
            return;
        }

    });



    //部件笔画检字法结果页面中，点击上一页、下一页时的换页函数
    $(document).on('click', '.stroke_page', function()
    {
        var current_order = $("#current_order").text();
        var url = $(this).attr("data-url");

        if(current_order=='1')
        {
            url = 'stroke_normal_search?' + url;

        }
        else if(current_order=='2')
        {
            url = 'stroke_advanced_search?' + url;
        }

        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_stroke_result(data);
          });
    });


    //点击部件笔划检索结果中的跳页按钮时的响应函数
    $("#stroke_page_btn").click( function ()
    {
        var new_page = $('#new_page').val();
        var regex = /^[1-9]{1}[0-9]*$/;

        if(new_page.match(regex) == null)
        {
            $("#search_tip").html("格式不对");
            return;
        }

        if(new_page>$("#total").html()/$("#perpage").html()+1)
        {
            $("#search_tip").html("页码超过范围啦");
            return;
        }

        var current_order = $("#current_order").text();
        var url = $(this).attr("data-url") + '&page_num=' + new_page;


        if(current_order=='1')
        {
            url = 'stroke_normal_search?' + url;
        }
        else if(current_order=='2')
        {
            url = 'stroke_advanced_search?' + url;
        }


        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_stroke_result(data);
          });
    });



});



var g_stroke_alias =
{
    "h":"1",
    "s":"2",
    "p":"3",
    "n":"4",
    "d":"4",
    "z":"5"
};

function letters_to_numbers(string)
{
    var ret = '';
    var len = string.length;
    for(var i=0;i<len;i++)
    {
        ret += g_stroke_alias[string[i]];
    }
    return ret;
}


function strokes_filter3()
{
    //判断输入内容所符合的模式
    //1、hs3-5，表示前两画为横、竖，剩余3-5画；
    //2、3-5hs，表示总笔画为3-5，前两画为横、竖。
    //又细分为以下5种

    $("#searcherror").text("");

    var regex1 = /^(\d{1,2})([hspndz]*)$/;
    var regex2 = /^(\d{1,2}-\d{1,2})([hspndz]*)$/;
    var regex3 = /^([hspndz]+)(\d{1,2})$/;
    var regex4 = /^([hspndz]+)(\d{1,2}-\d{1,2})$/;
    var regex5 = /^([hspndz]+)$/;

    //去除空格
    var input = $("#radical_input").val();

    input=input.replace(/\s/g,'');

    if(input == '')
    {
        $(".parts-results span").show();
        $("#searcherror").text("");
        return;
    }

    //经检查无问题
    if(m = input.match(regex1))
    {
        var num = m[1];
        var strokes = letters_to_numbers(m[2]);
        var fliter = num+'-'+strokes;
       

        $(".parts-results span").hide();
        var array = $(".parts-results span[data-stroke^=" + fliter +"]");
        if(array.length>0)
        {
            $(".parts-results span[data-stroke^=" + fliter +"]").show();

            $(".result-stoke[data-stroke^=" + num +'-' +"]").show();
        }
    }

    //无问题
    else if(m = input.match(regex2))
    {
        var strokes = letters_to_numbers(m[2]);
        var array = m[1].split('-');
        var small = parseInt(array[0]);
        var large = parseInt(array[1]);

        if(small>=large)
        {
            $("#searcherror").text("笔画范围有误");
            return;
        }

        $(".parts-results span").hide();
        for(var i=small;i<=large;i++)
        {
            var fliter = i+'-'+strokes;
            var array = $(".parts-results span[data-stroke^=" + fliter +"]");
            if(array.length>0)
            {
                $(".parts-results span[data-stroke^=" + fliter +"]").show();
            }
        }

        for(var i=small;i<=large;i++)
        {
            $(".result-stoke[data-stroke^=" + i +'-'+"]").show();
        }

    }
    //已满足
    else if(m = input.match(regex3))
    {
        var strokes = letters_to_numbers(m[1]);
        var left = parseInt(m[2]);
        var total = strokes.length + left;
        var fliter = total+'-'+strokes;

        $(".parts-results span").hide();
        var array = $(".parts-results span[data-stroke^=" + fliter +"]");
        if(array.length>0)
        {
            $(".parts-results span[data-stroke^=" + fliter +"]").show();
            $(".result-stoke[data-stroke^=" + total + '-'+"]").show();    
        }
    }
    // 已满足
    else if(m = input.match(regex4))
    {
        var strokes = letters_to_numbers(m[1]);
        var array = m[2].split('-');

        var small = parseInt(array[0]);
        var large = parseInt(array[1]);

        if(small>=large)
        {
            $("#searcherror").text("剩余笔画范围有误");
            return;
        }

        $(".parts-results span").hide();
        for(var i=small;i<=large;i++)
        {
            var total = strokes.length + i;
            var fliter = total+'-'+strokes;

            var array = $(".parts-results span[data-stroke^=" + fliter +"]");
            if(array.length>0)
            {
                $(".parts-results span[data-stroke^=" + fliter +"]").show();
                $(".result-stoke[data-stroke^=" + total + '-'+"]").show();    
            }
        }
    }
    //已满足
    else if(m = input.match(regex5))
    {
        var strokes = letters_to_numbers(m[1]);
        $(".parts-results span").hide();
        for(var i=1;i<=22;i++)
        {
            var fliter = i+'-'+strokes;
            var array = $(".parts-results span[data-stroke^=" + fliter +"]");
            if(array.length>0)
            {
                $(".parts-results span[data-stroke^=" + fliter +"]").show();
                $(".result-stoke[data-stroke^=" + i + '-'+ "]").show();
            }
        }
    }

    else
    {
        $("#searcherror").text("格式错误");
    }
}



//渲染部件笔画检字法结果集的函数
function render_stroke_result(data)
{
    //查询到的字对象的集合
    var q = data.q;
    var page_num = data.page_num;
    var pages = data.pages;
    var page_size = data.page_size;
    var total = data.total;
    var data = data.result;

    //如果没有检索到数据
    if(total==0)
    {
        $("#total").html(0);
        $("#perpage").html(0);

        $('.hanzi-wrap').html('没有检索到数据！');
        $(".con-left").fadeIn(600);
        $(".con-right").addClass("con-right-new");
        return;
    }

    //显示符合要求的条目数
    $("#total").html(total);
    $("#perpage").html(page_size);

    $('.hanzi-wrap').html('');
    $('.pagination').empty();

    //本次查询到的字对象的个数
    len = data.length;
    for (var i=0;i<len;i++)
    {
        var char = "";
        if(data[i].source == 1)//如果是unicode
        {
            var data_value = 'source=unicode|code='+data[i].remark +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split +'|';
            //var data_value = 'source=unicode;code='+data[i].remark +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

            char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=1&type=char&text=';
            char += data[i].hanzi_char;
            char += '" data-value="';
            char += data_value + '">';
            char += data[i].hanzi_char;
            char += '</a></li>';
        }
        else if(data[i].source == 2)//如果是台湾异体字
        {
            var data_value = 'source=台湾异体字|code='+data[i].seq_id +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';

            // var data_value = 'source=台湾异体字;code='+data[i].seq_id +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

            if(data[i].hanzi_char != "")
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=2&type=char&text=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=2&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        }
        else if(data[i].source == 3)   //如果是汉字大字典
        {

            if(data[i].hanzi_char != "")
            {
                var data_value = 'source=汉字大字典|code='+data[i].hanzi_char +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';

                // var data_value = 'source=汉字大字典;code='+data[i].hanzi_char +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=char&text=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=汉字大字典|code='+data[i].hanzi_pic_id +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';

                //var data_value = 'source=汉字大字典;code='+data[i].hanzi_pic_id +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        }
        else if(data[i].source == 4)   //如果是高丽异体字
        {
            if(data[i].hanzi_char != "")
            {
                var data_value = 'source=高丽异体字|code='+data[i].hanzi_char +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';

                //var data_value = 'source=高丽异体字;code='+data[i].hanzi_char +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=char&text=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=高丽异体字|code='+data[i].hanzi_pic_id +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';

                //var data_value = 'source=高丽异体字;code='+data[i].hanzi_pic_id +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        }
        else if(data[i].source == 5)   //如果是敦煌俗字典
        {
            if(data[i].hanzi_char != "")
            {
                var data_value = 'source=敦煌俗字典|code='+data[i].hanzi_char +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';
                //var data_value = 'source=敦煌俗字典;code='+data[i].hanzi_char +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi + ';as_std_hanzi=' + data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=char&text=';
                char += data[i].hanzi_char;
                char += '" data-value="';
                char += data_value + '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=敦煌俗字典|code='+data[i].hanzi_pic_id +'|radical='+data[i].radical+ '|max_strokes='+data[i].max_strokes +'|std_hanzi='+data[i].std_hanzi + '|min_split=' + data[i].min_split+'|';
                //var data_value = 'source=敦煌俗字典;code='+data[i].hanzi_pic_id +';variant_type='+data[i].variant_type+';std_hanzi='+data[i].std_hanzi+';as_std_hanzi='+data[i].as_std_hanzi;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=pic&text=';
                char += data[i].hanzi_pic_id;
                char += '" data-value="';
                char += data_value + '"><img src="';
                char += data[i].pic_url;
                char += '" alt="';
                char += data[i].hanzi_pic_id;
                char += '"></a></li>';
            }
        }
        //把字填到左面板里去
        $('.hanzi-wrap').append(char);
    }


    var str = '';
    var prev = page_num-1;
    var next = page_num+1;

    var url = '';
    if(page_num == 1)
    {
        str += '<li>上一页</li>';
    }
    else
    {
        url = 'q=' + q + '&page_num=' + prev +'&page_size=' + page_size;
        str += '<li class="stroke_page" data-url="' + url + '">上一页</li>';
    }

    str += '<li>' + page_num + '页/' + pages + '页</li>';

    if(page_num == pages)
    {
        str += '<li>下一页</li>';
    }
    else
    {
        url = 'q=' + q + '&page_num=' + next +'&page_size=' + page_size;
        str += '<li class="stroke_page" data-url="' + url + '">下一页</li>';
    }

    $('.pagination').append(str);


    //给翻页按纽增加data-url属性， 以便单击时利用
    var new_url = 'q=' + q + '&page_size=' + page_size;
    $('#stroke_page_btn').attr("data-url",new_url);


    //让隐藏的左面板显示出来
    $(".con-left").fadeIn(600);
    $(".con-right").addClass("con-right-new");
}



function render_inverse_result(data)
{
    $('.pages-box').empty();
    $('.hanzi-wrap').html('');

    if(data="none")
    {
        $("#total").html(0);
        $("#perpage").html(0);

        $('.hanzi-wrap').html('没有检索到数据！');
        $(".con-left").fadeIn(600);
        $(".con-right").addClass("con-right-new");
        return;
    }

    $("#total").html(1);
    $("#perpage").html(1);

    var str = '<table class="reverse">';

    if(data.hanzi_pic_id != "")
    {
        str +='<tr><td>所查字</td><td><img src="' + data.hanzi_pic_id + '"></td></tr>';
    }
    else
    {
        str +='<tr><td>所查字</td><td>' + data.hanzi_char + '</td></tr>';
    }

    str +='<tr><td>来源</td><td>' + data.source + '</td></tr>';
    str +='<tr><td>正字</td><td>' + data.std_hanzi + '</td></tr>';
    str +='<tr><td>兼正字</td><td>' + data.as_std_hanzi + '</td></tr>';
    str +='<tr><td>混合拆分</td><td>' + data.mix_split + '</td></tr>';
    str += '</table>';

    $('.hanzi-wrap').append(str);

    $(".con-left").fadeIn(600);
    $(".con-right").addClass("con-right-new");
}
