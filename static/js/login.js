register = document.getElementById("register")

$(() =>  {
    console.log('Login page Loaded')
    /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
    particlesJS.load('particles-js', 'static/js/particlesjs-config.json', () => {
        console.log('callback - particles.js config loaded')
    })
    register.href ='http://' + document.domain + ':5000/register'
})
