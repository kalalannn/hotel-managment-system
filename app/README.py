# на примере юзера объясняю, как работает ORM (object-relational mapping)

''' User model '''
class User(Base):
    __tablename__  = 'users'

    # тут классически описываем поля из таблицы базы данных
    # используем типы данных из библиотеки SQL Alchemy. они автоматом переводятся в типы данных используемой БД
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    birth_date = Column(Date)

    # классический внешний ключ
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    # а вот тут новая инфа
    # внешним ключом связываются таблицы в реляционной БД, но объектам в питоне не ясно, что такое внешний ключ
    # и в этой части мы как раз отражаем связь таблиц в связь объектов

    # смотрим ERD -> роль и юзер связаны, значит и их объекты должны быть связаны.
    role = relationship('Role', back_populates='user', uselist=False) # создается связь между объектами
    # role - поле, которое в дальнейшем вернет нам объект роль из юзера
    # 'Role' - название класса, с которым связываемся
    #
    # back_populates='user' - обратная связь с объекта роль на объект юзер. 
    # ВАЖНО: аналогичное поле должно быть у класса Роль. выглядит вот так:
    user = relationship('User', back_populates='role')
    # благодаря двум таким связям мы потом сможем из одного объекта переходить на другой и обратно
    # uselist=False означает, что связь 1 к 1.
    #
    # названия полей должны соответствовать
    role = relationship('Role', back_populates='user', uselist=False)
    # \_________________________________________|_
    #   _______________________________________|  \
    #  |                                           \
    user = relationship('User', back_populates='role') 
    # в конструктор потом передаем не внешний ключ role_id, а объект role
    #
    # остальное по аналогии
    hotels = relationship('Hotel', back_populates='owner')
    reserv_cust = relationship('Reservation', back_populates='customer')
    reserv_resept = relationship('Reservation', back_populates='receptionist')
    feedbacks = relationship("Feedback", back_populates="user")

    def __init__(self, username, password, first_name, last_name, email, birth_date, role):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.role = role