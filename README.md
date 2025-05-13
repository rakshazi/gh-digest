# 📬 GitHub Notification Digest Action

This project is a GitHub Action that **sends you a daily digest of all your unread GitHub notifications by email**.
Say goodbye to notification overload and hello to one informative email—complete with context, repository info, clickable links, and message snippets.  
After the digest is sent, the notifications are automatically marked as read.

---

## ✨ How it works?

- 🕙 **Runs daily at 7am UTC**
- 📥 **Collects all unread GitHub notifications**
- 📨 **Sends a single, easy-to-read email to your chosen address using your SMTP server**
- ℹ️ **Digest includes:**  
  - Repository name  
  - Notification type (Issue, Pull Request, etc.)  
  - Title  
  - Reason for notification  
  - Clickable link  
  - Short snippet/comment preview (if available)
- ✅ **Marks notifications as read if email was sent successfully**

---

## 🛠 Setup & Usage

### 1. **Clone or Fork this Repository**

```bash
git clone https://github.com/rakshazi/gh-digest.git
```


### 2. **Configure Secrets**

Go to your repository on GitHub, then **Settings → Secrets and variables → Actions** and **add these secrets**:

| Secret Name   | Description                                                    |
| ------------- | -------------------------------------------------------------- |
| `GH_TOKEN`    | GitHub Personal Access Token with `notifications` scope        |
| `SMTP_USER`   | Your email address for SMTP login (e.g. gh-digest@example.com) |
| `SMTP_PASS`   | SMTP password for your email address                           |
| `SMTP_HOST`   | SMTP server address (e.g. smtp.example.com)                    |
| `SMTP_PORT`   | SMTP server port (e.g. 587 for TLS)                            |
| `MAIL_TO`     | Email address to send the digest to                            |

### 3. **Edit Workflow if Needed**

By default, the workflow is in `.github/workflows/gh-digest.yml` and sends the digest to `github@etke.cc`.  
If you want to use a different schedule or email, you can edit:

- **Cron Schedule:**  
  The workflow uses this cron:  
```
schedule:
- cron: '0 7 * * *' # Every day at 7am UTC
```

### 4. **Done**

1. **Every day at 7am UTC**, the workflow runs.
2. It **fetches all unread notifications** from GitHub.
3. It **generates a digest** that summarizes each notification with enough context to understand it—no need to open individual links!
4. It **sends the digest** via your SMTP server.
5. If successful, it **marks all those notifications as read**.

---

## 📝 Example Digest

You’ll receive an email like this:

🔔 [your-org/your-repo]

* Type: PullRequest
* Title: Improve digest script readability
* Reason: assigned
* Link: https://github.com/your-org/your-repo/pull/42
* Snippet: Here's a summary of changes to help...

---

🔔 [another-repo]

...


*(If there are no unread notifications, you’ll get a sweet "No unread notifications! Have a great day!")*
