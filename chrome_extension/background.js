async function sendOpenTabs() {
  try {
    const pingRes = await fetch('http://127.0.0.1:5000/ping');
    if (!pingRes.ok) throw new Error("No backend");

    const tabs = await chrome.tabs.query({});
    const tabUrls = tabs.map(tab => tab.url);

    await fetch('http://127.0.0.1:5000/tabs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ urls: tabUrls })
    });
  } catch (err) {
    console.log("Server pole töös");
  }
}

setInterval(sendOpenTabs, 5000);