# 🚀 Lab Scanner - GitHub Setup Guide

Your project is now initialized as a local Git repository! Here's how to push it to GitHub.

---

## 📋 Step-by-Step Instructions

### **Step 1: Create a Repository on GitHub**

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `lab-scanner` (or your preferred name)
4. Description: `Professional Vulnerability Scanner - Enterprise-grade network and web scanning tool`
5. Choose **Public** or **Private** (based on your preference)
6. **Do NOT** initialize with README (we already have one)
7. Click **Create repository**

### **Step 2: Add GitHub Remote to Local Repository**

After creating the repository on GitHub, you'll see instructions. Run these commands:

```bash
cd ~/Desktop/scanner2

# Add the remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Verify remote was added
git remote -v
```

**Example:**
```bash
git remote add origin https://github.com/john-hacker/lab-scanner.git
```

### **Step 3: Push to GitHub**

```bash
# Rename branch to 'main' (GitHub default)
git branch -M main

# Push your code
git push -u origin main
```

The `-u` flag sets `main` as the default upstream branch for future pushes.

---

## 🔐 Authentication Options

### **Option A: HTTPS with Personal Access Token (Recommended for 2FA)**

1. Generate a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click **"Tokens (classic)"**
   - Click **"Generate new token (classic)"**
   - Select scopes: `repo`, `gist`
   - Copy the token
   
2. When prompted for password, paste the token instead:
   ```bash
   Username: your_github_username
   Password: paste_your_token_here
   ```

3. Save credentials (optional):
   ```bash
   # Store credentials so you don't need to enter them again
   git config --global credential.helper store
   
   # Next push will ask for credentials, then save them
   git push -u origin main
   ```

### **Option B: SSH (Most Secure)**

1. Generate SSH key (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter for all prompts to use defaults
   ```

2. Add SSH key to GitHub:
   - Copy the public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to GitHub Settings → SSH and GPG keys
   - Click **New SSH key**
   - Paste the key
   - Click **Add SSH key**

3. Update remote to use SSH:
   ```bash
   cd ~/Desktop/scanner2
   git remote set-url origin git@github.com:USERNAME/REPO_NAME.git
   ```

4. Test SSH connection:
   ```bash
   ssh -T git@github.com
   # Should say: "Hi USERNAME! You've successfully authenticated..."
   ```

5. Push to GitHub:
   ```bash
   git push -u origin main
   ```

---

## 📝 Example: Complete Setup

Here's a complete example:

```bash
# 1. Navigate to project
cd ~/Desktop/scanner2

# 2. Configure Git (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Create repo on GitHub (web UI)
# Then add the remote:
git remote add origin https://github.com/yourusername/lab-scanner.git

# 4. Rename branch and push
git branch -M main
git push -u origin main

# 5. On future changes, just run:
git add .
git commit -m "Your commit message"
git push
```

---

## ✅ Verify It Worked

After pushing, verify on GitHub:

1. Go to `https://github.com/yourusername/lab-scanner`
2. You should see:
   - All your files and folders
   - The commit history
   - README.md displayed
   - File structure visible

---

## 🔄 Future Workflow

After initial setup, the workflow is simple:

```bash
# After making changes:
git add .                           # Stage changes
git commit -m "Brief description"   # Commit locally
git push                            # Push to GitHub
```

---

## 📚 Additional GitHub Setup

### Add GitHub Profile to Commits (Optional)

Configure Git to match your GitHub account:

```bash
git config --global user.name "Your GitHub Name"
git config --global user.email "your-github-email@example.com"
```

### Create Useful Files

Consider adding these to your GitHub repo:

#### `.github/workflows/ci.yml` (GitHub Actions - CI/CD)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r lab_scanner/requirements.txt
      - name: Run tests
        run: cd lab_scanner && python -m pytest tests/
```

#### `CONTRIBUTING.md` (Contribution guidelines)
```markdown
# Contributing to Lab Scanner

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
```

#### `LICENSE` (Choose a license)
```
MIT License - For open-source projects with minimal restrictions
GPL 3.0 - For open-source with copyleft requirements
Apache 2.0 - For permissive open-source
```

---

## 🆘 Troubleshooting

### "fatal: 'origin' does not appear to be a 'git' repository"

**Solution:** Add the remote:
```bash
git remote add origin https://github.com/yourusername/lab-scanner.git
```

### "ERROR: Permission denied (publickey)"

**Solution:** Using SSH but key not set up. Use HTTPS instead or set up SSH:
```bash
git remote set-url origin https://github.com/yourusername/lab-scanner.git
git push -u origin main
```

### "ERROR: The referenced branch does not exist"

**Solution:** Rename branch first:
```bash
git branch -M main
git push -u origin main
```

### Credentials Not Saving

**Solution:** Save credentials permanently:
```bash
git config --global credential.helper store
git push  # Enter credentials once, will be saved
```

---

## 💡 Best Practices

1. **Write clear commit messages:**
   ```bash
   git commit -m "Fix: Resolve timeout issue in port scanner"
   git commit -m "Feature: Add network discovery CIDR support"
   ```

2. **Commit frequently** - One logical change per commit

3. **Use branches for features:**
   ```bash
   git checkout -b feature/new-scanner
   # Make changes
   git push -u origin feature/new-scanner
   # Create Pull Request on GitHub
   ```

4. **Keep .gitignore updated** - Already done! Check `.gitignore`

5. **Add tags for releases:**
   ```bash
   git tag -a v1.0.0 -m "Lab Scanner v1.0.0 Release"
   git push origin v1.0.0
   ```

---

## 📊 After Pushing

Once on GitHub, you can:

✅ Share the repo link with others  
✅ Collaborate with contributors  
✅ Use GitHub Issues for bug tracking  
✅ Create GitHub Projects for planning  
✅ Set up GitHub Pages for documentation  
✅ Configure GitHub Actions for CI/CD  
✅ Manage releases and versions  

---

## 🎯 Summary

```bash
# The essential commands:
git remote add origin https://github.com/yourusername/lab-scanner.git
git branch -M main
git push -u origin main

# Then for future changes:
git add .
git commit -m "message"
git push
```

---

**Your Lab Scanner project is now ready for GitHub!** 🚀

Need help? Visit [GitHub Docs](https://docs.github.com) or ask GitHub support.
