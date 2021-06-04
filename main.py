#!venv/bin/python3.8
from bs4 import BeautifulSoup as bs4
import sqlite3
import json
import requests

num_of_cars = int(input("How many cars you want: "))
detailes_type = ('الماركة', 'النوع', 'الفئه', 'الموديل', 'الوارد', 'اللون', 'المواصفات', 'نوع الوقود', 'نوع القير', 'حجم المحرك', 'الحالة', 'الممشى', 'نوع الدفع', 'المنطقة','الجوال', 'السعر')

def get_number(text: str):
    return ''.join([t for t in text if t.isnumeric()])

def main():
    coon = sqlite3.connect('cars_db.sqlite3')
    cursor = coon.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS cars {detailes_type};")
    json_data = {"cars":[]}
    count = 0
    with open('urls.txt', 'r') as f:
        for url in f.readlines():
            if count == num_of_cars:
                break
            else:
                if url != '':
                    try:
                        r = requests.get(url)
                        soup = bs4(r.content, 'html.parser')
                        divs_detailes = soup.find('div', class_="carDetailesCC").find_all('div')
                        try:
                            phone = soup.find('div', class_="callUsPV blueBtn").find('a').text.strip()
                        except Exception:
                            phone = 'None'
                        try:
                            price = get_number(soup.find('div', class_="priceContainer").text.strip())
                        except Exception:
                            price = 'None'
                        car_detailes = {detaile.text.strip().replace('\n', '').split(':')[0]:detaile.text.strip().replace('\n', '').split(':')[1] for detaile in divs_detailes}
                        car_dict = {detaile_type:car_detailes.get(detaile_type, 'None') for detaile_type in detailes_type}
                        car_dict['الجوال'] = phone
                        car_dict['السعر'] = price
                        value = tuple([str(val if val != '' else 'None') for _, val in car_dict.items()])
                        json_data['cars'].append(car_dict)
                        sql = f"INSERT INTO cars {detailes_type} VALUES{value}"
                        cursor.execute(sql)
                        coon.commit()
                        print("Done",count+1)
                        count+=1
                    except Exception as err:
                        if 'find_all' in str(err):
                            pass
                        else:
                            print(err)
                else:
                    pass
        with open('cars_db.json', 'w+') as f:
            json.dump(json_data, f)

if __name__ == '__main__':
    main()