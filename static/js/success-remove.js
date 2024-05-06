function timer() {
    document.getElementById('timer').innerText = 'Переадрессация назад через ' + time/1000 + " сек";
    if (time > 0){
        time -= 100;
        setTimeout(timer, 100);
    }
    else {
        window.location.href = '/';
    }
}

var time = 3000;
timer();