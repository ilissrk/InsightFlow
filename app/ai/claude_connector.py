from typing import Dict, Optional, List
import anthropic
from pydantic import BaseModel
import json
import asyncio

class ClaudeConnector:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key)
        self.system_prompt = """You are an AI analytics assistant for InsightFlow.
        Your role is to help analyze data, generate insights, and answer queries.
        Use the available tools and data to provide accurate and helpful responses."""

    async def generate_insight(self, data: Dict, context: Optional[Dict] = None) -> Dict:
        """Generate insights from provided data using Claude"""
        try:
            prompt = self._build_insight_prompt(data, context)
            response = await self._get_claude_response(prompt)
            return self._parse_insight_response(response)
        except Exception as e:
            raise Exception(f"Error generating insight: {str(e)}")

    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Process natural language queries using Claude"""
        try:
            prompt = self._build_query_prompt(query, context)
            response = await self._get_claude_response(prompt)
            return self._parse_query_response(response)
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")

    async def _get_claude_response(self, prompt: str) -> str:
        """Get response from Claude API"""
        try:
            response = await self.client.messages.create(
                model="claude-2",
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def _build_insight_prompt(self, data: Dict, context: Optional[Dict] = None) -> str:
        """Build prompt for insight generation"""
        prompt = "Analyze the following data and generate insights:\n\n"
        prompt += json.dumps(data, indent=2)
        if context:
            prompt += "\n\nContext:\n" + json.dumps(context, indent=2)
        return prompt

    def _build_query_prompt(self, query: str, context: Optional[Dict] = None) -> str:
        """Build prompt for query processing"""
        prompt = f"Process the following analytics query:\n{query}\n\n"
        if context:
            prompt += "Context:\n" + json.dumps(context, indent=2)
        return prompt

    def _parse_insight_response(self, response: str) -> Dict:
        """Parse and structure Claude's insight response"""
        try:
            # Add response parsing logic here
            return {
                "insights": response,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error parsing insight response: {str(e)}")

    def _parse_query_response(self, response: str) -> Dict:
        """Parse and structure Claude's query response"""
        try:
            # Add response parsing logic here
            return {
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error parsing query response: {str(e)}")