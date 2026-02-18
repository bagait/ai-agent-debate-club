# AI Agent Debate Club

A simple framework for staging a debate between two AI agents with different personas, judged by a third AI moderator. This project uses the fast Groq API with Llama 3 to create an engaging and dynamic conversation on any topic you provide.



## Features

-   **Distinct AI Personas**: An AI Enthusiast argues for the topic, while an AI Skeptic argues against it.
-   **Structured Debate Flow**: The debate follows a clear, turn-based structure with opening statements and rebuttals.
-   **AI-Powered Moderation**: A third, more powerful AI agent (Llama 3 70B) analyzes the entire debate transcript to provide a summary and declare a winner.
-   **Fast & Dynamic**: Powered by the Groq API for near-instantaneous agent responses, making the debate feel alive.
-   **Customizable**: Easily change the debate topic, number of rounds, or even the agent personas in the `main.py` file.

## Installation

1.  **Clone the repository:**

    bash
    git clone https://github.com/bagait/ai-agent-debate-club.git
    cd ai-agent-debate-club
    

2.  **Create a virtual environment (recommended):**

    bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    

3.  **Install the dependencies:**

    bash
    pip install -r requirements.txt
    

4.  **Set up your API key:**

    -   Get a free API key from [GroqCloud](https://console.groq.com/keys).
    -   Create a file named `.env` in the project root.
    -   Add your API key to the `.env` file like this:

        
        GROQ_API_KEY="gsk_YourSecretKeyHere"
        

## Usage

Run the debate from your terminal by providing a topic in quotes. The script will handle the rest.

**Syntax:**

bash
python main.py "<your_debate_topic>"


### Example Debates

**Example 1: A classic AI topic**

bash
python main.py "All creative jobs will eventually be replaced by AI"


**Example 2: A philosophical topic**

bash
python main.py "Human consciousness is simply a complex algorithm"


**Example 3: A fun, lighthearted topic**

bash
python main.py "Pineapple is a valid and delicious pizza topping"


## How It Works

This project orchestrates a conversation between three distinct Large Language Model (LLM) instances:

1.  **The Enthusiast**: This agent receives a system prompt that instructs it to be optimistic and argue *for* the debate topic. Its goal is to highlight potential benefits and advancements.

2.  **The Skeptic**: This agent's system prompt instructs it to be cautious and critical, arguing *against* the topic. It focuses on risks, challenges, and limitations.

3.  **The Moderator**: This is a more powerful agent (using Llama 3 70B) that remains inactive during the debate. Once the debate concludes, it receives the entire conversation transcript. Its system prompt guides it to impartially summarize both sides' arguments, declare a winner based on the quality of reasoning within the debate, and provide a justification.

The `main.py` script manages the turn-based flow. It maintains a shared `history` of the conversation, which is passed to the active agent on its turn. This gives each agent the context of what has been said previously, allowing for direct rebuttals and a coherent discussion.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
