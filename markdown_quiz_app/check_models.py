import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyCQxqd20Uni7WoljXiMg2_MxO5trQLRwzQ"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

with open("model_list_out.txt", "w") as f:
    try:
        f.write("Listing models:\n")
        models = list(genai.list_models())
        for m in models:
            f.write(f"- {m.name} ({m.display_name})\n")
    except Exception as e:
        f.write(f"Error: {str(e)}\n")
