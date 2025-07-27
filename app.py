from flask import render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime, date, timedelta
import uuid
from transformers import AutoModelForCausalLM, AutoTokenizer
from supabase import create_client, Client
from config import app, supabase

# Register blueprints
from routes.community import bp as community_bp
app.register_blueprint(community_bp, url_prefix='/community')

app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here")
from diary_bot import generate_bot_response, DIARY_BOT_PROMPT

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required environment variables SUPABASE_URL and SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Qwen model with better error handling
model_name = "Qwen/Qwen3-0.6B"
model = None
tokenizer = None

try:
    print("Loading Qwen3 model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if not tokenizer:
        raise ValueError("Failed to initialize tokenizer")
        
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        trust_remote_code=True
    )
    if not model:
        raise ValueError("Failed to initialize model")
        
    print("Qwen3 model loaded successfully!")
    
    # Test the model with a simple prompt to ensure it's working
    test_prompt = "Hello"
    test_input = tokenizer(test_prompt, return_tensors="pt").to(model.device)
    _ = model.generate(**test_input, max_new_tokens=5)
    print("Model test generation successful!")
    
except Exception as e:
    print(f"Error loading Qwen3 model: {str(e)}")
    print("AI features will be disabled.")

def clean_ai_response(response):
    """
    Clean AI response by removing thinking tags and internal reasoning
    """
    import re
    
    # Remove <think>...</think> blocks
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove any other common reasoning patterns
    response = re.sub(r'\[thinking\].*?\[/thinking\]', '', response, flags=re.DOTALL | re.IGNORECASE)
    response = re.sub(r'\(thinking:.*?\)', '', response, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace
    response = re.sub(r'\s+', ' ', response).strip()
    
    return response

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    try:
        user_data = supabase.table("user_info").select("*").eq("user_id", session["user_id"]).execute()
        if not user_data.data:
            return redirect(url_for("first_login"))
        return redirect(url_for("home"))
    except Exception as e:
        print(f"Database error: {str(e)}")
        session.clear()
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        auth_option = request.form["auth_option"]
        try:
            print(f"Attempting {auth_option} for email: {email}")  # Debug log
            if auth_option == "Sign Up":
                user = supabase.auth.sign_up({"email": email, "password": password})
                print(f"Sign up successful. User ID: {user.user.id}")  # Debug log
                session["user_id"] = user.user.id
                flash("Account created successfully! Please complete your profile.", "success")
                return redirect(url_for("first_login"))
            else:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                print(f"Login successful. User ID: {user.user.id}")  # Debug log
                session["user_id"] = user.user.id
                user_data = supabase.table("user_info").select("*").eq("user_id", user.user.id).execute()
                print(f"User data found: {bool(user_data.data)}")  # Debug log
                if not user_data.data:
                    flash("Please complete your profile.", "success")
                    return redirect(url_for("first_login"))
                flash("Welcome back! 🌸", "success")
                return redirect(url_for("home"))
        except Exception as e:
            print(f"Auth error: {str(e)}")  # Debug log
            flash(f"Error: {str(e)}", "error")
    return render_template("login.html")

@app.route("/first_login", methods=["GET", "POST"])
def first_login():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        week = int(request.form["week"])
        supabase.table("user_info").insert({
            "user_id": session["user_id"],
            "name": name,
            "age": age,
            "week": week
        }).execute()
        return redirect(url_for("home"))
    return render_template("first_login.html")

@app.route("/logout")
def logout():
    supabase.auth.sign_out()
    session.clear()
    flash("Logged out successfully! 🌸", "success")
    return redirect(url_for("login"))

@app.route("/diary_bot", methods=["GET", "POST"])
def diary_bot():
    if "user_id" not in session:
        if request.is_json:
            return jsonify({"error": "Not authenticated"}), 401
        return redirect(url_for("login"))
    
    # Check if AI service is available
    if model is None or tokenizer is None:
        if request.is_json:
            return jsonify({"error": "AI service is currently unavailable"}), 503
        flash("AI service is currently unavailable. The model failed to load. Please try again later.", "error")
        return redirect(url_for("home"))
    
    # Get user info
    try:
        user_data = supabase.table("user_info").select("*").eq("user_id", session["user_id"]).execute()
        if not user_data.data:
            if request.is_json:
                return jsonify({"error": "User profile not complete"}), 400
            return redirect(url_for("first_login"))
        
        user_info = user_data.data[0]
        
        # Handle AJAX POST request
        if request.method == "POST" and request.is_json:
            data = request.get_json()
            user_input = data.get("message", "").strip()
            language = data.get("language", "English")
            
            if not user_input:
                return jsonify({"error": "Message cannot be empty"}), 400
            
            try:
                # Prepare system prompt with user context (English only, concise)
                system_prompt = (
                    f"You are Muse, a supportive pregnancy companion. "
                    f"IMPORTANT: Always respond in English only. Never use Spanish, French, or any other language. "
                    f"User: {user_info['name']}, {user_info['age']} years old, {user_info['week']} weeks pregnant. "
                    f"Be warm, empathetic, and supportive. Keep responses concise and focused on pregnancy/mental health support. "
                    f"Respond only in English language."
                )
                
                # Get minimal chat history for context (last 2 messages only for speed)
                chat_history = supabase.table("chats")\
                    .select("message, response")\
                    .eq("user_id", session["user_id"])\
                    .order("timestamp", desc=True)\
                    .limit(2)\
                    .execute()
                
                # Build minimal messages array for faster processing
                messages = [{"role": "system", "content": system_prompt}]
                for chat in reversed(chat_history.data):
                    messages.extend([
                        {"role": "user", "content": chat["message"]},
                        {"role": "assistant", "content": chat["response"]}
                    ])
                messages.append({"role": "user", "content": user_input})
                
                # Generate response
                text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                
                model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
                
                # Generate response with maximum speed optimization
                generated_ids = model.generate(
                    **model_inputs,
                    max_new_tokens=128,  # Further reduced for fastest responses
                    temperature=0.5,     # Lower for faster, more focused responses
                    top_p=0.7,          # Tighter sampling for speed
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    use_cache=True       # Enable caching for speed
                )
                
                # Decode response
                response = tokenizer.decode(
                    generated_ids[0][len(model_inputs.input_ids[0]):],
                    skip_special_tokens=True
                ).strip()
                
                # Clean the response to remove thinking tags and internal reasoning
                response = clean_ai_response(response)
                
                # Store in database
                chat_data = {
                    "user_id": session["user_id"],
                    "message": user_input,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                }
                
                supabase.table("chats").insert(chat_data).execute()
                
                return jsonify({
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error in diary_bot API: {str(e)}")
                return jsonify({"error": "An error occurred while processing your message"}), 500
        
        # Handle regular GET request
        chat_history = supabase.table("chats")\
            .select("*")\
            .eq("user_id", session["user_id"])\
            .order("timestamp")\
            .execute()
            
        return render_template("diary_bot.html", 
                           chat_history=chat_history.data,
                           datetime=datetime,
                           timedelta=timedelta)
    
    except Exception as e:
        print(f"Error in diary_bot: {str(e)}")
        if request.is_json:
            return jsonify({"error": "Internal server error"}), 500
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("home"))

@app.route("/community", methods=["GET", "POST"])
def community():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        content = request.form.get("content")
        if not content:
            flash("Please enter some content for your post.", "error")
            return redirect(url_for("community"))
        
        try:
            # Simple content moderation - just check for basic inappropriate content
            inappropriate_words = ['spam', 'advertisement', 'buy now', 'click here']
            content_lower = content.lower()
            
            # Check if content is too short or contains obvious spam
            if len(content.strip()) < 5:
                flash("Please write a more detailed post to share with the community. 🙏", "error")
            elif any(word in content_lower for word in inappropriate_words):
                flash("Your post may not be appropriate for this community. Please review our guidelines. 🙏", "error")
            else:
                # Create post - approve most content for supportive community
                post_id = str(uuid.uuid4())
                supabase.table("community_posts").insert({
                    "post_id": post_id,
                    "user_id": session["user_id"],
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }).execute()
                
                # Create initial support count
                supabase.table("post_supports").insert({
                    "post_id": post_id,
                    "support_count": 0
                }).execute()
                
                flash("Post shared successfully! 🌸", "success")
        except Exception as e:
            print(f"Error in post creation: {str(e)}")
            flash("There was an error sharing your post. Please try again. 🙏", "error")
        
        return redirect(url_for("community"))
    
    try:
        # Verify database connection first
        try:
            supabase.table("community_posts").select("count").limit(1).execute()
        except Exception as conn_error:
            print(f"Database connection error: {str(conn_error)}")
            flash("Unable to connect to the database. Please try again later.", "error")
            return redirect(url_for("home"))

        # Get posts without join query (since no foreign keys exist)
        posts_data = supabase.table("community_posts")\
            .select("*")\
            .order("timestamp", desc=True)\
            .limit(10)\
            .execute()

        if not posts_data.data:
            flash("No posts found. Be the first to share!", "info")
            return render_template("community.html", posts=[], has_more=False)
        
        # Get all user info for lookups
        users_data = supabase.table("user_info").select("*").execute()
        users_dict = {user["user_id"]: user for user in users_data.data}
        
        # Get post supports
        supports_data = supabase.table("post_supports").select("*").execute()
        supports_dict = {s["post_id"]: s["support_count"] for s in supports_data.data}
        
        # Get comments without join query (using comment_replies table)
        comments_data = supabase.table("comment_replies")\
            .select("*")\
            .order("timestamp")\
            .execute()
        
        comments_by_post = {}
        for comment in comments_data.data:
            post_id = comment["post_id"]
            if post_id not in comments_by_post:
                comments_by_post[post_id] = []
            comments_by_post[post_id].append(comment)

        # Process posts data
        posts = []
        for post in posts_data.data:
            # Calculate relative time for the post
            post_time = datetime.fromisoformat(post["timestamp"].replace("Z", "+00:00"))
            now = datetime.now()
            delta = now - post_time
            
            if delta.days > 0:
                relative_time = f"{delta.days}d ago"
            elif delta.seconds > 3600:
                relative_time = f"{delta.seconds // 3600}h ago"
            else:
                relative_time = f"{max(1, delta.seconds // 60)}m ago"
            
            # Process comments for this post
            comments = []
            post_comments = comments_by_post.get(post["post_id"], [])
            for comment in post_comments:
                comment_time = datetime.fromisoformat(comment["timestamp"].replace("Z", "+00:00"))
                comment_delta = now - comment_time
                
                if comment_delta.days > 0:
                    comment_relative = f"{comment_delta.days}d ago"
                elif comment_delta.seconds > 3600:
                    comment_relative = f"{comment_delta.seconds // 3600}h ago"
                else:
                    comment_relative = f"{max(1, comment_delta.seconds // 60)}m ago"
                
                # Get user info for this comment
                comment_user_info = users_dict.get(comment["user_id"], {"name": "Unknown"})
                
                comments.append({
                    "user_name": comment_user_info["name"],
                    "content": comment["content"],
                    "relative_time": comment_relative
                })
            
            # Get user info for this post
            user_info = users_dict.get(post["user_id"], {"name": "Unknown", "week": 0})
            
            posts.append({
                "post_id": post["post_id"],
                "user_name": user_info["name"],
                "user_week": user_info["week"],
                "content": post["content"],
                "relative_time": relative_time,
                "support_count": supports_dict.get(post["post_id"], 0),
                "comments": comments
            })
        
        return render_template("community.html", 
                             posts=posts,
                             has_more=len(posts_data.data) == 10)
    except Exception as e:
        print(f"Error loading community page: {str(e)}")
        flash("There was an error loading the community. Please try again. 🙏", "error")
        return redirect(url_for("home"))

@app.route("/support_post", methods=["POST"])
def support_post():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        post_id = data.get("post_id")
        
        if not post_id:
            return jsonify({"error": "Post ID is required"}), 400
        
        # Get current support count
        support_data = supabase.table("post_supports").select("*").eq("post_id", post_id).execute()
        
        if support_data.data:
            # Update existing support count
            current_count = support_data.data[0]["support_count"]
            new_count = current_count + 1
            supabase.table("post_supports").update({"support_count": new_count}).eq("post_id", post_id).execute()
        else:
            # Create new support entry
            supabase.table("post_supports").insert({"post_id": post_id, "support_count": 1}).execute()
            new_count = 1
        
        return jsonify({"success": True, "new_count": new_count})
    
    except Exception as e:
        print(f"Error supporting post: {str(e)}")
        return jsonify({"error": "Failed to support post"}), 500

@app.route("/add_comment", methods=["POST"])
def add_comment():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        post_id = data.get("post_id")
        content = data.get("content", "").strip()
        
        if not post_id or not content:
            return jsonify({"error": "Post ID and content are required"}), 400
        
        # Get user info
        user_data = supabase.table("user_info").select("name").eq("user_id", session["user_id"]).execute()
        if not user_data.data:
            return jsonify({"error": "User not found"}), 400
        
        user_name = user_data.data[0]["name"]
        
        # Add comment to database
        comment_data = {
            "post_id": post_id,
            "user_id": session["user_id"],
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        supabase.table("comment_replies").insert(comment_data).execute()
        
        return jsonify({
            "success": True,
            "comment": {
                "user_name": user_name,
                "content": content,
                "relative_time": "Just now"
            }
        })
    
    except Exception as e:
        print(f"Error adding comment: {str(e)}")
        return jsonify({"error": "Failed to add comment"}), 500

@app.route("/load_more_posts")
def load_more_posts():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    offset = request.args.get("offset", type=int, default=0)
    
    try:
        # Get posts without join query (since no foreign keys exist)
        posts_data = supabase.table("community_posts")\
            .select("*")\
            .order("timestamp", desc=True)\
            .range(offset, offset + 9)\
            .execute()
        
        if not posts_data.data:
            return jsonify({"posts": [], "has_more": False})
        
        # Get all user info for lookups
        users_data = supabase.table("user_info").select("*").execute()
        users_dict = {user["user_id"]: user for user in users_data.data}
        
        # Get post supports
        supports_data = supabase.table("post_supports").select("*").execute()
        supports_dict = {s["post_id"]: s["support_count"] for s in supports_data.data}
        
        posts = []
        for post in posts_data.data:
            post_time = datetime.fromisoformat(post["timestamp"].replace("Z", "+00:00"))
            now = datetime.now()
            delta = now - post_time
            
            if delta.days > 0:
                relative_time = f"{delta.days}d ago"
            elif delta.seconds > 3600:
                relative_time = f"{delta.seconds // 3600}h ago"
            else:
                relative_time = f"{max(1, delta.seconds // 60)}m ago"
            
            # Get user info for this post
            user_info = users_dict.get(post["user_id"], {"name": "Unknown", "week": 0})
            
            posts.append({
                "post_id": post["post_id"],
                "user_name": user_info["name"],
                "user_week": user_info["week"],
                "content": post["content"],
                "relative_time": relative_time,
                "support_count": supports_dict.get(post["post_id"], 0)
            })
        
        return jsonify({
            "posts": posts,
            "has_more": len(posts_data.data) == 10
        })
    except Exception as e:
        print(f"Error loading more posts: {str(e)}")
        return jsonify({"error": "Failed to load posts"}), 500


@app.route("/mental_summary")
def mental_summary():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Get today's chat messages
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time()).isoformat()
    today_end = datetime.combine(today, datetime.max.time()).isoformat()
    
    chats = supabase.table("chats")\
        .select("message, response")\
        .eq("user_id", session["user_id"])\
        .gte("timestamp", today_start)\
        .lte("timestamp", today_end)\
        .execute()
    
    # Get today's mood
    mood_data = supabase.table("mood_log")\
        .select("mood_value")\
        .eq("user_id", session["user_id"])\
        .gte("timestamp", today_start)\
        .lte("timestamp", today_end)\
        .execute()
    
    # Analyze mood and generate insights
    avg_mood = sum([m["mood_value"] for m in mood_data.data]) / len(mood_data.data) if mood_data.data else 5
    
    if avg_mood >= 8:
        today_emoji = "🌟"
        today_mood_description = "You're radiating positivity today!"
    elif avg_mood >= 6:
        today_emoji = "😊"
        today_mood_description = "You're having a good day!"
    elif avg_mood >= 4:
        today_emoji = "😐"
        today_mood_description = "You're feeling okay today."
    else:
        today_emoji = "🫂"
        today_mood_description = "Today might be challenging, but you're not alone."
    
    # Generate insights from chat history
    messages = " ".join([f"{c['message']} {c['response']}" for c in chats.data])
    
    # Use Qwen to analyze emotions and generate insights
    if messages and model and tokenizer:
        try:
            analysis_prompt = f"Based on these chat messages, provide a brief emotional insight and three supportive affirmations: {messages}"
            messages_list = [{"role": "user", "content": analysis_prompt}]
            
            text = tokenizer.apply_chat_template(
                messages_list,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=True
            )
            
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                top_k=20,
                repetition_penalty=1.1
            )
            
            output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
            try:
                index = len(output_ids) - output_ids[::-1].index(151668)
            except ValueError:
                index = 0
                
            response = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
            
            # Split response into insights and affirmations
            parts = response.split("\n")
            today_insights = parts[0] if parts else "Take a moment to reflect on your journey today."
            daily_affirmations = parts[1:4] if len(parts) > 1 else [
                "You are strong and capable of handling anything that comes your way.",
                "Your body is working beautifully to nurture new life.",
                "You deserve all the love and support surrounding you."
            ]
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            today_insights = "Take a moment to reflect on your journey today."
            daily_affirmations = [
                "You are strong and capable of handling anything that comes your way.",
                "Your body is working beautifully to nurture new life.",
                "You deserve all the love and support surrounding you."
            ]
    else:
        today_insights = "Start chatting with Muse to get personalized insights!"
        daily_affirmations = [
            "You are strong and capable of handling anything that comes your way.",
            "Your body is working beautifully to nurture new life.",
            "You deserve all the love and support surrounding you."
        ]
    
    # Generate wellness tips based on pregnancy week
    user_data = supabase.table("user_info").select("week").eq("user_id", session["user_id"]).execute()
    week = user_data.data[0]["week"] if user_data.data else 0
    
    wellness_tips = [
        f"Week {week}: Remember to stay hydrated and aim for 8-10 glasses of water daily.",
        "Practice gentle stretching or pregnancy-safe yoga to ease any discomfort.",
        "Take breaks throughout the day to rest and connect with your baby.",
        "Consider starting a gratitude journal to boost your mood."
    ]
    
    # Create emotion chart if enough data
    mood_history = supabase.table("mood_log")\
        .select("mood_value, timestamp")\
        .eq("user_id", session["user_id"])\
        .order("timestamp")\
        .limit(7)\
        .execute()
    
    emotion_chart = None
    if mood_history.data:
        df = pd.DataFrame(mood_history.data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format='ISO8601')
        df["date"] = df["timestamp"].dt.date
        
        fig = px.line(df, 
                     x="date",
                     y="mood_value",
                     title="Your Emotional Journey",
                     labels={"date": "Date", "mood_value": "Emotional State"},
                     color_discrete_sequence=["#ff9999"])
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", color="#4a2e4a"),
            showlegend=False
        )
        
        emotion_chart = pio.to_html(fig, full_html=False)
    
    return render_template("mental_summary.html",
                         today_emoji=today_emoji,
                         today_mood_description=today_mood_description,
                         today_insights=today_insights,
                         daily_affirmations=daily_affirmations,
                         wellness_tips=wellness_tips,
                         emotion_chart=emotion_chart)

@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Get user info
    user_data = supabase.table("user_info").select("*").eq("user_id", session["user_id"]).execute()
    user_info = user_data.data[0] if user_data.data else {"name": "", "age": 0, "week": 0}
    
    # Define pregnancy milestones and baby size comparisons
    milestones = {
        4: "Your baby is the size of a poppy seed! Focus on taking folic acid and staying hydrated. 🌱",
        8: "Your little one is like a raspberry! Morning sickness might peak - try ginger tea. 🫐",
        12: "Baby's grown to a plum! Time for your first trimester screening. 🍑",
        16: "Your baby is an avocado! You might start feeling tiny movements. 🥑",
        20: "Baby's the size of a banana! Anatomy scan time - so exciting! 🍌",
        24: "Your little one is like a corn on the cob! Time for glucose screening. 🌽",
        28: "Baby's grown to an eggplant! Third trimester begins - you're almost there! 🍆",
        32: "Your baby is the size of a squash! Start preparing your hospital bag. 🎃",
        36: "Little one's like a honeydew melon! Weekly check-ups begin now. 🍈",
        40: "Baby's the size of a small pumpkin! Any day now! 🎉"
    }
    
    # Find the closest milestone
    current_week = user_info["week"]
    closest_milestone = min(milestones.keys(), key=lambda x: abs(x - current_week))
    milestone = milestones[closest_milestone]
    
    if request.method == "POST":
        if "mood" in request.form:
            # Handle mood logging
            mood = int(request.form["mood"])
            supabase.table("mood_log").insert({
                "user_id": session["user_id"],
                "mood_value": mood,
                "timestamp": datetime.now().isoformat()
            }).execute()
            flash("Mood logged! Keep tracking your journey 🌈", "success")
        else:
            # Handle user info update
            try:
                name = request.form["name"]
                age = int(request.form["age"])
                week = int(request.form["week"])
                if age < 18 or age > 50:
                    raise ValueError("Age must be between 18 and 50")
                if week < 1 or week > 40:
                    raise ValueError("Week must be between 1 and 40")
                
                supabase.table("user_info").upsert({
                    "user_id": session["user_id"],
                    "name": name,
                    "age": age,
                    "week": week
                }).execute()
                flash("Profile updated successfully! 💖", "success")
                user_info = {"name": name, "age": age, "week": week}
                
                # Update milestone for new week
                closest_milestone = min(milestones.keys(), key=lambda x: abs(x - week))
                milestone = milestones[closest_milestone]
            except ValueError as e:
                flash(f"Error: {str(e)}", "error")
            except Exception as e:
                flash("An error occurred while updating your profile", "error")
    
    # Get mood data for chart
    mood_data = supabase.table("mood_log").select("mood_value, timestamp").eq("user_id", session["user_id"]).order("timestamp").execute()
    mood_chart = None
    if mood_data.data:
        df = pd.DataFrame(mood_data.data)
        # Fix datetime parsing
        df["timestamp"] = pd.to_datetime(df["timestamp"], format='ISO8601')
        
        # Create mood chart with Plotly
        fig = px.line(df, 
                     x="timestamp", 
                     y="mood_value",
                     title="Your Mood Journey",
                     labels={"timestamp": "Date", "mood_value": "Mood"},
                     color_discrete_sequence=["#ff9999"])
        
        # Customize chart appearance
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", color="#4a2e4a"),
            showlegend=False,
            hovermode="x unified",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        fig.update_traces(
            line=dict(width=3),
            mode="lines+markers",
            marker=dict(size=8, color="#ff9999")
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(74, 46, 74, 0.1)",
            showline=True,
            linewidth=2,
            linecolor="#4a2e4a"
        )
        
        fig.update_yaxes(
            range=[0, 10],
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(74, 46, 74, 0.1)",
            showline=True,
            linewidth=2,
            linecolor="#4a2e4a",
            ticktext=["😢", "😕", "😐", "🙂", "😊", "😃", "🤗", "🥰", "😍", "🌟"],
            tickvals=list(range(1, 11))
        )
        
        mood_chart = pio.to_html(fig, full_html=False)
    
    return render_template("home.html", 
                         user_info=user_info, 
                         milestone=milestone, 
                         mood_chart=mood_chart)

if __name__ == "__main__":
    app.run(debug=True)