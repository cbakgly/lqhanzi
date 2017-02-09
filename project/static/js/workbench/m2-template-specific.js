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
//汉大去重库，修改事件
$(function(){
    $(".z-table-responsive tbody tr td .modify").click(function() {
        str = $(this).text()=="修改"?"确定":"修改";
        $(this).text(str);   // 按钮被点击后，在“编辑”和“确定”之间切换
        $(this).parent().siblings("td:eq(2)").each(function() {  // 获取当前行的第3列单元格
            obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
            if(!obj_text.length){
                // 如果没有文本框，则在td添加文本框
                $(this).children('span').hide();
                $(this).append("<input type='text' value='"+$(this).children('span:nth-child(2)').text()+"'>");
            }else{
                // 如果已经存在文本框，则将其显示为文本框修改的值
                $(this).children('span').show();
                var val = $(this).children('input').val();
                $(this).children('input').remove();
                $(this).children('span:nth-child(2)').text(val);
                // $(this).remove('input');
            }
        });
    });
});
// 筛选：更多多选项
$(function(){
    var flag=true;
    $(".expand-ft .more").click(function(){
        if(flag){
            $(".expand-items").css({
                "height":"auto",
                "overflow":"auto"
            });
            $(this).find('span').text('收起').siblings('i').removeClass('icon-down-arrow').addClass('icon-up-arrow');
            flag = false;
        }else  {
            $(".expand-items").css({
                "height":"36px",
                "overflow":"hidden"
            });
            $(this).find('span').text('更多').siblings('i').removeClass('icon-up-arrow').addClass('icon-down-arrow');
            flag = true;
        }
    });
});