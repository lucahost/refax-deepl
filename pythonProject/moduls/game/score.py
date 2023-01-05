from pythonProject.moduls.config import app_config
class_names = app_config.class_names


class Score:
    def __init__(self, predictions, number_of_challenges, current_challenge):
        challenges = set(map(lambda x: x[0], predictions))
        grouped = [[y for y in predictions if y[0] == x] for x in challenges]

        self.scores = [ChallengeScore(prediction) for prediction in grouped]
        self.current_challenge = current_challenge
        self.global_score = self.get_global(number_of_challenges)
        self.current_score = self.get_current_challenge()

    def get_global(self, number_of_challenges):
        score_sum = sum([score.score for score in self.scores])
        return score_sum / number_of_challenges

    def get_current_challenge(self):
        current = None
        for score in self.scores:
            if score.challenge == self.current_challenge:
                current = score
        if current is None:
            return 0
        return current.score


class ChallengeScore:
    def __init__(self, predictions):
        self.challenge = predictions[0][0]
        challenge_number = class_names.index(self.challenge)
        values = [x[1][challenge_number] for x in predictions]
        self.score = sum(values) / len(values)
