const VOTE_URL = "/vote";
const RAND_URL = "/quotes";

async function vote(is_up, quote_id)
{
	//make URL

	const url = `${VOTE_URL}?id=${quote_id}&up=${is_up}`;
	const response = await fetch(url, { method: "POST" });
	const response_obj = await response.json();
	document.getElementById("vote_count_" + quote_id).innerHTML = response_obj.votes;
	
	voteButtons = document.querySelector("div.vote_buttons button");
	for (let i = 0; i < voteButtons.length; i++) {
		voteButtons[i].disabled = true;
	};


	return 1;
};

async function add_random_quotes(count)
{
	const response = await fetch(RAND_URL);
	const response_array = await response.json();
	for (i = 0; i < response_array.length; i++) {
		let q = response_array[i];
		add_quote_to_page(q.id, q.quote, q.author, q.votes);
	};
};

function add_quote_to_page(id, quote, author, vote_count)
{
  const quote_html = `
    <div class="vote-cont">
        <div class="quote-contain">
            <p class="quote">${quote}</p>
            <p class="author"><i>~ ${author}</i></p>
        </div>
        <div class="vote-buttons">
            <button class="vote-btn upvote" aria-label="up" onclick="vote(true, '${id}')">
                <svg viewBox="0 0 24 24">
                    <path d="M4 14h6v8h4v-8h6L12 4 4 14z"/>
                </svg>
            </button>
            <span class="vote-count" id="vote_count_${id}">${vote_count}</span>
            <button class="vote-btn downvote" aria-label="down" onclick="vote(false, '${id}')">
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
