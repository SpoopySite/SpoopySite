document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('input').onkeyup = function (event) {
    const code = event.keyCode || event.which;
    if (code !== 13) return;
    go();
  };
  document.getElementById('go').onclick = go;
});

function go() {
  window.location.pathname = "spoopy/" + document.getElementById('input').value;
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('js/serviceworker.js').then(() => console.log("Service Worker Registered"));
}
