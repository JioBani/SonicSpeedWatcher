var passDataArr;

function onGetData(dataArr) {
    passDataArr = dataArr;
    var i = 0;
    dataArr.forEach((data)=>{
        document.getElementById("show_table_body").innerHTML += getTableTime(data,i);
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
    console.log(index);
}