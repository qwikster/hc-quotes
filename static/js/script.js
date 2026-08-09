const VOTE_URL = "/vote";
const RAND_URL = "/quotes";

function esc(str) {
  return String(str).replace(/[&<>"']/g, match => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[match]);
}

async function vote(is_up, quote_id)
{
	//make URL

	const url = `${VOTE_URL}?id=${quote_id}&up=${is_up}`;
	const response = await fetch(url, { method: "POST" });
	const response_obj = await response.json();
	document.getElementById("vote_count_" + quote_id).innerHTML = response_obj.votes;

	voteButtons = document.getElementsByClassName("q" + quote_id);
	for (let i = 0; i < voteButtons.length; i++) {
		voteButtons[i].disabled = true;
	};
	return 1;
};

async function add_random_quotes(count)
{
  const response = await fetch(RAND_URL);
  const auth = await fetch("/me");
	const response_array = await response.json();
	for (i = 0; i < response_array.length; i++) {
		let q = response_array[i];
		add_quote_to_page(q.id, esc(q.quote), esc(q.author), q.votes, q.voted, auth);
	};
};

async function add_quote_to_page(id, quote, author, vote_count, is_voted, auth)
{
	let vote_class = "";
	if (!auth.ok) {
		vote_class = "disabled";
	};
	if (is_voted) {
		vote_class = "disabled";
	};

  const quote_html = `
  <div class="vote-cont">
    <a class="hidelink" href="/q/${id}" target="_self">
        <div class="quote-contain">
            <p class="quote">❝${quote}❞</p>
            <p class="author"><i>~ ${author}</i></p>
        </div>
        </a>
        <div class="vote-buttons">
            <button ${vote_class} class="vote-btn upvote q${id}" aria-label="up" onclick="vote(true, '${id}')">
                <svg viewBox="0 0 24 24">
                    <path d="M4 14h6v8h4v-8h6L12 4 4 14z"/>
                </svg>
            </button>
            <span class="vote-count" id="vote_count_${id}">${vote_count}</span>
            <button ${vote_class} class="vote-btn downvote q${id}" aria-label="down" onclick="vote(false, '${id}')">
                <svg viewBox="0 0 24 24">
                    <path d="M20 10h-6V2h-4v8H4l8 10 8-10z"/>
                </svg>
            </button>
        </div>
  </div>
	`;
	var div = document.createElement("div");
	div.innerHTML = quote_html.trim();
	document.getElementById("quotes-all").appendChild(div.firstChild); //copied from somewhere i think

}

async function replaceLoginButtonIfNeeded()
{
	const response = await fetch("/me");
	if (!response.ok) {
		//get button
		let button = document.querySelector("button.login");
		let button_link = document.getElementById("login-button-link");
		//change to LOGIN
		button.innerHTML = "Login w/HC";
		button_link.href = "/login";
	};
	return 1;
};

async function Search(offset)
{
	//get values
	let select_value = document.getElementById("search-mode-select").value;
	let search_value = document.getElementById("search-bar").value;
	//send request
	
	const response = await fetch(`/quotes?query=${search_value}&sort=${select_value}`);
	const auth = await fetch("/me");
	const response_array = await response.json();
	for (i = 0; i < response_array.length; i++) {
		let q = response_array[i];
		add_quote_to_page(q.id, esc(q.quote), esc(q.author), q.votes, q.voted, auth);
	};
};
