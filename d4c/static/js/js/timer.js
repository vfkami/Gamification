var countdownNumberEl = document.getElementById('countdown-number');
var countdown = 7;

countdownNumberEl.textContent = countdown;

setInterval(function() {
  countdown = --countdown <= 0 ? 7 : countdown;

  countdownNumberEl.textContent = countdown;
}, 1000);