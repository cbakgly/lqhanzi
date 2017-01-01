/**
 * Created by ZhouYi on 2017/01/01.

 //TODOs:
 1. 翻页功能，等前端设计好按钮样式大小位置
 2. 任务包编号等APIs
 */
function AjaxHelper() {
    this.ajax = function (url, type, dataType, data, callback) {
        $.ajax({
            url: url,
            method: type,
            cache: false,
            dataType: dataType,
            data: data,
            tranditional: true,
            success: callback,
            error: function (xhr, status, err) {
                console.log(err);
            }
        })
    }
}

AjaxHelper.prototype.get = function(url, data, callback) {
    this.ajax(url, 'GET', 'json', data, callback)
}

var ajaxHelper = new AjaxHelper();

var app = new Vue({
    el: '#task-package-complete',
    data: {
	    tasks: [],
	    result: [],
        param: {'status': 1},
        url: '/api/v1/task_packages/',
        map_type: {0: '录入', 1: '拆字', 2: '去重', 3: '互助'},
        map_stage: {0: '初次', 1: '回查', 2: '审查'},
    },
    created: function() {
        var vm = this
        callback = function(data) {
            vm.result = data.results
        }
        ajaxHelper.get(vm.url, {'status': 1}, callback)
    },
    watch: {
        tasks: function() {
            // 定义vm变量，让它指向this,this是当前的Vue实例
            var vm = this
            callback = function(data) {
                vm.result = data.results
            }
            if (vm.tasks.length === 0) {
                ajaxHelper.get(vm.url, {'status': 1}, callback)
            } else {
                vm.param.business_type_in = vm.tasks.join(",")
                ajaxHelper.get(vm.url, vm.param, callback)
            }
        }
    }
});