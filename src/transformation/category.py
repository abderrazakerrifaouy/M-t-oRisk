


class Category:

    @staticmethod
    def temperature_category(temp):
        if temp < 0:
            return "Très froid"
        elif temp <= 12:
            return "Froid"
        elif temp <= 22:
            return "Doux"
        elif temp <= 35:
            return "Chaud"
        else:
            return "Très chaud"

    @staticmethod
    def precipitation_category(precipitation):
        if precipitation < 1:
            return "Aucune"
        elif precipitation < 5:
            return "Faible"
        elif precipitation < 20:
            return "Modérée"
        else:
            return "Forte"
    @staticmethod
    def wind_speed_category(speed_max, gusts_max):
        if gusts_max >= 60:
            return "Très fort "
        if speed_max < 10:
            return "Calme"
        elif speed_max <= 29:
            return "Modéré"
        elif speed_max <= 50:
            return "Fort"
        else:
            return "Très fort"
        
    @staticmethod
    def add_Categories_temp(data):
        data['Categorie_temperature'] = data['temperature_max'].apply(Category.temperature_category)
        return data
    
    @staticmethod
    def add_Categories_prec(data):
        data['Categorie_precipitation'] = data['precipitation'].apply(Category.precipitation_category)
        return data

    @staticmethod
    def add_Categories_wind(data):
        data['Categorie_wind'] = data.apply(lambda row: Category.wind_speed_category(row['wind_speed_max'], row['wind_gusts_max']), axis=1)
        return data