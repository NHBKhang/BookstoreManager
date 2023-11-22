function invalid() {
    var username = document.getElementById('username');
    var password = document.getElementById('password');
    if (username.value == "") {
        document.getElementById(error-username).style.display = "block";
        // $(".input.email").css("border-color", "red");
    } else {
        document.getElementById(error-username).style.display = "none";
        // $(".input.email").css("border-color", "gray");
    }
    if (password.value == "") {
        document.getElementById(error-password).style.display = "block";
        // $(".input.password").css("border-color", "red");
    } else {
        document.getElementById(error-password).style.display = "none";
        // $(".input.password").css("border-color", "gray");
    }
}