window.onscroll = function () {
    let r = document.getElementById("return")
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        r.style.display = "block";
    } else {
        r.style.display = "none";
    }
}
function scrollToTop()
{
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}