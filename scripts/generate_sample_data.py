import random
from datetime import datetime, timedelta
import uuid
import json

# Sample data pools
names_pool = [
    "Priya Sharma", "Sofia Lopez", "Emma Wilson", "Aisha Khan", "Maria Garcia",
    "Anjali Patel", "Sarah Johnson", "Mei Chen", "Isabella Santos", "Fatima Ahmed",
    "Rachel Cohen", "Nina Patel", "Laura Rodriguez", "Yuki Tanaka", "Anna Kowalski",
    "Zara Malik", "Lisa Kim", "Diana Martinez", "Maya Singh", "Elena Popov"
]

topics = [
    "morning sickness", "food cravings", "baby movement", "sleep tips", "exercise",
    "nursery planning", "pregnancy yoga", "nutrition", "birth plan", "baby names",
    "maternity clothes", "prenatal vitamins", "ultrasound", "baby shower", "breastfeeding",
    "pregnancy books", "hospital bag", "labor signs", "self-care", "mood swings"
]

emotions = ["excited", "nervous", "happy", "worried", "grateful", "overwhelmed", "peaceful", "anxious", "confident", "tired"]

message_templates = [
    "Anyone else experiencing {topic}?",
    "Need advice about {topic}!",
    "Feeling {emotion} about {topic}",
    "Tips for dealing with {topic}?",
    "Just had my {week} week appointment, {topic} update!",
    "How do you handle {topic}?",
    "Celebrating a milestone: {topic}!",
    "Struggling with {topic}, any suggestions?",
    "Share your {topic} experiences!",
    "Looking for recommendations about {topic}"
]

responses = [
    "Have you tried {suggestion}? That helped me a lot!",
    "I went through the same thing! {experience}",
    "My doctor recommended {advice} for that.",
    "Here's what worked for me: {tips}",
    "Sending support! {encouragement}"
]

suggestions = [
    "staying hydrated", "gentle exercise", "prenatal yoga", "meditation",
    "talking to your doctor", "joining support groups", "reading pregnancy books",
    "getting more rest", "eating small, frequent meals", "taking warm baths"
]

encouragements = [
    "You're doing great! 💖",
    "Stay strong, mama! 🌸",
    "This too shall pass! 🌟",
    "You've got this! 💝",
    "We're here for you! 🤗"
]

# Generate user data
users = []
user_ids = []
for i in range(100):
    user_id = str(uuid.uuid4())
    user_ids.append(user_id)
    users.append({
        "user_id": user_id,
        "name": random.choice(names_pool),
        "age": random.randint(22, 40),
        "week": random.randint(4, 40)
    })

# Generate chat data
chats = []
base_date = datetime.now() - timedelta(days=30)
for user_id in user_ids:
    num_chats = random.randint(5, 15)
    for _ in range(num_chats):
        chat_time = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        topic = random.choice(topics)
        emotion = random.choice(emotions)
        message = random.choice(message_templates).format(
            topic=topic,
            emotion=emotion,
            week=random.randint(4, 40)
        )
        
        # Generate AI response using templates
        suggestion = random.choice(suggestions)
        encouragement = random.choice(encouragements)
        response = f"{random.choice(responses).format(suggestion=suggestion, experience='I found it got better over time.', advice=suggestion, tips=suggestion, encouragement=encouragement)} {encouragement}"
        
        chats.append({
            "user_id": user_id,
            "message": message,
            "response": response,
            "timestamp": chat_time.isoformat()
        })

# Generate community posts
posts = []
post_ids = []
base_date = datetime.now() - timedelta(days=30)
for i in range(150):
    post_id = str(uuid.uuid4())
    post_ids.append(post_id)
    post_time = base_date + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    topic = random.choice(topics)
    emotion = random.choice(emotions)
    content = random.choice(message_templates).format(
        topic=topic,
        emotion=emotion,
        week=random.randint(4, 40)
    )
    posts.append({
        "post_id": post_id,
        "user_id": random.choice(user_ids),
        "content": content,
        "timestamp": post_time.isoformat()
    })

# Generate mood logs
mood_logs = []
for user_id in user_ids:
    num_logs = random.randint(10, 30)
    for _ in range(num_logs):
        log_time = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        mood_logs.append({
            "user_id": user_id,
            "mood_value": random.randint(1, 10),
            "timestamp": log_time.isoformat()
        })

# Generate post supports
post_supports = []
for post_id in post_ids:
    post_supports.append({
        "post_id": post_id,
        "support_count": random.randint(0, 50)
    })

# Generate comments
comments = []
for post_id in post_ids:
    num_comments = random.randint(0, 5)
    for _ in range(num_comments):
        comment_time = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        comments.append({
            "post_id": post_id,
            "user_id": random.choice(user_ids),
            "content": random.choice(responses).format(
                suggestion=random.choice(suggestions),
                experience="I went through that too!",
                advice=random.choice(suggestions),
                tips=random.choice(suggestions),
                encouragement=random.choice(encouragements)
            ),
            "timestamp": comment_time.isoformat()
        })

# Save to SQL file
with open('d:/mamamuse/db/sample_data.sql', 'w', encoding='utf-8') as f:
    # Insert user_info
    for user in users:
        f.write(f"INSERT INTO user_info (user_id, name, age, week) VALUES ('{user['user_id']}', '{user['name']}', {user['age']}, {user['week']});\n")
    
    # Insert chats
    for chat in chats:
        f.write(f"INSERT INTO chats (user_id, message, response, timestamp) VALUES ('{chat['user_id']}', '{chat['message'].replace("'", "''")}', '{chat['response'].replace("'", "''")}', '{chat['timestamp']}');\n")
    
    # Insert community_posts
    for post in posts:
        f.write(f"INSERT INTO community_posts (post_id, user_id, content, timestamp) VALUES ('{post['post_id']}', '{post['user_id']}', '{post['content'].replace("'", "''")}', '{post['timestamp']}');\n")
    
    # Insert mood_logs
    for log in mood_logs:
        f.write(f"INSERT INTO mood_log (user_id, mood_value, timestamp) VALUES ('{log['user_id']}', {log['mood_value']}, '{log['timestamp']}');\n")
    
    # Insert post_supports
    for support in post_supports:
        f.write(f"INSERT INTO post_supports (post_id, support_count) VALUES ('{support['post_id']}', {support['support_count']});\n")
    
    # Insert comment_replies
    for comment in comments:
        f.write(f"INSERT INTO comment_replies (post_id, user_id, content, timestamp) VALUES ('{comment['post_id']}', '{comment['user_id']}', '{comment['content'].replace("'", "''")}', '{comment['timestamp']}');\n")

print("Sample data generation complete!")
