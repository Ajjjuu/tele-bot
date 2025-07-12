from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from db import init_db, Session, User, Media
import random
import os


BOT_TOKEN = "7892130919:AAEve83rfOhsodgHB0Er7lFhXz33hO9kAxk"
# Database initialization
# Init DB
init_db()

# List of admin Telegram user IDs (as strings)
ADMINS = ["1410698950"] 
MAX_FILE_SIZE_MB = 49

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Initialize database session
    session = Session()
    tg_user = update.effective_user
    tg_id = str(tg_user.id)
    username = tg_user.username
    first_name = tg_user.first_name
    last_name = tg_user.last_name

    # Check if the user exists in the database, otherwise create a new user
    user = session.query(User).filter_by(telegram_id=tg_id).first()
    if not user:
        user = User(
            telegram_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            tokens=5
        )
        session.add(user)
        session.commit()
        welcome_msg = "🎉 Registered! You've been given 5 tokens."
    else:
        welcome_msg = f"👋 Welcome back! You have {user.tokens} tokens."
    # Close database session
    session.close()

    # Define custom keyboard layout
    keyboard = [
        # Token and buy options
        ["/tokens", "/buy"],
        ["/nature", "/puppy", "/surprise"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Send welcome + instructions
    instructions = (
        "👇 Here are some commands you can use:\n"
        "• /tokens – See your available tokens\n"
        "• /buy – Buy more tokens\n"
        "• /nature – Get a random nature video"
        "• /puppy – Get a random puppy video\n"
        "• /surprise – Get a random surprise video"
    )
    await update.effective_message.reply_text(welcome_msg)
    await update.effective_message.reply_text(instructions, reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle button presses from inline keyboards
    query = update.callback_query
    await query.answer()
    if query.data == 'nature':
        await nature(update, context)
    elif query.data == 'puppy':
        await puppy(update, context)
    elif query.data == 'tokens':
        await tokens(update, context)
    elif query.data == 'buy':
        await buy(update, context)
    elif query.data == 'surprise':
        await surprise(update, context)


async def tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve and display user's token balance
    session = Session()
    user = session.query(User).filter_by(telegram_id=str(update.effective_user.id)).first()
    # await update.effective_message.reply_text(f"🪙 You have {user.tokens} tokens.")
    await update.effective_message.reply_text(f"🪙 I'm still building it, try something else.")
    session.close()

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Placeholder for buying tokens functionality
    session = Session()
    # user = session.query(User).filter_by(telegram_id=str(update.effective_user.id)).first()
    # media = session.query(Media).first()

    # if not media:
    #     await update.effective_message.reply_text("No media available yet.")
    # elif user.tokens >= media.token_cost:
    #     user.tokens -= media.token_cost
    #     session.commit()
    #     await update.effective_message.reply_text(f"🎬 Sending: {media.title} (Cost: {media.token_cost} tokens)")
    #     await update.effective_message.bot.send_video(chat_id=update.effective_chat.id, video=media.file_id)
    # else:
    #     await update.effective_message.reply_text("❌ Not enough tokens.")
    await update.effective_message.reply_text(f"🪙 I'm still building it, try something else.")
    session.close()

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle video uploads and save media information to the database
    if update.effective_message.video:
        file_id = update.effective_message.video.file_id
        print(f"Received video file_id: {file_id}")
        session = Session()
        media = Media(title="Test Video", file_id=file_id, token_cost=2)
        session.add(media)
        # Save media information to the database
        session.commit()
        await update.effective_message.reply_text(f"✅ Video saved! file_id: {file_id}")
        print(f"Video saved with title: {media.title}, file_id: {media.file_id}, token_cost: {media.token_cost}")
        print("closing session...")
        session.close()
    else:
        await update.effective_message.reply_text("❗Please send a video file with this command.")

async def nature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a random nature video
    # Define the path to the nature videos folder
    nature_folder = os.path.join(os.path.dirname(__file__), 'Nature')
    print("Nature folder path:", nature_folder)
    # List all video files in the folder
    video_files = [f for f in os.listdir(nature_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    if not video_files:
        await update.effective_message.reply_text("No nature videos available.")
    else:
        # Select a random video file
        video_path = os.path.join(nature_folder, random.choice(video_files))
        print("choosed file?", video_path)
        await update.effective_message.reply_text("🌿 Sending a random nature video...")
        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)

async def puppy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a random puppy video
    # Define the path to the puppy videos folder
    puppies_folder = os.path.join(os.path.dirname(__file__), 'Puppies')
    print("Puppies folder path:", puppies_folder)
    # List all video files in the folder
    video_files = [f for f in os.listdir(puppies_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    if not video_files:
        await update.effective_message.reply_text("No puppy videos available.")
    else:
        # Select a random video file
        video_path = os.path.join(puppies_folder, random.choice(video_files))
        print("chosen file?", video_path)
        await update.effective_message.reply_text("🐶 Sending a random puppy video...")
        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)

async def surprise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a random surprise video
    # Define the path to the surprise videos folder, currently empty and needs to be updated
    surprise_folder = ""
    print("Surprise", surprise_folder)
    video_files = [
            f for f in os.listdir(surprise_folder)
            if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')) and
            # Ensure the file size is within the allowed limit
            os.path.getsize(os.path.join(surprise_folder, f)) <= MAX_FILE_SIZE_MB * 1024 * 1024
        ]
    if not video_files:
        await update.effective_message.reply_text("Sorry no media found")
    else:
        video_path = os.path.join(surprise_folder, random.choice(video_files))
        print("chosen file?", video_path)
        await update.effective_message.reply_text("Sending a surprise...")
        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle text messages and provide an inline keyboard with options
    keyboard = [
        [InlineKeyboardButton("🌿 Nature", callback_data='nature'), InlineKeyboardButton("🐶 Puppy", callback_data='puppy')],
        [InlineKeyboardButton("🪙 Tokens", callback_data='tokens'), InlineKeyboardButton("💳 Buy", callback_data='buy')],
        [InlineKeyboardButton("🎁 Surprise", callback_data='surprise')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        "Hi! Here are some commands you can use:\n 👇 Choose an option:",
        reply_markup=reply_markup
    )

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle unknown commands
    await update.effective_message.reply_text("❌ Sorry, I don't recognize that command. Please use the buttons below or type /start to see available options.")

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Admin-only command to get the total number of registered users
    # Check if the user is an admin
    if str(update.effective_user.id) not in ADMINS:
        await update.effective_message.reply_text("❌ You are not authorized to use this command.")
        return
    session = Session()
    count = session.query(User).count()
    # Close database session
    session.close()
    await update.effective_message.reply_text(f"👥 Total registered users: {count}")

# Initialize the Telegram bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add a handler for button presses from inline keyboards
app.add_handler(CallbackQueryHandler(button_handler))

# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tokens", tokens))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("upload", upload))
# Add command handlers for video categories
app.add_handler(CommandHandler("nature", nature))
app.add_handler(CommandHandler("puppy", puppy))
app.add_handler(CommandHandler("surprise", surprise))
app.add_handler(CommandHandler("users", users))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

# Start the bot
app.run_polling()
