
const NEWS_SOURCES = {
  WSJ: {
    name: 'Wall Street Journal (Daily)',
    baseUrl: 'https://api.wsj.com/api',
    apiKey: process.env.REACT_APP_WSJ_API_KEY,
  },
  TECHCRUNCH: {
    name: 'TechCrunch (Daily)',
    baseUrl: 'https://techcrunch.com/wp-json/wp/v2',
  },
  REUTERS: {
    name: 'Reuters (Daily)',
    baseUrl: 'https://api.reuters.com',
  }
};

export const fetchCompetitiveNews = async (competitors = ['Google', 'Microsoft', 'Amazon', 'Proofpoint', 'Mimecast']) => {
  const newsData = {
    sources: [],
    articles: [],
    analysis: {},
    lastUpdated: new Date().toISOString()
  };

  try {
    if (NEWS_SOURCES.WSJ.apiKey) {
      for (const competitor of competitors) {
        const response = await fetch(`${NEWS_SOURCES.WSJ.baseUrl}/search?query=${competitor}+security&limit=10`, {
          headers: {
            'Authorization': `Bearer ${NEWS_SOURCES.WSJ.apiKey}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          newsData.articles.push(...data.articles?.map(article => ({
            ...article,
            source: 'WSJ',
            competitor,
            relevanceScore: calculateRelevanceScore(article, competitor)
          })) || []);
        }
      }
    }

    for (const competitor of competitors) {
      try {
        const response = await fetch(`${NEWS_SOURCES.TECHCRUNCH.baseUrl}/posts?search=${competitor}&per_page=5`);
        if (response.ok) {
          const data = await response.json();
          newsData.articles.push(...data.map(article => ({
            title: article.title.rendered,
            content: article.excerpt.rendered,
            url: article.link,
            publishedDate: article.date,
            source: 'TechCrunch',
            competitor,
            relevanceScore: calculateRelevanceScore(article, competitor)
          })));
        }        } catch (error) {
        }
    }

    newsData.analysis = analyzeCompetitivePositioning(newsData.articles);
    
    return newsData;
    
  } catch (error) {
    return {
      sources: ['Error fetching external sources'],
      articles: [],
      analysis: { error: error.message }
    };
  }
};

const calculateRelevanceScore = (article, competitor) => {
  const title = (article.title?.rendered || article.title || '').toLowerCase();
  const content = (article.content?.rendered || article.excerpt?.rendered || article.content || '').toLowerCase();
  
  let score = 0;
  
  if (title.includes(competitor.toLowerCase())) score += 30;
  if (content.includes(competitor.toLowerCase())) score += 20;
  
  const securityKeywords = ['security', 'email', 'threat', 'protection', 'cybersecurity', 'phishing'];
  securityKeywords.forEach(keyword => {
    if (title.includes(keyword)) score += 15;
    if (content.includes(keyword)) score += 10;
  });
  
  const mdoKeywords = ['defender', 'office 365', 'microsoft 365', 'azure'];
  mdoKeywords.forEach(keyword => {
    if (title.includes(keyword)) score += 25;
    if (content.includes(keyword)) score += 15;
  });
  
  return Math.min(score, 100);
};

const analyzeCompetitivePositioning = (articles) => {
  const analysis = {
    competitorMentions: {},
    trendingTopics: {},
    sentimentAnalysis: {},
    marketShare: {},
    recentDevelopments: []
  };
  
  articles.forEach(article => {
    if (!analysis.competitorMentions[article.competitor]) {
      analysis.competitorMentions[article.competitor] = 0;
    }
    analysis.competitorMentions[article.competitor]++;
    
    const topics = extractTopics(article.title + ' ' + article.content);
    topics.forEach(topic => {
      if (!analysis.trendingTopics[topic]) {
        analysis.trendingTopics[topic] = 0;
      }
      analysis.trendingTopics[topic]++;
    });
    
    const articleDate = new Date(article.publishedDate);
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    if (articleDate > thirtyDaysAgo && article.relevanceScore > 60) {
      analysis.recentDevelopments.push({
        competitor: article.competitor,
        title: article.title,
        source: article.source,
        date: article.publishedDate,
        relevanceScore: article.relevanceScore
      });
    }
  });
  
  return analysis;
};

const extractTopics = (text) => {
  const topics = [];
  const keywords = [
    'artificial intelligence', 'ai', 'machine learning', 'cloud security',
    'zero trust', 'phishing protection', 'email security', 'threat intelligence',
    'ransomware', 'malware', 'endpoint protection', 'compliance',
    'data protection', 'privacy', 'gdpr', 'hipaa'
  ];
  
  keywords.forEach(keyword => {
    if (text.toLowerCase().includes(keyword)) {
      topics.push(keyword);
    }
  });
  
  return topics;
};

export default {
  fetchCompetitiveNews,
  NEWS_SOURCES
};
