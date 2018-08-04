var socket = io.connect('http://' + document.domain + ':' + location.port)
const index = document.getElementById("welcometext")
const maindoor = document.getElementById("maindoor")
const video = document.getElementById("video")

$(() =>  {
    console.log("Livefeed loaded")
    index.href = 'http://' + document.domain + ':5000/'
    logout.href = 'http://' + document.domain + ':' +'5000/logout'
    livefeed.href = 'http://' + document.domain + ':5000/livefeed' 
    video.src = 'http://'+ document.domain + ':8000/index.html'
    hello.classList.remove("active")
    live.classList.add("active")
    // videoHandler(()=>{
    //     const img = document.getElementById("img-video-tag")
    //     img.setAttribute('style', img.getAttribute('style'))
    // })
    getData()
})

function getData() {
    $.get('http://' + document.domain + ':' +'5000/data', (data) => {
        //console.log("Data" + data)
        jsonObj = JSON.parse(data)
        // console.log(jsonObj)
        // console.log(jsonObj.maindoor)
        if(jsonObj.maindoor == 1){
            maindoor.checked = true
        }
        else maindoor.checked = false
        // updateStatus( jsonObj)
        //console.log(jsonObj.ledRoom1)

    })
}

socket.on('mainDoorHandler', (value) => {
    if(value == 1)
        maindoor.checked = true
    else maindoor.checked = false
})

maindoor.addEventListener( "change" , () => {
    if( maindoor.checked == true ) 
        flag = 1
    else flag = 0
    socket.emit( 'maindoorLivefeed' , flag )
})