import requests
import json
from bs4 import BeautifulSoup

habr_link = "https://career.habr.com/vacancies?type=all&page="

with open('vacancies.json', 'r', encoding="utf8") as f:
    vacancies_data = json.load(f)


def main():
    for page in range(1, 11):
        vacancies = requests.get(habr_link + str(page))
        sp = BeautifulSoup(vacancies.content, "html.parser")
        all_cards = sp.find_all("div", class_="vacancy-card__info")
        for card in all_cards:
            company = card.find("div", class_="vacancy-card__company-title")
            vacancy_name = card.find("div", class_="vacancy-card__title")
            vacancy_additions = card.find("div", class_="vacancy-card__meta")
            vacancy_skills = card.find("div", class_="vacancy-card__skills")
            link = card.find("div", class_="vacancy-card__title")
            vacancy_link = "https://career.habr.com/" + link.a["href"]
            vacancy_page = requests.get(vacancy_link)
            vacancy_content = BeautifulSoup(vacancy_page.content, "html.parser")
            vacancy_description = vacancy_content.find("div", class_="style-ugc").extract()

            vacancies_data["list"][link.a["href"]] = {}
            vacancies_data["list"][link.a["href"]]["company_name"] = company.a.string
            vacancies_data["list"][link.a["href"]]["vacancy_name"] = vacancy_name.a.string
            vacancies_data["list"][link.a["href"]]["vacancy_additions"] = vacancy_additions.get_text()
            vacancies_data["list"][link.a["href"]]["vacancy_skills"] = vacancy_skills.get_text()
            vacancies_data["list"][link.a["href"]]["vacancy_description"] = vacancy_description.get_text()
            print("Получено ", len(vacancies_data["list"]), " вакансий.")

    with open('vacancies.json', 'w', encoding="utf8") as f:
        json.dump(vacancies_data, f)


if __name__ == '__main__':
    main()
