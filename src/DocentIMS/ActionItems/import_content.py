#python 3

import pandas as pd
import openpyxl
from zope.lifecycleevent import modified
import plone.api
from zope.component.hooks import setSite
import transaction
from pandas import *
import os

 
print os.path.abspath(__file__)

setSite(app['Plone'])
portal = plone.api.portal.get()


df = pd.read_excel('ai_import.xlsx')
print(df)

my_dict = df.to_dict(orient='index')

for i in range(0, len(my_dict)):
    title = my_dict[i].get('Title')
    id = my_dict[i].get('ID')
    date = my_dict[i].get('date')
    initial_due_date = my_dict[i].get('initial_due_date')
    texte = my_dict[i].get('text')

    action_item = plone.api.content.create(
                type='Document',
                container=portal,
                title=title,
                date=date,
                initial_due_date=initial_due_date,
                description=texte
    )

     
    a =1 
 


    # for key, value in my_dict[i].items():

   
 