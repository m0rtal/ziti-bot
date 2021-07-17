from database.database import Database

# orm_database = Database("postgresql://postgres:@192.168.1.11/test")
orm_database = Database("sqlite://database.sqlite")

result = orm_database.get_crawled()
for el in result:
    print(el.crawled_url)
