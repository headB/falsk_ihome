function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
        url:"/api/v1.0/session", 
        type:'delete',
        headers:{'X-CSRFToken':getCookie('csrf_token')},
        dataType:'json',
        success:
    function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    }
    })
}

$(document).ready(function(){
})