"""
Research Agent Service - Orchestrates the three-agent workflow
"""
import json
import logging
from typing import Dict, List, Optional
from django.conf import settings
from django.utils import timezone
from openai import AzureOpenAI
from .models import Agent, Report, ReportRequest, EmailDelivery
from .agent_prompts_new import AGENT_PROMPTS
from .email_service import EmailService
import os

logger = logging.getLogger(__name__)

class ResearchAgentService:
    """Service for orchestrating the research agent workflow"""
    
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
        
        self.email_service = EmailService()
    
    def run_research_pipeline(self, 
                            query: str, 
                            agent_type: str = "competitive_intelligence_agent",
                            focus_areas: List[str] = None,
                            user_email: str = None,
                            user_name: str = "Research User",
                            delivery_preferences: Dict = None) -> Dict:
        """
        Run the complete research pipeline with the specified agent
        """
        focus_areas = focus_areas or []
        delivery_preferences = delivery_preferences or {"format": "email", "schedule": "immediate"}
        
        logger.info(f"Starting research pipeline for agent: {agent_type}")
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
            
            # Step 1: Run the primary research agent
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
            )
            
            # Handle email delivery if requested
            if user_email and delivery_preferences.get("schedule") == "immediate":
                try:
                    email_delivery = self.email_service.send_report_email(
                        report=report,
                        recipient_email=user_email,
                        recipient_name=user_name
                    )
                    logger.info(f"Email delivery initiated: {email_delivery.id}")
                except Exception as email_error:
                    logger.error(f"Email delivery failed: {str(email_error)}")
            
            # Update report request status
            report_request.status = "completed"
            report_request.completed_at = timezone.now()
            report_request.save()
            
            return {
                "status": "success",
                "report_id": report.id,
                "request_id": report_request.id,
                "research_output": research_result,
                "formatted_output": formatted_result,
                "delivery_output": delivery_result,
                "email_sent": user_email is not None
            }
            
        except Exception as e:
            logger.error(f"Research pipeline failed: {str(e)}")
            if 'report_request' in locals():
                report_request.status = "failed"
                report_request.save()
            raise e
    
    def _run_research_agent(self, agent_type: str, query: str, focus_areas: List[str]) -> str:
        """Run the primary research agent"""
        logger.info(f"Running research agent: {agent_type}")
        
        # Get the appropriate prompt
        prompt = AGENT_PROMPTS.get(agent_type, AGENT_PROMPTS["competitive_intelligence_agent"])
        
        # Add focus areas to the prompt
        if focus_areas:
            prompt += f"\n\nFOCUS AREAS: Please focus your analysis specifically on: {', '.join(focus_areas)}."
        
        # Add output format instructions
        prompt += """\n\nOUTPUT FORMAT: Please structure your response as a professional research report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-5 main points)
3. Detailed Analysis
4. Strategic Recommendations
5. Action Items
6. Sources and Confidence Level"""
        
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
        logger.debug(f"Research agent output length: {len(result)} characters")
        return result
    
    def _run_formatting_agent(self, research_content: str, user_name: str) -> str:
        """Run the formatting agent to create email-ready content"""
        logger.info("Running formatting agent")
        
        prompt = AGENT_PROMPTS["formatting_agent"]
        prompt += """\n\nPlease transform the research content into a professional, email-ready HTML format with:
- Clear section headers
- Bullet points for key findings
- Executive summary at the top
- Professional styling suitable for business communication
- Actionable recommendations highlighted"""
        
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
    
    def schedule_recurring_reports(self, agent_type: str, query: str, 
                                 user_email: str, schedule_type: str = "weekly") -> Dict:
        """Schedule recurring reports (placeholder for future implementation)"""
        logger.info(f"Scheduling {schedule_type} reports for {user_email}")
        
        # This would integrate with a task scheduler like Celery
        # For now, return confirmation
        return {
            "status": "scheduled",
            "agent_type": agent_type,
            "query": query,
            "email": user_email,
            "schedule": schedule_type,
            "next_run": "To be implemented with task scheduler"
        }

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
            
            # Enhance prompt with focus areas if provided
            if focus_areas:
                prompt += f"\n\nFocus your analysis specifically on: {', '.join(focus_areas)}"
            
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON response if possible
            try:
                structured_data = json.loads(content)
                return {
                    'success': True,
                    'content': content,
                    'structured_data': structured_data,
                    'confidence_score': structured_data.get('confidence_level', 0.8)
                }
            except json.JSONDecodeError:
                return {
                    'success': True,
                    'content': content,
                    'structured_data': {},
                    'confidence_score': 0.7
                }
                
        except Exception as e:
            logger.error(f"Agent {agent_type} failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'structured_data': {},
                'confidence_score': 0.0
            }

class ReportGenerationService:
    """Service for generating comprehensive reports."""
    
    def __init__(self):
        self.agent_service = AgentService()
    
    def generate_report(self, request: ReportRequest) -> Report:
        """Generate a comprehensive report using the agent pipeline."""
        try:
            # Update request status
            request.status = 'processing'
            request.save()
            
            # Step 1: Generate primary research using specialized agent
            primary_response = self.agent_service.generate_agent_response(
                agent_type=request.agent.agent_type,
                query=request.query,
                focus_areas=request.focus_areas
            )
            
            if not primary_response['success']:
                raise Exception(f"Primary agent failed: {primary_response['error']}")
            
            # Step 2: Format the report using formatting agent
            formatted_response = self._format_report(
                primary_content=primary_response['content'],
                request=request
            )
            
            # Step 3: Create report record
            report = Report.objects.create(
                request=request,
                agent=request.agent,
                title=self._generate_report_title(request),
                content=formatted_response['content'],
                raw_data=primary_response.get('structured_data', {}),
                format='html',
                confidence_score=primary_response.get('confidence_score', 0.7),
                key_insights=self._extract_key_insights(primary_response)
            )
            
            # Step 4: Generate file if needed
            if request.delivery_format in ['pdf', 'docx', 'both']:
                file_path = self._generate_report_file(report, request.delivery_format)
                report.file_path = file_path
                report.save()
            
            # Update request status
            request.status = 'completed'
            request.completed_at = timezone.now()
            request.save()
            
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            request.status = 'failed'
            request.save()
            raise
    
    def _format_report(self, primary_content: str, request: ReportRequest) -> Dict[str, Any]:
        """Format the primary research into a polished report."""
        formatting_prompt = AGENT_PROMPTS['formatting_agent']
        
        format_query = f"""
        User: {request.user_name}
        Agent Type: {request.agent.get_agent_type_display()}
        Query: {request.query}
        Focus Areas: {', '.join(request.focus_areas) if request.focus_areas else 'General analysis'}
        
        Raw Research Content:
        {primary_content}
        
        Please format this into a professional email-ready report with proper HTML formatting,
        executive summary, key insights, and actionable recommendations.
        """
        
        return self.agent_service.generate_agent_response(
            agent_type='formatting_agent',
            query=format_query
        )
    
    def _generate_report_title(self, request: ReportRequest) -> str:
        """Generate an appropriate title for the report."""
        agent_name = request.agent.get_agent_type_display()
        timestamp = timezone.now().strftime("%Y-%m-%d")
        query_snippet = request.query[:50] + "..." if len(request.query) > 50 else request.query
        return f"{agent_name} Report - {query_snippet} ({timestamp})"
    
    def _extract_key_insights(self, response: Dict[str, Any]) -> List[str]:
        """Extract key insights from agent response."""
        structured_data = response.get('structured_data', {})
        insights = []
        
        # Try different possible structures
        if isinstance(structured_data, dict):
            if 'key_insights' in structured_data:
                insights = structured_data['key_insights']
            elif 'insights' in structured_data:
                insights = structured_data['insights']
            elif 'recommendations' in structured_data:
                insights = structured_data['recommendations']
        
        # Fallback to extracting from content
        if not insights:
            content = response.get('content', '')
            # Simple extraction of bullet points or numbered items
            lines = content.split('\n')
            insights = [line.strip() for line in lines 
                       if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.'))][:5]
        
        return insights[:5]  # Limit to top 5 insights
    
    def _generate_report_file(self, report: Report, file_format: str) -> str:
        """Generate downloadable file for the report."""
        # For now, we'll create a simple HTML file
        # In production, you might want to use libraries like python-docx or reportlab
        
        reports_dir = Path(settings.REPORTS_DIR)
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{report.id}_{timestamp}.html"
        file_path = reports_dir / filename
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ border-bottom: 2px solid #0078d4; padding-bottom: 20px; }}
                .content {{ margin-top: 20px; }}
                .insights {{ background-color: #f5f5f5; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report.title}</h1>
                <p>Generated on: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Agent: {report.agent.get_agent_type_display()}</p>
                <p>Confidence Score: {report.confidence_score or 'N/A'}</p>
            </div>
            <div class="content">
                {report.content}
            </div>
            <div class="insights">
                <h3>Key Insights</h3>
                <ul>
                    {''.join([f'<li>{insight}</li>' for insight in report.key_insights])}
                </ul>
            </div>
        </body>
        </html>
        """
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(file_path.relative_to(Path(settings.MEDIA_ROOT)))

class EmailDeliveryService:
    """Service for handling email delivery of reports."""
    
    def send_report_email(self, report: Report, recipient_email: str, 
                         recipient_name: str) -> EmailDelivery:
        """Send report via email."""
        try:
            # Create delivery record
            delivery = EmailDelivery.objects.create(
                report=report,
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                subject=f"📊 {report.title}",
                status='queued'
            )
            
            # Prepare email content
            email_subject = f"📊 {report.title}"
            
            # Create email body
            email_body = f"""
            Dear {recipient_name},
            
            Your requested {report.agent.get_agent_type_display()} report is ready!
            
            {report.content}
            
            ---
            Report Details:
            • Generated: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            • Agent: {report.agent.get_agent_type_display()}
            • Word Count: {report.word_count}
            • Confidence Score: {report.confidence_score or 'N/A'}
            
            Best regards,
            The Research Intelligence Team
            """
            
            # Create email message
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            
            # Add attachment if file exists
            if report.file_path:
                file_full_path = Path(settings.MEDIA_ROOT) / report.file_path
                if file_full_path.exists():
                    email.attach_file(str(file_full_path))
            
            # Send email
            email.send()
            
            # Update delivery status
            delivery.status = 'sent'
            delivery.sent_at = timezone.now()
            delivery.save()
            
            # Update request status if needed
            if report.request.status == 'completed':
                report.request.status = 'delivered'
                report.request.save()
            
            return delivery
            
        except Exception as e:
            logger.error(f"Email delivery failed: {str(e)}")
            delivery.status = 'failed'
            delivery.error_message = str(e)
            delivery.save()
            raise
    
    def schedule_recurring_delivery(self, request: ReportRequest):
        """Schedule recurring report delivery (placeholder for future implementation)."""
        # This would integrate with a task queue like Celery in production
        pass
