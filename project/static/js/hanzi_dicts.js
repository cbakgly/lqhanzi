

$(document).ready(function()
{
    //字典页面中，点击上一个、下一页时的换页函数
    $(document).on('click', '.stroke_page', function()
    {
        //var url = $(this).find("a").attr("href");
        var url = $(this).attr("data-url");
        //显示载入动画
        //$(".loading").show();
        
        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_dicts_result(data);

              //关闭载入动画
              //$(".loading").hide();
          });
    });


    //字典页面中，点击跳页按钮时的响应函数
    $("#dict_page_btn").click( function ()
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

        $.get(
          url,
          function (data)
          {
              //渲染数据
              render_dicts_result(data);
          });
    });


});





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
    var q = data.q;
    var page_num = data.page_num;
    var pages = data.pages;
    var page_size = data.page_size;
    var source = data.source;

    var title=new Array("零画","一画","二画","三画","四画","五画","六画","七画","八画","九画","十画",
                       "十一画","十二画","十三画","十四画","十五画","十六画","十七画","十八画","十九画","二十画",
                       "二十一画","二十二画","二十三画","二十四画","二十五画","二十六画","二十七画","二十八画","二十九画","三十画",
                       "三十一画","三十二画","三十三画","三十四画","三十五画","三十六画","三十七画","三十八画","三十九画","四十画"
                       );

    //清空首部检字结果区
    $(".strokes-lists").empty();
    $('.pagination').empty();


    var flag = -1;

    //查询到的字集和字的个数
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
        url = 'dicts_search?q=' + q + '&source=' + source + '&page_num=' + prev +'&page_size=' + page_size;
        str += '<li class="stroke_page" data-url="' + url + '">上一页</li>';
    }

    str += '<li>' + page_num + '页/' + pages + '页</li>';

    if(page_num == pages)
    {
        str += '<li>下一页</li>';
    }
    else
    {
        url = 'dicts_search?q=' + q + '&source=' + source + '&page_num=' + next +'&page_size=' + page_size;
        //str += '<li class="stroke_page" data-url="' + url + '"><a>下一页</a></li>';
        str += '<li class="stroke_page" data-url="' + url + '">下一页</li>';
    }

    $('.pagination').append(str);  

    //给翻页按纽增加data-url属性， 以便单击时利用
    var new_url = 'dicts_search?q=' + q + '&source=' + source + '&page_size=' + page_size;
    $('#dict_page_btn').attr("data-url",new_url); 
}

