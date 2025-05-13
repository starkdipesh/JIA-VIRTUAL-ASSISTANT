from plyer import notification  #pip install plyer
import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
url = "https://www.cricbuzz.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")
team1 = soup.find_all(class_ = "cb-col-50 cb-ovr-flo cb-hmscg-tm-name")[0].get_text()
team2 = soup.find_all(class_ = "cb-col-50 cb-ovr-flo cb-hmscg-tm-name")[1].get_text()
team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

a = print(f"{team1} : {team1_score}")
b = print(f"{team2} : {team2_score}")

notification.notify(
    title = "IPL SCORE :- ",
    message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
    timeout = 15
)
# <div class="cb-col-50 cb-ovr-flo cb-hmscg-tm-name">…</div>flex
# <div class="cb-ovr-flo" style="display:inline-block; width:100%;">54-2 (11.4)</div>
# <div class="cb-col-50 cb-ovr-flo cb-hmscg-tm-name">…</div>flex