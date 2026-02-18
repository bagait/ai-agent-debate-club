import os
import sys
from groq import Groq
from dotenv import load_dotenv

# --- Configuration & Constants ---
load_dotenv()

# For styling the console output
class C: 
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# --- Agent System Prompts ---
ENTHUSIAST_PROMPT = """You are an AI Enthusiast. Your persona is optimistic, forward-looking, and focused on the potential benefits and advancements of the debate topic. Your goal is to argue persuasively in favor of the topic. Be concise, compelling, and directly address the points made by your opponent."""

SKEPTIC_PROMPT = """You are an AI Skeptic. Your persona is cautious, critical, and focused on the potential risks, challenges, and limitations of the debate topic. Your goal is to argue persuasively against the topic. Be concise, compelling, and directly address the points made by your opponent."""

MODERATOR_PROMPT = """You are an impartial AI Moderator. Your role is to analyze the following debate transcript. Do not take a side. Your tasks are:
1. Briefly summarize the main arguments of the Enthusiast.
2. Briefly summarize the main arguments of the Skeptic.
3. Based purely on the persuasiveness, coherence, and strength of the arguments presented *in this transcript*, declare a winner.
4. Provide a one-sentence justification for your decision."""


class AIagent:
    """A simple wrapper for a Groq API agent with a specific persona."""
    def __init__(self, client, persona, model="llama3-8b-8192"):
        self.client = client
        self.persona = persona
        self.model = model

    def respond(self, history):
        """Generates a response based on the conversation history."""
        messages = [
            {"role": "system", "content": self.persona},
        ]
        messages.extend(history)
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=300,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"{C.RED}Error during API call: {e}{C.END}")
            return "I am unable to respond at this moment."

def run_debate(topic: str, rounds: int = 2):
    """Orchestrates the debate between the AI agents."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"{C.RED}ERROR: GROQ_API_KEY environment variable not found.{C.END}")
        print("Please create a .env file and add your Groq API key.")
        sys.exit(1)

    print(f"\n{C.BOLD}{C.CYAN}Debate Topic: {topic}{C.END}\n")

    client = Groq(api_key=api_key)

    enthusiast = AIagent(client, ENTHUSIAST_PROMPT)
    skeptic = AIagent(client, SKEPTIC_PROMPT)
    moderator = AIagent(client, MODERATOR_PROMPT, model="llama3-70b-8192")

    history = [
        {"role": "user", "content": f"The debate topic is: '{topic}'. You are the enthusiast. Please make your opening statement."}
    ]

    # Round 1: Enthusiast's Opening Statement
    print(f"{C.GREEN}{C.BOLD}Enthusiast (Opening Statement):{C.END}")
    response = enthusiast.respond(history)
    print(f"{C.GREEN}{response}{C.END}\n")
    history.append({"role": "assistant", "content": response})

    # Debate Rounds
    for i in range(rounds):
        print(f"{C.BOLD}{C.CYAN}--- Round {i + 1} ---{C.END}\n")

        # Skeptic's Turn
        history.append({"role": "user", "content": "You are the skeptic. Please present your counter-argument."})
        print(f"{C.RED}{C.BOLD}Skeptic:{C.END}")
        response = skeptic.respond(history)
        print(f"{C.RED}{response}{C.END}\n")
        history.pop() # Remove last user prompt
        history.append({"role": "assistant", "content": response})

        # Enthusiast's Turn
        history.append({"role": "user", "content": "You are the enthusiast. Please offer your rebuttal."})
        print(f"{C.GREEN}{C.BOLD}Enthusiast:{C.END}")
        response = enthusiast.respond(history)
        print(f"{C.GREEN}{response}{C.END}\n")
        history.pop() # Remove last user prompt
        history.append({"role": "assistant", "content": response})

    # Moderation
    print(f"\n{C.BOLD}{C.CYAN}--- Moderator's Judgment ---{C.END}\n")
    debate_transcript = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    moderator_input = [
        {"role": "user", "content": f"Here is the debate transcript on the topic '{topic}':\n\n{debate_transcript}"}
    ]
    judgment = moderator.respond(moderator_input)
    print(f"{C.BLUE}{judgment}{C.END}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} \"<debate_topic>\"")
        sys.exit(1)
    
    debate_topic = sys.argv[1]
    run_debate(debate_topic)
