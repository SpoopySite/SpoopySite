document.addEventListener("DOMContentLoaded", function () {
  const safe = document.querySelector('#results h2');
  const list = document.querySelector('#results ol');
  const heading = document.getElementById('header');
  const spinner = document.querySelector('.spinner');

  const cache = {
    get: (name) => {
      const i = JSON.parse(localStorage.getItem(name));
      if (!i || i && Date.now() - i.time > 172800000) return null;
      return i.data;
    },
    set: (name, data) => localStorage.setItem(name, JSON.stringify({data, time: Date.now()})),
    has: (name) => !!localStorage.getItem(name),
  };

  const suspect = window.location.pathname.slice(8).replace(/(^<|>$)/g, '');
  heading.innerHTML = suspect;
  if (cache.has(suspect)) {
    const res = cache.get(suspect);
    safe.innerHTML = res.safe ? 'Safe' : 'Unsafe';
    heading.innerHTML = res.chain[0].url;
    for (const item of res.chain) addResult(item, list, spinner);
    spinner.remove();
  } else {
    const ws = new WebSocket(`${getWS()}/ws/${suspect}`);
    ws.onmessage = (event) => {
      let item;
      try {
        item = JSON.parse(event.data);
      } catch (err) {
        console.error(err.stack);
        safe.innerHTML = err.message;
        return;
      }
      if (item["end"]) {
        spinner.remove()
      } else{
        addResult(item, list, spinner);
      }

      if (item.chain) {
        safe.textContent = item.safe ? 'Safe' : 'Unsafe';
        heading.textContent = item.chain[0].url;
        cache.set(item.chain[0].url, item);
        cache.set(suspect, item);
        spinner.remove();
      }
    }
  }
});

function addResult(item, list, spinner) {
  const li = document.createElement('li');
  const p = document.createElement('p');
  p.textContent = `${item.url} ${item.safety ? '\u2714' : '\u274c'}`;
  const reasons = document.createElement('p');
  reasons.textContent = item.reasons.join(', ');
  li.append(p);
  li.append(reasons);
  list.insertBefore(li, spinner);
}

function getWS() {
  const l = window.location;
  const protocol = l.protocol.endsWith('s:') ? 'wss' : 'ws';
  return `${protocol}://${l.host}`;
}
