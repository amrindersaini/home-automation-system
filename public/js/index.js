var socket = io()//load socket.io-client and connect to the host that serves the page
var componentStatus
const ledRoom1 = document.getElementById("switch-led-room1")
const ledRoom2 = document.getElementById("switch-led-room2")
const fanRoom1 = document.getElementById("switch-fan-room1")
const fanRoom2 = document.getElementById("switch-fan-room2")
const bulbIcon1 = document.getElementById("bulb1")
const bulbIcon2 = document.getElementById("bulb2")
$(() =>  {
    console.log('App successfully loaded')
    getData()
    startTime()
})
 
function getData() {
    $.get('http://localhost:8000/data', (data) => {
        //console.log(data)
        updateStatus(data)
    })
}

function setIcon(data){
    //console.log(data)
    if(data.room1Led == false)
        bulbIcon1.src = 'images/iconmonstr-light-bulb-12.svg'
    else
        bulbIcon1.src = 'images/iconmonstr-light-bulb-18.svg'
    if(data.room2Led == false)
        bulbIcon2.src = 'images/iconmonstr-light-bulb-12.svg'
    else
        bulbIcon2.src = 'images/iconmonstr-light-bulb-18.svg'
}

function updateStatus(serverStatus){
    // console.log(serverStatus)
    // console.log(serverStatus.room1Led)
    setIcon(serverStatus)
    ledRoom1.checked = serverStatus.room1Led
    ledRoom2.checked = serverStatus.room2Led
    fanRoom1.checked = serverStatus.room1Fan
    fanRoom2.checked = serverStatus.room2Fan

}

function setComponentStatus(){
    componentStatus = { room1Led: ledRoom1.checked, 
                        room2Led: ledRoom2.checked, 
                        room1Fan: fanRoom1.checked, 
                        room2Fan: fanRoom2.checked
    }
}

socket.on('data',updateStatus)

ledRoom1.addEventListener("change", () =>{
    setComponentStatus()
    socket.emit('statusChange',componentStatus)
    //ons.notification.alert('Value is ' + ledRoom1.checked)
})

ledRoom2.addEventListener("change", () =>{
    setComponentStatus()
    socket.emit('statusChange',componentStatus)
})

fanRoom1.addEventListener("change", () =>{
    setComponentStatus()
    socket.emit('statusChange',componentStatus)
})

fanRoom2.addEventListener("change", () =>{
    setComponentStatus()
    socket.emit('statusChange',componentStatus)
})

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML =
    h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}