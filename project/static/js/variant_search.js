
$(document).ready(function()
{
    var ext = $("#ext").text();
    if(ext !='')
    {
        $("#ext").text('');

        $("#variant_searchinput").val(ext);
        $("#current_variant").text(ext);

        $(".tip").text("正在查询中...");

        //触发按纽的点击事件
        //$('#variant_search_btn').click();
        //$(".loading").show();
        
        $.get(
          "variant_search",
          {"q":$(".ser-input").val()},
          function (data)
          {
              //渲染数据
              render_variant_result(data);
              addKeywordPoint();
          });
        //$(".loading").hide();
    }

    //给输入框添加回车键相应
    $('#variant_searchinput').keydown(function(e){
    if(e.keyCode==13){
       $('#variant_search_btn').click();
    }
    });

    //点击异体字搜索按钮时的响应函数
    $("#variant_search_btn").click( function ()
    {
        $("#current_variant").text($(".ser-input").val());
        $.get(
          "variant_search",
          {"q":$(".ser-input").val()},
          function (data)
          {
              //渲染数据
              render_variant_result(data);
              addKeywordPoint();
          });
    });

});


function SetSpanBkColor(variant_type)
{
    if(variant_type==1)
        return '"><span class="variantColor1">';
    else if(variant_type==2)
        return '"><span class="variantColor2">';
    else if(variant_type==3)
        return '"><span class="variantColor3">';
    else if(variant_type==4)
        return '"><span class="variantColor4">';
    else return '"><span>';
}


//在检索关键字下边添加小红点
function addKeywordPoint()
{
    $(".dict-result-lists a").each(function()
    {
        if( $(this).attr("href").indexOf( $("#current_variant").text() )!=-1 )
            $(this).find("span").addClass("keyword");
    });
}


//渲染异体字检字法结果集的函数
function render_variant_result(data)
{
    if(data=="none")
    {
        $(".tip").text("没有检索到数据！");
        return;
    }

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
                    char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?source=2&type=char&text=';
                    char += content[j].stdchar;
                    char += '">[<span>';
                    char += content[j].stdchar;
                    char += '</span>]</a></p>';
                }
                else
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?source=2&type=pic&text=';
                    char += content[j].stdchar;
                    char += '">[<span><img src="';
                    char += content[j].pic_url;
                    char += '"></span>]</a></p>';
                   
                }

                //异体字
                char += '<div class="hanzi-variants">';
                len3 = content[j].variant.length;
                var variant = content[j].variant;
                for (var k=0;k<len3;k++)
                {
                    if(variant[k].type == 'char')
                    {
                        char += '<a target="_blank" href="/variant_detail?source=2&type=char&text=';
                        char += variant[k].text;
                        char += SetSpanBkColor(variant[k].variant_type)
                        //char += '"><span class="normal">';
                        char += variant[k].text;
                        char += '</span></a>';
                    }
                    else
                    {
                        char += '<a target="_blank" href="/variant_detail?source=2&type=pic&text=';
                        char += variant[k].text; 
                        char += SetSpanBkColor(variant[k].variant_type)
                        //char += '"><span>';
                        char += '<img src="';
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
                    char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?source=4&type=char&text=';
                    char += content[j].stdchar;
                    char += '">[<span>';
                    char += content[j].stdchar;
                    char += '</span>]</a></p>';
                }
                else
                {
                    char += '<p class="hanzi-normal"><a target="_blank" href="/variant_detail?source=4&type=pic&text=';
                    char += content[j].stdchar;
                    char += '">[<span><img src="';
                    char += content[j].pic_url;
                    char += '"></span>]</a></p>';
                }
                //异体字
                char += '<div class="hanzi-variants">';
                len3 = content[j].variant.length
                var variant = content[j].variant;
                for (var k=0;k<len3;k++)
                {
                    if(variant[k].type == 'char')
                    {
                        char += '<a target="_blank" href="/variant_detail?source=4&type=char&text=';
                        char += variant[k].text;
                        char += SetSpanBkColor(variant[k].variant_type)
                        //char += '"><span class="normal">';
                        char += variant[k].text;
                        char += '</span></a>';
                    }
                    else
                    {
                        char += '<a target="_blank" href="/variant_detail?source=4&type=pic&text=';
                        char += variant[k].text;
                        char += SetSpanBkColor(variant[k].variant_type)
                        //char += '"><span>';
                        char += '<img src="';
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
            char += '<div class="hanzi-variants2">';

            count = data[i].content.length;
            variant = data[i].content;
            for(var k=0;k<count;k++)
            {
                if(variant[k].type == 'char')
                {
                    char += '<a target="_blank" href="/variant_detail?source=3&type=char&text=';
                    char += variant[k].text;
                    char += '"><span class="normal">';
                    char += variant[k].text;
                    char += '</span></a>';
                }
                else
                {
                    char += '<a target="_blank" href="/variant_detail?source=3&type=pic&text=';
                    char += variant[k].text;
                    char += '"><span><img src="';
                    char += variant[k].pic_url;
                    char += '"></span></a>';
                }
            }
            char += '</div>';

        }
        else if(data[i].source == 5)   //如果是敦煌俗字典
        {
            char += '<li class="dict-result-item">';
            char += '<h3 class="dict-title">《敦煌俗字典》</h3>';
            char += '<div class="hanzi-variants2">';

            count = data[i].content.length;
            variant = data[i].content;
            for(var k=0;k<count;k++)
            {
                if(variant[k].type == 'char')
                {
                    char += '<a target="_blank" href="/variant_detail?source=5&type=char&text=';
                    char += variant[k].text;
                    char += '"><span class="normal">';
                    char += variant[k].text;
                    char += '</span></a>';
                }
                else
                {
                    char += '<a target="_blank" href="/variant_detail?source=5&type=pic&text=';
                    char += variant[k].text;
                    char += '"><span><img src="';
                    char += variant[k].pic_url;
                    char += '"></span></a>';
                }
            }
            char += '</div>';
        }
        $('.dict-result-lists').append(char);
    }

    $('.no-result').hide();
    $('.dict-results').show();

}


