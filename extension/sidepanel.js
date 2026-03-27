chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === "UPDATE_SIDEBAR") document.getElementById('inputBox').value = msg.text;
});

async function callAI(text, task) {
    const output = document.getElementById('outputBox');
    output.innerText = "AI is thinking deeply...";
    try {
        const res = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, task })
        });
        const data = await res.json();
        output.innerText = data.output;
    } catch (e) { output.innerText = "Error: Python Backend Offline."; }
}

document.getElementById('processBtn').addEventListener('click', () => {
    callAI(document.getElementById('inputBox').value, "explain");
});

document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.body.innerText
    }, (results) => {
        callAI(results[0].result, "summarize");
    });
});

document.getElementById('copyBtn').addEventListener('click', () => {
    navigator.clipboard.writeText(document.getElementById('outputBox').innerText);
    alert("Copied to clipboard!");
});