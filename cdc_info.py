from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pynput.keyboard import Controller, Key
import time
import csv

# Open Erp
driver=webdriver.Chrome()
driver.get('https://erp.iitkgp.ac.in/SSOAdministration/login.htm?sessionToken=B86A9EBDA79E162825E15200683D35DB.worker1&requestedUrl=https://erp.iitkgp.ac.in/IIT_ERP3/')
driver.implicitly_wait(2)

# Set username and password
roll_number=''
passcode=''

# Set answer for any of the 3 questions set for your id
answer_ip=''
while True:
	try:
		driver.implicitly_wait(3)
		userid=driver.find_element_by_name('user_id').send_keys(roll_number)
		password=driver.find_element_by_name('password').send_keys(passcode)
		driver.implicitly_wait(5)
		# question=driver.find_element_by_xpath('//*[@id="question"]')
		# print(question.get_attribute('value'))
		answer=driver.find_element_by_name('answer').send_keys(answer_ip)
		signin=driver.find_element_by_xpath('//*[@id="loginFormSubmitButton"]').click()
		driver.implicitly_wait(3)
		cdc=driver.find_element_by_xpath('//*[@id="moduleUL"]/li[3]/a/strong').click()
		break
	except NoSuchElementException:
		print('Login Failed...Trying again')

driver.maximize_window()
student=driver.find_element_by_xpath('//*[@id="accordion"]/div/div[1]/h3/a').click()
application_for_placement=driver.find_element_by_xpath('//*[@id="collapse2610"]/div/div[1]/a[1]').click()


def get_counts(driver):	
	total=driver.find_element_by_xpath('//*[@id="pager37_right"]/div').text
	curr=total[9:12]
	total=total[-3:]
	return curr,total


ct=0
curr=""
total="121"


rows=[]
while(curr!=total):
	# print('----page break---')
	while(1):
		try:
			driver.switch_to.default_content()
			driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

			# Click inside for scrolling to work inside the table inside the iframe
			click_inside=driver.find_element_by_xpath('//*[@id="'+str(ct)+'"]/td[13]').click()
			company=driver.find_element_by_xpath('//*[@id="'+str(ct)+'"]/td[2]/a').text
			apply_button=driver.find_element_by_xpath('//*[@id="'+str(ct)+'"]/td[6]/a').click()
			# Wait for the popup to load
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable.ui-resizable")))
			

			# Switch to the cooresponding iframe for the company popup 
			driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ui-id-'+str(1+2*ct)+'"]/iframe'))
			WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/form/table/tbody/tr[6]/td/table/tbody/tr[2]/td[2]')))
			
			# Scrape required information
			pay_info=driver.find_element_by_xpath('//*[@id="ftpjnfvw"]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[2]').text
			jd=driver.find_element_by_xpath('//*[@id="ftpjnfvw"]/table/tbody/tr[8]/td').text
			add_info=driver.find_element_by_xpath('//*[@id="ftpjnfvw"]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[3]').text
			cg_criteria=driver.find_element_by_xpath('//*[@id="ftpjnfvw"]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[4]').text


			# Close button isn't accessible from the iframe hence switching back to the parent frame
			driver.switch_to.parent_frame()
			close=driver.find_element_by_xpath('/html/body/div['+str(4+ct)+']/div[1]/button/span[1]').click()
			
			info=[company,pay_info,add_info,cg_criteria,jd]
			rows.append(info)
			ct=ct+1
		
		# Condition for scroll..all companies in current view scraped 
		except NoSuchElementException:
			# all companies scraped
			if(curr==total):	
				break
			keyboard=Controller()
			keyboard.tap(Key.page_down)
			break
	curr,total=get_counts(driver)

col_names=['Company','Salary Info','Additional Criteria','CGPA Criteria','Job Description']
with open('CDC_Internship_All_info', 'w') as f: 
    write = csv.writer(f)    
    write.writerow(col_names) 
    write.writerows(rows) 



	
