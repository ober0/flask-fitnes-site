function updateTimer() {
  document.getElementById('timer').innerText = "Переадрессация назад через " + time/1000 + " сек";
  if (time <= 0){
    window.location.href = '/';
  }
  else {
    time -= 100;
    setTimeout(updateTimer, 100);
  }
}
var time = 3000;
updateTimer();