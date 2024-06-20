const tg = window.Telegram.WebApp;

var xhr = new XMLHttpRequest();
xhr.open("GET",
    window.location.protocol + '//' + window.location.host + '/api/get-user-data?' + tg.initData, 
    true);
xhr.onload = () => {
    if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
        }
    }
};
xhr.send();