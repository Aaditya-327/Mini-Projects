# python 3
import json, requests,os


def download_image(url,filename):
	img_data = requests.get(url).content
	with open(filename, 'wb') as handler:
		handler.write(img_data)


def subreddit_name(subr,sorts = ''):
	subreddit_name = subr	
	subreddit = '{}/{}'.format(subreddit_name,sorts)
	r = requests.get('http://www.reddit.com/r/{}.json'.format(subreddit),headers={'user-agent': 'Mozilla/5.0'})
	dictn = r.json()
	directory = '.\{}'.format(subreddit_name)
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	for i in range(1,25):
		try:		
			link_image = dictn['data']['children'][i]['data']['url']
			file_name = dictn['data']['children'][i]['data']['url'].split('/')[-1:]
			if len( set(link_image.lower().split('.')) & set(['jpg','png','jpeg','gif']) ) == 1:
				
				if os.path.isfile('./'+subreddit_name+'/'+file_name[0]):
					print('i ',i,' Image already here.')
				else:
					print('i ',i,' New image downloaded. From:',link_image)
					download_image(link_image,'./'+subreddit_name+'/'+file_name[0])
		except:
			print('This image skipped.')


# 1st arg: Subreddit name.
# 2nd arg: new / rising / controversial / top
# 2nd arg may produce errors in rare cases

subreddit_name('memes','top')
