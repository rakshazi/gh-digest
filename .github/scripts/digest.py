import os
import requests
import smtplib
import markdown
from email.message import EmailMessage
from dotenv import load_dotenv
from collections import defaultdict
from operator import itemgetter

load_dotenv()

GITHUB_API = "https://api.github.com/notifications"
TOKEN = os.environ['GH_TOKEN']
SMTP_SERVER = os.environ['SMTP_HOST']
SMTP_PORT = os.environ['SMTP_PORT']
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASS = os.environ['SMTP_PASS']
MAIL_TO = os.environ['MAIL_TO']

# mapping of notification types to emojis
TYPE_TO_EMOJI = {
    "Issue": "🐞",
    "PullRequest": "🔀",
    "Commit": "💾",
    "Release": "🏷️",
    "Discussion": "💬",
    "IssueComment": "💬",
    "PullRequestReviewComment": "📝",
    "PullRequestReview": "👀",
    "CheckSuite": "✅",
    "CheckRun": "✅",
    "RepositoryVulnerabilityAlert": "🚨",
    "Deployment": "🚀",
    "DeploymentStatus": "🚦",
    "SecurityAlert": "🔒",
    "WorkflowRun": "⚙️",
    "WorkflowJob": "🛠️",
    "CommitComment": "🗒️",
    "Default": "🔔",
}

# notification type to human-readable text
TYPE_TO_TEXT = {
    "Issue": "issue",
    "PullRequest": "pull request",
    "Commit": "commit",
    "Release": "release",
    "Discussion": "discussion",
    "IssueComment": "issue comment",
    "PullRequestReviewComment": "pull request review comment",
    "PullRequestReview": "pull request review",
    "CheckSuite": "check suite",
    "CheckRun": "check run",
    "RepositoryVulnerabilityAlert": "repository vulnerability alert",
    "Deployment": "deployment",
    "DeploymentStatus": "deployment status",
    "SecurityAlert": "security alert",
    "WorkflowRun": "workflow run",
    "WorkflowJob": "workflow job",
    "CommitComment": "commit comment",
    "Default": "notification",
}

# mapping of reason types to human-readable text
REASON_TO_TEXT = {
    "approval_requested": "you were requested to review and approve a deployment",
    "assign": "you were assigned to the issue",
    "author": "you created the thread",
    "comment": "you commented on the thread",
    "ci_activity": "a GitHub Actions workflow run that you triggered was completed",
    "invitation": "you accepted an invitation to contribute to the repository",
    "manual": "you subscribed to the thread (via an issue or pull request)",
    "member_feature_requested": "organization members have requested to enable a feature such as Copilot",
    "mention": "you were specifically @mentioned in the content",
    "review_requested": "you, or a team you're a member of, were requested to review a pull request",
    "security_alert": "GitHub discovered a security vulnerability in your repository",
    "security_advisory_credit": "you were credited for contributing to a security advisory",
    "state_change": "you changed the thread state (for example, closing an issue or merging a pull request)",
    "subscribed": "you're watching the repository",
    "team_mention": "you were on a team that was mentioned",
    "Default": "you received a notification about this thread",
}
# mapping of reason types to emojis
REASON_TO_EMOJI = {
    "approval_requested": "👀",
    "assign": "👤",
    "author": "✍️",
    "comment": "💬",
    "ci_activity": "🔄",
    "invitation": "📩",
    "manual": "🔔",
    "member_feature_requested": "🛠️",
    "mention": "🔔",
    "review_requested": "👀",
    "security_alert": "🚨",
    "security_advisory_credit": "🛡️",
    "state_change": "🔄",
    "subscribed": "🔔",
    "team_mention": "👥",
    "Default": "",
}


def emoji_for(notification_type):
    return TYPE_TO_EMOJI.get(notification_type, TYPE_TO_EMOJI["Default"])

def text_for(notification_type):
    return TYPE_TO_TEXT.get(notification_type, TYPE_TO_TEXT["Default"])

def reason_for(reason):
    return REASON_TO_TEXT.get(reason, REASON_TO_TEXT["Default"])

def reason_emoji_for(reason):
    return REASON_TO_EMOJI.get(reason, REASON_TO_EMOJI["Default"])


def fetch_notifications():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    r = requests.get(GITHUB_API, headers=headers)
    match(r.status_code):
        case 401:
            print("❌ Invalid GitHub token. Please check the configuration")
            os.exit(1)
        case 403:
            print("❌ GitHub API rate limit exceeded. Please try again later.")
            os.exit(1)
        case 200:
            return r.json()
        case 404:
            print("❌ GitHub API endpoint not found. Please check the URL.")
            os.exit(1)
        case 503:
            print("❌ GitHub API service unavailable. Please try again later.")
            os.exit(1)
        case _:
            print(f"❌ Unexpected error: {r.status_code}")
            os.exit(1)
    return r.json()

def mark_as_read(thread_ids):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    for tid in thread_ids:
        requests.patch(f"https://api.github.com/notifications/threads/{tid}", headers=headers)

def build_digest_grouped(notifs):
    if not notifs:
        return None, None

    # 1. Sort notifications by newest first
    notifs_sorted = sorted(notifs, key=lambda n: n.get('updated_at', ''), reverse=True)

    # 2. Group notifications by repository full name
    grouped = defaultdict(list)
    for n in notifs_sorted:
        repo = n['repository']['full_name']
        grouped[repo].append(n)

    lines = []
    for repo, repo_notifs in sorted(grouped.items()):
        # Get repo web URL from any notification
        repo_url = repo_notifs[0]['repository'].get('html_url', f"https://github.com/{repo}")
        lines.append(f"## {repo} ([web]({repo_url}))\n")

        for n in repo_notifs:
            subject = n['subject']
            notif_type = subject['type']
            title = subject['title']
            reason = n.get('reason', "")
            # Build notification web URL
            if subject.get('latest_comment_url'):
                web_url = subject['latest_comment_url']
                # hack to get the correct URL for issue comments
                if "issues/comments" in web_url:
                    web_url = f"{subject.get('url')}#issuecomment-{web_url.split('/')[-1]}"
            elif subject.get('url'):
                web_url = subject['url']
            else:
                web_url = repo_url
            web_url = web_url.replace("api.github.com/repos", "github.com").replace("/pulls/", "/pull/").replace("/issues/comments/", "/issues/")
            # yes, hacky, but it's better than sending additional API request just to get the tag
            if notif_type == "Release":
                web_url = repo_url + "/releases"

            snippet = ""
            comment_types = ["Issue", "IssueComment", "PullRequestReviewComment"]
            is_comment = notif_type in comment_types
            if is_comment and subject.get('latest_comment_url'):
                try:
                    c = requests.get(subject['latest_comment_url'], headers={
                        "Authorization": f"token {TOKEN}",
                        "Accept": "application/vnd.github+json"
                    })
                    if c.ok:
                        snippet = c.json().get('body', '')
                except Exception:
                    pass

            # Compose the notification line
            notif_line = f"""### [{emoji_for(notif_type)} {title}]({web_url})"""
            notif_line += f"\n_you have received this notification about the {emoji_for(notif_type)} {text_for(notif_type)} because {reason_emoji_for(reason)} {reason_for(reason)}._\n"
            if snippet:
                notif_line += f"\n\n{snippet.strip()}\n"
            lines.append(notif_line)
        lines.append('---')  # Separator between repos, if you want (can remove)

    digest_text = '\n\n'.join(lines)
    return digest_text, lines

def send_mail(digest_text, digest_lines):
    digest_text = f"### GitHub Notification Digest\n\n{digest_text}"
    msg = EmailMessage()
    msg['Subject'] = '📬 Your GitHub Notification Digest'
    msg['From'] = f'rakshazi/gh-digest <{SMTP_USER}>'
    msg['To'] = MAIL_TO
    msg.set_content(digest_text)
    html = ""
    for line in digest_lines:
        html += markdown.markdown(line)
    msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=60) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        os.exit(1)

def main():
    print("🔄 Fetching notifications...")
    notifications = fetch_notifications()

    # Mark as read IDs (done at the end IF email sending succeeds)
    thread_ids = [n['id'] for n in notifications]

    print(f"📝 Building digest from {len(notifications)} notifications...")
    digest, lines = build_digest_grouped(notifications)
    if not digest:
        print("🎉 No unread notifications!")
        return

    print("📧 Sending email...")
    send_mail(digest, lines)
    print("✅ Email sent!")

    print("✅ Marking notifications as read...")
    if thread_ids:
        mark_as_read(thread_ids)
    print("✅ Marked notifications as read!")

if __name__ == "__main__":
    main()
