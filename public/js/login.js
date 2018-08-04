$(() =>  {
    console.log('Login page Loaded')
})

function postData(loginInfo) {
    $.post('http://localhost:8000/loginpage',loginInfo)
}

$("#login").click( () => {
    var loginDetails = {
        username : $("username").text(),
        password : $("password").text()
    }
    postData(loginDetails)
})

