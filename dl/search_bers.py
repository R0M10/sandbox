# Загрузка датасета через ddgs и формирование папок с медведями
from pathlib import Path     # библеотека необходимая для указания пути к файлам
from ddgs import DDGS        # Поисковой движок
from fastcore.all import L   # Подключение продвинутого класса СПИСОК из доп. библиотеки от fastai
import requests
import time                  # модуль времени чтобы можно было вставлять ожидание для корректной работы скрипта
import sys                   # модуль для доступа к файлам 

def search_images(term, max_images=30, page=1, tries=5, sleep_s=2):
    print(f"Searching for '{term}' page {page}")
    max_images = int(max_images)

    candidate_kwargs = [
        dict(timeout=20),
        dict(requests_timeout=20),
        dict(timeout=60),
        dict(requests_timeout=60),
        {},
    ]

    last_err = None
    for attempt in range(tries):
        for kw in candidate_kwargs:
            try:
                with DDGS() as ddgs:
                    results = ddgs.images(term, max_results=max_images, page=page, **kw)
                    return L(results).itemgot('image')
            except Exception as e:
                last_err = e
        time.sleep(sleep_s * (attempt + 1))

    raise last_err

path = Path('bears')
path.mkdir(exist_ok=True)

bear_types = ('grizzly', 'black', 'teddy', 'polar')
target_count = 120
images_per_page = 100  # сколько запрашивать за раз

for bear in bear_types:
    dest_folder = path / bear
    dest_folder.mkdir(exist_ok=True)
    
    print(f"Starting download for {bear} bears")
    count = 0
    page = 1
    downloaded_urls = set()  # чтобы избежать дубликатов
    
    while count < target_count:
        try:
            urls = search_images(f'{bear} bear', max_images=images_per_page, page=page)
        except Exception as e:
            print(f"Error searching for {bear} bear page {page}: {e}")
            # возможно, увеличить page и попробовать снова, но если ошибка, то выходим
            break
        
        if not urls:
            print(f"No more images for {bear} bear at page {page}")
            break
        
        print(f"Got {len(urls)} URLs for page {page}")
        
        for url in urls:
            if url in downloaded_urls:
                continue  # уже пробовали
            
            # Пытаемся скачать
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Проверим, что это изображение (по Content-Type)
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        file_path = dest_folder / f'{count:03d}.jpg'
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        print(f'  Downloaded: {file_path} from {url} (successful count: {count+1})')
                        downloaded_urls.add(url)
                        count += 1
                        if count >= target_count:
                            break
                    else:
                        print(f'  Skipping {url} - not an image (content-type: {content_type})')
                else:
                    print(f'  Failed: {url} (status {response.status_code})')
            except Exception as e:
                print(f'  Error downloading {url}: {e}')
            # Если ошибка, просто переходим к следующему URL
        
        # Если после обработки всех URL на странице count не достигнут, переходим на следующую страницу
        page += 1
        # Небольшая задержка между страницами
        time.sleep(1)
    
    if count >= target_count:
        print(f"Successfully downloaded {count} images for {bear} bears")
    else:
        print(f"Warning: only downloaded {count} images for {bear} bears (target {target_count})")

print('Done!')