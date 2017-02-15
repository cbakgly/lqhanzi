/**
 * Created by wangwei on 16-12-20.
 */


var indexOf = function (value) {
    for (var i = 0, vlen = credits_arr.length; i < vlen; i++) {
        if (credits_arr[i] == value) {
            return i + 1;
        }
    }
}
//var username = "ww";
var appvm = new Vue({
    delimiters: ["#[", "]"],
    el: '#app',
    data: {
        username: "",
        selected: 1,
        cdata: [],
        //pagination: {},
        //page_size: 10,
        //current_page: 1,
        //first_entry: true,
        offset: 0,
        mycredit: 0,
        myrank: 1,
        credits_arr :{0:"总积分",1:"拆字积分",5:"去重积分",2:"录入积分",3:"图书校对",4:"论文下载"}
    },
    watch:{

    },
    methods: {
        trim: function(stri) {
            return stri.replace(/(^\s*)|(\s*$)/g, ""); },
        gen_url: function () {

            var username = document.getElementsByClassName("hidden-xs")[0].innerHTML;
            username = appvm.trim(username);

            base_url += "&user__username=" + username
            //base_url +=
            return base_url
        },
        /*get_offset: function () {
            var url = this.gen_url()
            var app = this
            axios({
                method:"get",
                url: url,
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken'
            })
                .then(function(data){
                    for (var i = 0; i < data.length; i++) {
                        if (indexof(data[i].sort) == app.selected) {
                            app.offset = data[i].rank - 2
                            break
                        }
                    }
                }).catch(function(error){
                    console.log(error);
            })
        },*/
        load_pages: function () {
            //this.current_page = page_num
            //appvm.get_offset()
            var url = "/api/v1/credits/?sort=" + appvm.selected;
            //url = url + "&offset=" + appvm.offset
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    appvm.cdata = data;
                    //appvm.pagination = data.pagination
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        },
        get_login_user: function () {
            var base_url = "/api/v1/credits/certain_user_credits/";

            //console.log(username)
            //var url = base_url+"&user__username="+username+"&sort=1"
            $.ajax({
                url: base_url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    appvm.cdata = data;
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].sort == 0) {
                            appvm.mycredit = data[i].credit;
                            appvm.myrank = data[i].rank;
                            break;
                        }
                    }
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        }
    }
});
appvm.get_login_user();

