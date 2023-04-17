import os

import gymnasium as gym
from pathlib import Path
import argparse

from stable_baselines3 import A2C
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import (EvalCallback,
                                                StopTrainingOnRewardThreshold)
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack, VecTransposeImage

environment_name = "ALE/Breakout-v5"

log_path = "tensorboard_logs"
a2c_model_path = os.path.join("saved_models", "a2c_model_breakout")


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="evaluate_policy phase")

    parser.add_argument("--n_eval_episodes", required=False, type=int, default=10,
                    help="Run evaluation for this many episodes")
    parser.add_argument("--load_model", required=False, type=Path, default=False,
                    help="Continue training from this model file")

    args = parser.parse_args()
    return args


def make_output_dirs():
    os.makedirs(log_path, exist_ok=True)
    os.makedirs(a2c_model_path, exist_ok=True)


def eval():
    """
    Evaluate model training
    """
    # Parse command line
    args = parse_cmd_line()

    print(f"{args.n_eval_episodes=}")
    print(f"{args.load_model=}")
    print(f"{log_path=}")

    # Initialize
    # make_output_dirs()

    env = make_atari_env(environment_name, n_envs=4, seed=0)
    env = VecFrameStack(env, n_stack=4)
    env = VecTransposeImage(env)

    print(f"Load model {args.load_model}")
    model = A2C.load(args.load_model, env=env)

    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=args.n_eval_episodes, render=True)
    print(f"mean_reward per episode = {mean_reward}")
    print(f"std_reward per episode = {std_reward}")

    env.close()


if __name__ == "__main__":
    eval()
