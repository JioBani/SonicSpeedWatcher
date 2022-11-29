function onGetData(dataArr) {

    dataArr.forEach((data)=>{
        document.getElementById("show_table_body").innerHTML += getTableTime(data);
    })

}

function getTableTime(passData) {
    var result = '<tr>';
    result += `<td class="enter_time">${passData['exitTime']}</td>`;
    result += `<td>${passData['exitTime']}</td>`;
    result += `<td>${passData['passingTime']}</td>`;
    result += `<td>${passData['velocity']}km/h</td>`;
    result += `<td>${passData['isSpeeding'] == 'true' ? '과속' : '' }</td>`;
    result += `<td></td>`;
    result += `<td style="text-align: center;">
                <img class = "icon" src="../static/web_image/icon_image.svg".svg" width="25px" height="25px">
               </td>`;
    result += "</tr>";
    return result;
}