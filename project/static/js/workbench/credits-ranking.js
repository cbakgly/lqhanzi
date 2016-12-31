/**
 * Created by wangwei on 16-12-20.
 */
var credits_arr = new Array("总积分", "拆字积分", "去重积分", "录入积分", "互助积分")
var indexOf = function (value) {
    for (var i = 0, vlen = credits_arr.length; i < vlen; i++) {
        if (credits_arr[i] == value) {
            return i + 1;
        }
    }
}
var vm = new Vue({
    delimiters: ["#[", "]"],
    el: '#app',
    data: {
        username: "",
        selected: 0,
        cdata: [],
        //pagination: {},
        //page_size: 10,
        //current_page: 1,
        //first_entry: true,
        offset: 0,
        mycredit: 0,
        myrank: 1,
    },
    methods: {
        gen_url: function () {

            var base_url = "/api/workbench/credits/?"
            if (vm.username == "") {
                var username = document.getElementsByClassName("hidden-xs")[0].innerHTML
                vm.username = vm.trim(username)
            }
            base_url += "&user__username=" + vm.username
            base_url += "&sort=" + vm.selected
            return base_url
        },
        get_offset: function () {
            var url = this.gen_url()
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        if (indexof(data[i].sort) == vm.selected) {
                            vm.offset = data[i].rank - 2
                            break
                        }
                    }
                    //vm.pagination = data.pagination
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })

        },
        load_pages: function () {
            //this.current_page = page_num
            vm.get_offset()
            url = this.gen_url()
            var url = url + "&offset=" + vm.offset
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    vm.cdata = data
                    //vm.pagination = data.pagination
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        },
        get_login_user: function () {
            var base_url = "/api/workbench/credits/certain_user_credits/"

            //console.log(username)
            //var url = base_url+"&user__username="+username+"&sort=1"
            $.ajax({
                url: base_url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    vm.cdata = data
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].sort == "总积分") {
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
        goto_pages: function (evt) {
            this.load_pages(evt.target.value)
        },

    }
});
vm.get_login_user();

