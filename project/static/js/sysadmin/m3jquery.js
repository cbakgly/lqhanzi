  $(function () {
    "use strict";
    //BAR CHART
    var bar = new Morris.Bar({
      element: 'bar-chart',
      resize: true,
      data: [
        {y: '初次未分配', a: 9704},
        {y: '初次进行中', a: 8704},
        {y: '回查未分配', a: 1222},
        {y: '回查进行中', a: 3456},
        {y: '审查未分配', a: 5000},
        {y: '审查进行中', a: 7456},
        {y: '审查已完成', a: 11456}
      ],
      barColors: ['#00a65a'],
      xkey: 'y',
      ykeys: ['a', 'b'],
      labels: ['CPU', 'DISK'],
      hideHover: 'auto'
    });

     var line = new Morris.Line({
      element: 'line-chart',
      resize: true,
      data: [
        {y: '2011 Q1', item1: 6810,item2: 3767,item3: 15073,item4: 2778},
        {y: '2011 Q2', item1: 2778,item2: 4820,item3: 8432,item4: 4820},
        {y: '2011 Q3', item1: 10687,item2: 6810,item3: 4820,item4: 15073},
        {y: '2011 Q4', item1: 3767,item2: 10687,item3: 15073,item4: 8432},
        {y: '2012 Q1', item1: 6810,item2: 15073,item3: 2778,item4: 5670},
        {y: '2012 Q2', item1: 5670,item2: 6810,item3: 15073,item4: 2778},
        {y: '2012 Q3', item1: 4820,item2: 15073,item3: 10687,item4: 15073},
      ],
      xkey: 'y',
      ykeys: ['item1','item2','item3','item4'],
      labels: ['合字','拆字','去重','录入'],
      lineColors: ['#e72a26','#01a75b','#fd9903','#50f0fe'],
      hideHover: 'auto'
    });


     $('input[id^=radioAll]').click(function(){
        if($(this).hasClass('btn-success')){
            $(this).removeClass('btn-success');
            $('input[name=radioA]').removeClass('btn-success');
        }else{
            $('input[name=radioA]').addClass('btn-success');
            $(this).addClass('btn-success');
        }
    })

    $('input[name^=radioA]').click(function(){
        if($(this).hasClass('btn-success')){
            $(this).removeClass('btn-success');
        }else{
            $(this).addClass('btn-success');
        }
    })

    $('#lowAll').click(function(){
        $('#leave').toggle();
    })
    $('#lowAll2').click(function(){
        $('#leave2').toggle();
    })

  });



