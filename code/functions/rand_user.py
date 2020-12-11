import string
import random

from faker import Faker


def create_user():
    mails = ['@gmail.com', '@yandex.ru', '@mail.ru', '@rambler.ru', '@yahoo.com']

    faker = Faker()
    username = faker.name()
    username = username.split(' ')[0]
    if len(username) < 6:
        username += 'qa'
    email = username + random.choice(mails)

    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    password = ''.join(random.choice(chars) for x in range(size))

    return username, email, password