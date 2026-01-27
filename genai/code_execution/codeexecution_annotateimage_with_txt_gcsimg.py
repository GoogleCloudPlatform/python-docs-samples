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
    # [START googlegenaisdk_codeexecution_with_txt_tableimg]
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
    #     import pandas as pd
    #     import seaborn as sns
    #
    #     data = [
    #         # Category, Task, G3P, G25P, Claude45, GPT51, LowerIsBetter
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
    #     columns = ["Category", "Task", "Gemini 3 Pro", "Gemini 2.5 Pro", "Claude Opus 4.5", "GPT-5.1", "LowerIsBetter"]
    #     df = pd.DataFrame(data, columns=columns)
    #
    #     competitors = ["Gemini 2.5 Pro", "Claude Opus 4.5", "GPT-5.1"]
    #     all_models = ["Gemini 3 Pro"] + competitors
    #
    #     normalized_rows = []
    #     for _, row in df.iterrows():
    #         task_scores = row[competitors].values
    #         if row["LowerIsBetter"]:
    #             sota = min(task_scores)
    #             normalized = {model: sota / row[model] for model in all_models}
    #         else:
    #             sota = max(task_scores)
    #             normalized = {model: row[model] / sota for model in all_models}
    #
    #         normalized["Category"] = row["Category"]
    #         normalized["Task"] = row["Task"]
    #         normalized_rows.append(normalized)
    #
    #     df_norm = pd.DataFrame(normalized_rows)
    #
    #     # Average per category
    #     df_avg = df_norm.groupby("Category")[all_models].mean().reset_index()
    #
    #     # Plotting
    #     sns.set_theme(style="whitegrid")
    #     plt.figure(figsize=(12, 7))
    #
    #     # Reshape for seaborn
    #     df_plot = df_avg.melt(id_vars="Category", value_vars=all_models, var_name="Model", value_name="Relative Performance")
    #
    #     ax = sns.barplot(data=df_plot, x="Category", y="Relative Performance", hue="Model", palette="viridis")
    #
    #     # Add a dashed line at 1.0 for prior SOTA
    #     plt.axhline(1.0, ls='--', color='gray', alpha=0.7, label='Prior SOTA (1.0)')
    #
    #     plt.title("Per-Category Performance Relative to Prior SOTA (Normalized to 1.0)", fontsize=16)
    #     plt.ylabel("Relative Performance (Prior SOTA = 1.0)", fontsize=12)
    #     plt.xlabel("Category", fontsize=12)
    #     plt.xticks(rotation=15)
    #     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    #     plt.ylim(0, 1.8) # Adjusted to see G3P lead clearly
    #     plt.tight_layout()
    #
    #     plt.savefig("performance_chart.png")
    #     plt.show()
    #
    #     ####################### 2. Executing Python Code #######################
    #     None
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/output-barplot-1.jpg
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/output-barplot-2.jpg
    #     Based on the data extracted from the benchmark table, I have calculated the average performance for each category normalized to the prior state-of-the-art (SOTA).
    #
    #     For each task, the prior SOTA was defined as the maximum score among **Gemini 2.5 Pro**, **Claude Opus 4.5**, and **GPT-5.1** (or the minimum for "lower is better" metrics like OmniDocBench). The performance of all models was then normalized relative to this baseline ($SOTA = 1.0$), and finally averaged across all benchmarks within each category.
    #
    #     The resulting bar chart illustrates Gemini 3 Pro's significant improvements over previous models, particularly in the **Screen**, **Spatial**, and **Visual Reasoning** categories.
    #
    #     ```python
    #     import matplotlib.pyplot as plt
    #     import pandas as pd
    #     import seaborn as sns
    #
    #     # Data extraction from the image
    #     data = [
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
    #     competitors = ["Gemini 2.5 Pro", "Claude Opus 4.5", "GPT-5.1"]
    #     all_models = ["Gemini 3 Pro"] + competitors
    #
    #     # Normalization Logic
    #     normalized_rows = []
    #     for row in data:
    #         cat, task, g3p, g25p, c45, g51, lib = row
    #         scores = {"Gemini 3 Pro": g3p, "Gemini 2.5 Pro": g25p, "Claude Opus 4.5": c45, "GPT-5.1": g51}
    #         comp_scores = [g25p, c45, g51]
    #
    #         if lib: # Lower is better
    #             sota = min(comp_scores)
    #             norm = {m: sota / scores[m] for m in all_models}
    #         else: # Higher is better
    #             sota = max(comp_scores)
    #             norm = {m: scores[m] / sota for m in all_models}
    #
    #         norm["Category"] = cat
    #         normalized_rows.append(norm)
    #
    #     # Grouping and Plotting
    #     df_avg = pd.DataFrame(normalized_rows).groupby("Category")[all_models].mean().reset_index()
    #     df_plot = df_avg.melt(id_vars="Category", var_name="Model", value_name="Relative Performance")
    #
    #     sns.set_theme(style="whitegrid")
    #     plt.figure(figsize=(12, 7))
    #     sns.barplot(data=df_plot, x="Category", y="Relative Performance", hue="Model", palette="viridis")
    #     plt.axhline(1.0, ls='--', color='gray', alpha=0.7, label='Prior SOTA (1.0)')
    #     plt.title("Per-Category Performance Relative to Prior SOTA", fontsize=16)
    #     plt.ylabel("Normalized Performance (Prior SOTA = 1.0)")
    #     plt.show()
    #     ```
    # [END googlegenaisdk_codeexecution_with_txt_tableimg]
    return True


if __name__ == "__main__":
    generate_content()
