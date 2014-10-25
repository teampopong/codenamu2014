'use strict';

var Law = {};

Law.initialize = function(){
    Law.barGroup = document.getElementsByClassName('law-list')[0];
};

Law.dataInput = function(data){
    var cnt = data.length, dataSet = [];
    if(cnt > 5){
        cnt = 5;
    }
    for(var i=0; i<cnt; i++){
        dataSet.push(data[i]);
    }

    return dataSet;
};

Law.drawGraph = function(data){
    var max_cnt = data[0][1];

    for(var i=0; i<data.length; i++){
        var title = data[i][0], count = data[i][1], width = count/max_cnt*100;

        var barElm = document.createElement('div');
        barElm.className = 'law-item';

        var barTitle = document.createElement('span');
        barTitle.className = 'law-title';
        barTitle.innerHTML = title;

        var barCount = document.createElement('span');
        barCount.className = 'law-count';
        barCount.innerHTML = count;

        var barBar = document.createElement('span');
        barBar.className = 'law-bar';
        barBar.style.width = width + '%';
        barBar.style.opacity = (6-i)/6;

        barElm.appendChild(barTitle);
        barElm.appendChild(barCount);
        barElm.appendChild(barBar);

        Law.barGroup.appendChild(barElm);
    }
};
