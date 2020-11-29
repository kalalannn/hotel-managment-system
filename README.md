# iis-hotel!

run:
    > .\manage.py runserver     # runs server
    > .\manage.py shell         # creates shell with app context
    > .\manage.py restart       # recreates database with default data
    > .\manage.py shell
    or > .\manage.py runserver

role1 = Role('ADMIN')
role2 = Role('DIRECTOR')
role3 = Role('RECEPTIONIST')
role4 = Role('CUSTOMER')
role5 = Role('ANON')

/users: [
    signin,
    signup,
]

<!-- /home: [
    home,
] -->

index => /hostels/list
/hotels: [
    list,
    edit(DIRECTOR) # => ADMIN + DIRECTOR
    delete(DIRECTOR)
]

/users: [
    list(ADMIN),
    edit(self, ADMIN),
    delete(ADMIN)
]

/reservations: [
    new,
    list()
]
