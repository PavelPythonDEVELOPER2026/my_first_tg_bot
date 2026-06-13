import vk_api

# ⚠️ ВСТАВИТЬ СЮДА СВОЙ СЕРВИСНЫЙ КЛЮЧ ДОСТУПА В КАВЫЧКАХ
TOKEN = "23661f7823661f7823661f78c82027b30c2236623661f78494bbd5f9741d404075f5613"

def analyze_vk_group(group_domain):
    # Авторизуемся в VK API с помощью твоего ключа
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    try:
        # Вызываем метод wall.get (получить посты со стены)
        # domain — это короткое имя паблика (например, 'habr', 'team')
        # count — сколько последних постов мы хотим скачать
        # v='5.131' - версия API (v - версия)
        response = vk.wall.get(domain=group_domain, count=5, v='5.131')

        print(f"\n--- Анализ паблика: {group_domain} ---")

        for post in response['items']:
            post_id = post['id']
            # Забираем лайки и просмотры
            likes = post['likes']['count']
            views = post.get('views', {}).get('count', 0)
            text = post.get('text', '')[:50].replace('\n', ' ') # Берем кусочек текста для красоты
            
            print(f"Пост ID {post_id}: ❤️ Лайков: {likes} | 👀 Просмотров: {views}")
            print(f"Текст: {text}...\n")
            
    except vk_api.exceptions.ApiError as error:
        print(f"Ошибка VK API: {error}")

# Запускаем скрипт для официального паблика Команды ВКонтакте (vk.com/team)
if __name__ == "__main__":
    analyze_vk_group("team")