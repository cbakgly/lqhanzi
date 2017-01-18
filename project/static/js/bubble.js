
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
            console.log(h);
            console.log(offset.left);
            w = $(this).width();
            console.log(w);

            $btip.css({ "left":offset.left-w/2-options.value-23  ,  "top":offset.top-h-$btip.height()+23}).show();

        });
        $this.on("mouseout",function(){
            window.timer = window.setInterval(function (){
                $btip.hide();
            }, 1000);
        });

/*        $btip.on("mousemove",function(){
            clearInterval(window.timer);
            $btip.show();
        });
        $btip.on("mouseout",function(){
            $btip.hide();
        });*/

    }
});
