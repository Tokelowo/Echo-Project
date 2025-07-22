// Gartner Reviews API integration service
const GARTNER_API_BASE = 'https://www.gartner.com/reviews/market/email-security-platforms';

/**
 * Service for integrating Gartner Peer Insights reviews for email security platforms
 * This service fetches and processes Gartner reviews data for competitive analysis
 */
class GartnerReviewsService {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 30 * 60 * 1000; // 30 minutes
  }

  /**
   * Fetch Gartner reviews for email security platforms
   * Note: This is a mock implementation since direct Gartner API access requires special credentials
   * In production, you would integrate with Gartner's official API or web scraping service
   */
  async fetchEmailSecurityReviews(forceRefresh = false) {
    const cacheKey = 'gartner_email_security_reviews';
    
    // Check cache first
    if (!forceRefresh && this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.data;
      }
    }

    try {
      // In a real implementation, this would call the Gartner API
      // For now, we'll simulate the data structure based on Gartner's review format
      const reviewsData = await this.simulateGartnerAPICall();
      
      // Cache the results
      this.cache.set(cacheKey, {
        data: reviewsData,
        timestamp: Date.now()
      });

      return reviewsData;
    } catch (error) {
      console.error('Error fetching Gartner reviews:', error);
      throw new Error('Failed to fetch Gartner reviews data');
    }
  }

  /**
   * Simulate Gartner API response with realistic email security platform data
   * This would be replaced with actual API calls in production
   */
  async simulateGartnerAPICall() {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    return {
      market: "Email Security Platforms",
      last_updated: new Date().toISOString(),
      total_vendors: 12,
      total_reviews: 2847,
      vendors: [
        {
          vendor_name: "Microsoft Defender for Office 365",
          overall_rating: 4.2,
          total_reviews: 412,
          recommendation_rate: 87,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/microsoft/product/microsoft-defender-for-office-365",
          key_strengths: [
            "Deep integration with Microsoft ecosystem",
            "Advanced threat protection capabilities",
            "Comprehensive security analytics",
            "Strong phishing and malware detection"
          ],
          key_weaknesses: [
            "Complex configuration for advanced features",
            "Requires Microsoft licensing expertise",
            "Limited third-party integrations"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 68,
            "Mid-Market (100-999 employees)": 24,
            "Small Business (<100 employees)": 8
          },
          recent_reviews: [
            {
              rating: 5,
              title: "Excellent Protection for Microsoft Environment",
              review_snippet: "Great integration with our existing Microsoft infrastructure. The ATP features have significantly reduced our phishing incidents.",
              reviewer_role: "IT Security Manager",
              company_size: "Enterprise",
              date: "2025-07-10"
            },
            {
              rating: 4,
              title: "Powerful but Complex",
              review_snippet: "Very capable solution but requires significant expertise to configure properly. Worth the investment for large organizations.",
              reviewer_role: "CISO",
              company_size: "Enterprise",
              date: "2025-07-08"
            }
          ]
        },
        {
          vendor_name: "Proofpoint Email Protection",
          overall_rating: 4.4,
          total_reviews: 523,
          recommendation_rate: 89,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/proofpoint",
          key_strengths: [
            "Industry-leading threat detection",
            "Excellent customer support",
            "Comprehensive compliance features",
            "Advanced sandboxing capabilities"
          ],
          key_weaknesses: [
            "High cost for full feature set",
            "Complex policy management",
            "Steep learning curve"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 72,
            "Mid-Market (100-999 employees)": 22,
            "Small Business (<100 employees)": 6
          }
        },
        {
          vendor_name: "Mimecast Email Security",
          overall_rating: 4.3,
          total_reviews: 387,
          recommendation_rate: 85,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/mimecast",
          key_strengths: [
            "Easy deployment and management",
            "Strong email archiving capabilities",
            "Good value for money",
            "Comprehensive email security suite"
          ],
          key_weaknesses: [
            "Occasional false positives",
            "Limited customization options",
            "Interface could be more intuitive"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 45,
            "Mid-Market (100-999 employees)": 38,
            "Small Business (<100 employees)": 17
          }
        },
        {
          vendor_name: "Abnormal Security",
          overall_rating: 4.5,
          total_reviews: 178,
          recommendation_rate: 92,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/abnormal-security",
          key_strengths: [
            "AI-powered behavioral analysis",
            "Excellent BEC protection",
            "Low false positive rate",
            "Quick deployment"
          ],
          key_weaknesses: [
            "Newer vendor with limited track record",
            "Higher pricing for advanced features",
            "Limited reporting capabilities"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 58,
            "Mid-Market (100-999 employees)": 32,
            "Small Business (<100 employees)": 10
          }
        },
        {
          vendor_name: "Barracuda Email Security Gateway",
          overall_rating: 4.0,
          total_reviews: 298,
          recommendation_rate: 78,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/barracuda",
          key_strengths: [
            "Cost-effective solution",
            "Good performance",
            "Reliable spam filtering",
            "Strong technical support"
          ],
          key_weaknesses: [
            "Limited advanced threat protection",
            "Interface needs modernization",
            "Lacks some AI-powered features"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 35,
            "Mid-Market (100-999 employees)": 45,
            "Small Business (<100 employees)": 20
          }
        },
        {
          vendor_name: "Trend Micro Email Security",
          overall_rating: 4.1,
          total_reviews: 234,
          recommendation_rate: 82,
          gartner_peer_insights_url: "https://www.gartner.com/reviews/market/email-security-platforms/vendor/trend-micro",
          key_strengths: [
            "Strong malware detection",
            "Global threat intelligence",
            "Good integration capabilities",
            "Comprehensive security features"
          ],
          key_weaknesses: [
            "Complex administration",
            "Resource intensive",
            "Occasional performance issues"
          ],
          reviewer_segments: {
            "Enterprise (1000+ employees)": 52,
            "Mid-Market (100-999 employees)": 33,
            "Small Business (<100 employees)": 15
          }
        }
      ],
      market_insights: {
        top_buying_factors: [
          "Threat detection accuracy",
          "Integration capabilities",
          "Total cost of ownership",
          "Ease of management",
          "Vendor support quality"
        ],
        emerging_trends: [
          "AI-powered behavioral analysis",
          "Zero-trust email security",
          "Cloud-native architectures",
          "API-first integrations",
          "Automated incident response"
        ],
        satisfaction_drivers: [
          "Reduction in successful phishing attacks",
          "Simplified security management",
          "Improved compliance posture",
          "Lower operational overhead"
        ]
      },
      competitive_landscape: {
        leaders: ["Proofpoint", "Microsoft", "Mimecast"],
        challengers: ["Abnormal Security", "Trend Micro"],
        niche_players: ["Barracuda"],
        market_size_usd: "3.2 billion",
        growth_rate: "12.8%"
      }
    };
  }

  /**
   * Get competitive comparison data from Gartner reviews
   */
  async getCompetitiveComparison(competitors = []) {
    const reviewsData = await this.fetchEmailSecurityReviews();
    
    if (competitors.length === 0) {
      // Return top competitors by rating
      return reviewsData.vendors
        .sort((a, b) => b.overall_rating - a.overall_rating)
        .slice(0, 5);
    }

    // Filter by specific competitors
    return reviewsData.vendors.filter(vendor => 
      competitors.some(comp => 
        vendor.vendor_name.toLowerCase().includes(comp.toLowerCase())
      )
    );
  }

  /**
   * Get market insights and trends from Gartner data
   */
  async getMarketInsights() {
    const reviewsData = await this.fetchEmailSecurityReviews();
    return {
      market_insights: reviewsData.market_insights,
      competitive_landscape: reviewsData.competitive_landscape,
      vendor_summary: reviewsData.vendors.map(v => ({
        name: v.vendor_name,
        rating: v.overall_rating,
        reviews: v.total_reviews,
        recommendation_rate: v.recommendation_rate
      }))
    };
  }
}

export default new GartnerReviewsService();
