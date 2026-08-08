const VOTE_URL = "/vote" 

function vote(is_up, quote_id)
{
	//make URL
	
	const url = `${VOTE_URL}?id=${quote_id}&up=${is_up}`;
	const response = await fetch(url, { method: "POST" });
	return 1;
};
