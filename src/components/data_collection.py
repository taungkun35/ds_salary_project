import os
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    service = Service(executable_path="chromedriver.exe")
    options = Options()
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        time.sleep(10)
        job_buttons = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
        for job_button in job_buttons:

            job_button.click()
            time.sleep(1)

            try:
                driver.find_element(By.XPATH,".//span[@class='SVGInline modal_closeIcon']").click() #clicking to the X.
                time.sleep(1)
            except NoSuchElementException:
                time.sleep(1)
                pass

            
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            #Scrape
            try:
                company_name = driver.find_element(By.XPATH,"//div[@class='css-87uc0g e1tk4kwz1']").text
            except NoSuchElementException:
                company_name = -1 
            
            try:
                location = driver.find_element(By.XPATH,"//div[@class='css-56kyx5 e1tk4kwz5']").text
            except NoSuchElementException:
                location = -1

            try:
                job_title = driver.find_element(By.XPATH,"//div[@class='css-1vg6q84 e1tk4kwz4']").text
            except NoSuchElementException:
                job_title = -1

            try:
                job_description = driver.find_element(By.XPATH,"//div[@class='jobDescriptionContent desc']").text
            except NoSuchElementException:
                job_description = -1

            try:
                salary_estimate = driver.find_element(By.XPATH,"//div[@class='css-19txzrf e14vl8nk0']//span[@data-test='detailSalary']").text
            except NoSuchElementException:
                salary_estimate = -1
            
            try:
                rating = driver.find_element(By.XPATH,"//span[@class='css-1m5m32b e1tk4kwz2']").text
            except NoSuchElementException:
                rating = -1 
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            
            '''
            try:
                #<div class="infoEntity">
                #    <label>Headquarters</label>
                #    <span class="value">San Francisco, CA</span>
                #</div>
                headquarters = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
            except NoSuchElementException:
                headquarters = -1
            
            try:
                competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            except NoSuchElementException:
                competitors = -1
            '''

            try:
                size = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text
            except NoSuchElementException:
                size = -1
            
            try:
                type_of_ownership = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                sector = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text
            except NoSuchElementException:
                sector = -1

            try:
                industry = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text
            except NoSuchElementException:
                industry = -1

            try:
                founded = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text
            except NoSuchElementException:
                founded = -1

            try:
                revenue = driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text
            except NoSuchElementException:
                revenue = -1
            
            if verbose:
                #print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                #print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            

            jobs.append({
                "Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue
            })
            #"Headquarters" : headquarters,
            #"Competitors" : competitors

        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,"//span[@alt='next-icon']").click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

if __name__ == '__main__':
    df = get_jobs('data scientist',1000,False)
    df.to_csv(os.path.join('notebook','data','data.csv'),index=False)