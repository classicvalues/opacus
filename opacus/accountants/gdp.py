# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .accountant import IAccountant
from .analysis import gdp as privacy_analysis


class GaussianAccountant(IAccountant):
    def __init__(self):
        self.noise_multiplier = None
        self.sample_rate = None
        self.steps = 0

    def step(self, *, noise_multiplier: float, sample_rate: float):
        if self.noise_multiplier is None:
            self.noise_multiplier = noise_multiplier

        if self.sample_rate is None:
            self.sample_rate = sample_rate

        if noise_multiplier != self.noise_multiplier or sample_rate != self.sample_rate:
            raise ValueError(
                "Noise multiplier and sample rate have to stay constant in GaussianAccountant."
            )
        self.steps += 1

    def get_epsilon(self, delta: float, poisson: bool = True) -> float:
        """
        Return privacy budget (epsilon) expended so far.

        Args:
            delta: target delta
            poisson: ``True`` is input batches was sampled via Poisson sampling,
                ``False`` otherwise
        """

        compute_eps = (
            privacy_analysis.compute_eps_poisson
            if poisson
            else privacy_analysis.compute_eps_uniform
        )
        return compute_eps(
            steps=self.steps,
            noise_multiplier=self.noise_multiplier,
            sample_rate=self.sample_rate,
            delta=delta,
        )

    def __len__(self):
        return self.steps

    @classmethod
    def mechanism(cls) -> str:
        return "gpd"
