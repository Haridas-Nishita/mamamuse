# MamaMuse

**Nurturing Minds, Empowering Moms**

---

![MamaMuse Banner](https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1200&q=80)

## 🌸 Inspiration
Pregnancy is a beautiful journey, but it can be filled with emotional ups and downs, anxiety, and loneliness. Inspired by real stories and the universal need for empathy, MamaMuse was created to be a digital companion—listening, uplifting, and connecting moms-to-be everywhere.

## ✨ What is MamaMuse?
MamaMuse is an AI-powered mental wellness platform for expecting mothers. It offers:
- **Empathetic Diary Bot (MUSE):** AI-powered, always-available emotional support.
- **Community:** A safe space to share stories, ask questions, and support each other.
- **Mood Tracking:** Log daily moods and visualize your emotional journey.
- **Personalized Content:** Week-by-week pregnancy insights and milestones.

## 🚀 Features
- **AI Diary Bot:** Built on Qwen3-0.6B (HuggingFace), delivers supportive, empathetic conversations.
- **Community Hub:** Post, comment, and support others in a positive environment.
- **Mood Visualization:** Beautiful charts powered by Plotly and Pandas.
- **Secure Authentication:** Supabase-powered login and user management.
- **Privacy First:** Your data is yours—secure and confidential.

## 🛠️ Built With
**Languages:** Python, HTML, CSS, JavaScript  
**Frameworks:** Flask, Jinja2  
**AI/ML:** HuggingFace Transformers (Qwen3-0.6B), PyTorch  
**Database:** Supabase (PostgreSQL, Auth)  
**Visualization:** Plotly, Pandas  
**Cloud Services:** Supabase, HuggingFace Model Hub  
**Other:** Gunicorn, python-dotenv, Accelerate

## 📦 Project Structure
```
├── app.py               # Main Flask app
├── config.py            # Flask & Supabase config
├── setup_db.py          # Database setup script
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── bot/                 # AI Diary Bot logic
├── db/                  # SQL scripts & sample data
├── routes/              # Flask blueprints (community, etc.)
├── scripts/             # Utility scripts
├── static/              # CSS, JS, images
├── templates/           # Jinja2 HTML templates
```

## ⚡ Quick Start
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/yourusername/mamamuse.git
   cd mamamuse
   ```
2. **Set Up Environment:**
   - Copy `.env.example` to `.env` and fill in your Supabase credentials.
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the Database:**
   ```bash
   python setup_db.py
   ```
5. **Run the App:**
   ```bash
   python app.py
   ```
6. **Open in Browser:**
   Go to `http://localhost:5000`

## 🏆 Accomplishments
- Built a truly empathetic AI bot for mental wellness.
- Fostered a safe, supportive community for moms-to-be.
- Created beautiful, insightful mood visualizations.
- Prioritized privacy and security throughout.

## 🚧 Challenges
- Tuning AI for genuine empathy and safety.
- Ensuring robust data privacy for sensitive health info.
- Balancing feature-richness with a simple, inviting UX.

## 📚 What We Learned
- The power of empathy and community in digital health.
- Integrating advanced AI models in real-world apps.
- The importance of privacy and trust in mental health tech.

## 🔮 What's Next for MamaMuse?
- Multilingual support for global reach.
- Direct access to mental health professionals.
- Mobile app for on-the-go support.
- Deeper, personalized wellness insights.

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

## 📄 License
[MIT](LICENSE)

---

**MamaMuse is more than an app—it’s a safe haven, a supportive friend, and a vibrant community for every mom-to-be. Together, we’re making mental wellness a joyful, shared journey.**
