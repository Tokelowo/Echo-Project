# Customer Review API Configuration Guide

## Issue: No Real Customer Reviews Showing

The system is currently unable to fetch real customer reviews due to missing API credentials.

### Required API Configurations:

#### 1. Reddit API (Free)
- Go to: https://www.reddit.com/prefs/apps
- Create a new app (script type)
- Add to .env file:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=YourAppName/1.0
```

#### 2. Alternative Sources (Web Scraping)
The system can also scrape public review sites, but this requires:
- User agent rotation (already implemented)
- Rate limiting (already implemented)
- Proper error handling (already implemented)

### Current Status:
- ❌ Reddit API: Authentication failed (401)
- ❌ G2 Crowd: Access denied (403)
- ✅ Web scraping fallbacks: Available but limited

### Solution Options:

#### Option 1: Configure Reddit API (Recommended)
1. Get Reddit API credentials (free)
2. Add to .env file
3. Restart Django server

#### Option 2: Use Alternative Data Sources
1. Microsoft Graph API for customer feedback
2. Azure Monitor customer insights
3. GitHub discussions/issues
4. Stack Overflow questions

#### Option 3: Manual Review Collection
1. Collect reviews from trusted sources
2. Store in database
3. Display with proper attribution

### No Demo Data
As requested, the system will show:
- Empty state when no real reviews available
- Clear messaging about API configuration needed
- Instructions for getting real customer reviews

### Files to Configure:
- `django-backend/.env` - Add API keys
- `research_agent/real_customer_reviews_service.py` - Review service
- `research_agent/cybersecurity_news_service_new.py` - Main service
