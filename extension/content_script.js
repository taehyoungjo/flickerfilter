let urlSent = false;
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
modal_div.appendChild(modal_text);

let close = document.createElement("button");
close.className = "close";
modal_div.appendChild(close);

close.onclick = function() {
	chrome.runtime.onMessage.removeListener();
	modal_div.style.display = "none";
	ignore_warning = true;
}

function playingListener(event) {
	if (!ignore_warning) {
		vid.pause();
		chrome.runtime.sendMessage({ greeting: "get_url" });
		modal_div.style.display = "block";
		modal_text.innerHTML = "Analyzing video...";
		urlSent = true;
	}
}

function messageListener(request, sender, sendResponse) {
	if (request.greeting == "url_changed") {
		modal_div.style.display = "none";
		close.style.display = "none";
		ignore_warning = false;
		if(urlSent == false) {
			vid = $('video').get(0);
			if (vid) {
				vid.addEventListener('playing', playingListener);
			}
		}
	}

	else if (request.greeting == "risk") {
		modal_text.innerHTML = "Epilpetic risk detected."
		close.style.display = "block";
		close.innerHTML = "Watch Anyways";
	}

	else if (request.greeting == "safe") {
		modal_text.innerHTML = "Looks good!"
		close.style.display = "block";
		close.innerHTML = "Watch Video";
	}
}

modal_div.style.display = "none";
chrome.runtime.onMessage.addListener(messageListener);

if (urlSent == false) {
	vid = $('video').get(0);
	if (vid) {
		vid.addEventListener('playing', playingListener);
	}
}

