import requests
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import os
from removebg import RemoveBg
from dotenv import *
dotenv.config()

def start(update, context):
  welcome_message = "Hallo, Perkenalkan Saya ThunderFlashBot yang digunakan untuk Generate berita, kutipan dan Gempa Terkini.\n ~Developed by @ISB"
  update.message.reply_text(welcome_message)
  
def news(update, context):
    update.message.reply_text("Memuat data...")
    url = 'https://jakpost.vercel.app/api/category/indonesia'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        featured_post = news_data['featured_post']
        posts = news_data['posts']

        featured_title = featured_post.get('title', '')
        featured_image_url = featured_post.get('image', '')
        featured_headline = featured_post.get('headline', '')
        featured_category = featured_post.get('category', '')

        featured_message = f"Berita Utama*\n\n" \
                           f"Judul: {featured_title}\n" \
                           f"Kategori: {featured_category}\n" \
                           f"Headline: {featured_headline}"

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=featured_image_url, caption=featured_message)

        random_posts = random.sample(posts, min(3, len(posts)))
        for post in random_posts:
            post_title = post.get('title', '')
            post_image_url = post.get('image', '')
            post_headline = post.get('headline', '')
            post_category = post.get('category', '')

            post_message = f"{post_category}\n\n" \
                           f"Judul: {post_title}\n" \
                           f"Headline: {post_headline}"

            context.bot.send_photo(chat_id=update.effective_chat.id, photo=post_image_url, caption=post_message)
    else:
        update.message.reply_text('Gagal mengambil berita.')
        
        
def movie_recommendation(update, context):
    update.message.reply_text("Memuat data untuk film yang populer, sedang tayang, dan direkomendasikan...")
    api_key = process.env.TMDB_API_KEY

    popular_movies_url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=en-US&page=1"
    popular_response = requests.get(popular_movies_url)
    if popular_response.status_code == 200:
        popular_movies_data = popular_response.json()
        popular_movies = random.sample(popular_movies_data["results"], min(3, len(popular_movies_data["results"])))
        update.message.reply_text("Film yang populer:")
        for movie in popular_movies:
            title = movie['title']
            description = movie['overview']
            popularity = movie['popularity']
            poster_path = movie['poster_path']
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=poster_url, caption=f"Title: {title}\nDescription: {description}\nPopularity: {popularity}")
            else:
                update.message.reply_text(f"Title: {title}\nDescription: {description}\nPopularity: {popularity}")
    else:
        update.message.reply_text('Gagal mengambil data film populer.')

    upcoming_movies_url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page=1'
    upcoming_response = requests.get(upcoming_movies_url)
    if upcoming_response.status_code == 200:
        upcoming_movies_data = upcoming_response.json()
        upcoming_movies = random.sample(upcoming_movies_data['results'], min(3, len(upcoming_movies_data['results'])))
        update.message.reply_text("Film yang akan datang:")
        for movie in upcoming_movies:
            title = movie['title']
            description = movie['overview']
            release_date = movie['release_date']
            poster_path = movie['poster_path']
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=poster_url, caption=f"Title: {title}\nDescription: {description}\nRelease Date: {release_date}")
            else:
                update.message.reply_text(f"Title: {title}\nDescription: {description}\nRelease Date: {release_date}")
    else:
        update.message.reply_text('Gagal mengambil data film yang akan datang.')
        
    recommend_movies_url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1'
    recommend_response = requests.get(recommend_movies_url)
    if recommend_response.status_code == 200:
        recommend_movies_data = recommend_response.json()
        recommend_movies = random.sample(recommend_movies_data['results'], min(3, len(recommend_movies_data['results'])))
        update.message.reply_text("Film yang sedang tayang dan direkomendasikan:")
        for movie in recommend_movies:
            title = movie['title']
            description = movie['overview']
            poster_path = movie['poster_path']
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=poster_url, caption=f"Title: {title}\nDescription: {description}")
            else:
                update.message.reply_text(f"Title: {title}\nDescription: {description}")
    else:
        update.message.reply_text('Gagal mengambil data film yang sedang tayang dan direkomendasikan.')
        
def help_command(update, context):
    command_list = '/news - Menampilkan berita terkini\n' \
                   '/gempa - Menampilkan informasi gempa terkini\n' \
                   '/quotes - Menampilkan kutipan acak\n' \
                   '/movie - Untuk mendapatkan rekomendasi, populer & ongoing films secara terupdate\n' \
                   '/help - Menampilkan daftar perintah\n' \
                   '/followme[text] - Menampilkan apa yang kamu ketikan.'
    update.effective_chat.send_message('Daftar perintah yang tersedia:\n' + command_list)

                              
def follow(update, context):
  if len(context.args) > 0:
    user_id = update.message.chat_id
    text = ''.join(context.args)
    context.user_data[user_id] = text 
    update.message.reply_text(f"Kukembalikan Pesanmu: {text}")
  else:
    update.message.reply_text("Silahkan Memasukkan Text Setelah '/followme'")
    

def unkown_commands(update, context):
  keyboard = [[InlineKeyboardButton("Panduan Pengguna", callback_data="go_to_help")]]
  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text("Perintah tidak ditemukan. Gunakan Tombol dibawah ini untuk bantuan!", reply_markup=reply_markup)
  
def click_button(update, context):
  query_data = update.callback_query
  if query_data.data == "go_to_help":
    try:
      query_data.answer()
      help_command(update, context)
    except Exception as e:
      print("Error detected:", e)
    
    
def gempa(update, context):
    update.message.reply_text("Memuat data...")
    url = "https://cuaca-gempa-rest-api.vercel.app/quake"

    try:
        response = requests.get(url)
        response.raise_for_status() 

        gempa_data = response.json()
        info_gempa = gempa_data['data']

        tanggal = info_gempa['tanggal']
        jam = info_gempa['jam']
        time = info_gempa['datetime']
        lintang = info_gempa['lintang']
        bujur = info_gempa['bujur']
        magnitudo = info_gempa['magnitude']
        kedalaman = info_gempa['kedalaman']
        wilayah = info_gempa['wilayah']
        potensi_tsunami = info_gempa['potensi']
        shakemap_url = info_gempa['shakemap']

        description = f"Gempa Terkini:\n" \
                     f"Tanggal: {tanggal}\n" \
                     f"Waktu: {jam} | {time}\n" \
                     f"Lintang: {lintang}\n" \
                     f"Bujur: {bujur}\n" \
                     f"Kekuatan:: {magnitudo} SR\n" \
                     f"Kedalaman: {kedalaman}\n" \
                     f"Wilayah: {wilayah}\n" \
                     f"Potensi Tsunami: {potensi_tsunami}\n" \
                     f"\n" \
                     f"Sumber: BMKG (https://data.bmkg.go.id/)"

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=shakemap_url, caption=description)

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Failed to take quake Information: {e}")

def quotes(update, context):
    url = "https://api.kanye.rest/"
    response = requests.get(url)
    if response.status_code == 200:
        quotes_data = response.json()
        random_quote = quotes_data['quote']
        update.message.reply_text("Kutipan: " + random_quote)
    else:
        update.message.reply_text('Gagal mengambil kutipan.')

def process_photo(update, context):
   update.message.reply_text("Processing...")
    if update.message.caption == '/remove_bg':
        API_KEY = process.env.RMBG_API_KEY
        removebg = RemoveBg(API_KEY,          "error.log")
        photo_file = context.bot.get_file(update.message.photo[-1].file_id)
        file_extension = photo_file.file_path.split('.')[-1]
        photo_path = f"remove/input_photo.{file_extension}"
        photo_file.download(photo_path)
        removebg.remove_background_from_img_file(photo_path)
        result_path = f"remove/input_photo.jpg_no_bg.png"
        
        with open(result_path, "rb") as file:
         context.bot.send_photo(chat_id=update.effective_chat.id, photo=file, caption="Result.")
        
        try:
            os.remove(photo_path)
            os.remove(result_path)
        except Exception as e:
            update.message.reply_text(f"Error saat menghapus file server side: {e}")
    else:
        update.message.reply_text("Kirimkan foto dengan caption /remove_bg untuk menghapus latar belakangnya.")


def main():
    TOKEN=process.env.TELEGRAMBOT_TOKEN
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("news", news))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler("gempa", gempa))
    updater.dispatcher.add_handler(CommandHandler("quotes", quotes))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("movie", movie_recommendation))
    updater.dispatcher.add_handler(CommandHandler("followme", follow))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unkown_commands))
        updater.dispatcher.add_handler(CallbackQueryHandler(click_button))
       updater.dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, process_photo))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
