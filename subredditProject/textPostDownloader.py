import json, requests
post_list = []
total_string = ''

inputted = 'Showerthoughts ; new ; 24'

def subs(inputted):

	splitted = [i.replace(' ','').replace('\n','') for i in inputted.split(';')]
	if splitted[1].lower() == 'new':
		splitted[1] == 'new'
	else:
		splitted[1] == ''

	if int(splitted[2])>1 and int(splitted[2])<=25:
		pass
	else:
		splitted[2] = '1'

	subreddit_name = splitted[0]
	sorts = splitted[1]
	numb = splitted[2]
	post_list = []
	numb = int(numb)
	start_num = 0
	subreddit = '{}/{}'.format(subreddit_name,sorts)

	try:
		r = requests.get(
			'http://www.reddit.com/r/{}.json'.format(subreddit),
			headers={'user-agent': 'Mozilla/5.0'})

		# view structure of an individual post
		# print(json.dumps(r.json()['data']['children'][0]))

		print(r.json())
		for post in r.json()['data']['children']:
			start_num += 1
			post_list.append(post['data']['title'])
			if start_num==numb:break

		total_string = ''
		for _ in post_list:
			if _.strip()[-1:].lower() in 'qwertyuiopasdfghjklzxcvbnm':_ = _+'.'
			total_string += '# '+_+'\n'
		return total_string
	except:
		return 'Error in fetching data.'

total_string = subs(inputted)
print(total_string)
