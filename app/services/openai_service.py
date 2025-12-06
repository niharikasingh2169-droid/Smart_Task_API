import os
import json
from pathlib import Path
from typing import Tuple
from datetime import datetime, date

from dotenv import load_dotenv
from openai import AsyncOpenAI


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self) -> None:
        # Explicitly load .env from project root
        # Path: app/services/openai_service.py -> go up 2 levels to project root
        project_root = Path(__file__).resolve().parent.parent.parent
        env_path = project_root / '.env'
        
        # Load .env file explicitly
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            # Fallback: try loading from current directory
            load_dotenv(dotenv_path='.env', override=True)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                f"OPENAI_API_KEY is not set. "
                f"Tried loading from: {env_path} (exists: {env_path.exists()}). "
                f"Please check your .env file at the project root."
            )
        
        # Strip quotes and whitespace
        api_key = api_key.strip().strip('"').strip("'")
        if not api_key or api_key == "your_openai_api_key_here":
            raise RuntimeError(
                "OPENAI_API_KEY is not properly set. "
                "Please replace 'your_openai_api_key_here' with your actual OpenAI API key in the .env file."
            )
        
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_priority_score(
        self, title: str, description: str, due_date: str
    ) -> Tuple[int, str]:
        """
        Get priority score (1-5, where 1 is highest priority) based on task details.
        Returns: (priority_score, reasoning)
        """
        # Parse due date from dd-mm-yyyy format
        try:
            due_date_obj = datetime.strptime(due_date, '%d-%m-%Y').date()
            today = date.today()
            days_until_due = (due_date_obj - today).days
            print(f"Days until due date: {days_until_due}")
        except ValueError:
            # If date parsing fails, default to a large number
            days_until_due = 999
        
        
        prompt = f"""Analyze the following task and assign a priority score from 1 to 5, where 1 is the highest priority and 5 is the lowest priority.

Task Title: {title}
Task Description: {description}
Days left: {days_until_due}

Priority Guidelines Based on Days Left:
- 1-7 days remaining: Priority 1 (highest urgency)
- 8-20 days remaining: Priority 2 (high urgency)
- 21-40 days remaining: Priority 3 (medium urgency)
- 41-60 days remaining: Priority 4 (low urgency)
- 61+ days remaining: Priority 5 (lowest urgency)

Consider the following factors:
- Urgency based on due date (use the days left as primary factor)
- Keywords in the title and description like Urgent, Important, Critical, etc.
- Importance of the task
- Complexity and scope
- Any time-sensitive elements

Respond in the following JSON format:
{{
    "priority_score": <number between 1 and 5>,
    "reasoning": "<brief explanation of why this priority was assigned>"
}}"""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a task prioritization assistant. "
                                   "Always respond with valid JSON."
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            result = json.loads(response.choices[0].message.content)
            priority_score = int(result.get("priority_score", 3))
            reasoning = result.get("reasoning", "Priority assigned based on task analysis")

            # Clamp to valid range 1–5
            priority_score = max(1, min(5, priority_score))

            return priority_score, reasoning

        except Exception as e:
            # Fallback to default priority if API call fails
            return 3, f"Default priority assigned due to error: {str(e)}"
