import logging

from gym_jass.envs import SchieberEnv
from jass_bot.rl import JassPolicy
from stable_baselines import PPO2
from stable_baselines.common.vec_env import DummyVecEnv

from schieber.player.challenge_player.challenge_player import ChallengePlayer

from schieber.player.base_player import BasePlayer

from schieber.player.external_player import ExternalPlayer

logger = logging.getLogger(__name__)


class ModelPlayer(ChallengePlayer):
    """
    This player can be used to evaluate the strength of a trained RL model.
    """

    def __init__(self, name='unknown', seed=None, trumps='all',
                 model_path="/Users/joelito/MEGA/Studium/Master/Informatik/Courses/Data Science/Very Deep Learning/Project/schieber/tests/benchmarks/models/stich-higher-learning-rate_env=Schieber-v0_gamma=0.89_nsteps=90_learning_rate=0.001_policy=JassPolicy_model=PPO2_time=2019-01-13_12:08:28_final.pkl"):
        """
        Inits the player with a trained model. This model is based on the stable_baselines framework.
        (It has to implement the predict() function)
        :param model_path:
        """
        super().__init__(name, seed, trumps)
        env = SchieberEnv()
        env = DummyVecEnv([lambda: env])
        self.model = PPO2.load(load_path=model_path, env=env, policy=JassPolicy)


def choose_card(self, state=None):
    obs_dict = ExternalPlayer.build_observation(state, self.cards)
    obs = SchieberEnv.observation_dict_to_onehot_matrix(obs_dict)
    action = self.model.predict(obs)[0]
    return self.cards[action]
