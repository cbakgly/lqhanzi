/**
 * Created by ZhouYi on 2016/12/24.
 */
var creditsSort = new Vue({
  delimiters: ["#[", "]"],
  el: '#credits-sort',
  data: {
    result: '',
    sort: 1,
    options: [
      {text: '总积分', value: 1},
      {text: '拆字积分', value: 2},
      {text: '去重积分', value: 3},
      {text: '录入积分', value: 4},
      {text: '互助积分', value: 5},
    ]
  },
  watch: {
    sort: function(category) {
      this.getData(this.sort)
    }
  },
  methods: {
    getData: function(sortNum) {
        var app = this
        axios.get('http://127.0.0.1:8000/api/v1/workbench/credits?sort=' + sortNum)
          .then(function (response) {
            app.result = response.data.results;
          })
          .catch(function (error) {
            console.log(err);
          })
  }
}
});
