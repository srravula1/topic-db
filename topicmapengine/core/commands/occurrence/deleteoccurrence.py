"""
DeleteOccurrence class. Part of the StoryTechnologies project.

July 13, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicmapengine.core.topicstoreerror import TopicStoreError
from topicmapengine.core.commands.attribute.deleteattributes import DeleteAttributes


class DeleteOccurrence:

    def __init__(self, database_path, map_identifier, identifier=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:  # https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager
                connection.execute("DELETE FROM occurrence WHERE topicmap_identifier = ? AND identifier = ?", (self.map_identifier, self.identifier))
            DeleteAttributes(self.database_path, self.map_identifier, self.identifier).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()