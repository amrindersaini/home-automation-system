$(() =>  {
    console.log('Login page Loaded')
    /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
    particlesJS.load('particles-js', 'static/js/particlesjs-config.json', () => {
    console.log('callback - particles.js config loaded');
});
})

function postData(loginInfo) {
    $.post('http://' + document.domain + ':' +'5000/loginpage',loginInfo)
}

$("#login").click( () => {
    var loginDetails = {
        username : $("username").text(), password : $("password").text()
    }
    postData(loginDetails)
})