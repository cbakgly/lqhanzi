
// function get_radical()
// {
//   $.post("get_radical",
//     function (data)
//     {
//       for (var i=0;i<data.length;i++)
//       {
//         var char = '<a class="radical" href="/hanzi/check?page=1&radical=';
//         char += data[i].radical;          
//         char += '" target="checkresult">';
//         char += data[i].radical;
//         char += '</a>';
//         $('#radical_list').append(char); 
//       }
//     });
// }


// function get_parts()
// {
//   $.post("get_parts",
//     function (data)
//     {
//         var flag = 0;
//         for (var i=0;i<data.length;i++)
//         {
//           var char ="";
//           if( data[i].strokes != flag)
//           {
//               char = '<span class="result-stoke" ';
//               char += 'data-stroke="';
//               char += data[i].strokes;
//               char += '">'
//               char += data[i].strokes;
//               char += '</span>';
//               flag = data[i].strokes;
//           }

//           char += '<span class="result-item" ';
//           char += 'data-stroke="';
//           char += data[i].strokes;
//           char += data[i].stroke_order;
//           char += '">'
//           char += data[i].part_char;
//           char += '</span>';

//           $('.parts-results').append(char); 
//         }
//     });
// }




        




$(document).ready(function()
{

    //var options = $.extend({position:"t", value:15},{position:"b",value:35});


    // $(document).on('mouseover', '.hanzi-item', function()
    // {
    //     clearInterval(window.timer);
    //     offset = $(this).offset();
    //     h = $(this).height();
    //     w = $(this).width();
    //     $("#btip").css({ "position":"fixed","left":offset.left-30,"top":offset.top-h+5,"z-index":999});    
    //     $("#btip").show();

    // });

    // $(document).on('mouseout', '.hanzi-item', function()
    // {
    //     window.timer = window.setInterval(function (){$("#btip").hide();},1000);  
    //     $("#btip").hide();   
    // });


    // $(document).on('mouseover', '#btip', function()
    // {
    //     clearInterval(window.timer);
    //     $("#btip").show();
    // });


    // $(document).on('mouseout', '#btip', function()
    // {
    //       $("#btip").hide(); 
    // });


    //点击笔画数的响应函数
    $(document).on('click', '#strokes > span', function()
    {
        var text = $("#radical_input").val() + $(this).html();
        $("#radical_input").val(text);
        strokes_filter();
    });


    //点击笔顺时的响应函数
    $(document).on('click', '#stroke-order > span', function()
    {
        var text = $("#radical_input").val() + $(this).attr("data-value");
        $("#radical_input").val(text);
        strokes_filter();
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

    //点击检索结果中的字的响应函数
    //$(document).on('click', '.hanzi-item', function()
    //{
        // var text = $("#searchinput").val() + $(this).attr("data-value");
        // $("#searchinput").val(text);
    //});


    //部件笔画检字法结果页面中，点击上一个、下一页时的换页函数
    $(document).on('click', '.stroke_page', function()
    {
        //var url = $(this).find("a").attr("href");
        var url = $(this).attr("data-url");
        //显示载入动画
        $(".loading").show();
        
        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_stroke_result(data);

              //关闭载入动画
              $(".loading").hide();
          });
    });




    //点击部件笔画搜索按钮时的响应函数
    $("#strock_search_btn").click( function ()
    {
        //显示载入动画
        $(".loading").show();
        
        var order = $('.search-bottom input[name="r"]:checked').val();  
        $.get(
          "stroke_ajax_search",
          {"q":$(".ser-input").val(),"order":order,"page_num":1,"page_size":100,},
          function (data)
          {
              //渲染数据
              render_stroke_result(data);

              //关闭载入动画
              $(".loading").hide();
          });
    });




    //点击异体字搜索按钮时的响应函数
    $("#variant_search_btn").click( function ()
    {
        //显示载入动画
        $(".loading").show();
        
        //var order = $('.search-bottom input[name="r"]:checked').val();  
        $.get(
          "variant_search",
          {"q":$(".ser-input").val()},
          function (data)
          {
              //渲染数据
              render_variant_result(data);

              //关闭载入动画
              $(".loading").hide();
          });
    });


    // //点击部首时的响应函数
    // $(".treeview-menu .hanzi-item").click( function ()
    // {        alert("sssss");
    //     //搞清楚当前那个字典有效
    //     var dict = $(".dict-tabs .active").html();
    //     var source = 0;
    //     if(dict == '台湾异体字字典')
    //         source = 2;
    //     else if(dict == '高丽异体字字典')
    //         source = 4;
    //     else if(dict == '汉语大字典')
    //         source = 3;
    //     else if(dict == '敦煌俗字典')
    //         source = 5;


    //     alert(source);

    //     $.get(
    //       "dicts_search",
    //       {"q":$(this).html(),"source":source,"page_num":1,"page_size":200,},
    //       function (data)
    //       {
    //           //渲染数据
    //           render_dicts_result(data);
    //       });
    // });











});





//渲染部件笔画检字法结果集的函数
function render_stroke_result(data)
{
    //查询到的字对象的集合
    var q = data.q
    var page_num = data.page_num
    var pages = data.pages
    var page_size = data.page_size
    var order = data.order
    var data = data.result

    //查询到的字对象的个数
    len = data.length;

    //显示取到的条目数
    $("#stroke_result_count").html(len);   
    $('.hanzi-wrap').html('');
    $('.pagination').html('');

    for (var i=0;i<len;i++)
    {
        var char = "";
        if(data[i].source == 1)//如果是unicode
        {
            char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=1&type=char&text=';
            char += data[i].hanzi_char;
            char += '">';
            char += data[i].hanzi_char;
            char += '</a></li>';
        }
        else if(data[i].source == 2)//如果是台湾异体字
        {
            if(data[i].hanzi_char != "")
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=2&type=char&text=';
                char += data[i].hanzi_char;
                char += '">';
                char += data[i].hanzi_char; 
                char += '</a></li>';              
            }
            else
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=2&type=pic&text=';
                char += data[i].hanzi_pic_id;
                char += '"><img src="';
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
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=char&text=';
                char += data[i].hanzi_char;
                char += '">';
                char += data[i].hanzi_char; 
                char += '</a></li>';
            }
            else
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=pic&text=';
                char += data[i].hanzi_pic_id;
                char += '"><img src="';
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
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=char&text=';
                char += data[i].hanzi_char;
                char += '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=pic&text=';
                char += data[i].hanzi_pic_id;
                char += '"><img src="';
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
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=char&text=';
                char += data[i].hanzi_char;
                char += '">';
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=pic&text=';
                char += data[i].hanzi_pic_id;
                char += '"><img src="';
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
        url = 'stroke_ajax_search?q=' + q + '&order=' + order + '&page_num=' + prev +'&page_size=' + page_size;
        str += '<li class="stroke_page" data-url="' + url + '">上一页</li>';
    }

    str += '<li>' + page_num + '页/' + pages + '页</li>';

    if(page_num == pages)
    {
        str += '<li>下一页</li>';
    }
    else
    {
        url = 'stroke_ajax_search?q=' + q + '&order=' + order + '&page_num=' + next +'&page_size=' + page_size;
        //str += '<li class="stroke_page" data-url="' + url + '"><a>下一页</a></li>';
        str += '<li class="stroke_page" data-url="' + url + '">下一页</li>';
    }

    $('.pagination').append(str);  

    //让隐藏的左面板显示出来
    $(".con-left").show();
}



//渲染部件笔画检字法结果集的函数
function render_variant_result(data)
{
    //首先清空结果面板
    $('.dict-result-lists').html('');


    //对json数据进行遍历
    len = data.length;

    for (var i=0;i<len;i++)
    {
        var char = "";
        if(data[i].source == 2)//如果是台湾异体字
        {
            char += '<li class="dict-result-item">';
            char += '<h3 class="dict-title">《台湾异体字字典》</h3>';

            len2 = data[i].content.length;
            var content = data[i].content;
            for (var j=0;j<len2;j++)
            {
                //正字元素
                if(content[j].type == 'char')
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/hanzi/variant_detail?source=2&type=char&text=';
                    char += content[j].stdchar;
                    char += '">[<span>';
                    char += content[j].stdchar;
                    char += '</span>]</a></p>';
                }
                else
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/hanzi/variant_detail?source=2&type=pic&text=';
                    char += content[j].stdchar;
                    char += '">[<span><img src="';
                    char += content[j].pic_url;
                    char += '"></span>]</a></p>';
                   
                }
                //开始渲染异体字元素
                char += '<div class="hanzi-variants">';
                len3 = content[j].variant.length
                var variant = content[j].variant;
                for (var k=0;k<len3;k++)
                {
                    if(variant[k].type == 'char')
                    {
                        char += '<a target="_blank" href="/hanzi/variant_detail?source=2&type=char&text=';
                        char += variant[k].text;
                        char += '"><span class="normal">';
                        char += variant[k].text;
                        char += '</span></a>';
                    }
                    else
                    {
                        char += '<a target="_blank" href="/hanzi/variant_detail?source=2&type=pic&text=';
                        char += variant[k].text;                                    
                        char += '"><span><img src="';
                        char += variant[k].pic_url;
                        char += '"></span></a>';
                          
                    }
                }

                char += '</div>';
                char += '</li>';
            }
        }
        else if(data[i].source == 4)   //如果是高丽异体字
        {
            char += '<li class="dict-result-item">';
            char += '<h3 class="dict-title">《高丽异体字字典》</h3>';

            len2 = data[i].content.length;
            var content = data[i].content;
            for (var j=0;j<len2;j++)
            {
                //正字元素
                if(content[j].type == 'char')
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/hanzi/variant_detail?source=4&type=char&text=';
                    char += content[j].stdchar;
                    char += '">[<span>';
                    char += content[j].stdchar;
                    char += '</span>]</a></p>';
                }
                else
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/hanzi/variant_detail?source=4&type=pic&text=';
                    char += content[j].stdchar;
                    char += '">[<span><img src="';
                    char += content[j].pic_url;
                    char += '"></span>]</a></p>';
                }
                //开始渲染异体字元素
                char += '<div class="hanzi-variants">';
                len3 = content[j].variant.length
                var variant = content[j].variant;
                for (var k=0;k<len3;k++)
                {
                    if(variant[k].type == 'char')
                    {
                        char += '<a target="_blank" href="/hanzi/variant_detail?source=4&type=char&text=';
                        char += variant[k].text;
                        char += '"><span class="normal">';
                        char += variant[k].text;
                        char += '</span></a>';
                    }
                    else
                    {
                        char += '<a target="_blank" href="/hanzi/variant_detail?source=4&type=pic&text=';
                        char += variant[k].text;
                        char += '"><span><img src="';
                        char += variant[k].pic_url;
                        char += '"></span></a>';
                    }
                }

                char += '</div>';
                char += '</li>';
            }
        }

        $('.dict-result-lists').append(char);
    }

    for (var i=0;i<len;i++)
    {
        var char = "";
        if(data[i].source == 3)   //如果是汉字大字典
        {
            char += '<li class="dict-result-item">';
            char += '<h3 class="dict-title">《汉语大字典》</h3>';
            char += '<div class="desc"><a target="_blank" href="#">';
            char += data[i].content;
            char += '</a></div>';
        }
        else if(data[i].source == 5)   //如果是敦煌俗字典
        {
            char += '<li class="dict-result-item">';
            char += '<h3 class="dict-title">《敦煌俗字典》</h3>';
            char += '<div class="desc"><a target="_blank" href="#">';
            char += data[i].content;
            char += '</a></div>';
        }
        $('.dict-result-lists').append(char);
    }

    $('.no-result').hide();
    $('.dict-content').show();

}









//点击部首时的响应函数
function clickRadical(redical)
{
    //搞清楚当前那个字典有效
    var dict = $(".dict-tabs .active").html();
    var source = 0;
    if(dict == '台湾异体字字典')
        source = 2;
    else if(dict == '高丽异体字字典')
        source = 4;
    else if(dict == '汉语大字典')
        source = 3;
    else if(dict == '敦煌俗字典')
        source = 5;

    $.get(
      "dicts_search",
      {"q":redical,"source":source,"page_num":1,"page_size":200 },
      function (data)
      {
          //渲染数据
          render_dicts_result(data);
      });
}



function render_dicts_result(data)
{
  // b = {}
  // b['q'] = q
  // b['source'] = source
  // b['page_num'] = page_num  
  // b['pages'] = pages
  // b['page_size'] = page_size
  // b['result'] = a



    var title=new Array("零画","一画","二画","三画","四画","五画","六画","七画","八画","九画","十画",
                       "十一画","十二画","十三画","十四画","十五画","十六画","十七画","十八画","十九画","二十画",
                       "二十一画","二十二画","二十三画","二十四画","二十五画","二十六画","二十七画","二十八画","二十九画","三十画",
                       "三十一画","三十二画","三十三画","三十四画","三十五画","三十六画","三十七画","三十八画","三十九画","四十画"
                       );

    //清空首部检字结果区
    $(".strokes-lists").empty();
    var flag = -1;
    var data = data.result;
    var len = data.length;

    for(var i=0;i<len;i++)
    {
        if(flag != data[i].remain_strokes_num)
        {
            flag = data[i].remain_strokes_num;

            var str = '<li class="strokes-item"><span class="num">' + title[flag] + '</span>';
            str += '<div class="strokes-item-bd clearfix">';

            for(var j=i;j<len;j++)
            {
                if(data[j].hanzi_char != '')
                {
                    str += '<span class="hanzi-item">';
                    str += data[j].hanzi_char;
                    str += '</span>';
                }
                else
                {
                    str += '<span class="hanzi-item">';
                    str += '<img src="' + data[j].pic_url + '" alt="' + data[j].hanzi_pic_id + '"></span>';
                }

                //如果下一个字的剩余笔划数有变化，就跳出
                if( (j+1<len) && (flag != data[j+1].remain_strokes_num) )
                {
                    i = j;
                    break;
                }
            }
            str += '</div></li>';
            $(".strokes-lists").append(str);
        }
    }
}

