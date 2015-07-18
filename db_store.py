__author__ = 'shawn'
# interface to couchdb
import couchdb
from datetime import datetime


class DbStore():
    def __init__(self):
        # todo move and then get these from a config
        self.server = 'localhost'
        self.port = 5984
        self.couch = couchdb.Server()
        self.database = self.couch['luc']  # todo -- error check this

    def save_episode(self, episode):
        try:
            air_date = datetime.strptime(episode['airDate'], '%Y-%m-%d').isoformat()

            doc = {'episode':
                       {'name': episode['name'],
                        'airDate': air_date,
                        'writer': episode['writer'],
                        'episodeNumber': episode['episodeNumber'],
                        'type': 'episode'
                       }
            }
            if 'id' in episode:
                doc['id'] = episode['id']

            doc_id = self.database.save(doc)
        except Exception as e:
            print e
        return doc_id

    def save_doc(self, doc):
        doc_id = self.database.save(doc)
        return doc_id

    def get_all_episodes(self):
        view = self.database.list("_design/episodes", "_view/all_episodes")
        return view
