# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SiCKRAGE.
#
# SiCKRAGE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SiCKRAGE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
from sqlalchemy import Column, Integer, Text, Boolean, Index, ForeignKeyConstraint, orm
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from sickrage.core.databases import srDatabase


@as_declarative()
class MainDBBase(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MainDB(srDatabase):
    def __init__(self, name='main'):
        super(MainDB, self).__init__(name)
        MainDBBase.query = self.Session.query_property()
        MainDBBase.metadata.create_all(self.engine)
        for model in MainDBBase._decl_class_registry.values():
            if hasattr(model, '__tablename__'):
                self.tables[model.__tablename__] = model

    class TVEpisode(MainDBBase):
        __tablename__ = 'tv_episodes'
        __table_args__ = (
            ForeignKeyConstraint(['showid', 'indexer'], ['tv_shows.indexer_id', 'tv_shows.indexer']),
            Index('idx_showid_indexer', 'showid', 'indexer'),
            Index('idx_sta_epi_air', 'status', 'episode', 'airdate'),
            Index('idx_sta_epi_sta_air', 'season', 'episode', 'status', 'airdate'),
            Index('idx_status ', 'status', 'season', 'episode', 'airdate'),
            Index('idx_tv_episodes_showid_airdate', 'indexer_id', 'airdate'),
        )

        showid = Column(Integer, index=True, primary_key=True)
        indexer_id = Column(Integer, index=True)
        indexer = Column(Integer, index=True, primary_key=True)
        season = Column(Integer, index=True, primary_key=True)
        episode = Column(Integer, index=True, primary_key=True)
        scene_season = Column(Integer)
        scene_episode = Column(Integer)
        name = Column(Text)
        description = Column(Text)
        subtitles = Column(Text)
        subtitles_searchcount = Column(Integer)
        subtitles_lastsearch = Column(Integer)
        airdate = Column(Integer)
        hasnfo = Column(Boolean)
        hastbn = Column(Boolean)
        status = Column(Integer)
        location = Column(Text)
        file_size = Column(Integer)
        release_name = Column(Text)
        is_proper = Column(Boolean)
        absolute_number = Column(Integer)
        scene_absolute_number = Column(Integer)
        version = Column(Integer, default=-1)
        release_group = Column(Text)

        show = relationship('TVShow', back_populates='episodes', lazy='select')

    class IMDbInfo(MainDBBase):
        __tablename__ = 'imdb_info'
        __table_args__ = (
            ForeignKeyConstraint(['indexer_id'], ['tv_shows.indexer_id']),
        )

        indexer_id = Column(Integer, primary_key=True)
        rated = Column(Text)
        title = Column(Text)
        production = Column(Text)
        website = Column(Text)
        writer = Column(Text)
        actors = Column(Text)
        type = Column(Text)
        votes = Column(Text)
        seasons = Column(Integer)
        poster = Column(Text)
        director = Column(Text)
        released = Column(Text)
        awards = Column(Text)
        genre = Column(Text)
        rating = Column(Text)
        language = Column(Text)
        country = Column(Text)
        runtime = Column(Text)
        imdbid = Column(Text, index=True, unique=True)
        metascore = Column(Text)
        year = Column(Integer)
        plot = Column(Text)
        last_update = Column(Integer)

    class XEMRefresh(MainDBBase):
        __tablename__ = 'xem_refresh'

        indexer_id = Column(Integer, primary_key=True)
        indexer = Column(Integer, primary_key=True)
        last_refreshed = Column(Integer)

    class SceneNumbering(MainDBBase):
        __tablename__ = 'scene_numbering'

        indexer = Column(Integer, primary_key=True)
        indexer_id = Column(Integer, primary_key=True)
        season = Column(Integer, primary_key=True)
        episode = Column(Integer, primary_key=True)
        scene_season = Column(Integer)
        scene_episode = Column(Integer)
        absolute_number = Column(Integer)
        scene_absolute_number = Column(Integer)

    class IndexerMapping(MainDBBase):
        __tablename__ = 'indexer_mapping'

        indexer_id = Column(Integer, primary_key=True)
        indexer = Column(Integer, primary_key=True)
        mindexer_id = Column(Integer)
        mindexer = Column(Integer, primary_key=True)

    class Blacklist(MainDBBase):
        __tablename__ = 'blacklist'

        id = Column(Integer, primary_key=True)
        show_id = Column(Integer)
        keyword = Column(Text)

    class Whitelist(MainDBBase):
        __tablename__ = 'whitelist'

        id = Column(Integer, primary_key=True)
        show_id = Column(Integer)
        keyword = Column(Text)

    class History(MainDBBase):
        __tablename__ = 'history'

        id = Column(Integer, primary_key=True)
        showid = Column(Integer)
        resource = Column(Text)
        season = Column(Integer)
        episode = Column(Integer)
        action = Column(Integer)
        version = Column(Integer, default=-1)
        provider = Column(Text)
        date = Column(Integer)
        quality = Column(Integer)

    class FailedSnatchHistory(MainDBBase):
        __tablename__ = 'failed_snatch_history'

        id = Column(Integer, primary_key=True)
        date = Column(Integer)
        size = Column(Integer)
        release = Column(Text)
        provider = Column(Text)
        showid = Column(Integer)
        season = Column(Integer)
        episode = Column(Integer)
        old_status = Column(Integer)

    class FailedSnatch(MainDBBase):
        __tablename__ = 'failed_snatches'

        id = Column(Integer, primary_key=True)
        release = Column(Text)
        size = Column(Integer)
        provider = Column(Text)
