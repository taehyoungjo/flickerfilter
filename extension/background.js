let analyzer_url = "http://localhost:5000/fetch";

let rule1 = {
	conditions: [
		new chrome.declarativeContent.PageStateMatcher({
			pageUrl: { hostEquals: 'www.youtube.com', schemes: ['https'] },
			css: ["video"]
		})
	],
	actions: [ new chrome.declarativeContent.ShowPageAction() ]
};

chrome.runtime.onInstalled.addListener(function() {
	chrome.storage.sync.set({ toggled: true });
	chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
		chrome.declarativeContent.onPageChanged.addRules([rule1]);
	});
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.greeting == "get_url") {
		chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
			let video_url = tabs[0].url;
			$.get(analyzer_url, { url: video_url }, function(data) {
				if (data == true) {
					chrome.tabs.sendMessage(tabs[0].id, { greeting: "risk" });
				}
				else {
					chrome.tabs.sendMessage(tabs[0].id, { greeting: "safe" });
				}
			});
		});
	}
});

chrome.webNavigation.onHistoryStateUpdated.addListener(function(details) {
    if (details.frameId === 0) {
        // Fires only when details.url === currentTab.url
        chrome.tabs.get(details.tabId, function(tab) {
            if (tab.url === details.url) {
            	chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
					chrome.tabs.sendMessage(tabs[0].id, { greeting: "url_changed" });
				});
            }
        });
    }
});