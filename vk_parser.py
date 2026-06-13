import os
import vk_api
from dotenv import load_dotenv

# Загружаем переменные из общего файла .env
load_dotenv()

# Достаем ключ ВКонтакте из системы
TOKEN = os.getenv("VK_TOKEN")

def analyze_vk_group(group_domain):
    # Проверяем, удалось ли скрипту найти ключ в .env
    if not TOKEN:
        print("❌ Ошибка: Переменная VK_TOKEN не найдена в файле .env!")
        print("Убедись, что дописал строку VK_TOKEN=твой_ключ в файл .env")
        return

    # Авторизуемся в VK API
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    
    try:
        # Делаем запрос к серверам ВК (забираем последние 5 постов)
        response = vk.wall.get(domain=group_domain, count=5, v='5.131')
        
        print(f"\n--- Анализ паблика: {group_domain} ---")
        
        for post in response['items']:
            post_id = post['id']
            likes = post['likes']['count']
            views = post.get('views', {}).get('count', 0)
            text = post.get('text', '')[:50].replace('\n', ' ')
            
            print(f"Пост ID {post_id}: ❤️ Лайков: {likes} | 👀 Просмотров: {views}")
            print(f"Текст: {text}...\n")
            
    except vk_api.exceptions.ApiError as error:
        print(f"❌ Ошибка VK API: {error}")

if __name__ == "__main__":
    # Тестируем на официальном паблике Команды ВКонтакте
    analyze_vk_group("team")