from flask import Flask
from flask import render_template
from flask import request, redirect
import json

app = Flask('DataCleanUpUiTool')
DATA =   {
    "chapter_number": 1,
    "chapter_title": "Chapter 1. Of the Flight from Men, and the Silent Contemplation, and of Dwelling continually in the Cell, [a work] which was composed by Bishop Palladius for the Perfect Lausus",
    "saying": "A certain man said that there were once three men who loved labours, and they were monks. The first one chose to go about and see where there was strife, which he turned into peace ; the second chose to go about and visit the sick ; but the third departed to the desert that he might dwell in quietness. Finally the first man, who had chosen to still the contentions of men, was unable to make every man to be at peace with his neighbour, and his spirit was sad ; and he went to the man who had chosen to visit the sick, and he found him in affliction because he was not able to fulfil the law which he had laid down for himself. Then the two of them went to. the monk in the desert, and seeing each other they rejoiced, and the two men related to the third the tribulations which had befallen them in the world, and entreated him to tell them how he had lived in the desert. And he was silent, but after a little he said unto them, ' Come, let each of us go and fill a vessel of water '; and after they had filled the vessel, he said to them, ' Pour out some of the water into a basin, and look down to the bottom through it,' and they did so. And he said to them, ' What do you see ? ' and they said, ' We see nothing.' And after the water in the basin had ceased to move, he said to them a second time, ' Look into the water,' and they looked, and he said to them, ' What do you see ? ' And they said to him, ' We see our own faces distinctly '; and he said to them, ' Thus is it with the man who dwells with men, for by reason of the disturbance caused by this affair of the world he cannot see his sins ; but if he live in the peace and quietness of the desert he is able to see God clearly.'",
    "saying_count": 2
  }
FILE = '../skill/desert_father_sayings_v2.json'
TAGS = [
 'psalms',
 'fasting',
 'solitude',
 'solitary',
 'humility',
 'miracles',
 'scriptures',
 'vigils',
 'sins',
 'silence',
 'love',
 'obedience',
 'repentance',
 'fornication',
 'watchfulness',
 'abstinence',
 'prayer',
 'patience',
 'poverty',
 'weeping',
 'charity',
 'temptations',
 'QA'
 ]


@app.route('/', methods=["GET"])
def index():
    with open(FILE, 'r') as f:
        sayings = json.load(f)
        for saying in sayings:
            if 'verified' in saying:
                continue
            return redirect('/{}/{}'.format(saying['chapter_number'], saying['saying_count']))


@app.route('/<chapter_number>/<saying_id>', methods=["GET","POST"])
def saying_details(chapter_number, saying_id):
    saying_id = int(saying_id)
    chapter_number = int(chapter_number)
    render_data = {
        'tags': TAGS
    }
    if request.method == "GET":
        render_data['saying_data'] = get_saying_by_id(chapter_number, saying_id)
        print("Got Saying {} with Data {}".format(saying_id, render_data['saying_data']))
        return render_template('index.html', data=render_data)
    if request.method == "POST":
        saying_data = dict(request.form)
        saying_data['chapter_number'] = int(saying_data['chapter_number'])
        saying_data['saying_count'] = int(saying_data['saying_count'])
        saying_data['tags'] = request.form.getlist('tags')
        saying_data['verified'] = True
        print("Saving Saying {}".format(saying_data))

        save_saying(saying_data)
        return redirect('/')


def get_saying_by_id(chapter_number, saying_count):
    with open(FILE, 'r') as f:
        sayings = json.load(f)
        return [x for x in sayings if x['saying_count'] == saying_count and x['chapter_number'] == chapter_number ][0]

def save_saying(saying_data):
    with open(FILE, 'r') as f:
        sayings = json.load(f)
    saying = [x for x in sayings if x['saying_count'] == saying_data['saying_count'] and x['chapter_number'] == saying_data['chapter_number'] ][0]
    for field in saying_data:
        saying[field] = saying_data[field]
    with open(FILE, 'w') as f:
        json.dump(sayings, f)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
