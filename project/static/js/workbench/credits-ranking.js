/**
 * Created by wangwei on 16-12-20.
 */
var vm = new Vue({
    delimiters: ["#[", "]"],
    el: '#app',
    data: {
        username: "",
        selected: 0,
        cdata: [],
        pagination: {},
        page_size: 10,
        current_page: 1,
        first_entry: true,
        mycredit:0,
        myrank:1,
    },
    methods: {
        gen_url: function(){
            var base_url = "/api/workbench/credits/?"
            if ((vm.username != "") && (vm.selected==0))
                base_url += "&user__username="+vm.username
            else if ((vm.selected != 0) && (vm.username == ""))
                base_url += "&sort="+vm.selected
            else if ((vm.selected != 0) && (vm.username != ""))
                base_url += "&user__username="+vm.username+ "&sort="+ vm.selected
            base_url = base_url + '&page_size=' + vm.page_size + "&page=" + this.current_page
            return base_url
        },
        load_pages: function(page_num = 1) {
            this.current_page = page_num
            var url = this.gen_url()
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    vm.cdata = data.models
                    console.log(vm.cdata[0].credit)
                    vm.pagination = data.pagination
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        },
        get_login_user:function(){
            var base_url = "/api/workbench/credits/certain_user_credits/"
            //var username = document.getElementsByClassName("hidden-xs")[0].innerHTML
            //username = vm.trim(username)
            //console.log(username)
            //var url = base_url+"&user__username="+username+"&sort=1"
            $.ajax({
                url: base_url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    vm.cdata = data
                    for (var i = 0; i<data.length; i++){
                        if (data[i].sort == "总积分"){
                            vm.mycredit = data[i].credit
                            vm.myrank = data[i].rank
                            break
                        }
                    }
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        },
        goto_pages: function(evt) {
            this.load_pages(evt.target.value)
        },

    }
});
vm.get_login_user();

