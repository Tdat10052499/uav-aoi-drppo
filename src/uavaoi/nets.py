"""Feature extractors for SB3 policies (EXP-08 onward).

Moved from scripts/train_ppo.py on 07/11/2026 (FAO request, notes/yeu-cau/2026-11-06_fao_can-DAT_python-model.md
item 2 (a)). When a class lives in a script run as __main__, cloudpickle stores it *by value* with the
bytecode of the Python that trained it, so model.zip can only be loaded by the same Python minor version
(EXP-01..03 models need Python 3.12). Defined in an importable module, the class is pickled *by reference*
(uavaoi.nets.SmallCNN) and loads on any Python that has this code. Architecture unchanged.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class SmallCNN(BaseFeaturesExtractor):
    """Feature extractor for the 5 x 31 x 31 centred map (NatureCNN needs >= 36 x 36)."""

    def __init__(self, observation_space, features_dim: int = 256):
        super().__init__(observation_space, features_dim)
        c = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(c, 32, 3, stride=1, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=2, padding=1), nn.ReLU(),
            nn.Flatten(),
        )
        with torch.no_grad():
            n = self.cnn(torch.zeros(1, *observation_space.shape)).shape[1]
        self.head = nn.Sequential(nn.Linear(n, features_dim), nn.ReLU())

    def forward(self, x):
        return self.head(self.cnn(x))


class MapCandExtractor(BaseFeaturesExtractor):
    """Dict observation of TourGuidedEnv: SmallCNN on 'map' + MLP on the K x 4 candidate
    features 'cand', concatenated (EXP-08 arms M1-M3)."""

    def __init__(self, observation_space, features_dim: int = 256, cand_dim: int = 64):
        super().__init__(observation_space, features_dim)
        self.map_net = SmallCNN(observation_space["map"], features_dim=features_dim)
        n_cand = int(np.prod(observation_space["cand"].shape))
        self.cand_net = nn.Sequential(nn.Linear(n_cand, cand_dim), nn.ReLU())
        self.head = nn.Sequential(nn.Linear(features_dim + cand_dim, features_dim), nn.ReLU())

    def forward(self, obs):
        return self.head(torch.cat([self.map_net(obs["map"]), self.cand_net(obs["cand"])], dim=1))
