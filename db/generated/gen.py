from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from datetime import datetime

num_users = 1000
num_products = 2000
num_purchases = 10000

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
            email = fake.unique.email()
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            wholeadd = fake.address().split("\n")
            address = wholeadd[0]
            city = wholeadd[1].split(',')[0]
            state = fake.state()
            value = f'{str(fake.random_int(max=500000))}.{fake.random_int(max=99):02}'
            image = fake.image_url(width=200, height=200, placeholder_url='https://picsum.photos/{width}/{height}')
            writer.writerow([uid, email, password, firstname, lastname, address, city, state, value, image])
        print(f'{num_users} generated')
        fake.unique.clear()
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
            des = fake.sentence(nb_words=100)[:-1]
            image = fake.image_url(width=200, height=200, placeholder_url='https://picsum.photos/{width}/{height}')
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, category, available, des, image])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


percent_sellers = 0.5
num_sellers = int(percent_sellers * num_users)


def gen_sellers():
    sids = []
    with open('Sellers.csv', 'w') as f:    
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for sid in range(num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            uid = fake.unique.random_int(0, num_users-1)
            writer.writerow([sid, uid])
            sids.append(sid)
        print(f'{num_sellers} generated')
    fake.unique.clear()
    return sids 


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

def gen_purchases():
    uidpurchdict = {}
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for purch_id in range(num_purchases):
            if purch_id % 100 == 0:
                print(f'{purch_id}', end=' ', flush=True)
            uid = fake.random_int(0, num_users-1)
            time_purchased = fake.date_time()
            writer.writerow([purch_id, uid, time_purchased])
            uidpurchdict[purch_id] = str(uid)
        print(f'{num_purchases} generated')
    return uidpurchdict


def gen_purchases_details(num_purchases, available_pids, prod_dict):
    with open('PurchasesDetailed.csv', 'w') as f:
        writer = get_csv_writer(f)
        print ('purchases details...', end=' ', flush=True)
        for purch_id in range(num_purchases):
            if purch_id % 100 == 0:
                print(f'{purch_id}', end=' ', flush=True)
            num1 = fake.unique.random_int(0, len(available_pids)-1)
            num2 = fake.unique.random_int(0, len(available_pids)-1)
            num3 = fake.unique.random_int(0, len(available_pids)-1)
            fake.unique.clear()
            pid1, pid2, pid3 = available_pids[num1], available_pids[num2], available_pids[num3]

            if pid1 in prod_dict:
                sid = fake.random_element(elements = prod_dict[pid1])
                number = 1 
                if purch_id%2 == 0:
                    fulfill = True
                else:
                    fulfill = False
                writer.writerow([purch_id, pid1, sid, number, fulfill])
            if pid2 in prod_dict:
                sid = fake.random_element(elements = prod_dict[pid2])
                number = 1 
                if purch_id%2 == 0:
                    fulfill = True
                else:
                    fulfill = False
                writer.writerow([purch_id, pid2, sid, number, fulfill])
            if pid3 in prod_dict:
                sid = fake.random_element(elements = prod_dict[pid3])
                number = 1 
                if purch_id%2 == 0:
                    fulfill = True
                else:
                    fulfill = False
                writer.writerow([purch_id, pid3, sid, number, fulfill])
            
        print(f'{num_purchases} purchases details generated')
    return  

def gen_product_review(purchuiddict):
    with open('ProductReviews.csv', 'w') as f:
        with open('PurchasesDetailed.csv', "r") as purchases:
            hasPidUid = set()
            numreviews = 0
            writer = get_csv_writer(f)
            reader = csv.reader(purchases, dialect = 'unix')
            print('Product Reviews...', end = ' ', flush = True)
            for i in reader:
                pid = i[1]
                uid = purchuiddict[int(i[0])]
                if(pid + " " + uid) in hasPidUid:
                    continue
                else:
                    hasPidUid.add(pid + " " + uid)
                    text = fake.sentence(nb_words=100)[:-1]
                    rating = fake.pyint(1, 10)
                    pos = fake.pyint(0, 50)
                    neg = fake.pyint(0, 50)
                    time_purchased = fake.date_time()
                    writer.writerow([pid, uid, text, rating, pos, neg, time_purchased])
                    numreviews += 1
            print(f'{numreviews} generated')
    return


def gen_seller_review(purchuiddict):
    with open('SellerReviews.csv', 'w') as f:
        with open('PurchasesDetailed.csv', "r") as purchases_details:
            numreviews = 0
            writer = get_csv_writer(f)
            reader = csv.reader(purchases_details, dialect = 'unix')
            print('Seller Reviews...', end = ' ', flush = True)
            usedPidSid = set()
            for i in reader:
                sid = i[2]
                uid = purchuiddict[int(i[0])]
                if (uid + " " + sid) in usedPidSid:
                    continue
                else:
                    usedPidSid.add(uid + " " + sid)
                    text = fake.sentence(nb_words=100)[:-1]
                    pos = fake.pyint(0, 50)
                    neg = fake.pyint(0, 50)
                    rating = fake.pyint(1, 10)
                    time_written = fake.date_time()
                    writer.writerow([sid, uid, text, rating, pos, neg, time_written])
                    numreviews += 1
            print(f'{numreviews} generated')
    return   

def gen_line_item(available_sids, available_pids):
    with open('Line_item.csv', 'w') as li:
        used = set()
        writer = get_csv_writer(li)
        print('Line_item...', end = ' ', flush = True)
        for uid in range(num_users):
            num_uniitems = fake.random_int(0,20)
            for item in range(num_uniitems):
                if uid % 100 == 0:
                    print(f'{uid}', end=' ', flush=True)
                sid = fake.random_element(elements=available_sids)
                pid = fake.random_element(elements=available_pids)
                num_item = fake.random_int(0, 10)
                if (str(uid) + " " + str(pid) + " " + str(sid)) in used:
                    continue
                else:
                    used.add((str(uid) + " " + str(pid) + " " + str(sid)))
                    writer.writerow([uid, pid, sid, num_item])
        print(f'{num_uniitems} generated')
    return
    


gen_users(num_users)
available_pids = gen_products(num_products)
sids = gen_sellers()
prod_dict = gen_inventory(sids, available_pids)

uidpurchdict = gen_purchases()
gen_purchases_details(num_purchases, available_pids, prod_dict)

gen_product_review(uidpurchdict)
gen_seller_review(uidpurchdict)
gen_line_item(sids, available_pids)
