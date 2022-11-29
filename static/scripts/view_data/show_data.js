var passDataArr;

function onGetData(dataArr) {
    passDataArr = dataArr;
    var i = 0;
    dataArr.forEach((data)=>{
        document.getElementById("show_table_body").innerHTML += getTableTime(data,i);
        i++;
    })

}

function getTableTime(passData , i) {
    //asd
    var enterTime = new Date(Math.floor(Number(passData['enterTime'] * 1000)));
    var exitTime = new Date(Math.floor(Number(passData['exitTime'] * 1000)));
    var result = `<tr id = ${i}>`;
    result += `<td class="enter_time">${enterTime.toLocaleString('ko-KR')}</td>`;
    result += `<td>${exitTime.toLocaleString('ko-KR')}</td>`;
    result += `<td>${passData['passingTime'].toFixed(2)}</td>`;
    result += `<td>${passData['velocity'].toFixed(1)}km/h</td>`;
    result += `<td>${passData['isSpeeding'] == true ? '과속' : '' }</td>`;
    result += `<td></td>`;
    result += `<td style="text-align: center;">
                <button type="button" onclick="onClickShowImage(${i})">
                <img class = "icon" src="../static/web_image/icon_image.svg".svg" width="25px" height="25px">
                </button>
               </td>`;
    result += "</tr>";
    return result;
}

function onClickShowImage(index){

    var form = document.createElement('form');
    form.setAttribute('method', 'post'); //POST 메서드 적용
    form.setAttribute('action', 'http://192.168.137.42:8080/view_with_image');	// 데이터를 전송할 url
    for ( var key in params) {	// key, value로 이루어진 객체 params
        var hiddenField = document.createElement('input');
        hiddenField.setAttribute('type', 'hidden'); //값 입력
        hiddenField.setAttribute('name', key);
        hiddenField.setAttribute('value', passDataArr[index]['enterTime']);
        form.appendChild(hiddenField);
    }
    document.body.appendChild(form);
    form.submit();	// 전송~
}