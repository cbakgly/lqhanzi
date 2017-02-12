// user dropdownmenu
$(function () {
    $(".nav-tab .dropdown").mouseenter(function () {
        if (!$(this).children(".dropdown-menu").is(":animated")) {
            $(this).children(".dropdown-menu").fadeIn(600);
        }
    });
    $(".nav-tab .dropdown").mouseleave(function () {
        $(this).children(".dropdown-menu").fadeOut(600);
    });
});

//tab切换
$(function () {
    $(".main-sidebar .tab-nav-custom li").click(function () {
        var $this = $(this),
            index = $this.index();
        $this.addClass("active").siblings("li").removeClass("active");
        $(".main-sidebar .tab-con .tab-panel").eq(index).addClass("showing").siblings(".tab-panel").removeClass("showing");
    });
    $(".dict-tabs-nav li").click(function () {
        var $this = $(this),
            index = $this.index();
        $this.addClass("active").siblings("li").removeClass("active");
        $(".content-wrapper .tab-panel").eq(index).addClass("showing").siblings(".tab-panel").removeClass("showing");
    });
});

//tab切换
$(function () {
    $(".toggler").click(function () {
        $(".popup").hide("normal");
    })
});
