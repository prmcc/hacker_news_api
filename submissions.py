
import requests
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Pulling data from API
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status code:', r.status_code)

# Processing information from the API data
submission_ids = r.json() # this API contains only the id #s.
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Call the specific id of the url to get dict data
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(url)
#    print(submission_r.status_code)
    response_dict = submission_r.json()
    
    
    submission_dict = {
            'title' : response_dict['title'],
            'url' : response_dict.get('url', 'None returned'),
            'link' : ('https://hacker-news.firebaseio.com/v0/item/' +str(submission_id) +'.json'), 
            'comments' : response_dict.get('descendants',0)
            }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),reverse=True)

for submission_dict in submission_dicts:
    print('\nTitle:', submission_dict['title'])
    print('Article link:', submission_dict['link'])
    print('Comments:', submission_dict['comments'])

names, plot_dicts = [], []
for submission_dict in submission_dicts:
    names.append(submission_dict['title'])
    plot_dict = {
            'value' : submission_dict['comments'],
            'xlink' : submission_dict['url']
            }
    plot_dicts.append(plot_dict)
    
    
my_style = LS('#445229', base_style=LCS)
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = "Most Popular Stories on HN"
chart.x_labels = names

chart.add('',plot_dicts)
chart.render_to_file('hn_submissions.svg')
