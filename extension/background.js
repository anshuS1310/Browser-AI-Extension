chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
chrome.runtime.onMessage.addListener((req) => {
    chrome.runtime.sendMessage({ type: "UPDATE_SIDEBAR", text: req.text }).catch(() => {});
});