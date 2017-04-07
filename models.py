from sqlalchemy import create_engine, orm
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float, Table
from datetime import datetime
from auth import hash_password
import uuid

engine = create_engine('mysql+mysqldb://u:p@localhost/baseball', echo = True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#region cross tables
users_x_sports = Table(
    'users_x_sports',
    Base.metadata,
    Column('iduser', Integer, ForeignKey('users.id')),
    Column('idsport', Integer, ForeignKey('sports.id'))
)

users_x_leagues = Table(
    'users_x_leagues',
    Base.metadata,
    Column('iduser', Integer, ForeignKey('users.id')),
    Column('idleagues', Integer, ForeignKey('leagues.id'))
)

sports_x_leagues = Table(
    'sports_x_leagues',
    Base.metadata,
    Column('idsport', Integer, ForeignKey('sports.id')),
    Column('idleagues', Integer, ForeignKey('leagues.id'))
)

teams_x_leagues = Table(
    'teams_x_leagues',
    Base.metadata,
    Column('idteams', Integer, ForeignKey('teams.id')),
    Column('idleagues', Integer, ForeignKey('leagues.id'))
)

teams_x_seasons = Table(
    'teams_x_seasons',
    Base.metadata,
    Column('idteams', Integer, ForeignKey('teams.id')),
    Column('idseasons', Integer, ForeignKey('seasons.id'))
)

users_x_teams = Table(
    'users_x_teams',
    Base.metadata,
    Column('iduser', Integer, ForeignKey('users.id')),
    Column('idteam', Integer, ForeignKey('teams.id'))
)

#end region

#region framework tables
class BaseExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        if instance.active:
            instance.active = 1
        else:
            instance.active = 0
        instance.datecreated = datetime.now()
        instance.datemodified = datetime.now()
        instance.rowstamp = uuid.uuid4()
    def before_update(self, mapper, connection, instance):
        instance.datemodified = datetime.now()

class BaseUserExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        if instance.active:
            instance.active = 1
        else:
            instance.active = 0
        instance.datecreated = datetime.now()
        instance.datemodified = datetime.now()
        instance.rowstamp = uuid.uuid4()
        hashed = hash_password(instance.password)
        instance.password = hashed.split('$')[0]
        instance.salt = hashed.split('$')[1]
    def before_update(self, mapper, connection, instance):
        instance.datemodified = datetime.now()

class Users(Base):
    __tablename__ = 'users'
    __mapper_args__ = { 'extension' : BaseUserExtension() }
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = 1)
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))
    salt = Column(String(255))
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    profiles = orm.relationship('Profiles', backref = 'user')
    #leagues_owned = orm.relationship('Leagues', backref = 'user')
    sports = orm.relationship('Sports', secondary = users_x_sports, backref='users')
    leagues = orm.relationship('Leagues', secondary = users_x_leagues, backref='users')
    teams = orm.relationship('Teams', secondary = users_x_teams, backref='users')

    def __init__(self, active, firstname, lastname, username, email, password):
        self.active = active
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.firstname, self.lastname, self.rowstamp)
#end region

#region person tables
class Profiles(Base):
    __tablename__ = 'profiles'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    iduser = Column(Integer, ForeignKey('users.id'))
    idprofiletype = Column(Integer, ForeignKey('profiletypes.id'))
    active = Column(Boolean, default = 1)
    description = Column(Text)
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    
    images = orm.relationship('Images', backref = 'profile')

    def __init__(self, active, description):
        self.active = active
        self.description = description

    def __repr__(self):
       return "<User('%s','%s')>" % (self.description, self.rowstamp)

class ProfileTypes(Base):
    __tablename__ = 'profiletypes'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = 1)
    name = Column(String(50)) #player, coach, commissioner, spectator
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    profiles = orm.relationship('Profiles', backref = 'profiletype')

    def __init__(self, active, name):
        self.active = active
        self.name = name

    def __repr__(self):
       return "<User('%s','%s')>" % (self.name, self.rowstamp)

class Images(Base):
    __tablename__ = 'images'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    idprofile = Column(Integer, ForeignKey('profiles.id'))
    active = Column(Boolean, default = 1)
    name = Column(String(100))
    imageurl = Column(String(255))
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))

    def __init__(self, active, name, imageurl):
        self.active = active
        self.name = name
        self.imageurl = imageurl

    def __repr__(self):
       return "<User('%s','%s')>" % (self.name, self.rowstamp)
#end region

#region organization tables
class Sports(Base):
    __tablename__ = 'sports'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = 1)
    name = Column(String(50))
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    leagues = orm.relationship('Leagues', secondary = sports_x_leagues, backref='sports')

    def __init__(self, active, name):
        self.active = active
        self.name = name

    def __repr__(self):
       return "<User('%s', '%s')>" % (self.name, self.rowstamp)

class Leagues(Base):
    __tablename__ = 'leagues'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    commissioner = Column(Integer, ForeignKey('users.id'))
    active = Column(Boolean, default = 1)
    name = Column(String(50))
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    seasons = orm.relationship('Seasons', backref = 'league')
    teams = orm.relationship('Teams', secondary = teams_x_leagues, backref='leagues')

    def __init__(self, active, name):
        self.active = active
        self.name = name

    def __repr__(self):
       return "<User('%s', '%s')>" % (self.name, self.rowstamp)

class Seasons(Base):
    __tablename__ = 'seasons'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    idleague = Column(Integer, ForeignKey('leagues.id'))
    idseasontype = Column(Integer, ForeignKey('seasontypes.id'))
    active = Column(Boolean, default = 1)
    datestart = Column(DateTime)
    dateend = Column(DateTime)
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    teams = orm.relationship('Teams', secondary = teams_x_seasons, backref='seasons')

    def __init__(self, active, datestart, dateend):
        self.active = active
        self.datestart = datestart
        self.dateend = dateend

    def __repr__(self):
       return "<User('%s', '%s', '%s')>" % (self.datestart, self.dateend, self.rowstamp)

class SeasonTypes(Base):
    __tablename__ = 'seasontypes'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    idprofile = Column(Integer, ForeignKey('profiles.id'))
    active = Column(Boolean, default = 1)
    name = Column(String(50)) #player, coach, commissioner, spectator
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))
    seasons = orm.relationship('Seasons', backref = 'seasontype')

    def __init__(self, active, name):
        self.active = active
        self.name = name

    def __repr__(self):
       return "<User('%s','%s')>" % (self.name, self.rowstamp)

class Teams(Base):
    __tablename__ = 'teams'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    active = Column(Boolean, default = 1)
    name = Column(String(100))
    description = Column(Text)
    rank = Column(Integer)
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))

    def __init__(self, active, name, description, rank):
        self.active = active
        self.name = name
        self.description = description
        self.rank = rank

    def __repr__(self):
       return "<User('%s', '%s', '%s')>" % (self.name, self.rank, self.rowstamp)
#end region

#region game tables
class Games(Base):
    __tablename__ = 'games'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    idhometeam = Column(Integer, ForeignKey('teams.id'))
    idawayteam = Column(Integer, ForeignKey('teams.id'))
    idseason = Column(Integer, ForeignKey('seasons.id'))
    idleague = Column(Integer, ForeignKey('leagues.id'))
    idwinner = Column(Integer, ForeignKey('teams.id'))
    innings = orm.relationship('Innings', backref = 'game')
    active = Column(Boolean, default = 1)
    dateplayed = Column(DateTime)
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))

    def __init__(self, active):
        self.active = active

    def __repr__(self):
       return "<User('%s', '%s', '%s', '%s')>" % (self.idhometeam, self.idawayteam, self.dateplayed, self.rowstamp)

class Innings(Base):
    __tablename__ = 'innings'
    __mapper_args__ = { 'extension' : BaseExtension() }
    id = Column(Integer, primary_key = True)
    idgame = Column(Integer, ForeignKey('games.id'))
    inning = Column(Integer)
    half = Column(String(10))
    hits = Column(Integer)
    runs = Column(Integer)
    errors = Column(Integer)
    
    datecreated = Column(DateTime)
    datemodified = Column(DateTime)
    rowstamp = Column(String(50))

    def __init__(self, active, inning, half, hits, runs, errors):
        self.active = active
        self.inning = inning
        self.half = half
        self.hits = hits
        self.runs = runs
        self.errors = errors

    def __repr__(self):
       return "<User('%s', '%s', '%s', '%s')>" % (self.inning, self.hits, self.runs, self.errors)
#end region

users_table = Users.__table__
profiletypes_table = ProfileTypes.__table__
profiles_table = Profiles.__table__
images_table = Images.__table__
sports_table = Sports.__table__
leagues_table = Leagues.__table__
seasons_table = Seasons.__table__
seasontypes_table = SeasonTypes.__table__
teams_table = Teams.__table__
games_table = Games.__table__
innings_table = Innings.__table__

metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(engine)
