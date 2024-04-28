from model.llama import LlamaPrompter
import re

class LlamaResponseParser():
    def __init__(self):
        self.llama_model = LlamaPrompter()

    """Class to parse the request sent by the client to the server."""
    def post_to_llama(self, question: str, answer: str):
        """
        This method will delegate the creation of a response to the Llama class, after which it will extract the actual
        response from the JSON it gets to the actual string to respond with.

        :param input_text: The text you want Llama to respond to
        :return: response: The text Llama responded with in string format
        """
        prompt_to_ask = LlamaPrompter.format_prompt(question=question, answer=answer)
        return self.llama_model.ask_llama(prompt=prompt_to_ask)

    @staticmethod
    def parse_evaluation_response(response: str):
        """
        Parse the response by finding the overall evaluation score and pros and cons of the interviewee's answer

        Args:
            response (str): The response from the server

        Returns:
            dict: The overall evaluation score under key 'score' and a list of pros and consand pros and cons of the
                  interviewee's answer

        Example:
        {
            'evaluation_score': 80,
            'pros': [
                "Acknowledges the importance of teamwork: The candidate recognizes the value of collaboration in
                 achieving project goals, even if they struggled to implement it in their previous situation.",
                "Willingness to compromise: The candidate is open to finding a middle ground, even if it doesn't fully
                 align with their own perspective.",
                "Learned from the experience: The candidate identifies the importance of clear communication and
                 compromise in resolving disagreements, demonstrating that they can learn from past mistakes."
            ],
            'cons': [
                "Poor communication skills: The candidate's inability to effectively communicate their perspective
                 during the meeting with their colleague and manager suggests a need for improvement in this area.",
                "Lack of assertiveness: The candidate appears to have conceded to a compromise that did not fully align
                 with their own approach, which could indicate a lack of assertiveness in advocating for their own
                 ideas.",
                "Focus on individual perspective: The candidate's initial approach to the disagreement was to focus
                solely on their own part of the project, rather than prioritizing the team's goals and objectives."
            ]
        }
        """
        pat = re.compile("([0-9]{1,3}) out of 100")
        match = re.search(pat, response)
        evaluation = match.group(1)

        strengths_pattern = r'Strengths:(.*?)(?=Weaknesses:|$)'
        weaknesses_pattern = r'Weaknesses:(.*)'

        # Search for strengths and weaknesses in the text
        strengths_match = re.search(strengths_pattern, response, re.DOTALL)
        weaknesses_match = re.search(weaknesses_pattern, response, re.DOTALL)

        # Initialize lists to store strengths and weaknesses
        strengths = []
        weaknesses = []

        # If strengths are found, extract and append them to the strengths list
        if strengths_match:
            strengths_text = strengths_match.group(1).strip()
            strengths = [strength.strip() for strength in strengths_text.split('\n') if strength.strip()]

        # If weaknesses are found, extract and append them to the weaknesses list
        if weaknesses_match:
            weaknesses_text = weaknesses_match.group(1).strip()
            weaknesses = [weakness.strip() for weakness in weaknesses_text.split('\n') if weakness.strip()]

        # Create a dictionary to store strengths and weaknesses
        pros_and_cons = {
            "evaluation_score": evaluation,
            "pros": strengths,
            "cons": weaknesses
        }

        return pros_and_cons


if __name__ == "__main__":
    # Example usage of the LlamaResponseParser class, particularly the parse_evaluation_response method
    print(LlamaResponseParser.parse_evaluation_response(
    """Based on the answer provided, I would rate the candidate's response as an 85 out of 100 in terms of compatibility with other members of the team if hired. Here's my breakdown of the candidate's response:

    Strengths:
    
    Proactive conflict resolution: The candidate takes the initiative to resolve the disagreement by proposing a meeting with John to discuss their respective ideas. This demonstrates a proactive approach to conflict resolution, which is an important skill in any team environment.
    Collaboration: The candidate values collaboration and open communication within the team, as evident from their suggestion to prototype both solutions and their willingness to consider John's perspective.
    Data-driven decision making: The candidate advocates for gathering empirical data to make an informed decision, which is a valuable mindset in software engineering.
    Compromise: The candidate is willing to compromise and adopt a modified solution that incorporates elements of John's approach, demonstrating flexibility and a willingness to work towards a common goal.
    Weaknesses:
    
    Lack of assertiveness: While the candidate demonstrates a collaborative approach, they could have been more assertive in advocating for their own solution. This could be an area for improvement in a team setting.
    Limited focus on the bigger picture: The candidate's response focuses mainly on the technical aspects of the disagreement and the proposed solutions. They could have expanded their answer to include more context about the project's goals and how their proposed solution aligns with those objectives.
    Overall, the candidate demonstrates a strong ability to resolve conflicts and work collaboratively with others. However, they could improve their assertiveness and broader perspective-taking to better align with the team's goals and objectives."""
    ))