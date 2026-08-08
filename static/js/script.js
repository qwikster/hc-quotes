const VOTE_URL = "/vote";
const RAND_URL = "/quotes";

async function vote(is_up, quote_id)
{
	//make URL

	const url = `${VOTE_URL}?id=${quote_id}&up=${is_up}`;
	const response = await fetch(url, { method: "POST" });
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
	const quote_html = `<DIV CLASS="quote-contain"><BLOCKQUOTE><P>${quote}</P></BLOCKQUOTE><P>-- ${author}</P></DIV><DIV CLASS="vote_buttons"><BUTTON onclick='vote(true, "${id}")'>Upvote</BUTTON><SPAN id="vote_count">${vote_count}</SPAN><BUTTON onclick='vote(false, "${id}")'>Downvote</BUTTON></DIV>`;
	var div = document.createElement("div");
	div.innerHTML = quote_html.trim();
	document.GetElementById("quotes-all").appendChild(div.firstChild); //copied from somewhere i think

}
