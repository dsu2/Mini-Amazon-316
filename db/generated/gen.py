from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

num_sellers = 50
def gen_sellers():
    available_sids = []
    with open('Sellers.csv', 'w') as f:    
        writer = get_csv_writer(f)
        print('Sellers...', end= ' ', flush = True)
        for sid in range(num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            uid = fake.unique.random_int(0, 100)
            writer.writerow([sid, uid])
            available_sids.append(sid)
        print(f'{num_sellers} generated')
    fake.unique.clear()
    return available_sids 

numreviews = 1000
def gen_product_review():
    with open('ProductReviews.csv', 'w') as f:
        with open('Purchases.csv', "r") as purchases:
            writer = get_csv_writer(f)
            reader = csv.reader(purchases, dialect = 'unix')
            print('Product Reviews...', end = ' ', flush = True)
            for i in reader:
                if(int(i[0]) %5 == 0):
                    pid = i[2]
                    uid = i[1]
                    text = fake.sentence(nb_words=100)[:-1]
                    pos = fake.pyint(0, 50)
                    neg = fake.pyint(0, 50)
                    writer.writerow([pid, uid, text, pos, neg])
            print(f'{numreviews} generated')
    return

def gen_inventory(available_sids):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end = ' ', flush = True)
        for pid in range(num_products-1):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush = True)
            invNum = fake.random_int(0, 1000)
            sid = fake.random_element(elements=available_sids)
            pid = fake.unique.random_int(0, (num_products-1))
            writer.writerow([sid, pid, invNum])
        print(f'{num_products} generated')
    fake.unique.clear()
    return

gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
available_sids = gen_sellers()
gen_product_review()
gen_inventory(available_sids)