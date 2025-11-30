from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    #returns a collection of all the freebies for the Company.
    freebies = relationship('Freebie', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'
    
    @property
    def devs(self):
        #returns a collection of all devs who collected freebies from this company
        return [freebie.dev for freebie in self.freebies]
    
    def give_freebie(self, dev, item_name, value):
        #creates a new Freebie associated with this company and the given dev
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        return new_freebie
    
    @classmethod
    def oldest_company(cls):
        #returns the Company instance with the earliest founding year
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///freebies.db')
        session = Session(engine)
        return session.query(cls).order_by(cls.founding_year.asc()).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    #returns a collection of all the freebies that the Dev has collected
    freebies = relationship('Freebie', back_populates='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'

    @property
    def companies(self):
        #returns a collection of all companies that this dev has collected freebies from
        return [freebie.company for freebie in self.freebies]
    
    def received_one(self, item_name):
        #returns True if any freebie has the given item_name, otherwise False
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, dev, freebie):
        #changes the freebie's dev to the given dev if it belongs to this dev
        if freebie.dev == self:
            freebie.dev = dev

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    #returns the Dev instance for this Freebie
    dev = relationship('Dev', back_populates='freebies')
    #returns the Company instance for this Freebie
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        #returns formatted string: {dev name} owns a {item_name} from {company name}"""
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'