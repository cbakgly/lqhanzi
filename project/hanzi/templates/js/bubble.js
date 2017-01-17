
$(function() {
    $.fn.bubbletips = function(options) {
        var defaults = {
            position : "t",			//箭头指向上(t)、箭头指向下(b)、箭头指向左(l)、箭头指向右(r)
            value : 15				//小箭头偏离左边和上边的位置

        };
        var options = $.extend(defaults,options);

        //var bid = parseInt(Math.random()*100000);
        var $this = $(this);
        //$("body").prepend('<div class="bubble" id="btip'+bid+'"></div>');
        var $btip = $("#btip");
        //var $btipClose = $("#btipc"+bid);
        console.log($btip);

        var offset,h ,w ;
        $this.on("mousemove",function(){
            clearInterval(window.timer);
            offset = $(this).offset();
            h = $(this).height();
            w = $(this).width();
            window.timer = window.setTimeout(function (){
                $btip.css({ "visibility":"visible","left":offset.left-w/2-options.value-20  ,  "top":offset.top-h-$btip.height()+23}).show();
            }, 1000);
        });
        $this.on("mouseout",function(){

            window.timer = window.setTimeout(function (){
                $btip.hide();
            }, 1000);
        });
    }
});
