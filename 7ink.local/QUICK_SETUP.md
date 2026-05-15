# ⚡ Quick Setup: Crazy Domains → Cloudflare → Vercel

## Step 1: Deploy to Vercel (5 min)
```bash
cd D:\xampp\htdocs\7ink.local
git init
git add .
git commit -m "Initial"
git remote add origin https://github.com/YOUR_USERNAME/7ink-website.git
git push -u origin main
```
Then go to [Vercel.com](https://vercel.com) → Import GitHub repo → Deploy

**Your Vercel URL:** `https://7ink-website.vercel.app`

---

## Step 2: Create Cloudflare Account (2 min)
1. Go to [Cloudflare.com](https://www.cloudflare.com)
2. Sign up → Add site → Enter `7ink.com.au`
3. Select **Free Plan**
4. **Copy these nameservers:**
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`

---

## Step 3: Update Nameservers at Crazy Domains (5 min)
1. Log in to [Crazydomains.com.au](https://www.crazydomains.com.au)
2. My Domains → `7ink.com.au` → Edit Nameservers
3. Replace with Cloudflare nameservers above
4. Save

⏱️ **Wait 10 minutes - 48 hours for DNS to update**

---

## Step 4: Add DNS Records in Cloudflare (3 min)
1. Cloudflare Dashboard → Your domain → **DNS** → **Records**
2. **Add Record #1:**
   - Type: `CNAME`
   - Name: `@` (root)
   - Content: `cname.vercel.sh`
   - Proxy: **Proxied** ☁️
   - Save

3. **Add Record #2:**
   - Type: `CNAME`
   - Name: `www`
   - Content: `cname.vercel.sh`
   - Proxy: **Proxied** ☁️
   - Save

4. Go to **SSL/TLS** → Set to **"Full"**

---

## Step 5: Add Domain to Vercel (2 min)
1. Vercel Dashboard → Your project → **Settings** → **Domains**
2. Add Domain → `7ink.com.au` → Add
3. Add Domain → `www.7ink.com.au` → Add
4. Wait for verification ✅

---

## ✅ You're Done!

Test your site:
- https://7ink.com.au
- https://www.7ink.com.au

---

## 🔧 If Something's Wrong

| Problem | Solution |
|---------|----------|
| Domain not resolving | Wait 24 hours or check nameservers at Crazy Domains |
| Vercel shows "Not configured" | Verify CNAME records in Cloudflare → DNS |
| SSL error | Check Cloudflare SSL/TLS is set to "Full" |
| Admin not working | Admin requires Node.js backend (see DEPLOYMENT_GUIDE.md) |

---

**Total Time:** 15 minutes setup + 10 min - 48 hours DNS propagation
