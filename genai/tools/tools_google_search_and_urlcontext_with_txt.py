# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def generate_content() -> str:
    # [START googlegenaisdk_tools_google_search_and_urlcontext_with_txt]
    from google import genai
    from google.genai.types import Tool, GenerateContentConfig, HttpOptions, UrlContext, GoogleSearch

    client = genai.Client(http_options=HttpOptions(api_version="v1beta1"))
    model_id = "gemini-2.5-flash"

    tools = [
        Tool(url_context=UrlContext),
        Tool(google_search=GoogleSearch),
    ]

    # TODO(developer): Here put your URLs!
    url = 'https://www.google.com/search?q=events+in+New+York'

    response = client.models.generate_content(
        model=model_id,
        contents=f"Give me three day events schedule based on {url}. Also let me know what needs to taken care of considering weather and commute.",
        config=GenerateContentConfig(
            tools=tools,
            response_modalities=["TEXT"],
        )
    )

    for each in response.candidates[0].content.parts:
        print(each.text)
    # Here is a possible three-day event schedule for New York City, focusing on the dates around October 7-9, 2025, along with weather and commute considerations.
    #
    # ### Three-Day Event Schedule: New York City (October 7-9, 2025)
    #
    # **Day 1: Tuesday, October 7, 2025 - Art and Culture**
    #
    # *   **Morning (10:00 AM - 1:00 PM):** Visit "Phillips Visual Language: The Art of Irving Penn" at 432 Park Avenue. This exhibition is scheduled to end on this day, offering a last chance to see it.
    # *   **Lunch (1:00 PM - 2:00 PM):** Grab a quick lunch near Park Avenue.
    # *   **Afternoon (2:30 PM - 5:30 PM):** Explore the "Lincoln Center Festival of Firsts" at Lincoln Center. This festival runs until October 23rd, offering various performances or exhibits. Check their specific schedule for the day.
    # *   **Evening (7:00 PM onwards):** Experience a classic Broadway show. Popular options mentioned for October 2025 include "Six The Musical," "Wicked," "Hadestown," or "MJ - The Musical."
    #
    # **Day 2: Wednesday, October 8, 2025 - Unique Experiences and SoHo Vibes**
    #
    # *   **Morning (11:00 AM - 1:00 PM):** Head to Brooklyn for the "Secret Room at IKEA Brooklyn" at 1 Beard Street. This unique event is scheduled to end on October 9th.
    # *   **Lunch (1:00 PM - 2:00 PM):** Enjoy lunch in Brooklyn, perhaps exploring local eateries in the area.
    # *   **Afternoon (2:30 PM - 5:30 PM):** Immerse yourself in the "The Weeknd & Nespresso Samra Origins Vinyl Cafe" at 579 Broadway in SoHo. This pop-up, curated by The Weeknd, combines coffee and music and runs until October 14th.
    # *   **Evening (6:00 PM onwards):** Explore the vibrant SoHo neighborhood, known for its shopping and dining. You could also consider a dinner cruise to see the illuminated Manhattan skyline and the Statue of Liberty.
    #
    # **Day 3: Thursday, October 9, 2025 - Film and Scenic Views**
    #
    # *   **Morning (10:00 AM - 1:00 PM):** Attend a screening at the New York Greek Film Expo, which runs until October 12th in New York City.
    # *   **Lunch (1:00 PM - 2:00 PM):** Have lunch near the film expo's location.
    # *   **Afternoon (2:30 PM - 5:30 PM):** Take advantage of the pleasant October weather and enjoy outdoor activities. Consider biking along the rivers or through Central Park to admire the early autumn foliage.
    # *   **Evening (6:00 PM onwards):** Visit an observation deck like the Empire State Building or Top of the Rock for panoramic city views. Afterwards, enjoy dinner in a neighborhood of your choice.
    #
    # ### Weather and Commute Considerations:
    #
    # **Weather in Early October:**
    #
    # *   **Temperatures:** Expect mild to cool temperatures. Average daily temperatures in early October range from 10°C (50°F) to 18°C (64°F), with occasional warmer days reaching the mid-20s°C (mid-70s°F). Evenings can be quite chilly.
    # *   **Rainfall:** October has a higher chance of rainfall compared to other months, with an average of 33mm and a 32% chance of rain on any given day.
    # *   **Sunshine:** You can generally expect about 7 hours of sunshine per day.
    # *   **What to Pack:** Pack layers! Bring a light jacket or sweater for the daytime, and a warmer coat for the evenings. An umbrella or a light raincoat is highly recommended due to the chance of showers. Comfortable walking shoes are a must for exploring the city.
    #
    # **Commute in New York City:**
    #
    # *   **Public Transportation is Key:** The subway is generally the fastest and most efficient way to get around New York City, especially during the day. Buses are good for East-West travel, but can be slower due to traffic.
    # *   **Using Apps:** Utilize Google Maps or official MTA apps to plan your routes and check for real-time service updates. The subway runs 24/7, but expect potential delays or changes to routes during nights and weekends due to maintenance.
    # *   **Rush Hour:** Avoid subway and commuter train travel during peak rush hours (8 AM - 10 AM and 5 PM - 7 PM) if possible, as trains can be extremely crowded.
    # *   **Subway Etiquette:** When on the subway, stand to the side of the doors to let people exit before boarding, and move to the center of the car to make space. Hold onto a pole or seat, and remove your backpack to free up space.
    # *   **Transfers:** Subway fare is $2.90 per ride, and you get one free transfer between the subway and bus within a two-hour window.
    # *   **Walking:** New York City is very walkable. If the weather is pleasant, walking between nearby attractions is an excellent way to see the city.
    # *   **Taxis/Ride-sharing:** Uber, Lyft, and Curb (for NYC taxis) are available, but driving in the city is generally discouraged due to traffic and parking difficulties.
    # *   **Allow Extra Time:** Always factor in an additional 20-30 minutes for travel time, as delays can occur.

    # get URLs retrieved for context
    print(response.candidates[0].url_context_metadata)
    # [END googlegenaisdk_tools_google_search_and_urlcontext_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
