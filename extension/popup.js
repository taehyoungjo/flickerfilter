window.onload = function() {
	chrome.storage.sync.get(["toggled"], function(data) {
		$("#toggle").prop('checked', data.toggled);
	});

	$("#toggle").change(function() {
		if (this.checked) {
			chrome.storage.sync.set({ toggled: true });
			$("#alert").html("Refresh the page!");
		}
		else {
			chrome.storage.sync.set({ toggled: false });
			chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
				chrome.tabs.sendMessage(tabs[0].id, { greeting: "disable" });
			});
		}
	});
};
