import requests
from bs4 import BeautifulSoup
import os
import time
import datetime
from time import sleep
import tkinter as tk
from tkinter import *

password_evtukhov="KF24snmv"

BASE_URL=f"http://Evtukhov:{password_evtukhov}@extranet.immo.ru/QbillUserReportInterface2/form.php?id=395"
BASE_URL_SIM=f'http://Evtukhov:{password_evtukhov}@extranet.immo.ru/QbillUserReportInterface2/form.php?id=103'

#BASE_URL_EXTRANET="http://Evtukhov:xjvIh5fT@extranet.immo.ru/QbillUserReportInterface2/edit_usertreereports.php"
BASE_DOWNLOAD_URL=f'http://Evtukhov:{password_evtukhov}@extranet.immo.ru/QbillUserReportInterface2/'
#Реторр с авторизацией
BASE_URL_RETORR="http://admin:admin@retorr.vps6221.mtu.immo/export"

DELAY_BETWEEN_RQ = 3

#изначальное значение количества дней, за которые делаем отчет
value_days_ago=1
# directory='Отчет Salute'
#
#report_id='отчет'

#функция поиска на странице ссылки и выдача логического ответа
# def link_search(r):
#     html_code=r.text
#     soup = BeautifulSoup(html_code, 'lxml')
#     link = soup.find('td', attrs={'width': '100%', 'valign': 'top'}).a
#     #print(link['href'])
#     link_found=link
#     return bool (link_found)

#функция по определению даты от которой начинаем отчет
def from_date(value_days_ago):
    value_from_date=datetime.datetime.now() - datetime.timedelta(days=value_days_ago)
    value_from_date=value_from_date.strftime('%Y-%m-%d')
    return value_from_date
#функция по определению вчерашней даты
def yesterday():
    yesterday=datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday=yesterday.strftime('%Y-%m-%d')
    return yesterday

#Функция получения количества дней назад
def get_days_ago():
    global value_days_ago
    value_days_ago= int(entry.get())
    print(f'Расчитываем от {value_days_ago} дней назад')

#сохранение файла Extranet
def download_file(download_href, directory):
    report_id=f'отчет Extranet за {value_days_ago} дн'
    response=requests.get(download_href)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if response.status_code == 200:
        with open(f'{directory}/file_{report_id}.xls', 'wb') as f:
            f.write(response.content)
        print('File downloaded \n')
    else:
        print('Unsuccessfull, статус код:', response.status_code)

#сохранение файла Retorr
def download_file_retorr(download_href, directory):
    report_id=f'отчет Retorr за {value_days_ago} дн'
    response=requests.get(download_href)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if response.status_code == 200:
        with open(f'{directory}/file_{report_id}.csv', 'wb') as f:
            f.write(response.content)
        print('File downloaded \n')
    else:
        print('Unsuccessfull, статус код:', response.status_code)

#Функция по скачиванию всей статистики Салют
def salut_download():
    print('\nНачинаем работу с Extranet Салют общий')
    session=requests.Session()
    r=session.post(BASE_URL,data={
        'date_selected': '1',
        'content_category_selected': '1',
        'sale_kind_selected': '1',
        'uri_selected': '1',
        'transport_selected': '1',
        'cost_selected': '1',
        'quantity_selected': '1',
        'amount_selected': '1',
        'amount_with_nds_selected': '1',
        'next_step': '%C4%E0%EB%E5%E5+%3E%3E',
        'id': '395',
        'step': '0'
    })
    print(r.request.body,'\n')
    r=session.post(BASE_URL, data={
        'date1':from_date(value_days_ago),
        'date2': yesterday(), 
        'salut': '0',
        'agregate': '1',
        'next_step': '%C3%EE%F2%EE%E2%EE',
        'id': '395',
        'step': '1'
    })
    print(r.request.body,'\n')
    sleep(DELAY_BETWEEN_RQ)
    r=session.post(BASE_URL, data={
        'wait':'1',
        'id': '395', 
        'step': '4'
    })
    print(r.request.body,'\n')
    #sleep(DELAY_BETWEEN_RQ)
    html_code=r.text
    soup = BeautifulSoup(html_code, 'lxml')
    try:
        link = soup.find('td', attrs={'width': '100%', 'valign': 'top'}).a        
    except:
        print("Ошибка: не могу найти ссылку")
        sleep(DELAY_BETWEEN_RQ)

    # Выводим найденную ссылку
    print(f'Путь файла получен: {link['href']}')
    #print(href_elements)
    download_href=BASE_DOWNLOAD_URL+link['href']
    print(f'ссылка для скачивания получена {download_href}')
    download_file(download_href, directory='01 - Статистика Салют Extranet')

#Функция по скачиванию всей статистики СИМ-меню
def sim_menu_download():
    print('\nНачинаем работу с Extranet СИМ-меню')
    session=requests.Session()
    r=session.post(BASE_URL_SIM,data={
        'next_step': '%C4%E0%EB%E5%E5+%3E%3E',
        'id': '103',
        'step': '0'
    })
    print(r.request.body,'\n')
    r=session.post(BASE_URL_SIM, data={
        'date1' : from_date(value_days_ago),
        'date2': yesterday(),
        'agregate': '1',
        'country':'',
        'operator':'0',
        'operator_group': '0',
        'point_uri': '0',
        'promotion_type': '0', 
        'business_unit_group':'0', 
        'business_unit':'0',
        'sim_menu_version':'0',
        'product': '17,13,45',
        'next_step': '%C4%E0%EB%E5%E5+%3E%3E',
        'id': '103',
        'step': '1'
    })
    print(r.request.body,'\n')
    sleep(DELAY_BETWEEN_RQ)
    
    r=session.post(BASE_URL_SIM, data={
        'sort[]': '0',
        'next_step': '%C3%EE%F2%EE%E2%EE',
        'id': '103',
        'step': '3'
    })
    print(r.request.body,'\n')

    sleep(DELAY_BETWEEN_RQ)
    sleep(DELAY_BETWEEN_RQ)

    r=session.post(BASE_URL_SIM, data={
        'wait': '1',
        'id': '103', 
        'step': '4'
    })
    print(r.request.body,'\n')
    #sleep(DELAY_BETWEEN_RQ)
   

    #Находим все ссылки, которые есть на последней странице
    # for link in soup.find_all('a'):
    #     print(link.get('href'))

    #Создаем файл html последней страницы для сверки параметров
    # if not os.path.exists('html'):
    #     os.makedirs('html')
    # with open(f'html/file_тестовый.html', 'wb') as f:
    #         f.write(r.content)


    # while True:
    #     if link_search(r)==True:
    #         print('ссылка найдена')
    #         break
    #     else:
    #         print('ссылка не найдена, идет проверка следующей версии страницы')
    #         sleep(DELAY_BETWEEN_RQ)
    #         continue
    
    html_code=r.text
    soup = BeautifulSoup(html_code, 'lxml')
    # Выводим найденную ссылку
    link = soup.find('td', attrs={'width': '100%', 'valign': 'top'}).a
    print(f'Путь файла получен: {link['href']}')
    #формируем ссылку для скачивания
    download_href=BASE_DOWNLOAD_URL+link['href']
    print(f'ссылка для скачивания получена {download_href}')
    #Скачиваем файл
    download_file(download_href, directory='06 - Статистика СИМ-меню Extranet')

#Функция по скачиванию всей статистики Life RB (по сути это 3003)
def life_rb_download():
    print('\nНачинаем работу с Extranet Life RB')
    session=requests.Session()
    r=session.post(BASE_URL,data={
        'date_selected': '1',
        'content_category_selected': '1',
        'sale_kind_selected': '1',
        'uri_selected': '1',
        'transport_selected': '1',
        'cost_selected': '1',
        'quantity_selected': '1',
        'amount_selected': '1',
        'amount_with_nds_selected': '1',
        'next_step': '%C4%E0%EB%E5%E5+%3E%3E',
        'id': '395',
        'step': '0'
    })
    print(r.request.body,'\n')
    r=session.post(BASE_URL, data={
        'date1':from_date(value_days_ago),
        'date2': yesterday(), 
        'salut': '9',
        'agregate': '1',
        'next_step': '%C3%EE%F2%EE%E2%EE',
        'id': '395',
        'step': '1'
    })
    print(r.request.body,'\n')
    sleep(DELAY_BETWEEN_RQ)
    r=session.post(BASE_URL, data={
        'wait':'1',
        'id': '395', 
        'step': '4'
    })
    print(r.request.body,'\n')
    #sleep(DELAY_BETWEEN_RQ)
    html_code=r.text
    soup = BeautifulSoup(html_code, 'lxml')
    try:
        link = soup.find('td', attrs={'width': '100%', 'valign': 'top'}).a        
    except:
        print("Ошибка: не могу найти ссылку")
        sleep(DELAY_BETWEEN_RQ)

    # Выводим найденную ссылку
    print(f'Путь файла получен: {link['href']}')
    #print(href_elements)
    download_href=BASE_DOWNLOAD_URL+link['href']
    print(f'ссылка для скачивания получена {download_href}')
    download_file(download_href, directory='04 - Лайф РБ - weekly')  


#функция определяющая дату вчерашнего дня для Retorr
def whats_time_yesterday():
    #Выясняем текущую дату и время
    time_now=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=3)
    yesterday=time_now-datetime.timedelta(days=value_days_ago)
    #Форматируем под удобный нам формат 06.03.2024
    yesterday_format=yesterday.strftime('%d.%m.%Y')
    return yesterday_format

#функция определяющая дату сегодняшнего дня для Retorr
def whats_time_today():
    #Выясняем текущую дату и время
    time_now=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=3)
    #yesterday=time_now-datetime.timedelta(days=1)
    #Форматируем под удобный нам формат 06.03.2024
    time_now_format=time_now.strftime('%d.%m.%Y')
    return time_now_format



#Функция по скачиванию статистики Retorr
def retorr_download():
    print('\n Начинаем работу с Retorr')
    r=requests.get(BASE_URL_RETORR,params={
        '_token': 'DN95RdG841SbW8TLKmPAHr3xOf9KBFrPdTDZE51H',
        'dateFrom': f'{whats_time_yesterday()} 00:00',
        'dateTo': f'{whats_time_today()} 00:00',
        'msisnds[]': '',
        'actions[]': 'pay',
        'operators[]': '',
        'selected_methods[]': '',
    })       
#     print(r.url)   
#    # print(r.text)
#     if not os.path.exists('html_retorr_test'):
#         os.makedirs('html_retorr_test')
#     with open(f'html_retorr_test/file_тестовый.html', 'wb') as f:
#             f.write(r.content)
#     html_code=r.text
    # soup = BeautifulSoup(html_code, 'lxml')
    # inputs=soup.find_all('input', {'type':'submit'})
    # for input in inputs:
    #     if input['value']=='Файл':
    #         url_file=input['formaction']
    #         print(url_file)
    
    #формируем ссылку для скачивания
    download_href = f'{r.url}'
    print(f'ссылка для скачивания получена {download_href}')
    #Скачиваем файл
    download_file_retorr(download_href, directory='07 - Статистика Интернет-проекты Retorr')

root=tk.Tk()
root.title("Отчеты Extranet")
root.geometry("250x280")

button1=tk.Button(root, text="Salute общий", command=salut_download)
button2=tk.Button(root, text="Salute СИМ-меню", command=sim_menu_download)
button3=tk.Button(root, text="Retorr инетрент-проекты", command=retorr_download)
button4=tk.Button(root, text="Salute Life RB еженедельный", command=life_rb_download)

button1.pack()
button2.pack()
button3.pack()
button4.pack()

entry=Entry(root, width=5)
entry.pack()
button5=Button(root, text="дней назад", pady=10, command=get_days_ago)

button5.pack()

root.mainloop()

