from openai import OpenAI
import pandas as pd
import json
import re
import sqlite3

class DataAnalyzer:
    def __init__(self, key, data, null=False, dup=False, index=False):
        self.null = null
        self.dup = dup
        self.index = index
        self.data = data
        self.key = key
        self.client = OpenAI(api_key=self.key)
        self.df = self.load_data(drop_na=null, drop_dup=dup, reset_index=index)
        self.prompt_manager = self.PromptManager(self)

    def data_report_builder(self):
        df = self.load_data(drop_na=self.null, drop_dup=self.dup, reset_index=self.index, reset_data=True)
        total_null = df.isna().sum()
        total_duplicated = df.duplicated().sum()
        data_len = len(df)
        null_report = pd.DataFrame({
            "Column": total_null.index,
            "Missing Values": total_null.values,
            "% Missing": (total_null.values / data_len * 100).round(2)
        })
        return {
            "total_rows": data_len,
            "total_duplicates": int(total_duplicated),
            "null_report": null_report[null_report["Missing Values"] > 0].to_dict(orient="records")
        }

    def load_data(self, drop_na=True, drop_dup=True, reset_index=True, reset_data=False):
        if reset_data:
            self.data.seek(0)

        if hasattr(self.data, 'name'):
            name = self.data.name
        else:
            name = ""

        if name.endswith('.csv'):
            self.df = pd.read_csv(self.data)
        elif name.endswith('.xlsx'):
            self.df = pd.read_excel(self.data)
        elif name.endswith('.json'):
            self.df = pd.read_json(self.data)
        elif name.endswith('.parquet'):
            self.df = pd.read_parquet(self.data)
        elif name.endswith('.db') or name.endswith('.sqlite'):
            conn = sqlite3.connect(name)
            self.df = pd.read_sql_query("SELECT * FROM your_table", conn)
        elif name.endswith('.txt'):
            self.df = pd.read_csv(self.data, delimiter="\t")
        else:
            raise ValueError("Unsupported file format.")

        if drop_na:
            self.df.dropna(inplace=True)
        if drop_dup:
            self.df.drop_duplicates(inplace=True)
        if reset_index:
            self.df.reset_index(drop=True, inplace=True)

        return self.df

    def ai_summary(self):
        prompt = self.prompt_manager.data_summary_prompt()
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI data analyst."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content

    def ai_json(self):
        prompt = self.prompt_manager.data_json_prompt()
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're an expert data visualization assistant"},
                {"role": "user", "content": prompt}
            ],
        )
        content = response.choices[0].message.content

        try:
            json_block = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL).group(0)
            return json.loads(json_block)
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse AI JSON response.",
                "raw_response": content,
                "exception": str(e)
            }

    def data_chat(self, user_query, chat_history=None):
        if not user_query:
            return {"error": "No user query provided."}

        prompt = self.prompt_manager.data_chat_prompt(user_query)

        message_history = [{"role": "system", "content": "You are a smart and friendly data assistant."}]
        if chat_history:
            message_history += [{"role": role, "content": content} for role, content in chat_history]

        message_history.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=message_history,
        )

        return response.choices[0].message.content.strip()

    def data_chat_stream(self, user_query, chat_history=None):
        if not user_query:
            yield ""
            return

        prompt = self.prompt_manager.data_chat_prompt(user_query)

        message_history = [{"role": "system", "content": "You are a smart and friendly data assistant."}]
        if chat_history:
            message_history += [{"role": role, "content": content} for role, content in chat_history]

        message_history.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=message_history,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def data_describe(self):
        return self.df.describe().round(2).to_dict()

    def data_preview(self, n=20):
        return self.df.head(n).to_dict(orient="records")

    class PromptManager:
        def __init__(self, parent):
            self.parent = parent

        def data_summary_prompt(self):
            return f"""
You're a professional data analyst. Based on the sample below, provide a brief, one-paragraph summary describing what this dataset is about.

DATA SAMPLE:
{self.parent.df.head(100).to_string(index=False)}

Your response should:
- Be 3–4 sentences max
- Describe the purpose and type of data
- Mention any major categories or patterns
- Avoid listing all columns or repeating raw data
            """.strip()

        def data_json_prompt(self):
            columns_list = self.parent.df.columns.tolist()
            column_info = "\n".join([f"- {col}" for col in columns_list])
            return f"""
You are a data visualization assistant. Generate 1–3 chart ideas in JSON format using the dataset below.

IMPORTANT:
- Use ONLY the column names listed below
- Every chart must have both a valid "x" and "y" column
- Do NOT make up column names

AVAILABLE COLUMNS:
{column_info}

DATA SAMPLE:
{self.parent.df.head(5).to_string(index=False)}

STATS:
{self.parent.df.describe().to_string()}
            """.strip()

        def data_chat_prompt(self, user_query):
            sample_data = self.parent.df.head(10).to_csv(index=False)
            columns = self.parent.df.columns.tolist()
            return f"""
You are a professional data analyst.

Here is a sample of the dataset (in CSV format):
{sample_data}

Columns:
{columns}

The user asked: "{user_query}"

Answer clearly in plain English. Use the dataset to find patterns, trends, comparisons, or summaries. Provide specific numbers if possible. Do not write or mention Python code.
            """.strip()
