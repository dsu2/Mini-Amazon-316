\COPY Users FROM '/home/vcm/Mini-Amazon-316/db/generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM '/home/vcm/Mini-Amazon-316/db/generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY ProductDetails FROM '/home/vcm/Mini-Amazon-316/db/generated/ProductDetailed.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellers_id_seq',
                         (SELECT MAX(pid)+1 FROM ProductDetails),
                         false);
\COPY Sellers FROM '/home/vcm/Mini-Amazon-316/db/generated/Sellers.csv' WITH DELIMITER ',' NULL '' CSV



\COPY Sellers FROM '/home/vcm/Mini-Amazon-316/db/generated/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellers_id_seq',
                         (SELECT MAX(id)+1 FROM Sellers),
                         false);

\COPY Purchases FROM '/home/vcm/Mini-Amazon-316/db/generated/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY PurchasesDetails FROM '/home/vcm/Mini-Amazon-316/db/generated/PurchasesDetailed.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellers_id_seq',
                         (SELECT MAX(purch_id)+1 FROM PurchasesDetails),
                         false);
                         
\COPY Inventory FROM '/home/vcm/Mini-Amazon-316/db/generated/Inventory.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ProductReviews FROM '/home/vcm/Mini-Amazon-316/db/generated/ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY SellerReviews FROM '/home/vcm/Mini-Amazon-316/db/generated/SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Line_item FROM '/home/vcm/Mini-Amazon-316/db/generated/Line_item.csv' WITH DELIMITER ',' NULL '' CSV
