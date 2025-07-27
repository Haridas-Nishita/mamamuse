# 🌷 MamaMuse

> **Nurturing Minds, Empowering Moms — Your AI-Powered Mental Wellness Companion for Pregnancy**

---

## 🌸 Inspiration
Pregnancy is a time of transformation, filled with excitement, uncertainty, and a whirlwind of emotions. Too often, expecting mothers face these challenges alone, without access to mental health support or a safe, understanding community. MamaMuse was born from a desire to change that — to create a digital sanctuary where every mom-to-be feels heard, supported, and empowered.

## ✨ What is MamaMuse?
MamaMuse is an all-in-one mental wellness platform designed for pregnant women. It combines the power of AI, community, and beautiful design to:
- Offer a supportive, empathetic diary bot (MUSE) for emotional check-ins and conversations.
- Provide a vibrant, positive community for sharing stories, advice, and encouragement.
- Track moods and visualize emotional journeys with stunning charts.
- Deliver week-by-week pregnancy insights and milestones tailored to each user.

## 🚀 Features

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 🤖 AI Diary Bot (MUSE) | 24/7 empathetic support, powered by Qwen3-0.6B, for safe, judgment-free chats|
| 🫂 Community Hub       | Share posts, comment, and support other moms in a positive environment       |
| 📈 Mood Tracking       | Log daily moods and see your emotional journey visualized with Plotly         |
| 🗓️ Personalized Content| Get relevant tips and milestones for your current pregnancy week              |
| 🔒 Secure & Private    | Supabase-backed authentication and robust data privacy                       |
| 🌐 Multilingual Ready  | (Coming soon) Support for multiple languages                                 |

## 🛠️ Built With
- **Languages:** Python, HTML, CSS, JavaScript
- **Frameworks:** Flask, Jinja2
- **AI/ML:** HuggingFace Transformers (Qwen3-0.6B), PyTorch
- **Database & Auth:** Supabase (PostgreSQL, Auth)
- **Visualization:** Plotly, Pandas
- **Cloud Services:** Supabase, HuggingFace Model Hub
- **Other:** Gunicorn, python-dotenv, Accelerate

## 📦 Project Structure
```text
mamamuse/
├── app.py               # Main Flask app
├── config.py            # Flask & Supabase config
├── setup_db.py          # Database setup script
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── bot/                 # AI Diary Bot logic
├── db/                  # SQL scripts & sample data
├── routes/              # Flask blueprints (community, etc.)
├── scripts/             # Utility scripts
├── static/              # CSS, JS, images
├── templates/           # Jinja2 HTML templates
```

## 👩‍🍼 User Stories

- **Priya, First-Time Mom:** “I felt anxious and alone during my first trimester. MamaMuse’s diary bot was always there to listen, and the community made me feel understood.”
- **Sofia, Working Professional:** “Logging my moods helped me spot patterns and take better care of myself. The weekly tips were a bonus!”
- **Aisha, Community Seeker:** “I loved sharing my journey and learning from other moms. The support I received was incredible.”

## 📝 Usage Guide

1. **Sign Up / Log In:** Secure authentication via Supabase ensures your privacy from the start.
2. **Complete Your Profile:** Enter your pregnancy week to receive personalized content.
3. **Chat with MUSE:** Open the Diary Bot and start a conversation—vent, ask questions, or just share your day.
4. **Log Your Mood:** Use the mood tracker daily to build your emotional journey chart.
5. **Join the Community:** Post, comment, and support other moms in the Community tab.
6. **View Insights:** Access milestone tips and your mood history on your dashboard.

## ❓ FAQ

**Q: Is my data safe?**  
A: Absolutely. All sensitive information is encrypted and never shared without your consent.

**Q: Can I use MamaMuse on my phone?**  
A: Yes! The app is fully responsive and works on desktop, tablet, and mobile browsers.

**Q: Is the AI bot a replacement for therapy?**  
A: No. MUSE is designed for support and companionship, not as a substitute for professional mental health care.

**Q: Will there be more languages?**  
A: Multilingual support is on our roadmap!

## 🌟 Why MamaMuse?

- **Empathy-First AI:** MUSE is trained to listen, respond with warmth, and provide science-backed support.
- **Community-Powered:** Real stories, real advice, and real encouragement from moms like you.
- **Beautiful Visuals:** Track your moods and milestones with interactive, easy-to-understand charts.
- **Privacy by Design:** Your journey is yours—always private, always secure.

## 🤝 How to Contribute

We welcome contributions from developers, designers, and mental health advocates! To contribute:
1. Fork this repo and clone your fork.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a clear description.

For major changes, please open an issue first to discuss what you’d like to change.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> **MamaMuse isn’t just an app — it’s a safe haven, a supportive friend, and a vibrant community for every mom-to-be. Together, we’re making mental wellness a joyful, shared journey.**

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

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Haridas-Nishita/mamamuse.git
   cd mamamuse
   ```
2. **Set Up Environment**
   - Copy `.env.example` to `.env` and add your Supabase credentials.
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the Database**
   ```bash
   python setup_db.py
   ```
5. **Run the App**
   ```bash
   python app.py
   ```
6. **Open in Browser**
   Go to [http://localhost:5000](http://localhost:5000)

## 🏆 Accomplishments
- Developed an empathetic AI bot that delivers real, supportive conversations.
- Fostered a safe, inclusive community for expecting mothers.
- Created beautiful mood visualizations to help users track their emotional journey.
- Prioritized privacy and security at every step.
- Designed a platform that’s as welcoming as it is powerful.

## 🚧 Challenges
- **Crafting Empathy:** Tuning the AI for warmth, safety, and real understanding.
- **Data Privacy:** Protecting sensitive health data was non-negotiable.
- **Supabase Integration:** Learning to leverage Supabase for authentication and data.
- **Performance:** Balancing AI, real-time updates, and smooth UX.
- **User Experience:** Ensuring simplicity and accessibility for all users.

## 📚 What We Learned
- The transformative power of empathy and community in digital health.
- Integrating advanced AI models into real-world, user-facing applications.
- The critical importance of privacy, trust, and accessibility in mental health tech.
- That technology, when built with heart, can make a real difference.

## 🔮 What's Next for MamaMuse?
- **Multilingual Support:** Expanding MUSE for global reach.
- **Professional Resources:** Direct access to mental health professionals.
- **Mobile App:** Bringing MamaMuse to iOS and Android.
- **Personalized Insights:** Deeper, AI-driven wellness recommendations.
- **Healthcare Partnerships:** Collaborating with providers to reach more moms.


## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

> **MamaMuse isn’t just an app — it’s a safe haven, a supportive friend, and a vibrant community for every mom-to-be. Together, we’re making mental wellness a joyful, shared journey.**
