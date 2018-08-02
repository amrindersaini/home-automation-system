login = document.getElementById("login")
$(() =>  {
    console.log('Login page Loaded')
    /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
    particlesJS.load('particles-js', 'static/js/particlesjs-config.json', () => {
        console.log('callback - particles.js config loaded')
    })
    login.href ='http://' + document.domain + ':5000/login'
})


