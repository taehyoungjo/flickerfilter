let urlSent = false;

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.greeting == "url_changed") {
		if(urlSent == false) {
			let vid = $('video').get(0);
			if (vid) {
				vid.addEventListener('playing', function(event) {
					vid.pause();
					chrome.runtime.sendMessage({ greeting: "get_url" });
				});
				urlSent = true;
			}
		}
	}
});

if (urlSent == false) {
	let vid = $('video').get(0);
	if (vid) {
		vid.addEventListener('playing', function(event) {
			vid.pause();
			chrome.runtime.sendMessage({ greeting: "get_url" });
		});
		urlSent = true;
	}
}
