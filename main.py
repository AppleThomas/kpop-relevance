from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt

# Google stuff

# Choose options for Chrome window opened by selenium
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# create a webdriver with our desired options
driver = webdriver.Chrome(options=chrome_options)

# get url for search
url = "https://news.google.com/search?q=kpop"
driver.get(url)

# wait a second for it to load
time.sleep(2)
scroll_pause_time = 1

# get the screen height so we can track how much we have loaded
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
  # using the selenium driver, scroll until the screen is a specific height
  driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(
    screen_height=screen_height, i=i))
  i += 1
  # pause for the scroll to complete
  time.sleep(scroll_pause_time)
  # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
  scroll_height = driver.execute_script("return document.body.scrollHeight;")
  # Break the loop when the height we need to scroll to is larger than the total scroll height
  if (screen_height) * i > scroll_height:
    break

# grab the source code for the page and parse the html
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html5lib')

#all done! Close the driver
driver.quit()

# Actual Algorithm bit

# make txt file into a list
text_file = open('groups.txt', 'r')
groups = text_file.read().splitlines()
text_file.close()

#make a dict for groups
groups_found = dict()

for heading in soup.findAll('h3', class_='ipQwMb ekueJc RD0gLb'):
  #grab the title text from the articles
  title = heading.find('a', class_='DY5T1d RZIKme').text

  # see if any groups match in heading
  # if it does, either add or increment the group to the dict
  for i in groups:
    if i in title or i.upper() in title:
      if i in groups_found:
        groups_found[i] += 1
      else:
        groups_found.update({i: 1})

# make summary file
fileOut = open("kpopsumrev.txt", "w")

for i in groups_found:
  fileOut.write(i + "\n")
  for heading in soup.findAll('h3', class_='ipQwMb ekueJc RD0gLb'):
  #grab the title text from the articles
    title = heading.find('a', class_='DY5T1d RZIKme').text

    if i in title or i.upper() in title:
      fileOut.write("-- " + title + "\n")
  fileOut.write("\n")
fileOut.close()

# sort the dictionary in reverse order
groups_sorted = dict(
  sorted(groups_found.items(), key=lambda item: item[1], reverse=True))

# make bar graph of the data
names = list(groups_sorted.keys())
values = list(groups_sorted.values())
plt.bar(range(len(groups_sorted)), values, tick_label=names, color='pink')

plt.title("Kpop Group Relevance in Google News")
plt.ylabel("Number of Times Appeared")
plt.xlabel("Groups")

# makes the group names vertical
plt.xticks(range(len(groups_sorted)), groups_sorted, rotation=90)

# makes it so the names aren't cutoff
plt.tight_layout()

# saves a copy of the data
plt.savefig('results.png', dpi=400)

plt.show()    
  
