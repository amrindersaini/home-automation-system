var socket = io.connect('http://' + document.domain + ':' + location.port)
const index = document.getElementById("welcometext")
const maindoor = document.getElementById("maindoor")
const video = document.getElementById("video")
const maindoor = document.getElementById("maindoor")

$(() =>  {
    console.log("Livefeed loaded")
    index.href = 'http://' + document.domain + ':5000/'
    logout.href = 'http://' + document.domain + ':' +'5000/logout'
    livefeed.href = 'http://' + document.domain + ':5000/livefeed' 
    video.src = 'http://'+ document.domain + ':8000/index.html'
    // videoHandler(()=>{
    //     const img = document.getElementById("img-video-tag")
    //     img.setAttribute('style', img.getAttribute('style'))
    // })
})


