let url_sent = false;
let ignore_warning = false;
let vid;
// Creating the modal popup
let modal_div = document.createElement("div");
modal_div.className = "modal";
document.body.appendChild(modal_div);

// let modal_content_div = document.createElement("div");
// modal_content_div.className = "modal-content";
// modal_div.appendChild(modal_content_div);

let modal_text = document.createElement("p");
modal_text.className = "modal_text";
modal_div.appendChild(modal_text);

let close = document.createElement("button");
close.className = "close";
modal_div.appendChild(close);

close.onclick = function() {
	modal_div.style.display = "none";
	ignore_warning = true;
};

chrome.storage.sync.get(["toggled"], function(data) {
	if (data.toggled) {	
		chrome.runtime.onMessage.addListener(messageListener);

		vid = $('video').get(0);
		if (vid) {
			vid.addEventListener('playing', playingListener);
		}
	}
});

function disableExtension() {
	modal_div.style.display = "none";
	chrome.runtime.onMessage.removeListener(messageListener);
	vid.removeEventListener('playing', playingListener);
}



function playingListener(event) {
	if (!ignore_warning) {
		if(!url_sent) {
			modal_div.style.display = "block";
			modal_text.innerHTML = "Analyzing video...";
			chrome.runtime.sendMessage({ greeting: "get_url" });
			url_sent = true;
		}
		vid.pause();
	}
}

function messageListener(request, sender, sendResponse) {
	if (request.greeting == "url_changed") {
		modal_div.style.display = "none";
		close.style.display = "none";
		ignore_warning = false;
		url_sent = false;
		vid = $('video').get(0);
		if (vid) {
			vid.addEventListener('playing', playingListener);
		}
	}

	else if (request.greeting == "risk") {
		modal_text.innerHTML = "Epileptic risk detected"
		close.style.display = "block";
		close.innerHTML = "Watch Anyways";
	}

	else if (request.greeting == "safe") {
		modal_text.innerHTML = "Looks good!"
		close.style.display = "block";
		close.innerHTML = "Watch Video";
	}

	else if (request.greeting == "disable") {
		disableExtension();
	}
}

