from pathlib import Path
from json import dump

class Json:

    def save_json(self, data: dict = None) -> None:
       self._path = Path(__file__).resolve().parent.parent.parent
        
       with open(fr'{self._path}\produto.json', 'w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False, indent=2)
    
    def structure_json(self) -> dict:
        self._structure = {
            "title": '',
            "brand": '',  
            "categories": None,  
            "description": '',
            "skus": [],
            "properties": [],
            "reviews": [],
            "reviews_average_score": None,
            "url": ''
        }
        
        return  self._structure
 