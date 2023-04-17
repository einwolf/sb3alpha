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
    parser = argparse.ArgumentParser(description="Evaluation phase")

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

    # Play game
    step = 0
    done = False

    obs = env.reset()
    # obs, info = env.reset()

    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        # obs, rewards, terminated, truncated, info = env.step(action)

        # frame = env.render()

        # done = terminated or truncated
        done = done.all()
        if step > args.n_eval_episodes:
            done = True

    env.close()


if __name__ == "__main__":
    eval()
