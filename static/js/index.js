var socket = io.connect('http://' + document.domain + ':' + location.port)
var componentStatus
const ledRoom1 = document.getElementById("switch-led-room1")
const ledRoom2 = document.getElementById("switch-led-room2")
const fanRoom1 = document.getElementById("switch-fan-room1")
const fanRoom2 = document.getElementById("switch-fan-room2")
const bulbIcon1 = document.getElementById("bulb1")
const bulbIcon2 = document.getElementById("bulb2")
const logout = document.getElementById("logout")
const username = document.getElementById("username")

$(() =>  {
    console.log('App successfully loaded')
    getData() 
    startTime()
    getCurrentDate()
    logout.href = 'http://' + document.domain + ':' +'5000/logout'
})

function getData() {
    $.get('http://' + document.domain + ':' +'5000/data', (data) => {
        //console.log(data)
        //jsonObj = JSON.parse(data)
        updateStatus(data)
        //console.log(jsonObj.ledRoom1)
    })
}

function updateStatus(jsonObj){
    //console.log(jsonObj)
    //jsonObj = JSON.parse(jsonObj)
    console.log(jsonObj)
    jsonObj.room1Led ? jsonObj.room1Led = true : jsonObj.room1Led = false
    jsonObj.room2Led ? jsonObj.room2Led = true : jsonObj.room2Led = false
    jsonObj.room1Fan ? jsonObj.room1Fan = true : jsonObj.room1Fan = false
    jsonObj.room2Fan ? jsonObj.room2Fan = true : jsonObj.room2Fan = false
    //console.log(jsonObj)
    setIcon(jsonObj)   
    ledRoom1.checked = jsonObj.room1Led
    ledRoom2.checked = jsonObj.room2Led
    fanRoom1.checked = jsonObj.room1Fan
    fanRoom2.checked = jsonObj.room2Fan
}

function setIcon(data){
    //console.log(data)
    if(data.room1Led == false)
        bulbIcon1.src = '/static/images/iconmonstr-light-bulb-12.svg'
    else
        bulbIcon1.src = '/static/images/iconmonstr-light-bulb-18.svg'
    if(data.room2Led == false)
        bulbIcon2.src = '/static/images/iconmonstr-light-bulb-12.svg'
    else
        bulbIcon2.src = '/static/images/iconmonstr-light-bulb-18.svg'
}


function setComponentStatus(){
    componentStatus = { room1Led: ledRoom1.checked, 
                        room2Led: ledRoom2.checked, 
                        room1Fan: fanRoom1.checked, 
                        room2Fan: fanRoom2.checked
    }
    componentStatus.room1Led ? componentStatus.room1Led = 1 : componentStatus.room1Led = 0
    componentStatus.room2Led ? componentStatus.room2Led = 1 : componentStatus.room2Led = 0
    componentStatus.room1Fan ? componentStatus.room1Fan = 1 : componentStatus.room1Fan = 0
    componentStatus.room2Fan ? componentStatus.room2Fan = 1 : componentStatus.room2Fan = 0
}

socket.on('data',(status) =>{
    updateStatus(status)
    console.log(status) 
})

ledRoom1.addEventListener("change", () =>{
    buttonChange()
    //ons.notification.alert('Value is ' + ledRoom1.value)
})

ledRoom2.addEventListener("change", () =>{
    buttonChange()
})

fanRoom1.addEventListener("change", () =>{
    buttonChange()
})

fanRoom2.addEventListener("change", () =>{
    buttonChange()
})

function buttonChange(){
    setComponentStatus()
    socket.emit('statusChange',componentStatus)
}

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

function getCurrentDate(){
    let today = new Date()
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    var month = months[today.getMonth()]
    var date = today.getDate()
    var year = today.getFullYear()
    document.getElementById('date').innerHTML = month + ' ' + date +','+year
}