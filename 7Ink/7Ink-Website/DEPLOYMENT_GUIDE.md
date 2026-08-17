# 7ink.com.au Deployment Guide
## Crazy Domains + Cloudflare + Vercel Setup

---

## 🎯 Complete Setup Workflow

### Phase 1: Deploy to Vercel
### Phase 2: Set Up Cloudflare DNS
### Phase 3: Update Crazy Domains Nameservers

---

## Phase 1: Deploy to Vercel

### Step 1A: Create GitHub Repository (Recommended)
1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Name: `7ink-website`
4. Description: "7ink.com.au website"
5. Click "Create repository"

### Step 1B: Push Your Code to GitHub
```bash
cd D:\xampp\htdocs\7ink.local
git init
git add .
git commit -m "Initial commit: 7ink.com.au website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/7ink-website.git
git push -u origin main
```

### Step 1C: Deploy to Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Sign up with GitHub account
3. Click "New Project"
4. Import your `7ink-website` GitHub repository
5. Keep default settings
6. Click "Deploy" (wait 2-5 minutes)
7. You'll get a Vercel preview URL

**✅ Note your Vercel URL: `https://7ink-website.vercel.app`**

---

## Phase 2: Set Up Cloudflare DNS

### Step 2A: Create Cloudflare Account
1. Go to [Cloudflare.com](https://www.cloudflare.com)
2. Sign up (free plan is fine)
3. Verify email

### Step 2B: Add Domain to Cloudflare
1. Log in to Cloudflare dashboard
2. Click "Add a Site"
3. Enter: `7ink.com.au`
4. Click "Add Site"
5. Select **Free Plan** ($0/month)
6. Click "Continue"

### Step 2C: Get Cloudflare Nameservers
Cloudflare will display two nameservers like:
- `ns1.cloudflare.com`
- `ns2.cloudflare.com`

**✅ Copy these nameservers - you'll need them next**

---

## Phase 3: Update Crazy Domains Nameservers

### Step 3A: Log In to Crazy Domains
1. Go to [Crazydomains.com.au](https://www.crazydomains.com.au)
2. Log in to your account
3. Go to "My Domains"
4. Click on `7ink.com.au`

### Step 3B: Change Nameservers to Cloudflare
1. Find "Nameservers" or "DNS Settings"
2. Click "Edit Nameservers"
3. Replace current nameservers with Cloudflare's:
   - **Nameserver 1:** `ns1.cloudflare.com`
   - **Nameserver 2:** `ns2.cloudflare.com`
4. Click "Save"

⏱️ **Wait 24-48 hours for DNS to propagate** (usually 30 minutes to 2 hours)

---

## Phase 4: Configure Cloudflare DNS Records

### Step 4A: Verify Domain in Cloudflare
1. Return to Cloudflare dashboard
2. Look for your domain status
3. Click "Check Nameserver"
4. Click "Continue" once verified

### Step 4B: Add DNS Records for Vercel
1. In Cloudflare dashboard, go to your domain
2. Click "DNS" → "Records"
3. Click "Add Record"

**Add these records:**

**Record 1: Root Domain (@)**
- Type: `CNAME`
- Name: `@` or leave blank (root domain)
- Content: `cname.vercel.sh` (or `cname-global.vercel.sh`)
- TTL: Auto
- Proxy Status: **Proxied** (orange cloud icon)
- Click "Save"

**Record 2: WWW Subdomain**
- Type: `CNAME`
- Name: `www`
- Content: `cname.vercel.sh`
- TTL: Auto
- Proxy Status: **Proxied**
- Click "Save"

### Step 4C: SSL/TLS Settings
1. In Cloudflare, go to "SSL/TLS"
2. Set Encryption Mode to **"Full"** or **"Full (strict)"**
3. This encrypts traffic between Cloudflare and Vercel

---

## Phase 5: Add Domain to Vercel

### Step 5A: Add Domain in Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your `7ink-website` project
3. Go to "Settings" → "Domains"
4. Click "Add Domain"
5. Enter: `7ink.com.au`
6. Click "Add"

### Step 5B: Verify Domain
- Vercel will check if DNS is properly configured
- If using Cloudflare CNAME as above, it should verify automatically
- If not, check Cloudflare DNS records

### Step 5C: Add WWW Domain (Optional but Recommended)
1. Click "Add Domain" again
2. Enter: `www.7ink.com.au`
3. Click "Add"
4. Verify using Cloudflare

---

## ✅ Verification Checklist

- [ ] Domain purchased from Crazy Domains
- [ ] Project deployed to Vercel
- [ ] Cloudflare account created
- [ ] Domain added to Cloudflare
- [ ] Nameservers updated at Crazy Domains
- [ ] DNS records added in Cloudflare:
  - [ ] CNAME @ → cname.vercel.sh
  - [ ] CNAME www → cname.vercel.sh
- [ ] SSL/TLS set to "Full" in Cloudflare
- [ ] Domains added to Vercel project
- [ ] DNS propagation complete (test with ping or nslookup)

---

## 🧪 Test Your Setup

### Check DNS Propagation
```bash
# On Windows, open Command Prompt and run:
nslookup 7ink.com.au
nslookup www.7ink.com.au

# Should return Vercel's IP addresses
```

### Test Website
1. Visit `https://7ink.com.au` in browser
2. Visit `https://www.7ink.com.au`
3. Both should load your website

---

## 🛡️ Cloudflare Benefits (Free Plan)

- **DNS Management**: Full control over DNS records
- **SSL/TLS**: Free SSL certificate
- **Security**: DDoS protection
- **Performance**: Global CDN
- **Analytics**: View traffic statistics
- **Email Forwarding**: Forward emails (optional)

---

## 🚨 Troubleshooting

### Domain Not Resolving
- **Check:** DNS propagation time (up to 48 hours)
- **Test:** Use `nslookup 7ink.com.au` in Command Prompt
- **Fix:** Verify nameservers in Crazy Domains match Cloudflare's

### Getting "Not Yet Configured" in Vercel
- **Check:** CNAME records are properly set in Cloudflare
- **Verify:** Name is `@` (or blank) for root domain
- **Wait:** Can take 5-15 minutes for Vercel to detect

### SSL Certificate Issues
- **Check:** Cloudflare SSL/TLS is set to "Full"
- **Verify:** Vercel shows green checkmark for domain
- **Wait:** SSL provisioning can take 10-30 minutes

### Admin Section Not Working
- Requires PHP backend (Vercel doesn't support)
- Options:
  - Convert to Node.js API
  - Use Vercel serverless functions
  - Host admin separately

---

## 📋 Important Settings Summary

| Service | Setting | Value |
|---------|---------|-------|
| Crazy Domains | Nameserver 1 | `ns1.cloudflare.com` |
| Crazy Domains | Nameserver 2 | `ns2.cloudflare.com` |
| Cloudflare DNS | @ | CNAME → cname.vercel.sh |
| Cloudflare DNS | www | CNAME → cname.vercel.sh |
| Cloudflare SSL | Encryption Mode | Full (strict) |
| Vercel | Domain | 7ink.com.au |
| Vercel | WWW Domain | www.7ink.com.au |

---

## 🔗 Useful Links

- [Vercel Docs](https://vercel.com/docs)
- [Cloudflare Docs](https://developers.cloudflare.com/)
- [Crazy Domains Support](https://www.crazydomains.com.au/contact)
- [Cloudflare + Vercel Guide](https://vercel.com/guides/cloudflare)

---

## 📝 DNS Propagation Timeline

| Time | Status |
|------|--------|
| 0-5 min | Nameservers changed at Crazy Domains |
| 5-30 min | DNS propagates globally (usually works within this time) |
| 30 min - 2 hours | Most users can access site |
| 2-48 hours | Full DNS propagation (worst case) |

**Tip:** Check propagation with [whatsmydns.net](https://www.whatsmydns.net)

---

## Important Notes

**PHP Admin Section:**
- The `/admin` section uses PHP which Vercel doesn't support by default
- Current setup: Static HTML/CSS/JS only
- **Options to enable admin:**
  - Option A: Convert admin to JavaScript/Node.js
  - Option B: Use Vercel's serverless functions (Node.js)
  - Option C: Host admin separately on traditional PHP hosting

---

## Troubleshooting

**Issue: Admin section not working**
- Admin requires PHP backend
- Convert to static HTML or use Node.js API routes

**Issue: Assets/images not loading**
- Check file paths are relative (not absolute)
- Ensure all files are committed to Git

**Issue: Domain not resolving**
- Update your domain registrar's nameservers
- Follow Vercel's DNS setup guide

---

## File Structure
```
7ink.local/
├── index.html          (Main page)
├── blog.html
├── contact.html
├── admin/              (Admin section - requires backend)
│   └── index.php
├── assets/             (CSS, JS, images)
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── vendor/
│   └── scss/
├── forms/              (Forms directory)
├── docs/               (Documentation)
├── javascripts/
├── stylesheets/
├── package.json        (Node.js config)
├── vercel.json         (Vercel config)
└── .gitignore          (Git ignore rules)
```

---

## Next Steps

1. ✅ Created `package.json` - dependency manager
2. ✅ Created `vercel.json` - deployment configuration
3. ✅ Created `.gitignore` - exclude unnecessary files
4. 📋 Choose deployment method (GitHub or Vercel CLI)
5. 🚀 Deploy to Vercel
6. 🔗 Configure domain (7ink.com.au)

---

**Need Help?**
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Documentation](https://docs.github.com)
- Support: support@7ink.com.au
