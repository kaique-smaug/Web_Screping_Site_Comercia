from requests import get
from bs4 import BeautifulSoup
from src.json_exporter.write_json import Json
from re import search

class Scraper:
    def __init__(self):
        self._product = None
        self._list_name = []
        self._list_current_price = []
        self._list_old_price = []
        self._list_categories = []
        self._list_description = []
        self.__column_one_table = []
        self.__column_two_table = []
        self._list_name_people_review = []
        self._list_date_people_review = []
        self._list_score_people_review = []
        self._list_text_review = []
        self._list_score = []

    def _fetch_page(self) -> None:
        self._response = get('https://infosimples.com/vagas/desafio/commercia/product.html')
        
        if self._response.status_code == 200:
            return self._response.text
        
        else:
            raise Exception(f"Erro ao acessar a página: {self._response.status_code}")
    
    def extract_text_list(self, value, list) -> list:

        for response in value:
            if response != '':
                
                list.append(response.get_text())
            else:
                list.append('')
        
        return list
    
    def main(self):
        self._response__fetch_page = self._fetch_page()
        self._ressponse_html = self._response__fetch_page
        self._response_bs = BeautifulSoup(self._ressponse_html, 'html.parser')
        self._response_Json_intancce = Json()

        self._product = self._response_Json_intancce.structure_json()      
        
        self._product['title'] = self._response_bs.find(id='product_title').get_text(strip=True)

        self._product['brand']  = self._response_bs.find(class_='brand').get_text(strip=True)

        self._categories  = self._response_bs.select('.current-category a') 

        if self._categories:
            self._product['categories'] = self.extract_text_list(self._categories, self._list_categories)

        self._descpiton  = self._response_bs.find(class_='proddet') 

        if self._descpiton:
            self._p = self._descpiton.find_all('p')
            
            if self._p:
                self._descpiton  = self.extract_text_list(self._p, self._list_description)
        
        self._product['description']  = f'{self._descpiton[0]}{self._descpiton[1]}'

        for response in self._response_bs.find_all('div', class_='card'):
            
            self._sku_name = response.find(class_='prod-nome') 
            self._sku_current_price = response.find(class_='prod-pnow') 
            self._sku_old_price = response.find(class_='prod-pold') 
        
        
            self._sku_name = self.extract_text_list([self._sku_name] if self._sku_name else [''], self._list_name)
            self._sku_current_price = self.extract_text_list([self._sku_current_price] if self._sku_current_price else [''], self._list_current_price)
            self._sku_old_price = self.extract_text_list([self._sku_old_price] if self._sku_old_price else [''], self._list_old_price)
        
        for i in range(len(self._sku_name)):
            
            self._product['skus'].append({
                'name': self._sku_name[i],
                'current_price': self._sku_current_price[i] if (self._sku_current_price[i] != '' and self._sku_current_price[i] is not None) else None,
                'old_price': self._list_old_price[i] if (self._list_old_price[i] != '' and self._list_old_price[i] is not None) else None,
                'available ': True if (self._list_current_price[i] != '' and self._list_current_price[i] is not False) else False
                })
        
        self._column_one_table = self._response_bs.select('table.pure-table td > b')
        self._column_two_table = self._response_bs.select('table.pure-table td + td')
        
        self._column_one_table = self.extract_text_list(self._column_one_table, self.__column_one_table)
        self._column_two_table = self.extract_text_list(self._column_two_table, self.__column_two_table)
        
        for i in range(len(self._column_one_table)):
            self._product['properties'].append({'label': self._column_one_table[i], 'value': self._column_two_table[i]})
        
        self._name_people_review = self._response_bs.select('div#comments div.pure-g div.pure-u-21-24 span.analiseusername')
        self._date_people_review = self._response_bs.select('div#comments div.pure-g div.pure-u-21-24 span.analisedate')
        self._score_people_review = self._response_bs.select('div#comments div.pure-g div.pure-u-21-24 span.analisestars')
        self._text_review = self._response_bs.select('div#comments div.analisebox p')

        self._name_people_review = self.extract_text_list(self._name_people_review, self._list_name_people_review)
        self._date_people_review = self.extract_text_list(self._date_people_review, self._list_date_people_review)
        self._score_people_review = self.extract_text_list(self._score_people_review, self._list_score_people_review)
        self._text_review = self.extract_text_list(self._text_review, self._list_text_review)

        for i in range(len(self._score_people_review )):
            
            self._product['reviews'].append({
                            'name': self._name_people_review[i],
                            'date': self._date_people_review[i],
                            'score': self._score_people_review[i].count('★'),
                            'text': self._text_review[i]
                        })
        
        self._average_score = self._response_bs.select('div#comments h4')
        
        self._text_review = self.extract_text_list(self._average_score, self._list_score)
        self._text_review = search(r'\d+(\.\d+)?', self._text_review[0])

        self._product['reviews_average_score'] = self._text_review.group()

        self._product['url'] = self._response.url
        
        self._response_Json_intancce.save_json(self._product)

        print('salvo')

scrap = Scraper()
scrap.main()