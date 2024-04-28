from llama_cpp import Llama
import re

MODEL_PATH = '/Users/vladco/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-chat-GGML/snapshots/3140827b4dfcb6b562cd87ee3d7f07109b014dd0/llama-2-13b-chat.ggmlv3.q5_1.bin'

class LlamaPrompter():
    
    def __init__(self):
        self.model = Llama(
            model_path=MODEL_PATH,
            n_threads=10,
            n_batch=512,
            n_gpu_layers=32,
            n_ctx=2048
        )
    
    @staticmethod
    def format_prompt(question, answer):
        return f"""
        USER:
        Strengths: [List of strenghts]
        Weaknesses: [List of weaknesses]

        You will take the role of an interviewer for a behavioral interview for an entry level position in Software Engineering. You will be given the question you asked the interviewee as well as the answer provided in this prompt, and your task will be to rate his answer on a scale from 0 to 100 in accordance to the level of expected compatibility with other members of the team if the candidate is hired.
        Question: {question}
        Answer: {answer}

        ASSISTANT:
        """
    
    def ask_llama(self, prompt):
        response = self.model(prompt=prompt, max_tokens=1024, temperature=.7, top_p=1, echo=True)
        print(response["choices"][0]["text"])
        return re.split("[\n ]Overall,", response["choices"][0]["text"].split("ASSISTANT:")[1])[0]