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


def generate_content() -> bool:
    # [START googlegenaisdk_codeexecution_barplot_with_txt_img]
    import io
    from PIL import Image
    from google import genai
    from google.genai import types

    # Read a local image as input
    image_pil = Image.open("sample_images/tabular_data.png")
    image_pil = image_pil.convert("RGB")
    byte_io = io.BytesIO()
    image_pil.save(byte_io, format="JPEG")
    image_bytes = byte_io.getvalue()
    image = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            image,
            "Make a bar chart of per-category performance, normalize prior SOTA as 1.0 for each task,"
            "then take average per-category. Plot using matplotlib with nice style.",
        ],
        config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution)]),
    )

    img_count = 0
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        if part.executable_code is not None:
            print("####################### 1. Generate Python Code #######################")
            print(part.executable_code.code)
        if part.code_execution_result is not None:
            print("####################### 2. Executing Python Code #######################")
            print(part.code_execution_result.output)
        # For local executions, save the output to a local filename
        if part.as_image() is not None:
            print("####################### 3. Save Output #######################")
            img_count += 1
            output_location = f"sample_images/output-barplot-{img_count}.jpg"
            image_data = part.as_image().image_bytes
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")
            image.save(output_location)
            print(f"Output is saved to {output_location}")
    # Example response:
    #     ####################### 1. Generate Python Code #######################
    #     import matplotlib.pyplot as plt
    #     import numpy as np
    #
    #     data = [
    #         # Category, Benchmark, G3P, G2.5P, C4.5, GPT5.1, lower_is_better
    #         ("Visual Reasoning", "MMMU Pro", 81.0, 68.0, 72.0, 76.0, False),
    #         ("Visual Reasoning", "VLMsAreBiased", 50.6, 24.3, 32.7, 21.7, False),
    #         ("Document", "CharXiv Reasoning", 81.4, 69.6, 67.2, 69.5, False),
    #         ("Document", "OmniDocBench1.5*", 0.115, 0.145, 0.120, 0.147, True),
    #         ("Spatial", "ERQA", 70.5, 56.0, 51.3, 60.0, False),
    #         ("Spatial", "Point-Bench", 85.5, 62.7, 38.5, 41.8, False),
    #         ("Spatial", "RefSpatial", 65.5, 33.6, 19.5, 28.2, False),
    #         ("Spatial", "CV-Bench", 92.0, 85.9, 83.8, 84.6, False),
    #         ("Spatial", "MindCube", 77.7, 57.5, 58.5, 61.7, False),
    #         ("Screen", "ScreenSpot Pro", 72.7, 11.4, 49.9, 3.50, False),
    #         ("Screen", "Gui-World QA", 68.0, 42.8, 44.9, 38.7, False),
    #         ("Video", "Video-MMMU", 87.6, 83.6, 84.4, 80.4, False),
    #         ("Video", "Video-MME", 88.4, 86.9, 84.1, 86.3, False),
    #         ("Video", "1H-VideoQA", 81.8, 79.4, 52.0, 61.5, False),
    #         ("Video", "Perception Test", 80.0, 78.4, 74.1, 77.8, False),
    #         ("Video", "YouCook2", 222.7, 188.3, 145.8, 132.4, False),
    #         ("Video", "Vatex", 77.4, 71.3, 60.1, 62.9, False),
    #         ("Video", "Motion Bench", 70.3, 66.3, 65.9, 61.1, False),
    #         ("Education", "Math Kangaroo", 84.4, 77.4, 68.9, 79.9, False),
    #         ("Biomedical", "MedXpertQA-MM", 77.8, 65.9, 62.2, 65.5, False),
    #         ("Biomedical", "VQA-RAD", 81.9, 71.4, 76.0, 72.2, False),
    #         ("Biomedical", "MicroVQA", 68.8, 63.5, 61.4, 61.5, False),
    #     ]
    #
    #     normalized_scores = []
    #     for cat, bench, g3p, g25p, c45, gpt, lib in data:
    #         others = [g25p, c45, gpt]
    #         if lib:
    #             sota = min(others)
    #             norm_score = sota / g3p
    #         else:
    #             sota = max(others)
    #             norm_score = g3p / sota
    #         normalized_scores.append((cat, norm_score))
    #
    #     categories = {}
    #     for cat, score in normalized_scores:
    #         if cat not in categories:
    #             categories[cat] = []
    #         categories[cat].append(score)
    #
    #     avg_per_category = {cat: np.mean(scores) for cat, scores in categories.items()}
    #
    #     # Plotting
    #     cats = list(avg_per_category.keys())
    #     values = [avg_per_category[c] for c in cats]
    #
    #     # Sort categories for better visualization if needed, or keep order from data
    #     plt.figure(figsize=(10, 6))
    #     plt.style.use('ggplot')
    #     bars = plt.bar(cats, values, color='skyblue', edgecolor='navy')
    #
    #     plt.axhline(y=1.0, color='red', linestyle='--', label='Prior SOTA (1.0)')
    #     plt.ylabel('Normalized Performance (SOTA = 1.0)')
    #     plt.title('Gemini 3 Pro Performance relative to Prior SOTA (Normalized)', fontsize=14)
    #     plt.xticks(rotation=45, ha='right')
    #     plt.ylim(0, max(values) * 1.2)
    #
    #     for bar in bars:
    #         yval = bar.get_height()
    #         plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{yval:.2f}x', ha='center', va='bottom')
    #
    #     plt.legend()
    #     plt.tight_layout()
    #     plt.savefig('performance_chart.png')
    #     plt.show()
    #
    #     print(avg_per_category)
    #
    #     ####################### 2. Executing Python Code #######################
    #     {'Visual Reasoning': np.float64(1.3065950426525028), 'Document': np.float64(1.1065092453773113), 'Spatial': np.float64(1.3636746436001959), 'Screen': np.float64(1.4856952211773211), 'Video': np.float64(1.0620548283943443), 'Education': np.float64(1.0563204005006257), 'Biomedical': np.float64(1.1138909257119955)}
    #
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/output-barplot-1.jpg
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/output-barplot-2.jpg
    #     Based on the data provided in the table, I have calculated the per-category performance of Gemini 3 Pro normalized against the prior state-of-the-art (SOTA), which is defined as the best performance among Gemini 2.5 Pro, Claude Opus 4.5, and GPT-5.1 for each benchmark.
    #
    #     For benchmarks where lower values are better (indicated by an asterisk, e.g., OmniDocBench1.5*), the normalization was calculated as $\text{Prior SOTA} / \text{Gemini 3 Pro Score}$. For all other benchmarks, it was calculated as $\text{Gemini 3 Pro Score} / \text{Prior SOTA}$. The values were then averaged within each category.
    #
    #     The resulting bar chart below shows that Gemini 3 Pro outperforms the prior SOTA across all categories, with the most significant gains in **Screen** (1.49x), **Spatial** (1.36x), and **Visual Reasoning** (1.31x) benchmarks.
    #
    #     ![Gemini 3 Pro Performance Chart](performance_chart.png)
    # [END googlegenaisdk_codeexecution_barplot_with_txt_img]
    return True


if __name__ == "__main__":
    generate_content()
