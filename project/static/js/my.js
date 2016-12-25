/**
 * Created by zf on 2016/12/22.
 */
$(function () {
    //bootstrap WYSIHTML5 - text editor
    $(".pad .textarea").wysihtml5();
    //Date range picker with time picker
    $('#reservationtime').daterangepicker({timePicker: true, timePickerIncrement: 30, format: 'MM/DD/YYYY h:mm A'});
});
//更多搜索
$(function () {
    var $choices = $('.z-ser .col:gt(2)');
    $choices.hide();
    var $toggleBtn = $('.btns .more');
    var flag=true;
    $toggleBtn.click(function() {
        if(flag){
            $choices.slideDown(600);
            $(this).find('span').text('收起搜索').siblings('i').removeClass('icon-down-arrow').addClass('icon-up-arrow');
            flag = false;
        }else  {
            $choices.slideUp(600);
            $(this).find('span').text('更多搜索').siblings('i').removeClass('icon-up-arrow').addClass('icon-down-arrow');
            flag = true;
        }
    });
});
//点击修改弹出层
$(function () {
    //展示层
    function showLayer(id) {
        var layer = $('#' + id),layerwrap = layer.find('.hw-layer-wrap');
        layer.fadeIn();
        //屏幕居中
        layerwrap.css({
            'margin-top': -layerwrap.outerHeight() / 2
        });
    }
    //隐藏层
    function hideLayer() {
        $('.hw-overlay').fadeOut();
    }
    $('.hwLayer-ok,.hwLayer-cancel,.hwLayer-close').on('click', function() {
        hideLayer();
    });
    //触发弹出层
    $('.show-layer').on('click', function() {
        var layerid = $(this).data('show-layer');
        showLayer(layerid);
    });
    //点击或者触控弹出层外的半透明遮罩层，关闭弹出层
    $('.hw-overlay').on('click', function(event) {
        if (event.target == this) {
            hideLayer();
        }
    });

    //按ESC键关闭弹出层
    $(document).keyup(function(event) {
        if (event.keyCode == 27) {
            hideLayer();
        }
    });
});
