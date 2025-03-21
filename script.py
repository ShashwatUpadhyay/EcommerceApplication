import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ProductRecommendation.settings'
django.setup()
import pandas as pd 
from shop.models import Product

import csv 
def fill_db_with_flipkart_com():
    csv_file_path = 'Woo_Product_Dummy_Data_Set_Simple_and_Variable.csv' 

    with open(csv_file_path, mode='r' , encoding='utf-8') as file:
        render = csv.DictReader(file)
        for row in render:
                try:
                    product_name = row['product_name']
                    product_image = eval(row['image'])[0]
                    description = row['description']
                    category = row['product_category_tree'].split('>>')[0].strip('[]"')
                    price = row['retail_price']
                    
                    print(product_image,product_image,description,category,price)
                    Product.objects.update_or_create(
                    title = product_name,
                    defaults={
                    'images' : product_image,
                    'description' : description,
                    'category' : category,
                    'price' : price}
                    )
                    print('Data inserted successfully \n\n\n\n\n')
                except Exception as e:
                    print(e)
                    