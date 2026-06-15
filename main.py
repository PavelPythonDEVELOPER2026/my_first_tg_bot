import os
from fastapi import FastAPI
import vk_api
from dotenv import load_dotenv

# 1. Загружаем переменные окружения из файла .env
load_dotenv()
TOKEN = os.getenv("VK_TOKEN")

# 2. Инициализируем наше веб-приложение FastAPI
app = FastAPI(title="VK Parser API")

# 3. Главная страница (эндпоинт "/"). Просто проверяем, что сервер живой
@app.get("/")
def read_root():
    return {"message": "Привет! Это Junior API для парсинга ВК"}

# 4. Страница парсинга. {group_domain} — это имя группы, которое мы введем в браузере
@app.get("/parse/{group_domain}")
def parse_vk(group_domain: str):
    # Проверяем, загрузился ли токен, чтобы код не упал дальше
    if not TOKEN:
        return {"error": "Токен VK_TOKEN не найден в .env"}
    
    # Авторизуемся в библиотеке vk_api с помощью нашего токена
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    
    try:
        # Делаем запрос к серверам VK: получаем 3 последних поста со стены (wall)
        response = vk.wall.get(domain=group_domain, count=3, v='5.131')
        
        # Создаем пустой список, куда будем собирать только нужные нам метрики
        parsed_posts = []
        
        # Перебираем полученные посты в цикле
        for post in response['items']:
            parsed_posts.append({
                "post_id": post['id'],
                "likes": post['likes']['count'],
                "views": post.get('views', {}).get('count', 0), # .get() защищает, если просмотров нет
                "text_preview": post.get('text', '')[:50]  # берем первые 50 символов текста
            })
            
        # Возвращаем красивый JSON-ответ в браузер
        return {
            "group": group_domain,
            "posts": parsed_posts
        }
            
    except Exception as e:
        # Если что-то пошло не так (например, группы не существует), отдаем ошибку
        return {"error": f"Не удалось собрать данные: {str(e)}"}