# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy the Poverty Dashboard to Streamlit Cloud.

## 📋 Prerequisites

- GitHub account with the repository pushed
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- API keys for India Poverty API (NDAP)

## 🔧 Deployment Steps

### 1. Prepare Repository

The repository is already configured with:
- ✅ `.python-version` (Python 3.13)
- ✅ `requirements.txt` (all dependencies pinned)
- ✅ `app.py` (main entry point)
- ✅ `.streamlit/config.toml` (theme and server settings)
- ✅ `.streamlit/secrets.toml.example` (secrets template)

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select repository: `anonymous-pxe/Poverty_dashboard`
   - Branch: `feature/initial-dashboard-implementation`
   - Main file path: `app.py`
   - App URL: `povertydashboard` (or your preferred subdomain)

3. **Advanced Settings**
   - Python version: 3.13
   - Click "Advanced settings" before deploying

### 3. Configure Secrets

In Streamlit Cloud app settings, add the following secrets:

```toml
[api]
india_poverty_api_key = "gAAAAABpg20RfAwUAEq8ibudPDW7_cLCZrmUjpOVRH0W4rwwewM09vTDi1LxAXKkpRr0DaS7GES5iu9XzDOeGk-FEpMJgIL06oZ1WTR9HCrw6cmJbJvXKVKlo3VaaCkwfSaIimDLObK9RX3kl6RmWWEF88VvEpKj5ZxO-JoQzSWp2go-_rexphfoj49OMGDEVPAG25wIMFUW"
india_poverty_api_url = "https://loadqa.ndapapi.com/v1/openapi"
world_bank_api_url = "https://api.worldbank.org/v2"

[settings]
cache_ttl = "3600"
```

### 4. Deploy

1. Click "Deploy!" button
2. Wait for deployment (2-5 minutes)
3. Your app will be available at: `https://povertydashboard.streamlit.app`

## 🔍 Verification Checklist

After deployment, verify:

- [ ] ✅ App loads without errors
- [ ] ✅ All 7 pages are accessible (Dashboard, Global Trends, Rural vs Urban, Analysis, Visualization, Reports, Learn More)
- [ ] ✅ Sidebar navigation works
- [ ] ✅ Filters function correctly
- [ ] ✅ Charts and visualizations render
- [ ] ✅ Data loads from APIs (check for placeholder vs real data)
- [ ] ✅ Export functionality works (CSV, Excel)
- [ ] ✅ Custom CSS loads correctly
- [ ] ✅ Metrics and KPI cards display properly

## 🐛 Troubleshooting

### Issue: Import Errors

**Solution**: Check that all dependencies are in `requirements.txt` and properly pinned.

### Issue: Secrets Not Loading

**Solution**: 
1. Verify secrets are added in Streamlit Cloud dashboard
2. Check config.py has proper fallback values
3. Restart the app from Streamlit Cloud

### Issue: API Errors

**Solution**:
1. Verify API keys are correct in secrets
2. Check API endpoints are accessible
3. Review logs for specific error messages
4. App will fall back to placeholder data if APIs fail

### Issue: CSS Not Loading

**Solution**:
1. Check `assets/css/style.css` exists in repository
2. Verify app.py loads CSS correctly
3. Clear browser cache
4. Check file path is relative to app.py

## 📊 Monitoring

### Check App Status
- Streamlit Cloud dashboard shows app status
- View logs for errors
- Monitor API usage in logs

### Performance
- Data is cached using `@st.cache_data`
- Cache TTL: 3600 seconds (1 hour)
- Clear cache using sidebar button

## 🔄 Updating the App

1. Make changes locally
2. Commit and push to branch:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin feature/initial-dashboard-implementation
   ```
3. Streamlit Cloud auto-deploys on push
4. Changes appear in ~2-3 minutes

## 📝 Environment Variables

### Required Secrets
- `api.india_poverty_api_key`: NDAP API key
- `api.india_poverty_api_url`: NDAP endpoint (optional, has default)
- `api.world_bank_api_url`: World Bank endpoint (optional, has default)

### Optional Secrets
- `settings.cache_ttl`: Cache duration in seconds (default: 3600)

## 🌐 Custom Domain (Optional)

To use a custom domain:
1. Go to Streamlit Cloud app settings
2. Navigate to "General" tab
3. Add your custom domain
4. Follow DNS configuration instructions

## 📈 App URLs

- **Streamlit Cloud**: https://povertydashboard.streamlit.app
- **Repository**: https://github.com/anonymous-pxe/Poverty_dashboard
- **Branch**: feature/initial-dashboard-implementation

## 🆘 Support

- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: https://github.com/anonymous-pxe/Poverty_dashboard/issues

## ✅ Post-Deployment

After successful deployment:
1. Test all features
2. Share the URL with stakeholders
3. Monitor usage and performance
4. Collect feedback for improvements
5. Plan iterative updates

---

**Happy Deploying!** 🎉
