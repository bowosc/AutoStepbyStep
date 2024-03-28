import openai, math, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 


# gpt setup stuff
openai.api_key = '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'
messages = [ {"role": "system", "content":  
              "You are a intelligent assistant."} ] 
# the prompt machine, actually asks the questions
def askgpt(question):   
  messages.append(
      {"role": "user", "content": question},
  )
  chat = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", messages=messages
  )

  reply = chat.choices[0].message.content
  return(reply)
  messages.append({"role": "assistant", "content": reply})

# driver stuff, selenium prep, logging into codestepbystep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=2400,1200")
driver = webdriver.Chrome(options=chrome_options)

action = ActionChains(driver) 

driver.get("https://www.codestepbystep.com/login")
element = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/form/div/div[1]/input')
element.send_keys("bowiee")
element = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/form/div/div[2]/input')
element.send_keys("3.141592")
element = driver.find_element(By.XPATH, '//*[@id="submitbutton"]')
element.click()
driver.get("https://www.codestepbystep.com/problem/view/java/parameters/getFirstDigit")

print("signin complete, first page loaded")


# runnin' through the site
for i in range(2):
    prompt = driver.find_element(By.XPATH, '//*[@id="description"]').text
    print("prompted")

    response = askgpt(prompt + ". Please respond with written code, in the Java programming language. Follow the above instructions EXACTLY as they are written - for example, if it asks for a method, include only a method (not a class). Please use tabs instead of spaces to indent the code. I'll tip you a 50 for your trouble IF and only if you truly include nothing at all in your response other than code. Thanks!")
    print("response produced:")
    response = response[:response.rfind('```')]
    response = response.split('```')[1]
    response = response.replace("    ", "")
    response = response.replace("java", "")
    print(response)
    
    
    #find box and enter response
    codebox = driver.find_element(By.CLASS_NAME, "CodeMirror")
    action.click(codebox).perform()
    
    #for i in range(200):
    #    action.send_keys(Keys.BACKSPACE)

    action.send_keys(response).perform()
    print("typed response")


    #click submit (control-s is keybinded on this page to press submit)
    ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .send_keys('s') \
        .key_up(Keys.CONTROL) \
        .perform()
    

    print('response submitted')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nextlink'))).click()



print("all done :)")



















# original gpt thing, too afraid to delete in case i need a replacement after breaking something 
'''
def askgpt(question):   
  messages.append(
      {"role": "user", "content": question},
  )
  chat = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo", messages=messages
  )

  reply = chat.choices[0].message.content
  print(f"ChatGPT : {reply}")
  messages.append({"role": "assistant", "content": reply})
  return(reply)
  '''