from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, ContextTypes
import re
import random

TOKEN = "7496004298:AAFpbGvSvLpIZWbaNnfFnOu7i57a_tpFWxM"  # Replace with your bot token

# Define states
NAME, GRAMMAR, FILL_IN, READING, WRITING = range(5)
# Grammar questions
import random

# Expanded Grammar Questions (More questions added)
all_grammar_questions = [
    ("She ___ to school every day.", ["go", "goes", "going", "gone"], 1),
    ("I ___ TV when my friend called.", ["watched", "was watching", "have watched", "watch"], 1),
    ("If it ___ tomorrow, we will stay home.", ["rain", "rains", "raining", "will rain"], 1),
    ("The book is ___ the table.", ["in", "at", "on", "under"], 2),
    ("We ___ in this city since 2010.", ["live", "are living", "have lived", "lived"], 2),
    ("She ___ tennis every weekend.", ["plays", "play", "playing", "played"], 0),
    ("The sun ___ in the east.", ["rise", "rises", "rising", "rose"], 1),
    ("I ___ to the gym three times a week.", ["go", "goes", "going", "gone"], 0),
    ("He ___ a great movie last night.", ["saw", "see", "seeing", "seen"], 0),
    ("They ___ their homework before dinner.", ["finish", "finished", "finishing", "finishes"], 1),
    ("She ___ her homework before going to bed.", ["did", "done", "doing", "does"], 0),
    ("John ___ to Paris last summer.", ["go", "goes", "going", "went"], 3),
    ("By this time next year, I ___ my studies.", ["finish", "will finish", "will have finished", "finished"], 2),
    ("She ___ her friend at the airport yesterday.", ["meet", "met", "meeting", "meets"], 1),
    ("We ___ a party next weekend.", ["have", "had", "will have", "having"], 2),
    ("They ___ their project before the deadline.", ["complete", "completed", "completing", "will complete"], 3),
    ("My brother ___ his homework now.", ["do", "does", "doing", "is doing"], 3),
    ("The baby ___ when the phone rang.", ["sleep", "slept", "was sleeping", "sleeps"], 2),
    ("If I ___ rich, I would travel the world.", ["am", "was", "were", "been"], 2),
    ("She always ___ to the same coffee shop.", ["go", "goes", "going", "gone"], 1),
    ("Neither John nor his friends ___ interested in the trip.", ["is", "are", "was", "were"], 1),
]

# Expanded Fill-in-the-Blank Questions
all_fill_in_the_blanks = [
    ("My brother is taller ___ me.", "than"),
    ("I have never ___ to London before.", "been"),
    ("She ___ her homework before dinner.", "finished"),
    ("Can you ___ me with this problem?", "help"),
    ("The opposite of 'expensive' is ___", "cheap"),
    ("The baby is sleeping, please be ___", "quiet"),
    ("A dog is ___ than a cat.", "bigger"),
    ("I am interested ___ learning new languages.", "in"),
    ("We are going ___ vacation next week.", "on"),
    ("She is afraid ___ spiders.", "of"),
    ("The train arrived later ___ expected.", "than"),
    ("He has been working here ___ five years.", "for"),
    ("I prefer coffee ___ tea.", "to"),
    ("She was born ___ 1995.", "in"),
    ("He apologized ___ being late.", "for"),
    ("The book was written ___ a famous author.", "by"),
    ("She is married ___ a doctor.", "to"),
    ("They have been living here ___ 2010.", "since"),
    ("We went home ___ it started raining.", "before"),
    ("He is responsible ___ managing the project.", "for"),
    ("She succeeded ___ passing the exam.", "in"),
    ("He is good ___ playing chess.", "at"),
]

# Reading passage and questions
reading_passages = [
    {
        "passage": """Lisa wakes up early every morning. She drinks a cup of tea and reads the news. 
        Then, she goes to work by bus. Lisa works as a teacher in a primary school. She loves her job 
        and enjoys teaching children. After work, she spends time with her family. In the evening, 
        she enjoys watching movies or reading books before going to bed at 10 PM.""",
        "questions": [
            ("What does Lisa drink in the morning?", "tea"),
            ("How does Lisa go to work?", "by bus"),
            ("What is Lisa’s job?", "teacher"),
            ("What does Lisa do in the evening?", ["watching movies", "reading books"]),
            ("At what time does Lisa go to bed?", "10 PM"),
        ]
    },
    {
        "passage": """Tom loves sports. He plays football with his friends every weekend. His favorite 
        team is Manchester United, and he watches all their matches on TV. Tom also enjoys swimming and 
        goes to the pool twice a week. When he is not playing, he reads sports magazines. He dreams of 
        becoming a professional football player one day.""",
        "questions": [
            ("What sport does Tom play every weekend?", "football"),
            ("What is Tom’s favorite football team?", "Manchester United"),
            ("What other sport does Tom enjoy?", "swimming"),
            ("How often does Tom go swimming?", "twice a week"),
            ("What is Tom’s dream job?", ["professional football player", "football player"]),
        ]
    },
    {
        "passage": """Emma enjoys baking. She often makes cakes and cookies for her family. 
        Her favorite recipe is chocolate cake. She learned baking from her grandmother, who 
        was a professional baker. Every Sunday, Emma and her grandmother bake together. She 
        hopes to open her own bakery in the future.""",
        "questions": [
            ("What does Emma enjoy doing?", "baking"),
            ("Who taught Emma to bake?", "her grandmother"),
            ("What is Emma’s favorite recipe?", "chocolate cake"),
            ("When does Emma bake with her grandmother?", "every Sunday"),
            ("What is Emma’s future goal?", ["open a bakery", "own a bakery"]),
        ]
    },
    {
        "passage": """John is a doctor who works in a large hospital. He specializes in heart surgery 
        and has helped many patients recover. He wakes up early every day and starts work at 7 AM. 
        After work, he enjoys jogging in the park to stay healthy. On weekends, he spends time with 
        his family and plays chess with his son.""",
        "questions": [
            ("What is John’s profession?", "doctor"),
            ("What does John specialize in?", ["heart surgery", "surgery"]),
            ("What time does John start work?", "7 AM"),
            ("What does John do after work?", "jogging"),
            ("Who does John play chess with?", "his son"),
        ]
    },
    {
        "passage": """Sophia loves traveling. She has visited many countries, including France, 
        Japan, and Australia. She enjoys learning about different cultures and trying new food. 
        Her favorite place so far has been Paris because of its beautiful architecture and delicious 
        pastries. She hopes to visit South America next year.""",
        "questions": [
            ("What does Sophia love to do?", "traveling"),
            ("Which countries has Sophia visited?", ["France", "Japan", "Australia"]),
            ("What does Sophia enjoy learning about?", "different cultures"),
            ("What is Sophia’s favorite city so far?", "Paris"),
            ("Where does Sophia want to travel next?", "South America"),
        ]
    },
    {
        "passage": """Michael is a software engineer who works for a tech company. He spends most of his day coding and solving problems. 
        In his free time, he likes to play video games and read science fiction novels. He also enjoys hiking on weekends.""",
        "questions": [
            ("What is Michael's profession?", "software engineer"),
            ("What does Michael do in his free time?", ["play video games", "read science fiction novels"]),
            ("What does Michael enjoy on weekends?", "hiking"),
        ]
    },
    {
        "passage": """Anna is a musician who plays the violin in an orchestra. She practices for several hours every day and performs in concerts regularly. 
        She also teaches violin to young students. Anna loves classical music and dreams of performing at Carnegie Hall one day.""",
        "questions": [
            ("What instrument does Anna play?", "violin"),
            ("What does Anna do besides performing?", "teaches violin"),
            ("What is Anna's dream?", "performing at Carnegie Hall"),
        ]
    },
    {
        "passage": """David is a chef who owns a small restaurant. He specializes in Italian cuisine and loves creating new dishes. 
        He works long hours but enjoys seeing his customers happy. In his spare time, he likes to travel and try new foods.""",
        "questions": [
            ("What type of cuisine does David specialize in?", "Italian"),
            ("What does David enjoy about his job?", "seeing his customers happy"),
            ("What does David like to do in his spare time?", ["travel", "try new foods"]),
        ]
    },
    {
        "passage": """Emily is a journalist who writes for a popular magazine. She covers stories about technology and innovation. 
        She travels frequently to interview experts and attend conferences. Emily enjoys meeting new people and learning about the latest trends.""",
        "questions": [
            ("What does Emily write about?", ["technology", "innovation"]),
            ("What does Emily enjoy about her job?", ["meeting new people", "learning about the latest trends"]),
        ]
    },
    {
        "passage": """Chris is a photographer who specializes in nature and wildlife photography. He travels to remote locations to capture stunning images. 
        His work has been featured in several magazines and exhibitions. Chris is passionate about conservation and hopes his photos inspire others to protect the environment.""",
        "questions": [
            ("What type of photography does Chris specialize in?", ["nature", "wildlife"]),
            ("What has Chris's work been featured in?", ["magazines", "exhibitions"]),
            ("What is Chris passionate about?", "conservation"),
        ]
    },
    # New passages
    {
        "passage": """Maria is a scientist who studies marine life. She spends most of her time researching coral reefs and their ecosystems. 
        Maria often travels to tropical locations to collect data and observe marine species. She is passionate about protecting the oceans 
        and raising awareness about climate change. In her free time, she enjoys scuba diving and photography.""",
        "questions": [
            ("What does Maria study?", "marine life"),
            ("What does Maria research?", "coral reefs"),
            ("Why does Maria travel to tropical locations?", ["collect data", "observe marine species"]),
            ("What is Maria passionate about?", ["protecting the oceans", "raising awareness about climate change"]),
            ("What does Maria enjoy in her free time?", ["scuba diving", "photography"]),
        ]
    },
    {
        "passage": """James is a pilot who flies international routes for a major airline. He has visited over 50 countries and loves exploring new cultures. 
        James enjoys the challenge of flying in different weather conditions and ensuring the safety of his passengers. In his downtime, he likes to read books 
        about aviation history and spend time with his family.""",
        "questions": [
            ("What is James's profession?", "pilot"),
            ("How many countries has James visited?", "over 50"),
            ("What does James enjoy about his job?", ["flying in different weather conditions", "ensuring passenger safety"]),
            ("What does James like to read about?", "aviation history"),
            ("Who does James spend time with in his downtime?", "his family"),
        ]
    },
    {
        "passage": """Sarah is a veterinarian who works at an animal hospital. She treats a variety of animals, from cats and dogs to exotic pets. 
        Sarah is known for her compassion and dedication to animal welfare. She also volunteers at a local animal shelter on weekends. In her free time, 
        she enjoys hiking with her dog and gardening.""",
        "questions": [
            ("What is Sarah's profession?", "veterinarian"),
            ("What types of animals does Sarah treat?", ["cats", "dogs", "exotic pets"]),
            ("What is Sarah known for?", ["compassion", "dedication to animal welfare"]),
            ("Where does Sarah volunteer on weekends?", "local animal shelter"),
            ("What does Sarah enjoy in her free time?", ["hiking with her dog", "gardening"]),
        ]
    },
    {
        "passage": """Alex is a graphic designer who works for a creative agency. He designs logos, websites, and marketing materials for clients. 
        Alex is passionate about art and technology and enjoys combining the two in his work. He often attends design conferences to stay updated on the latest trends. 
        In his spare time, he likes to paint and play the guitar.""",
        "questions": [
            ("What is Alex's profession?", "graphic designer"),
            ("What does Alex design?", ["logos", "websites", "marketing materials"]),
            ("What is Alex passionate about?", ["art", "technology"]),
            ("Why does Alex attend design conferences?", "to stay updated on the latest trends"),
            ("What does Alex enjoy in his spare time?", ["painting", "playing the guitar"]),
        ]
    },
    {
        "passage": """Laura is a fitness trainer who helps people achieve their health goals. She creates personalized workout plans and provides nutritional advice. 
        Laura is passionate about promoting a healthy lifestyle and often shares tips on social media. In her free time, she enjoys yoga, running, and cooking healthy meals.""",
        "questions": [
            ("What is Laura's profession?", "fitness trainer"),
            ("What does Laura create for her clients?", ["personalized workout plans", "nutritional advice"]),
            ("What is Laura passionate about?", "promoting a healthy lifestyle"),
            ("Where does Laura share health tips?", "social media"),
            ("What does Laura enjoy in her free time?", ["yoga", "running", "cooking healthy meals"]),
        ]
    },
]
def choose_reading_passage(grammar_wrong, fill_in_wrong):
    if grammar_wrong >= 3 and fill_in_wrong >= 3:
        # Choose a short passage (3 questions)
        short_passages = [p for p in reading_passages if len(p["questions"]) == 3]
        return random.choice(short_passages)
    else:
        # Choose a long passage (5 questions)
        long_passages = [p for p in reading_passages if len(p["questions"]) == 5]
        return random.choice(long_passages)

# Example usage
grammar_mistakes = 3
fill_in_mistakes = 3

selected_passage = choose_reading_passage(grammar_mistakes, fill_in_mistakes)
print("Selected Passage:\n", selected_passage["passage"])
print("\nQuestions:")
for q in selected_passage["questions"]:
    print("-", q[0])
async def ask_reading_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask reading comprehension questions."""
    user_id = update.effective_chat.id
    passage_data = user_data[user_id]["selected_reading"]
    index = user_data[user_id]["reading_index"]

    if index < len(passage_data["questions"]):
        question, correct_answer = passage_data["questions"][index]
        user_data[user_id]["correct_answer"] = correct_answer if isinstance(correct_answer, list) else [correct_answer]

        await update.message.reply_text(f"Q{index+1}: {question}")

        user_data[user_id]["reading_index"] += 1
        return READING
    else:
        return await writing_section(update, context)

# Store user data
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the English placement test."""
    await update.message.reply_text("Welcome to the English Placement Test!\nWhat is your name?")
    return NAME  # Ask for the name first

# Get name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the student's name."""
    user_id = update.effective_chat.id
    user_data[user_id] = {
        "name": update.message.text,
        "score": 0,
        "answers": [],
        "used_grammar": set(),
        "used_fill": set(),
        "used_reading": set(),
        "question_index": 0,
        "fill_index": 0,
        "reading_index": 0,
        "selected_grammar": random.sample(all_grammar_questions, 5),  # Select 5 random grammar questions
        "selected_fill": random.sample(all_fill_in_the_blanks, 5),    # Select 5 random fill-in questions
        "selected_reading": random.sample(reading_passages, 1)[0],    # Select 1 random reading passage
        "grammar_questions_asked": 0,  # Initialize the counter for grammar questions asked
    }

    await update.message.reply_text(f"Thank you, {user_data[user_id]['name']}!\nLet's start with Grammar & Vocabulary.")
    await grammar_section(update, context)
    return GRAMMAR
    # Select 5 random grammar and fill-in-the-blank questions for each student
    user_data[user_id] = {
        "score": 0,
        "answers": [],
        "question_index": 0,
        "fill_index": 0,
        "reading_index": 0,
        "selected_grammar": random.sample(all_grammar_questions, 5),
        "selected_fill": random.sample(all_fill_in_the_blanks, 5),
    }
    return await grammar_section(update, context)

# Grammar section
async def grammar_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask grammar questions without repetition."""
    user_id = update.effective_chat.id

    # Check if 5 questions have already been asked
    if user_data[user_id]["grammar_questions_asked"] >= 5:
        return await fill_in_section(update, context)  # Move to the next section

    # Get the list of selected grammar questions
    selected_grammar = user_data[user_id]["selected_grammar"]

    # Get the current question index
    question_index = user_data[user_id]["question_index"]

    # Get the current question
    question, options, correct_index = selected_grammar[question_index]

    # Store the correct answer
    user_data[user_id]["correct_answer"] = options[correct_index]

    # Create a reply markup with the options
    reply_markup = ReplyKeyboardMarkup([options], one_time_keyboard=True)

    # Send the question to the user
    await update.message.reply_text(f"{question}", reply_markup=reply_markup)

    # Increment the question index and counter
    user_data[user_id]["question_index"] += 1
    user_data[user_id]["grammar_questions_asked"] += 1

    return GRAMMAR
# Check grammar answer
async def check_grammar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Check grammar answers."""
    user_id = update.effective_chat.id
    answer = update.message.text.lower()
    correct_answer = user_data[user_id]["correct_answer"].lower()

    if answer == correct_answer:
        user_data[user_id]["score"] += 2
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text(f"❌ Incorrect. The correct answer is: {user_data[user_id]['correct_answer']}")

    # Check if 5 questions have been asked
    if user_data[user_id]["grammar_questions_asked"] >= 5:
        return await fill_in_section(update, context)  # Move to the next section
    else:
        return await grammar_section(update, context)  # Ask the next question
# Fill-in-the-blank section
async def fill_in_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask fill-in-the-blank questions without repetition."""
    user_id = update.effective_chat.id

    # Check if 5 questions have already been asked
    if user_data[user_id]["fill_index"] >= 5:
        return await reading_section(update, context)  # Move to the next section

    # Get the list of selected fill-in questions
    selected_fill = user_data[user_id]["selected_fill"]

    # Get the current question index
    fill_index = user_data[user_id]["fill_index"]

    # Get the current question
    question, correct_answer = selected_fill[fill_index]

    # Store the correct answer
    user_data[user_id]["correct_answer"] = correct_answer.lower()

    # Send the question to the user
    await update.message.reply_text(f"Fill in the blank: {question}")

    # Increment the question index
    user_data[user_id]["fill_index"] += 1

    return FILL_IN  # Return the correct state
# Check fill-in-the-blank answers
async def check_fill_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Check fill-in-the-blank answers."""
    user_id = update.effective_chat.id
    answer = update.message.text.lower()
    correct_answer = user_data[user_id]["correct_answer"]

    if answer == correct_answer:
        user_data[user_id]["score"] += 2
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text(f"❌ Incorrect. The correct answer is: {correct_answer}")

    # Check if 5 questions have been asked
    if user_data[user_id]["fill_index"] >= 5:
        return await reading_section(update, context)  # Move to the next section
    else:
        return await fill_in_section(update, context)  # Ask the next question
    # Check if 5 questions have been asked
    if user_data[user_id]["fill_index"] >= 5:
        return await reading_section(update, context)  # Move to the next section
    else:
        return FILL_IN  # Ask the next question
# Reading section
async def reading_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the reading section."""
    user_id = update.effective_chat.id
    passage_data = user_data[user_id]["selected_reading"]

    await update.message.reply_text("Now, read the following passage and answer the questions:\n\n" + passage_data["passage"])
    return await ask_reading_question(update, context)

# Ask reading questions
async def ask_reading_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask reading comprehension questions."""
    user_id = update.effective_chat.id
    passage_data = user_data[user_id]["selected_reading"]
    index = user_data[user_id]["reading_index"]

    if index < len(passage_data["questions"]):
        question, correct_answer = passage_data["questions"][index]
        user_data[user_id]["correct_answer"] = correct_answer if isinstance(correct_answer, list) else [correct_answer]

        await update.message.reply_text(f"Q{index+1}: {question}")

        user_data[user_id]["reading_index"] += 1
        return READING  # Continue asking reading questions
    else:
        return await writing_section(update, context)  # Move to the writing section
# Check reading answers
async def check_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Check reading answers."""
    user_id = update.effective_chat.id
    answer = update.message.text.lower()
    correct_answers = [ans.lower() for ans in user_data[user_id]["correct_answer"]]

    if any(re.search(ans, answer) for ans in correct_answers):
        user_data[user_id]["score"] += 2
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text(f"❌ Incorrect. The correct answer is: {', or '.join(user_data[user_id]['correct_answer'])}")

    return await ask_reading_question(update, context)  # Continue asking reading questions  
# Writing section
async def writing_section(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the writing section."""
    await update.message.reply_text("Final section: Writing!\nWrite a short paragraph (5–7 sentences) about your daily routine.")
    return WRITING


# Check writing answers
async def check_writing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Evaluate the writing section and store student scores."""
    user_id = update.effective_chat.id
    name = user_data[user_id]["name"]
    user_data[user_id]["answers"].append(update.message.text)
    user_data[user_id]["score"] += 5

    final_score = user_data[user_id]["score"]
    level = determine_level(final_score)

    # Save student score to a file
    with open("student_scores.txt", "a") as file:
        file.write(f"{name}: {final_score}/40 - {level}\n")

    try:
        await update.message.reply_text(f"🏆 {name}, your final score: {final_score}/40\nYour English level: {level}")
    except Exception as e:
        print(f"Error sending message: {e}")

    return ConversationHandler.END
async def view_scores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the list of student scores to the admin."""
    try:
        with open("student_scores.txt", "r") as file:
            scores = file.read()
        
        if scores:
            await update.message.reply_text(f"📋 Student Scores:\n{scores}")
        else:
            await update.message.reply_text("No scores recorded yet.")
    except FileNotFoundError:
        await update.message.reply_text("No scores recorded yet.")

def determine_level(score: int) -> str:
    if score <= 20:
        return "Beginner"
    elif score <= 30:
        return "Elementary"
    elif score <= 40:
        return "Intermediate"
    else:
        return "Advanced"

# Main function
def main():
    app = Application.builder().token(TOKEN).concurrent_updates(2).build()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        GRAMMAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_grammar)],
        FILL_IN: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_fill_in)],  # Add FILL_IN state
        READING: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_reading)],
        WRITING: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_writing)],
    },
    fallbacks=[]
)

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("scores", "view_scores"))  # Corrected handler
    app.run_polling(poll_interval=2)  # Adds a delay to prevent timeout issues

if __name__ == "__main__":
    main()