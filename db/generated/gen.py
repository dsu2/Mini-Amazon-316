from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from datetime import datetime

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()
categories = ['Electronics', 'Decor', 'Grocery', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Pets', 'Books', 'Movies', 'Games', 'Golf']

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
            category = fake.random_element(categories)
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, category, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_product_details(num_products):
    with open('ProductDetailed.csv', 'w') as f:
        writer = get_csv_writer(f)
        print ('product details...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            des = fake.sentence(nb_words=100)[:-1]
            image = fake.image_url(width=200, height=200, placeholder_url='https://picsum.photos/{width}/{height}') 
            writer.writerow([pid, des, image])
        print(f'{num_products} product details generated')
    return


num_sellers = 50


def gen_sellers():
    sids = []
    with open('Sellers.csv', 'w') as f:    
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for sid in range(num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            uid = fake.unique.random_int(0, 99)
            writer.writerow([sid, uid])
            sids.append(sid)
        print(f'{num_sellers} generated')
    fake.unique.clear()
    return sids 


def gen_product_review():
    with open('ProductReviews.csv', 'w') as f:
        with open('Purchases.csv', "r") as purchases:
            hasPidUid = set()
            numreviews = 0
            writer = get_csv_writer(f)
            reader = csv.reader(purchases, dialect='unix')
            print('Product Reviews...', end=' ', flush=True)
            for i in reader:
                if (int(i[0]) % 5 == 0):
                    pid = i[2]
                    uid = i[1]
                    if(pid + " " + uid) in hasPidUid:
                        continue
                    else:
                        hasPidUid.add(pid + " " + uid)
                        text = fake.sentence(nb_words=100)[:-1]
                        pos = fake.pyint(0, 50)
                        neg = fake.pyint(0, 50)
                        time_purchased = fake.date_time_between(datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S'), "now")
                        writer.writerow([pid, uid, text, pos, neg, time_purchased])
                        numreviews += 1
            print(f'{numreviews} generated')
    return

def gen_inventory(available_sids, available_pids):
    proddict = {}
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end = ' ', flush = True)
        for i in range(len(available_pids)):
            if i % 100 == 0:
                print(f'{i}', end=' ', flush = True)
            invNum = fake.random_int(0, 1000)
            sid = fake.random_element(elements=available_sids)
            pid = available_pids[i]
            writer.writerow([sid, pid, invNum])
            if pid in proddict:
                proddict[pid] = proddict[pid].append(sid)
            else:
                proddict[pid] = [sid]
        print(f'{len(available_pids)} generated')
    fake.unique.clear()
    return proddict

def gen_purchases(num_purchases, available_pids, prod_dict):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            if pid in prod_dict:
                uid = fake.random_int(min=0, max=num_users-1)
                sid = fake.random_element(elements = prod_dict[pid])
                time_purchased = fake.date_time()
                writer.writerow([id, uid, pid, time_purchased, sid])
            else:
                continue
        print(f'{num_purchases} generated')
    return

def gen_purchases_details(num_purchases):
    with open('PurchasesDetailed.csv', 'w') as f:
        writer = get_csv_writer(f)
        print ('purchases details...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            total_amt = fake.random_int(min=0.00, max=300.00)
            no_of_items = fake.random_int(min=0, max=num_products) 
            writer.writerow([id, total_amt, no_of_items])
        print(f'{num_purchases} purchases details generated')
    return  

def gen_seller_review():
    with open('SellerReviews.csv', 'w') as f:
        with open('Purchases.csv', "r") as purchases:
            numreviews = 0
            writer = get_csv_writer(f)
            reader = csv.reader(purchases, dialect = 'unix')
            print('Seller Reviews...', end = ' ', flush = True)
            usedPidSid = set()
            for i in reader:
                if(int(i[0]) %5 == 0):
                    sid = i[4]
                    uid = i[1]
                    if (uid + " " + sid) in usedPidSid:
                        continue
                    else:
                        usedPidSid.add(uid + " " + sid)
                        text = fake.sentence(nb_words=100)[:-1]
                        pos = fake.pyint(0, 50)
                        neg = fake.pyint(0, 50)
                        time_purchased = fake.date_time_between(datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S'), "now")
                        writer.writerow([sid, uid, text, pos, neg, time_purchased])
                        numreviews += 1
            print(f'{numreviews} generated')
    return   

def gen_line_item(available_sids, available_pids):
    with open('Line_item.csv', 'w') as li:
        used = set()
        writer = get_csv_writer(li)
        print('Line_item...', end = ' ', flush = True)
        for uid in range(num_users):
            num_uniitems = fake.random_int(0,99)
            for item in range(num_uniitems):
                if uid % 100 == 0:
                    print(f'{uid}', end=' ', flush=True)
                sid = fake.random_element(elements=available_sids)
                pid = fake.random_element(elements=available_pids)
                num_item = fake.random_int(0, 1000)
                if (str(uid) + " " + str(pid) + " " + str(sid)) in used:
                    continue
                else:
                    used.add((str(uid) + " " + str(pid) + " " + str(sid)))
                    writer.writerow([uid, pid, sid, num_item])
        print(f'{num_uniitems} generated')
    return
    

'''
gen_users(num_users)
available_pids = gen_products(num_products)
gen_product_details(num_products)
sids = gen_sellers()
prod_dict = gen_inventory(sids, available_pids)
gen_purchases(num_purchases, available_pids, prod_dict)

gen_product_review()
gen_seller_review()
gen_line_item(sids, available_pids)
'''

gen_purchases_details(num_purchases)