import { fetchEnhancedMarketIntelligence, fetchCompetitiveMetrics } from './api';

export class MarketTrendsReportGenerator {
  constructor() {
    this.reportHistory = JSON.parse(localStorage.getItem('marketTrendsHistory') || '[]');
  }

  async generateDailyReport() {
    try {
      const [marketData, competitiveMetrics] = await Promise.all([
        fetchEnhancedMarketIntelligence(true),
        fetchCompetitiveMetrics(true)
      ]);

      const report = {
        date: new Date().toISOString().split('T')[0],
        timestamp: new Date().toISOString(),
        data: {
          marketData,
          competitiveMetrics,
          summary: this.generateSummary(marketData, competitiveMetrics),
          insights: this.generateInsights(marketData, competitiveMetrics),
          recommendations: this.generateRecommendations(marketData, competitiveMetrics)
        }
      };

      this.saveReport(report);
      
      this.exportToMarkdown(report);

      return report;
    } catch (error) {
      console.error('Error generating daily report:', error);
      throw error;
    }
  }

  generateSummary(marketData, competitiveMetrics) {
    const totalArticles = competitiveMetrics?.total_articles_analyzed || 0;
    const topTrend = Object.entries(competitiveMetrics?.technology_trends || {})
      .sort(([,a], [,b]) => b - a)[0];
    const topThreat = marketData?.threat_analysis ? 
      Object.entries(marketData.threat_analysis).sort(([,a], [,b]) => b - a)[0] : null;

    return {
      totalArticles,
      topTechnology: topTrend ? `${topTrend[0]} (${topTrend[1]} mentions)` : 'AI/ML Detection',
      topThreat: topThreat ? `${topThreat[0]} (${topThreat[1]} incidents)` : 'Malware',
      microsoftPosition: competitiveMetrics?.market_presence?.['Microsoft Defender for Office 365'] || {},
      marketActivity: this.assessMarketActivity(competitiveMetrics)
    };
  }

  generateInsights(marketData, competitiveMetrics) {
    const insights = [];
    
    const techTrends = Object.entries(competitiveMetrics?.technology_trends || {})
      .filter(([, value]) => value > 0)
      .sort(([, a], [, b]) => b - a);

    if (techTrends.length > 0) {
      insights.push({
        type: 'technology',
        priority: 'high',
        title: `${techTrends[0][0]} Leading Market Conversations`,
        description: `With ${techTrends[0][1]} mentions, ${techTrends[0][0]} is dominating current cybersecurity discussions. This represents a strategic opportunity for MDO to leverage Microsoft's AI capabilities.`,
        action: 'Amplify AI/ML messaging and demonstrate superior capabilities'
      });
    }

    const microsoftData = competitiveMetrics?.market_presence?.['Microsoft Defender for Office 365'];
    if (microsoftData) {
      const competitorActivity = Object.values(competitiveMetrics?.market_presence || {})
        .reduce((sum, competitor) => sum + (competitor.articles_count || 0), 0);
      
      insights.push({
        type: 'competitive',
        priority: competitorActivity > 10 ? 'high' : 'medium',
        title: `Market Competition Level: ${competitorActivity > 10 ? 'High' : 'Moderate'}`,
        description: `Total competitor news activity: ${competitorActivity} articles. Microsoft has ${microsoftData.articles_count} articles and ${microsoftData.security_mentions} security mentions.`,
        action: competitorActivity > 10 ? 'Monitor competitor moves closely' : 'Opportunity for thought leadership'
      });
    }

    if (marketData?.threat_analysis) {
      const activeThreat = Object.entries(marketData.threat_analysis)
        .filter(([, count]) => count > 0)
        .sort(([, a], [, b]) => b - a)[0];
      
      if (activeThreat) {
        insights.push({
          type: 'threat',
          priority: activeThreat[1] > 3 ? 'critical' : 'high',
          title: `${activeThreat[0]} Threats Highly Active`,
          description: `${activeThreat[1]} ${activeThreat[0].toLowerCase()} incidents reported. Email security solutions must prioritize protection against this threat vector.`,
          action: `Emphasize MDO's ${activeThreat[0].toLowerCase()} protection capabilities in messaging`
        });
      }
    }

    return insights;
  }

  generateRecommendations(marketData, competitiveMetrics) {
    const recommendations = [];

    recommendations.push({
      timeframe: 'immediate',
      category: 'Marketing',
      action: 'Launch AI/ML-focused thought leadership campaign',
      priority: 'high',
      rationale: 'AI/ML detection showing highest market interest'
    });

    recommendations.push({
      timeframe: 'immediate',
      category: 'Product',
      action: 'Develop threat-specific protection messaging',
      priority: 'high',
      rationale: 'Active threat landscape requires targeted messaging'
    });

    recommendations.push({
      timeframe: 'medium',
      category: 'Strategy',
      action: 'Expand market share in emerging technology areas',
      priority: 'medium',
      rationale: 'Low competitor activity in several technology categories'
    });

    recommendations.push({
      timeframe: 'medium',
      category: 'Competitive',
      action: 'Strengthen differentiation messaging',
      priority: 'medium',
      rationale: 'Competitive landscape showing similar positioning'
    });

    return recommendations;
  }

  assessMarketActivity(competitiveMetrics) {
    const totalTechMentions = Object.values(competitiveMetrics?.technology_trends || {})
      .reduce((a, b) => a + b, 0);
    const totalCompetitorActivity = Object.values(competitiveMetrics?.market_presence || {})
      .reduce((sum, company) => sum + (company.articles_count || 0), 0);

    if (totalTechMentions > 20 || totalCompetitorActivity > 15) {
      return 'high';
    } else if (totalTechMentions > 10 || totalCompetitorActivity > 8) {
      return 'moderate';
    } else {
      return 'low';
    }
  }

  saveReport(report) {
    this.reportHistory = this.reportHistory.filter(r => {
      const reportDate = new Date(r.date);
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return reportDate >= thirtyDaysAgo;
    });

    this.reportHistory.push(report);
    localStorage.setItem('marketTrendsHistory', JSON.stringify(this.reportHistory));
  }

  exportToMarkdown(report) {
    const markdown = this.generateMarkdownReport(report);
    
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `market-trends-report-${report.date}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  generateMarkdownReport(report) {
    const { data } = report;
    
    return `# Email Security Market Trends Report
## ${new Date(report.timestamp).toLocaleDateString('en-US', { 
  weekday: 'long', 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric' 
})}

---

## 📊 Executive Summary

**Market Activity Level:** ${data.summary.marketActivity.toUpperCase()}
**Articles Analyzed:** ${data.summary.totalArticles}
**Top Technology Trend:** ${data.summary.topTechnology}
**Primary Threat:** ${data.summary.topThreat}

## 🔍 Key Insights

${data.insights.map(insight => `
### ${insight.title} (${insight.priority.toUpperCase()} PRIORITY)
${insight.description}

**Recommended Action:** ${insight.action}
`).join('\n')}

## 📈 Strategic Recommendations

### Immediate Actions (Next 30 Days)
${data.recommendations.filter(r => r.timeframe === 'immediate').map(r => 
`- **${r.category}:** ${r.action} (${r.priority} priority)`
).join('\n')}

### Medium-Term Actions (Next 90 Days)
${data.recommendations.filter(r => r.timeframe === 'medium').map(r => 
`- **${r.category}:** ${r.action} (${r.priority} priority)`
).join('\n')}

## 📊 Data Summary

**Technology Trends:**
${Object.entries(data.competitiveMetrics?.technology_trends || {})
  .filter(([, value]) => value > 0)
  .map(([tech, mentions]) => `- ${tech}: ${mentions} mentions`)
  .join('\n')}

**Market Presence:**
${Object.entries(data.competitiveMetrics?.market_presence || {})
  .map(([vendor, data]) => `- ${vendor}: ${data.articles_count} articles, ${data.security_mentions} security mentions`)
  .join('\n')}

---

*Report generated automatically on ${new Date(report.timestamp).toLocaleString()}*
*Next update: Tomorrow at 8:00 AM*
*Classification: Microsoft Internal Use Only*
`;
  }

  getReportHistory() {
    return this.reportHistory;
  }

  getLatestReport() {
    return this.reportHistory[this.reportHistory.length - 1] || null;
  }
}

export const initializeDailyReports = () => {
  const reportGenerator = new MarketTrendsReportGenerator();
  
  const scheduleDaily = () => {
    const now = new Date();
    const next8AM = new Date();
    next8AM.setHours(8, 0, 0, 0);
    
    if (now > next8AM) {
      next8AM.setDate(next8AM.getDate() + 1);
    }
    
    const timeUntil8AM = next8AM - now;
    
    setTimeout(() => {
      reportGenerator.generateDailyReport();
      
      setInterval(() => {
        reportGenerator.generateDailyReport();
      }, 24 * 60 * 60 * 1000);
    }, timeUntil8AM);
  };

  scheduleDaily();
  return reportGenerator;
};

export default MarketTrendsReportGenerator;
