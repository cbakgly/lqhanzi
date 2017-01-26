
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

    $(document).on('mouseover', '.hanzi-item', function()
    {
        // offset = $(this).offset();
        // w1 = $(this).width();
        // h1 = $(this).height();

        // w2 = $('#btip').width();
        // h2 = $('#btip').height();
        // 
        var options = $.extend({position:"t", value:15},{position:"b",value:35});

        offset = $(this).offset();
        h = $(this).height();
        w = $(this).width();
     
        $("#btip").css({ "visibility":"visible","left":offset.left-w/2-options.value-23,"top":offset.top-h-$("#btip").height()+40});
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

    //点击部件笔画搜索按钮时的响应函数
    $("#strock_search_btn").click( function ()
    {
        //显示载入动画
        //$(".loading").show();
        //var url = $(this).find("a").attr("href");
        var order = $('.search-bottom input[name="r"]:checked').val();  
        $.get(
          "stroke_ajax_search",
          {"q":$(".ser-input").val(),"order":order,"page_num":1,"page_size":100,},
          function (data)
          {
              //渲染数据
              render_stroke_result(data);

              //关闭载入动画
              //$(".loading").hide();
          });
    });



    //部件笔画检字法结果页面中，点击上一个、下一页时的换页函数
    $(document).on('click', '.stroke_page', function()
    {
        var url = $(this).attr("data-url");
    
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
        var regex = /^[1-9]+$/;

        if(new_page.match(regex) == null)
        {
            alert("页码格式不对");
            return;
        }

        var url = $(this).attr("data-url");
        url += '&page_num=' + new_page;

        alert(url);return;
        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_stroke_result(data);
          });
    });



});





//渲染部件笔画检字法结果集的函数
function render_stroke_result(data)
{
    //查询到的字对象的集合
    var q = data.q;
    var page_num = data.page_num;
    var pages = data.pages;
    var page_size = data.page_size;
    var order = data.order;
    var data = data.result;

    //查询到的字对象的个数
    len = data.length;

    //显示取到的条目数
    $("#stroke_result_count").html(len);   
    $('.hanzi-wrap').html('');
    $('.pagination').empty();

    for (var i=0;i<len;i++)
    {

        var char = "";
        if(data[i].source == 1)//如果是unicode
        {
            var data_value = 'source=unicode;code='+data[i].remark +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

            char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=1&type=char&text=';
            char += data[i].hanzi_char;
            char += '" data-value="';
            char += data_value + '">';
            char += data[i].hanzi_char;
            char += '</a></li>';
        }
        else if(data[i].source == 2)//如果是台湾异体字
        {
            var data_value = 'source=台湾异体字;code='+data[i].seq_id +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

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
                // char += '"><img src="';

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
                var data_value = 'source=汉字大字典;code='+data[i].hanzi_char +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=char&text=';
                char += data[i].hanzi_char;

                char += '" data-value="';
                char += data_value + '">';

                char += data[i].hanzi_char; 
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=汉字大字典;code='+data[i].hanzi_pic_id +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=3&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="'; 
                // char += '"><img src="';

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
                var data_value = 'source=高丽异体字;code='+data[i].hanzi_char +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=char&text=';
                char += data[i].hanzi_char;

                char += '" data-value="';
                char += data_value + '">';
                // char += '">';

                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=高丽异体字;code='+data[i].hanzi_pic_id +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=4&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="'; 
                // char += '"><img src="';

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
                var data_value = 'source=敦煌俗字典;code='+data[i].hanzi_char +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=char&text=';
                char += data[i].hanzi_char;

                char += '" data-value="';
                char += data_value + '">';                
                // char += '">';
                
                char += data[i].hanzi_char;
                char += '</a></li>';
            }
            else
            {
                var data_value = 'source=敦煌俗字典;code='+data[i].hanzi_pic_id +';similar_parts='+data[i].similar_parts+';split_serial='+data[i].mix_split;

                char = '<li><a class="hanzi-item" target="_blank" href="/hanzi/variant_detail?source=5&type=pic&text=';
                char += data[i].hanzi_pic_id;

                char += '" data-value="';
                char += data_value + '"><img src="';
                // char += '"><img src="';

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


    //给翻页按纽增加data-url属性， 以便单击时利用
    var new_url = 'stroke_ajax_search?q=' + q + '&order=' + order + '&page_size=' + page_size;
    $('#stroke_page_btn').attr("data-url",new_url); 


    //让隐藏的左面板显示出来
    //$(".con-left").show();
    $(".con-left").fadeIn(600);
    $(".con-right").addClass("con-right-new");
}

