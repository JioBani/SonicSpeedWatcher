
var config = {

	type: 'line',


	data: {

		labels: [],

		datasets: [{
			label: '전체 차량',
			backgroundColor: 'yellow',
			borderColor: 'rgb(115, 251, 132)',
			borderWidth: 2,
			data: [],
			fill : false,
		},
    {
			label: '과속 차량',
			backgroundColor: 'yellow',
      borderColor: 'rgb(255, 99, 132)',
			borderWidth: 2,
			data: [],
			fill : false,
		},
  ]
	},

	options: {
		responsive : false,
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: { display: true, labelString: '시각' },
			}],
			yAxes: [{
				display: true,
				scaleLabel: { display: true, labelString: '차량(대)' }
			}]
		}
	}
};

var ctx = null
var chart = null
var LABEL_SIZE = 20;
var tick = 0;

function drawChart() {
	ctx = document.getElementById('canvas').getContext('2d');
	chart = new Chart(ctx, config);
}

function init(enterTime) {

  for(let i=19; i>=0; i--) {
    var date = new Date(enterTime);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    const seconds = ('0' + date.getSeconds()).slice(-2);
    const timeStr = hours + '시' + minutes + '분';
		chart.data.labels[i] = timeStr;
    enterTime = enterTime - 60000;
	}

	chart.update();
}

function addChartData(index , value) {
	tick++;
	tick %= 100;
	let n = chart.data.datasets[index].data.length;
	if(n < LABEL_SIZE)
		chart.data.datasets[index].data.push(value);
	else {

		chart.data.datasets[index].data.push(value);
		chart.data.datasets[index].data.shift();

		chart.data.labels.push(tick);
		chart.data.labels.shift();
	}
	chart.update();
}

function hideshow() {
	if(canvas.style.display == "none") 	canvas.style.display = "block"
	else canvas.style.display = "none"
}

