"""
Research Agent Service - Orchestrates the three-agent workflow with web scraping
"""
import json
import logging
from typing import Dict, List, Optional
from django.conf import settings
from django.utils import timezone
from openai import AzureOpenAI
from .models import Agent, Report, ReportRequest, EmailDelivery
from .agent_prompts_new import AGENT_PROMPTS
import os

logger = logging.getLogger(__name__)

# Try to import web scraping service, with fallback if bs4 is not available
try:
    from .web_scraping_service import WebScrapingService
    WEB_SCRAPING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Web scraping service not available: {e}")
    WEB_SCRAPING_AVAILABLE = False
    WebScrapingService = None

logger = logging.getLogger(__name__)

class ResearchAgentService:
    """Service for orchestrating the research agent workflow with real-time web data"""
    
    def __init__(self):
        # Azure OpenAI configuration
        self.endpoint = getattr(settings, 'AZURE_EXISTING_AIPROJECT_ENDPOINT', 
                               os.environ.get('AZURE_EXISTING_AIPROJECT_ENDPOINT', ''))
        self.api_key = getattr(settings, 'OPENAI_API_KEY', 
                              os.environ.get('OPENAI_API_KEY', ''))
        self.api_version = "2024-12-01-preview"
        self.deployment = "gpt-4o"
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure OpenAI endpoint and API key must be configured")        
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
        )
          # Initialize web scraping service if available
        if WEB_SCRAPING_AVAILABLE:
            self.web_scraper = WebScrapingService()
        else:
            self.web_scraper = None
            logger.info("Web scraping service disabled - bs4 package not available")
    
    def run_research_pipeline(self, 
                            query: str, 
                            agent_type: str = "competitive_intelligence_agent",
                            focus_areas: List[str] = None,
                            user_email: str = None,
                            user_name: str = "Research User",
                            delivery_preferences: Dict = None,
                            use_multi_agent: bool = True) -> Dict:
        """
        Run the complete research pipeline with multi-agent collaboration
        """
        focus_areas = focus_areas or []
        delivery_preferences = delivery_preferences or {"format": "email", "schedule": "immediate"}
        
        logger.info(f"Starting research pipeline - Multi-agent: {use_multi_agent}")
        logger.info(f"Primary agent: {agent_type}")
        logger.info(f"Query: {query}")
        logger.info(f"Focus areas: {focus_areas}")
        
        try:
            # Create report request
            agent = self._get_or_create_agent(agent_type)
            report_request = ReportRequest.objects.create(
                agent=agent,
                user_email=user_email or "research@microsoft.com",
                user_name=user_name,
                query=query,
                focus_areas=focus_areas,
                delivery_format=delivery_preferences.get("format", "email"),
                schedule_type=delivery_preferences.get("schedule", "immediate"),
                status="processing"
            )
            
            if use_multi_agent:
                # Multi-agent collaboration workflow
                research_result = self._run_multi_agent_collaboration(query, focus_areas, agent_type)
            else:
                # Single agent workflow (legacy)
                research_result = self._run_research_agent(agent_type, query, focus_areas)
            
            # Step 2: Format the results
            formatted_result = self._run_formatting_agent(research_result, user_name)
            
            # Step 3: Handle delivery
            delivery_result = self._run_delivery_agent(
                formatted_result, 
                user_name, 
                user_email, 
                delivery_preferences
            )
            
            # Create the final report
            report = Report.objects.create(
                request=report_request,
                agent=agent,
                title=f"{agent.get_agent_type_display()} Report: {query[:50]}...",
                content=formatted_result,
                raw_data={
                    "research_output": research_result,
                    "formatted_output": formatted_result,
                    "delivery_output": delivery_result
                },
                format="html",
                key_insights=self._extract_insights(research_result),
                confidence_score=0.85  # Default confidence score
            )            # Handle email delivery if requested
            email_sent = False
            logger.info(f"Email delivery check - user_email: {user_email}, schedule: {delivery_preferences.get('schedule')}")
            if user_email and delivery_preferences.get("schedule") == "immediate":
                try:
                    logger.info(f"Attempting to send email to {user_email}")
                    from .email_service import send_report_email
                    email_delivery = send_report_email(
                        report=report,
                        recipient_email=user_email,
                        recipient_name=user_name
                    )
                    logger.info(f"Email delivery initiated: {email_delivery.id}")
                    email_sent = True
                except Exception as email_error:
                    logger.error(f"Email delivery failed: {str(email_error)}")
                    import traceback
                    logger.error(f"Email error traceback: {traceback.format_exc()}")
            else:
                logger.info(f"Email not sent - conditions not met. user_email: {bool(user_email)}, schedule: {delivery_preferences.get('schedule')}")            # Update report request status
            report_request.status = "completed"
            report_request.completed_at = timezone.now()
            report_request.save()
            
            logger.info(f"Research pipeline completed successfully. Report ID: {report.id}, Email sent: {email_sent}")
            
            return {
                "status": "success",
                "report_id": report.id,
                "request_id": report_request.id,
                "research_output": research_result,
                "formatted_output": formatted_result,
                "delivery_output": delivery_result,
                "email_sent": email_sent
            }
            
        except Exception as e:
            logger.error(f"Research pipeline failed: {str(e)}")
            if 'report_request' in locals():
                report_request.status = "failed"
                report_request.save()
            raise e
    
    def _run_research_agent(self, agent_type: str, query: str, focus_areas: List[str]) -> str:
        """Run the primary research agent with real-time web data"""
        logger.info(f"Running research agent: {agent_type} with web scraping integration")
          # Gather real-time market intelligence
        logger.info("Gathering real-time market intelligence from web sources...")
        try:
            if self.web_scraper:
                market_intelligence = self.web_scraper.get_comprehensive_market_intelligence(
                    include_microsoft=True,
                    include_competitors=True,
                    include_market_trends=True,
                    max_articles_per_category=5  # Limit for performance
                )
                
                # Format the web data for AI analysis
                web_context = self._format_market_intelligence_for_ai(market_intelligence, agent_type)
                logger.info(f"Successfully gathered market intelligence: {market_intelligence['summary']}")
            else:
                logger.info("Web scraping service not available, using fallback knowledge")
                web_context = "Note: Real-time web data unavailable. Analysis based on training data and cached knowledge."
            
        except Exception as e:
            logger.warning(f"Failed to gather web intelligence: {str(e)}. Proceeding with cached knowledge.")
            web_context = "Note: Real-time web data unavailable. Analysis based on training data."
        
        # Get the appropriate prompt
        prompt = AGENT_PROMPTS.get(agent_type, AGENT_PROMPTS["competitive_intelligence_agent"])
        
        # Add web context to the prompt
        prompt += f"\n\nREAL-TIME MARKET DATA:\n{web_context}\n\n"
        prompt += "IMPORTANT: Use the above real-time market data to enhance your analysis. Reference specific recent developments, competitor activities, and market trends from the provided data."
        
        # Add focus areas to the prompt
        if focus_areas:
            prompt += f"\n\nFOCUS AREAS: Please focus your analysis specifically on: {', '.join(focus_areas)}."
        
        # Add output format instructions
        prompt += """\n\nOUTPUT FORMAT: Please structure your response as a professional research report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-5 main points)
3. Detailed Analysis (incorporating real-time data)
4. Strategic Recommendations
5. Action Items
6. Sources and Confidence Level

IMPORTANT: Use clean, professional formatting without markdown symbols. Do not use asterisks (*), hashtags (#), or other markdown formatting. Use plain text with clear section headings and bullet points using simple dashes (-) or numbers."""
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
            top_p=0.9
        )
        
        result = response.choices[0].message.content
        
        # Clean any markdown formatting from the result
        result = clean_markdown_formatting(result)
        
        logger.debug(f"Research agent output length: {len(result)} characters")
        return result
    
    def _run_formatting_agent(self, research_content: str, user_name: str) -> str:
        """Run the formatting agent to create email-ready content"""
        logger.info("Running formatting agent")
        
        prompt = AGENT_PROMPTS["formatting_agent"]
        prompt += """\n\nPlease transform the research content into a professional, email-ready HTML format with:
- Clear section headers using HTML <h2>, <h3> tags
- Bullet points using HTML <ul> and <li> tags
- Executive summary at the top
- Professional styling suitable for business communication
- Actionable recommendations highlighted with HTML formatting

CRITICAL: Do not use any markdown formatting symbols such as:
- No hashtags (#) for headers
- No asterisks (*) for bold or emphasis
- No markdown bullet points
- Use proper HTML tags only for formatting
- Ensure clean, professional appearance without markdown artifacts

Transform any existing markdown symbols in the content to proper HTML formatting."""
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"User: {user_name}\nResearch Content: {research_content}"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=4096,
            temperature=0.3,
            top_p=0.9
        )
        
        result = response.choices[0].message.content
        logger.debug(f"Formatting agent output length: {len(result)} characters")
        return result
    
    def _run_delivery_agent(self, formatted_content: str, user_name: str, 
                           user_email: str, delivery_preferences: Dict) -> str:
        """Run the delivery agent to handle scheduling and delivery logic"""
        logger.info("Running delivery agent")
        
        prompt = AGENT_PROMPTS["delivery_agent"]
        prompt += """\n\nPlease provide delivery confirmation and scheduling details for this report.
Include information about:
- Delivery method confirmation
- Scheduling details
- Email composition summary
- Subscription management notes"""
        
        delivery_info = {
            "recipient": user_name,
            "email": user_email,
            "format": delivery_preferences.get("format", "email"),
            "schedule": delivery_preferences.get("schedule", "immediate"),
            "content_length": len(formatted_content)
        }
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Delivery Info: {json.dumps(delivery_info)}\nReport Content: {formatted_content[:500]}..."}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=1024,
            temperature=0.3,
            top_p=0.9
        )
        
        result = response.choices[0].message.content
        logger.debug(f"Delivery agent output length: {len(result)} characters")
        return result
    
    def _get_or_create_agent(self, agent_type: str) -> Agent:
        """Get or create an agent of the specified type"""
        agent, created = Agent.objects.get_or_create(
            agent_type=agent_type,
            defaults={
                "name": agent_type.replace("_", " ").title(),
                "description": AGENT_PROMPTS.get(agent_type, "AI Research Agent"),
                "model_name": self.deployment,
                "is_active": True
            }
        )
        if created:
            logger.info(f"Created new agent: {agent.name}")
        return agent
    
    def _extract_insights(self, research_content: str) -> List[str]:
        """Extract key insights from research content"""
        # Simple extraction - look for key phrases
        insights = []
        lines = research_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['key finding', 'insight', 'recommendation', 'important', 'critical']):
                if len(line) > 20 and len(line) < 200:  # Reasonable length
                    insights.append(line)
          # Return top 5 insights
        return insights[:5]

    def _run_multi_agent_collaboration(self, query: str, focus_areas: List[str], primary_agent: str) -> str:
        """
        Run all three agents in collaboration to create a comprehensive report
        Each agent contributes their specialized perspective and they cross-reference findings
        """
        logger.info("Starting multi-agent collaboration workflow")
        
        # Define agent types for collaboration
        agent_types = [
            "competitive_intelligence_agent",
            "product_intelligence_agent", 
            "market_trends_agent"
        ]
        
        # Ensure primary agent is first in the list
        if primary_agent in agent_types:
            agent_types.remove(primary_agent)
            agent_types.insert(0, primary_agent)
        
        agent_outputs = {}
        
        # Phase 1: Independent Analysis - Each agent does initial research
        logger.info("Phase 1: Independent agent analysis")
        for agent_type in agent_types:
            logger.info(f"Running independent analysis: {agent_type}")
            prompt = AGENT_PROMPTS.get(agent_type, AGENT_PROMPTS["competitive_intelligence_agent"])
            
            if focus_areas:
                prompt += f"\n\nFOCUS AREAS: Please focus your analysis specifically on: {', '.join(focus_areas)}."
            
            prompt += """\n\nOUTPUT FORMAT: Provide your specialized perspective in a structured format:
1. Executive Summary (2-3 sentences from your domain expertise)
2. Key Domain-Specific Findings (3-5 insights unique to your specialization)
3. Critical Data Points (quantifiable metrics or qualitative observations)
4. Cross-Domain Implications (how your findings might impact other areas)
5. Recommendations (actionable next steps from your perspective)

IMPORTANT: Use clean, professional formatting without markdown symbols. Do not use asterisks (*), hashtags (#), or other markdown formatting."""
            
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9
            )
            
            result = response.choices[0].message.content
            result = clean_markdown_formatting(result)
            agent_outputs[agent_type] = result
            logger.debug(f"{agent_type} independent analysis completed: {len(result)} characters")
        
        # Phase 2: Cross-Analysis - Agents review each other's findings
        logger.info("Phase 2: Cross-agent analysis and synthesis")
        
        synthesis_prompt = """You are the Lead Research Coordinator. You have received independent analyses from three specialized agents:

1. Competitive Intelligence Agent - Focus on competitor analysis and market positioning
2. Product Intelligence Agent - Focus on product capabilities and performance  
3. Market Trends Agent - Focus on industry trends and market dynamics

Your task is to synthesize these perspectives into a comprehensive, unified report that:
- Integrates insights across all three domains
- Identifies patterns and connections between findings
- Resolves any conflicting viewpoints with reasoned analysis
- Provides holistic strategic recommendations
- Maintains high analytical rigor and professional tone

AGENT FINDINGS:

COMPETITIVE INTELLIGENCE ANALYSIS:
{competitive_analysis}

PRODUCT INTELLIGENCE ANALYSIS:  
{product_analysis}

MARKET TRENDS ANALYSIS:
{market_analysis}

Create a unified report that synthesizes these perspectives while maintaining the expertise from each domain.

SYNTHESIS OUTPUT FORMAT:
1. Executive Summary (comprehensive overview integrating all perspectives)
2. Integrated Key Findings (cross-domain insights and patterns)
3. Competitive Landscape Analysis (from CI agent + market context)
4. Product Strategy Implications (from PI agent + competitive positioning)
5. Market Opportunity Assessment (from MT agent + product capabilities)
6. Strategic Recommendations (unified actionable guidance)
7. Risk Assessment and Mitigation
8. Implementation Roadmap

IMPORTANT: Use clean, professional formatting without markdown symbols. Do not use asterisks (*), hashtags (#), or other markdown formatting."""
        
        # Prepare agent findings for synthesis
        competitive_analysis = agent_outputs.get("competitive_intelligence_agent", "No competitive intelligence analysis available")
        product_analysis = agent_outputs.get("product_intelligence_agent", "No product intelligence analysis available")  
        market_analysis = agent_outputs.get("market_trends_agent", "No market trends analysis available")
        
        synthesis_content = synthesis_prompt.format(
            competitive_analysis=competitive_analysis,
            product_analysis=product_analysis,
            market_analysis=market_analysis
        )
        
        messages = [
            {"role": "system", "content": "You are an expert research coordinator with deep knowledge of cybersecurity, email security, and enterprise technology markets."},
            {"role": "user", "content": synthesis_content}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=6144,  # Larger token limit for comprehensive synthesis
            temperature=0.5,  # Lower temperature for more focused synthesis
            top_p=0.9
        )
        
        synthesized_result = response.choices[0].message.content
        synthesized_result = clean_markdown_formatting(synthesized_result)
        
        logger.info("Multi-agent collaboration completed")
        logger.debug(f"Synthesized report length: {len(synthesized_result)} characters")
        
        return synthesized_result

    def _format_market_intelligence_for_ai(self, market_intelligence: Dict, agent_type: str) -> str:
        """Format market intelligence data for AI analysis"""
        try:
            formatted_data = []
            
            # Add summary information
            summary = market_intelligence.get('summary', {})
            formatted_data.append(f"DATA SUMMARY:")
            formatted_data.append(f"- Total Microsoft articles: {summary.get('total_microsoft_articles', 0)}")
            formatted_data.append(f"- Total competitor articles: {summary.get('total_competitor_articles', 0)}")
            formatted_data.append(f"- Total market trend articles: {summary.get('total_market_trend_articles', 0)}")
            formatted_data.append(f"- Sources: {', '.join(summary.get('sources_covered', []))}")
            formatted_data.append(f"- Last updated: {market_intelligence.get('last_updated', 'Unknown')}")
            formatted_data.append("")
            
            # Add Microsoft news if relevant
            if agent_type in ['competitive_intelligence_agent', 'product_intelligence_agent']:
                microsoft_news = market_intelligence.get('microsoft_news', [])
                if microsoft_news:
                    formatted_data.append("RECENT MICROSOFT NEWS:")
                    for i, article in enumerate(microsoft_news[:3], 1):  # Top 3 articles
                        formatted_data.append(f"{i}. {article['title']}")
                        formatted_data.append(f"   Source: {article['source']}")
                        formatted_data.append(f"   Date: {article.get('published_date', 'Unknown')}")
                        formatted_data.append(f"   Summary: {article['summary'][:200]}...")
                        formatted_data.append(f"   URL: {article['url']}")
                        formatted_data.append("")
            
            # Add competitor news
            competitor_news = market_intelligence.get('competitor_news', {})
            if competitor_news and agent_type == 'competitive_intelligence_agent':
                formatted_data.append("RECENT COMPETITOR NEWS:")
                for competitor, articles in competitor_news.items():
                    if articles:  # Only show competitors with articles
                        formatted_data.append(f"\n{competitor.upper()} NEWS:")
                        for i, article in enumerate(articles[:2], 1):  # Top 2 per competitor
                            formatted_data.append(f"{i}. {article['title']}")
                            formatted_data.append(f"   Source: {article['source']}")
                            formatted_data.append(f"   Summary: {article['summary'][:150]}...")
                            formatted_data.append("")
            
            # Add market trends
            if agent_type in ['market_trends_agent', 'competitive_intelligence_agent']:
                market_trends = market_intelligence.get('market_trends', [])
                if market_trends:
                    formatted_data.append("RECENT MARKET TRENDS:")
                    for i, article in enumerate(market_trends[:3], 1):  # Top 3 trends
                        formatted_data.append(f"{i}. {article['title']}")
                        formatted_data.append(f"   Source: {article['source']}")
                        formatted_data.append(f"   Date: {article.get('published_date', 'Unknown')}")
                        formatted_data.append(f"   Summary: {article['summary'][:200]}...")
                        formatted_data.append("")
            
            formatted_content = "\n".join(formatted_data)
            
            # Truncate if too long (to fit in context window)
            if len(formatted_content) > 8000:
                formatted_content = formatted_content[:8000] + "\n... (truncated for length)"
            
            return formatted_content
            
        except Exception as e:
            logger.error(f"Error formatting market intelligence: {str(e)}")
            return "Market intelligence data temporarily unavailable."

def clean_markdown_formatting(text: str) -> str:
    """Clean markdown formatting symbols from text to ensure professional appearance"""
    import re
    
    # Remove markdown headers (# ## ###)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold markdown (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Remove italic markdown (*text* or _text_)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove markdown bullet points and replace with HTML
    text = re.sub(r'^\s*\*\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s+', '• ', text, flags=re.MULTILINE)
    
    # Remove code blocks (```text```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Clean up multiple spaces and newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove any remaining asterisks or hashtags that might be orphaned
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+', '', text)
    
    return text.strip()

# Convenience functions for easy import
def run_competitive_intelligence(query: str, user_email: str = None, **kwargs) -> Dict:
    """Run competitive intelligence analysis"""
    service = ResearchAgentService()
    return service.run_research_pipeline(
        query=query,
        agent_type="competitive_intelligence_agent",
        user_email=user_email,
        **kwargs
    )

def run_product_intelligence(query: str, user_email: str = None, **kwargs) -> Dict:
    """Run product intelligence analysis"""
    service = ResearchAgentService()
    return service.run_research_pipeline(
        query=query,
        agent_type="product_intelligence_agent",
        user_email=user_email,
        **kwargs
    )

def run_market_trends(query: str, user_email: str = None, **kwargs) -> Dict:
    """Run market trends analysis"""
    service = ResearchAgentService()
    return service.run_research_pipeline(
        query=query,
        agent_type="market_trends_agent",
        user_email=user_email,
        **kwargs
    )

def run_comprehensive_research(query: str, user_email: str = None, **kwargs) -> Dict:
    """Run comprehensive multi-agent research analysis using all three specialized agents"""
    service = ResearchAgentService()
    return service.run_research_pipeline(
        query=query,
        agent_type="competitive_intelligence_agent",  # Primary agent
        user_email=user_email,
        use_multi_agent=True,  # Explicitly enable multi-agent collaboration
        **kwargs
    )

def run_single_agent_research(query: str, agent_type: str, user_email: str = None, **kwargs) -> Dict:
    """Run research using a single specialized agent (legacy mode)"""
    service = ResearchAgentService()
    return service.run_research_pipeline(
        query=query,
        agent_type=agent_type,
        user_email=user_email,
        use_multi_agent=False,  # Disable multi-agent collaboration
        **kwargs
    )
