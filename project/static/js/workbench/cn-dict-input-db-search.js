/**
 * Created by ZhouYi on 2017/01/05.
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

AjaxHelper.prototype.get = function (url, data, callback) {
    this.ajax(url, 'GET', 'json', data, callback)
}

var ajaxHelper = new AjaxHelper();

var hanzi_input = new Vue({
    delimiters: ["#[", "]]"],
    el: "#search",
    data: {
        urls: search_url,
        params: {
            'page_num': '',
            'stage': 0,

            'hanzi_char_draft': '',
            'hanzi_pic_id_draft': '',
            'variant_type_draft': '请选择',
            'std_hanzi_draft': '',
            'notes_draft': '',

            'is_draft_equals_review': 0,
            'is_review_equals_final': 0,
            'is_checked': 0,
            'is_submitted': 0,
        },
        models: [],
        context: {},
        bool: [
            {text: '否', value: 0},
            {text: '是', value: 1},
        ],
        add_tail: {
            1: 'review',
            2: 'final'
        },
        options_stage: [
            {text: '初次', value: 0},
            {text: '回查', value: 1},
            {text: '审查', value: 2},
        ],
        options_type: [
            {text: '纯正字', value: 0},
            {text: '狭义异体字', value: 1},
            {text: '广义且正字', value: 2},
            {text: '广义异体字', value: 3},
            {text: '狭义且正字', value: 4},
            {text: '特定异体字', value: 5},
            {text: '特定且正字', value: 6},
            {text: '误刻误印', value: 7},
            {text: '其他不入库类型', value: 8},
            {text: '其他入库类型', value: 9}
        ],
        titles: [
            {text: '序号', show: true},
            {text: '册', show: false},
            {text: '页码', show: true},
            {text: '序号/初次', show: true},
            {text: '文字/初次', show: true},
            {text: '图片字/初次', show: true},
            {text: '正异类型/初次', show: true},
            {text: '通行字/初次', show: true},
            {text: '注释信息/初次', show: true},
            {text: '序号/回查', show: false},
            {text: '文字/回查', show: false},
            {text: '图片字/回查', show: false},
            {text: '正异类型/回查', show: false},
            {text: '通行字/回查', show: false},
            {text: '注释信息/回查', show: false},
            {text: '序号/审查', show: false},
            {text: '文字/审查', show: false},
            {text: '图片字/审查', show: false},
            {text: '正异类型/审查', show: false},
            {text: '通行字/审查', show: false},
            {text: '注释信息/审查', show: false},
            {text: '初次=回查', show: true},
            {text: '回查=审查', show: true},
            {text: '是否审核', show: true},
            {text: '是否入库', show: true},
            {text: '更新时段', show: true},
            {text: '操作', show: true}
        ]
    },
    created: function () {
        var vm = this;
        ajaxHelper.get(vm.urls, null, function (data) {
            vm.context = data.html_context;
            vm.models = data.models;
        })
    },
    methods: {
        searchResult: function () {
            var vm = this;

            for (keyname in vm.params) {
                if (vm.params[keyname] === '请选择' || vm.params[keyname] === '') {
                    delete vm.params[keyname]
                }
            }
            if ('stage' in vm.params && vm.params.stage > 0) {
                for (property in vm.params) {
                    if (property.slice(-5) === 'draft') {
                        new_name = property.slice(0, -5) + vm.add_tail[vm.params['stage']]
                        vm.params[new_name] = vm.params[property]
                        delete vm.params[property]
                    }
                }
            }
            delete vm.params['stage']
            ajaxHelper.get(vm.urls, vm.params, function (data) {
                vm.models = data.models;
                vm.context = data.html_context;
            })
        },
        clearAllResult: function () {
            for (var key in this.params) {
                this.params[key] = "";
            }
            $('#reservationtime').val("");
        },
        gotoPage: function (url) {
            var vm = this;
            ajaxHelper.get(url, null, function (data) {
                vm.models = data.models;
                vm.context = data.html_context;
            })
        },
        get_detail_url: function (item) {
            return '/workbench/task/input_page_detail/?pk=' + item.id;
        }
    }
});