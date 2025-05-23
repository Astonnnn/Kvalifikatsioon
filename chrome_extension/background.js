let blockedSites = [];

const redirectUrl = chrome.runtime.getURL("block.html")

function isBlocked(url) {
  return blockedSites.some(site => url.includes(site))
}

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  const url = details.url;
  console.log("sssss")
  if(isBlocked(url)) {
    chrome.tabs.update(details.tabId, { url: redirectUrl })
  };
});



async function sendOpenTabs() {
  try {
    const pingRes = await fetch('http://127.0.0.1:5000/ping');
    if (!pingRes.ok) throw new Error("No backend");

    const tabs = await chrome.tabs.query({active: true, lastFocusedWindow: true});
    const tabUrls = tabs.map(tab => tab.url);

    const response = await fetch('http://127.0.0.1:5000/tabs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ urls: tabUrls })
    });
    await receiveBlocked()
  } catch (err) {
    console.log("Server pole töös");
  }
}

async function receiveBlocked() {
  try {

    const response = await fetch('http://127.0.0.1:5000/tabs', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });


    const data = await response.json();
    const lehed = data.Blokeeritud;
    console.log(lehed);
    console.log(typeof lehed);
    blockedSites = lehed;



  } catch (err) {
    console.log(err)
  }

}




setInterval(sendOpenTabs, 5000);