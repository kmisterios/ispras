1) Для начала требуется отчистить файл res1.json
2)Чтобы запустить паука, нужно ввести атрибуты в формате:
scrapy crawl article -o res1.json -a start_date=dd.mm.yyyy -a stop_date=dd.mm.yyyy -a type=n (a /na /an)
Где 'n' - для новостей, 'a' - для статей, 'na' и 'an' - для статей и новостей.
