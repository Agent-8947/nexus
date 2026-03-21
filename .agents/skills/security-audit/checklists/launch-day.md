# Launch Day Security Checklist

1. [ ] No Exposed .git Folder (`curl -I https://yoursite.com/.git/config`)
2. [ ] Debug Mode Disabled (`NODE_ENV=production`)
3. [ ] Database RLS/Security Rules Enabled (Supabase/Firebase policies)
4. [ ] No Hardcoded API Keys in Frontend Code
5. [ ] HTTPS Enforced
6. [ ] Security Headers Configured (`securityheaders.com` check)
7. [ ] Rate Limiting on Auth/AI Endpoints
8. [ ] No Sensitive Data in URLs
9. [ ] Error Messages Don't Leak Info (Generic errors only)
10. [ ] Admin Routes Protected / IP Whitelisted
