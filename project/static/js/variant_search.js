$(document).ready(function()
{
    //点击异体字搜索按钮时的响应函数
    $("#variant_search_btn").click( function ()
    {
        $.get(
          "variant_search",
          {"q":$(".ser-input").val()},
          function (data)
          {
              //渲染数据
              render_variant_result(data);
          });
    });

});


//渲染异体字检字法结果集的函数
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
    $('.dict-results').show();

}


