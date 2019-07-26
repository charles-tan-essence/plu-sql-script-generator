# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:24:29 2019

@author: charles.tan
"""

'''
Take in 3 columns:
    1. PLU Name
    2. PLU ID (Audience List ID)
    3. Corresponding AD ID
    
Output a .sql file
'''

def define_lists(plu_names, plu_ids, ad_ids):
    plu_names_list = plu_names.split('\n')
    plu_ids_list = plu_ids.split('\n')
    ad_ids_list = ad_ids.split('\n')
    
    if plu_names_list[-1] == '' and (plu_ids_list[-1] == '' and \
                     ad_ids_list[-1] == ''):
        del plu_names_list[-1]
        del plu_ids_list[-1]
        del ad_ids_list[-1]
    else:
        print('Please check the final file')
    
    return(plu_names_list, plu_ids_list, ad_ids_list)

def generate_when_then_string(plu_names, plu_ids, ad_ids):
    when_then_string = ''
    if len(plu_names) == len(plu_ids) and\
    len(plu_ids) == len(ad_ids) and\
    len(ad_ids) == len(plu_names):
        for i in range(len(plu_names)):
            when_then_string += ('-- '+plu_names[i]+': '+plu_ids[i]+'\nWHEN ad_in IN ('+ad_ids[i]+')\nTHEN '+plu_ids[i]+'\n')
        when_then_string = when_then_string[:-2] # remove the last newline
        return(when_then_string)
    else:
        raise Exception('Length of data not equal')

def generate_ad_id_strings(ad_ids):
    the_string = ''
    for ad_id in ad_ids:
        the_string += (ad_id+',')
    the_string = the_string[:-1] # to drop that last comma
    return(the_string)




def create_sql_file(filename, campaign_start_date, campaign_end_date,
                    contact_name, contact_region, plu_names,
                    plu_ids, ad_ids):
    
    plu_names, plu_ids, ad_ids = define_lists(plu_names, plu_ids, ad_ids)
    
    print(plu_names)
    print(plu_ids)
    print(ad_ids)
    
    sql_string = \
'''#StandardSQL
/*
Campaign Start Date: 
'''+campaign_start_date+'''
Campaign End Date:
'''+campaign_end_date+'''
Contact:
'''+contact_name+''' ('''+contact_region+''')
*/
SELECT
CASE
'''+generate_when_then_string(plu_names, plu_ids, ad_ids)+'''
END AS list_id,
user_id AS cookie_encrypted
FROM `essence-dt-raw.5295.impressions_2542116`
WHERE _PARTITIONTIME BETWEEN TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL
3
DAY)) AND CURRENT_TIMESTAMP()
AND ad_id IN (
'''+generate_ad_id_strings(ad_ids)+'''
 )
AND user_id <> '0'
GROUP BY list_id, 
cookie_encrypted
'''
    with open(filename, 'w') as f:
        f.write(sql_string)