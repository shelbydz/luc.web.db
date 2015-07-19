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
            if 'id' in episode:
                # See if this already exists in the db:
                existing_doc = self.database[episode['id']]
                existing_doc['episode']['name'] = episode['name']
                existing_doc['episode']['airDate'] = episode['airDate']
                existing_doc['episode']['writer'] = episode['writer']
                existing_doc['episode']['episodeNumber'] = int(episode['episodeNumber'])
                doc_id = self.database.save(existing_doc)
            else:
                air_date = datetime.strptime(episode['airDate'], '%Y-%m-%d').isoformat()
                doc = {'episode':
                                dict(name=episode['name'], airDate=air_date, writer=episode['writer'],
                                    episodeNumber=episode['episodeNumber'], type='episode')
                }
                doc_id = self.database.save(doc)
        except Exception as e:
            print e
        return doc_id

    def save_doc(self, doc):
        doc_id = self.database.save(doc)
        return doc_id

    def get_all_episodes(self, query):
        view = []
        if query is None:
            view = self.database.list("_design/episodes", "_view/all_episodes")
        else:
            view = self.database.list("_design/episodes", "_view/all_episodes", query)
        return view
