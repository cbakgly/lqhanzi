jQuery.CateNav=function(elem1,elem2){
    var currObj;
    var offsetTop=0;
    var h2List=new Array(),h3List=new Array();
    //添加锚点
    var addPoint=function(){
        var i1=i2=0;
        $(elem2).find('h2').each(function(){
            $(this).prepend('<a name="'+h2List[i1]+'"></a>');
            i1++;
        });
        $(elem2).find('h3').each(function(){
            $(this).prepend('<a name="'+h3List[i2]+'"></a>');
            i2++;
        });
    };
    //点击锚点，跳转制定位置
    var clickPoint=function(){
        $(elem2+' a').click(function(e){
            e.preventDefault();
            $(elem2+' li').removeClass('active');
            $(this).parent('li').addClass('active');
            currObj=$("[name='"+$(this).attr('href').replace(/#/,'')+"']");
            offsetTop=currObj.offset().top;
            //console.log(currObj.offset().top);  //
            $('html,body').animate({
                scrollTop:offsetTop
            },600,'swing');
        });
    };
    //屏幕滚动，显示并选中锚点
    var scrollWin=function(){
        var windowTop=0;
        $(window).scroll(function(){
            windowTop=$(window).scrollTop();
            $(elem2+' a').each(function(){
                currObj=$("[name='"+$(this).attr('href').replace(/#/,'')+"']");
                //console.log(currObj); console.log(currObj.offset());
                offsetTop=currObj.offset().top;
                //console.log("windowTop="+windowTop);
                if(windowTop>=offsetTop){
                    $(elem2+' li').removeClass('active');
                    $(this).parent('li').addClass('active');
                    return;
                }
            });
        });
    };
    var init=function(){
        addPoint();
        clickPoint();
        scrollWin();
    }
    init();
}
//返回顶部
$(function(){
    $(window).scroll(function(){
        var t = $(window).scrollTop();
        if(t >= 100){
            $(".gotop").fadeIn(500);
        }else{
            $(".gotop").fadeOut(1000);
        }
    });
    $(".gotop").click(function(){
        $("html,body").animate({
            "scrollTop":0
        },400);
    });
})