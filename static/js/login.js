$(() =>  {
    console.log('Login page Loaded')
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