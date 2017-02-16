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
var appvm = new Vue({
    delimiters: ["#[", "]"],
    el: '#app',
    data: {
        searchname: "",
        selected: 1,
        cdata: [],
        offset: 0,
        mycredit: 0,
        myrank: 1,
        credits_arr :{0:"总积分",1:"拆字积分",5:"去重积分",2:"录入积分",3:"图书校对",4:"论文下载"}
    },
    watch:{

    },
    methods: {
        load_pages: function () {
            var url = "/api/v1/credits/searchcredit/";
            $.ajax({
                url: url,
                method:'GET',
                enctype : "multipart/form-data",
                dataType: 'json',
                data:{
                    'select_sort':this.selected,
                    'search_name':this.searchname
                },
                cache: false,
                success: function (data) {
                    appvm.cdata = data;
                },
                error: function (xhr, status, err) {
                    console.log('error');
                }
            })
        },
        get_login_user: function () {
            var base_url = "/api/v1/credits/certain_user_credits/";
            $.ajax({
                url: base_url,
                dataType: 'json',
                cache: false,
                success: function (data) {
                    console.log(data);
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

