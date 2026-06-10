# Shopify — Web Performance

Shopify is an e-commerce platform. This environment covers the **Web Performance** dashboard and optimization tools available to merchants in the Shopify admin.

## Components to Implement

### Performance Dashboard
- Overall performance score (similar to Lighthouse score, 0-100)
- Score breakdown by page type (home page, collection pages, product pages, cart page)
- Historical performance trend chart (line/area chart over time)
- Comparison to similar stores / benchmark

### Core Web Vitals Display
- Largest Contentful Paint (LCP) metric with status (good/needs improvement/poor)
- First Input Delay (FID) or Interaction to Next Paint (INP) metric
- Cumulative Layout Shift (CLS) metric
- Per-metric trend sparklines

### Performance Recommendations
- List of actionable recommendations (e.g., optimize images, reduce third-party scripts, lazy-load below-fold content)
- Priority/impact indicators per recommendation
- Status tracking (addressed/dismissed/pending)
- Detail view per recommendation with explanation

### Third-Party Script Audit
- Table of third-party apps/scripts loaded on the storefront
- Per-script impact on page load time
- Ability to view details for each script
- Recommendations for heavy scripts

### Speed Report by Page
- Table of individual pages with their load metrics
- Sortable columns (URL, LCP, CLS, total blocking time)
- Filter by page type
- Pagination for large stores

### Settings
- Performance monitoring enable/disable
- Alert thresholds configuration (notify when score drops below X)
- Reporting frequency (daily, weekly, monthly)
