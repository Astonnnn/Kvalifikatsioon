async function sendOpenTabs() {
  const tabs = await chrome.tabs.query({});
  const tabUrls = tabs.map(tab => tab.url);

  fetch('http://localhost:5000/tabs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ urls: tabUrls })
  });
}

// Iga viie sekundi tagant kutsub funktsiooni välja
setInterval(sendOpenTabs, 5000);
