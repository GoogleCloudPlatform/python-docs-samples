# Copyright 2024 Google LLC
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
#

from google.cloud import discoveryengine_v1 as discoveryengine


def check_grounding_sample(
    project_id: str,
) -> discoveryengine.CheckGroundingResponse:
    # [START genappbuilder_check_grounding]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"

    client = discoveryengine.GroundedGenerationServiceClient()

    # The full resource name of the grounding config.
    # Format: projects/{project_id}/locations/{location}/groundingConfigs/default_grounding_config
    grounding_config = client.grounding_config_path(
        project=project_id,
        location="global",
        grounding_config="default_grounding_config",
    )

    request = discoveryengine.CheckGroundingRequest(
        grounding_config=grounding_config,
        answer_candidate="Titanic was directed by James Cameron. It was released in 1997.",
        facts=[
            discoveryengine.GroundingFact(
                fact_text=(
                    "Titanic is a 1997 American epic romantic disaster movie. It was directed, written,"
                    " and co-produced by James Cameron. The movie is about the 1912 sinking of the"
                    " RMS Titanic. It stars Kate Winslet and Leonardo DiCaprio. The movie was released"
                    " on December 19, 1997. It received positive critical reviews. The movie won 11 Academy"
                    " Awards, and was nominated for fourteen total Academy Awards."
                ),
                attributes={"author": "Simple Wikipedia"},
            ),
            discoveryengine.GroundingFact(
                fact_text=(
                    'James Cameron\'s "Titanic" is an epic, action-packed romance'
                    "set against the ill-fated maiden voyage of the R.M.S. Titanic;"
                    "the pride and joy of the White Star Line and, at the time,"
                    "the largest moving object ever built. "
                    'She was the most luxurious liner of her era -- the "ship of dreams" -- '
                    "which ultimately carried over 1,500 people to their death in the "
                    "ice cold waters of the North Atlantic in the early hours of April 15, 1912."
                ),
                attributes={"author": "Simple Wikipedia"},
            ),
        ],
        grounding_spec=discoveryengine.CheckGroundingSpec(citation_threshold=0.6),
    )

    response = client.check_grounding(request=request)

    # Handle the response
    print(response)
    # [END genappbuilder_check_grounding]

    return response


def rank_sample(
    project_id: str,
) -> discoveryengine.RankResponse:
    # [START genappbuilder_rank]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"

    client = discoveryengine.RankServiceClient()

    # The full resource name of the ranking config.
    # Format: projects/{project_id}/locations/{location}/rankingConfigs/default_ranking_config
    ranking_config = client.ranking_config_path(
        project=project_id,
        location="global",
        ranking_config="default_ranking_config",
    )
    request = discoveryengine.RankRequest(
        ranking_config=ranking_config,
        model="semantic-ranker-512@latest",
        top_n=10,
        query="What is Google Gemini?",
        records=[
            discoveryengine.RankingRecord(
                id="1",
                title="Gemini",
                content="The Gemini zodiac symbol often depicts two figures standing side-by-side.",
            ),
            discoveryengine.RankingRecord(
                id="2",
                title="Gemini",
                content="Gemini is a cutting edge large language model created by Google.",
            ),
            discoveryengine.RankingRecord(
                id="3",
                title="Gemini Constellation",
                content="Gemini is a constellation that can be seen in the night sky.",
            ),
        ],
    )

    response = client.rank(request=request)

    # Handle the response
    print(response)
    # [END genappbuilder_rank]

    return response
