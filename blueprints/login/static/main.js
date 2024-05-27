const tg = window.Telegram.WebApp;
const login = document.getElementById('login');
const password = document.getElementById('password');
const checkbox = document.getElementById('save_data');
const main_button = tg.MainButton;

function onValueChange(e) {
    if (!login.value.trim().length || !password.value.trim().length) {
        main_button.setParams(
            {
                'color': '#808080',
                'is_active': false
            }
        );
    }
    else {
        main_button.setParams(
            {
                'color': '#24A1DE',
                'is_active': true
            }
        );
    }
}

main_button.setParams(
    {
        'text': 'Войти',
        'color': '#808080',
        'is_active': false,
        'is_visible': true
    }
);


main_button.onClick(() => {
    main_button.showProgress(false);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            main_button.hideProgress();
            tg.sendData(xhr.responseText);
            tg.close();
        }
    };
    xhr.send(JSON.stringify({
        'login': login.value,
        'password': password.value,
        'save_login_data': checkbox.value
    }));

});

login.addEventListener('input', onValueChange);
password.addEventListener('input', onValueChange);
