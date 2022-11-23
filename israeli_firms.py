# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 15:37:17 2022

@author: vaneb
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


# web scraping firm detail data for around 14k Israeli construction firms
# webpage is in hebrew, so splitting string from right to left was performed

def main():
    
    #create list 
    data_list = []
    
    driver = webdriver.Chrome(r'C:\Python\envs\chromedriver')
    
    url = 'https://isra-service.com/%d7%9e%d7%a4%d7%aa-%d7%90%d7%aa%d7%a8/'
    
    driver.get(url)
    
    #get company list class
    list = driver.find_element(By.CLASS_NAME,'wsp-kablankablans-list')
    
    #get lists inside company list class
    firms = list.find_elements(By.TAG_NAME,'li')
    
    links = []
    
    #create list of links in order to avoid page timeout
    for i in range(len(firms)):
    
        links.append(i.find_element(By.TAG_NAME,'a').get_attribute('href'))
    
    #loop through firm list
    for idx, firm_link in enumerate(links):
        
        driver.get(firm_link)
        
        sections = driver.find_elements(By.XPATH,".//*[@class='elementor-widget-wrap elementor-element-populated']")
    
        #MAIN section  = 5
        first_section = sections[5]
        comp_name = first_section.find_element(By.XPATH,".//*[@class='jet-listing-dynamic-field__content']").text
        comp_categories = first_section.find_elements(By.XPATH,".//*[@class='jet-listing-dynamic-terms__link']")
        
        main_data_dict = {'Company_name':comp_name,
                          'Categories':' ,'.join([x.text for x in comp_categories])}
        
        
        data_dict = {}
    
        #First DETAIL section = 11
        sect_data1 = sections[11].find_elements(By.XPATH,".//*[@class='jet-listing-dynamic-field__content']")
    
        #Second DETAIL section = 12
        sect_data2 = sections[12].find_elements(By.XPATH,".//*[@class='jet-listing-dynamic-field__content']")
        
        sect_data = sect_data1 + sect_data2
        
        #List of 16 columns (based on google translator)
        col_names = ['Unknown_column_name','Phone','Known_contrator','Phone_of_contractor',
                     'Name_of_contractor','Contractor_Number','Regis_date','Class_date',
                     'City/town','Write in full','Branch description','Group','Classification',
                     'Scope (in thousands of NIS)','Employees','Note']
                         
    
        #first detail info should be treated as it is, other info is splitted by : (title as col name : text) 
        section_data = [x.text.split(': ')[-1] if idx is not 0 else x.text for idx, x in enumerate(sect_data)]
        
        
        #update dict with section info
        data_dict.update(dict(zip(col_names,section_data)))
               
        #update main dict with detail dict
        main_data_dict.update(data_dict)
        
        #append to list
        data_list.append(main_data_dict)
        
        #back and choose next firm
        driver.back()
            
    #create dataframe from data_list (list of dictionaries)
    df = pd.DataFrame(data_list)
    
    df.to_excel("Company_details.xlsx", index=False)
    print("Web Scrape script executed in ")
    
if __name__ == '__main__':
    
    main()

