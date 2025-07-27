# DiaryBot system prompt
DIARY_BOT_PROMPT = """You are MUSE (Mental Understanding and Support Entity), a supportive and empathetic AI companion focused on mental well-being.

Role: Engage in supportive conversations in English only.
Goal: Help users process emotions and thoughts.

Guidelines:
1. Show empathy and active listening
2. Ask clarifying questions when needed 
3. Provide constructive suggestions and coping strategies
4. Keep responses clear, concise and warm
5. Recognize signs of distress and recommend professional help if needed
"""

class DiaryBot:
    def __init__(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # Initialize Qwen model
        model_name = "Qwen/Qwen3-0.6B"
        try:
            print("Loading Qwen3 model...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype="auto",
                device_map="auto"
            )
            print("Qwen3 model loaded successfully!")
        except Exception as e:
            print(f"Error loading Qwen3 model: {str(e)}")
            self.model = None
            self.tokenizer = None

    def generate_response(self, user_message, conversation_history):
        """
        Generate a response using the Qwen3 model
        """
        try:
            if not self.model or not self.tokenizer:
                return "I'm currently having trouble processing messages. Please try again later."

            # Format the conversation for the model
            conversation = f"{DIARY_BOT_PROMPT}\n\nConversation history:\n{conversation_history}\n\nUser: {user_message}\nMUSE:"
            
            # Generate response
            inputs = self.tokenizer(conversation, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=500,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.pad_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the bot's response
            return response.split("MUSE:")[-1].strip()
        
        except Exception as e:
            print(f"Error in diary_bot: {str(e)}")
            return "I apologize, but I'm having trouble processing your message right now. Could you please try again?"

# Initialize the bot instance
diary_bot = DiaryBot()

# Function to use in routes
def generate_bot_response(user_message, conversation_history):
    return diary_bot.generate_response(user_message, conversation_history)
