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

_this is a real example from one of the [etke.cc](https://etke.cc) developers_

### GitHub Notification Digest

## etkecc/baibot ([web](https://github.com/etkecc/baibot))


### [🐞 FEATURE REQUEST - Agents as users](https://github.com/etkecc/baibot/issues/23#issuecomment-2868746331)
_You have received this notification about the new issue because you're watching the repository._


This requires a complete reworking of how the bot functions, so I don't think it will be happening.

Closing as unplanned.

----

A workaround would be to have separate agents in separate rooms. You can invoke the one you need by using its specific room. It is more cumbersome, but in the absence of a better way to do things, it gets the job done.


### [🐞 Support for text streaming output?](https://github.com/etkecc/baibot/issues/7#issuecomment-2868742060)
_You have received this notification about the new issue because you're watching the repository._


As you said, Matrix is not a good fit for streaming text - requiring hacks which incur both a serious overhead and complexity.

So I'd say.. this feature likely won't be happening.


### [🐞 Request support for gpt-image-1 and image input](https://github.com/etkecc/baibot/issues/40#issuecomment-2868701694)
_You have received this notification about the new issue because you're watching the repository._


baibot [v1.7.0](https://github.com/etkecc/baibot/blob/d2660be33c11975027c240411ee18463a9583a14/CHANGELOG.md#2025-05-10-version-170) is now out and among other features, now supports `gpt-image-1`.

You will need the following configuration (see the `image_generation` section):

```yml
base_url: https://api.openai.com/v1
api_key: YOUR_API_KEY_HERE
text_generation:
  model_id: gpt-4.1
  prompt: "You are a brief, but helpful bot called {{ baibot_name }} powered by the {{ baibot_model_id }} model. The date/time of this conversation's start is: {{ baibot_conversation_start_time_utc }}."
  temperature: 1.0
  max_response_tokens: 16384
  max_context_tokens: 128000
speech_to_text:
  model_id: whisper-1
text_to_speech:
  model_id: tts-1-hd
  voice: onyx
  speed: 1.0
  response_format: opus
image_generation:
  model_id: gpt-image-1
  style: null
  size: 1024x1024
  quality: null
```

`style` needs to be `null`, because it's not a supported parameter for `gpt-image-1`.

Also, `quality` had better be `null`, because the OpenAI library we use only supports `standard` and `hd` values for this parameter, which are not valid for the `gpt-image-1` model (it expects `high`, `medium` or `low`).


### [🐞 Image to text support?](https://github.com/etkecc/baibot/issues/5#issuecomment-2868698557)
_You have received this notification about the new issue because you're watching the repository._


baibot [v1.7.0](https://github.com/etkecc/baibot/blob/d2660be33c11975027c240411ee18463a9583a14/CHANGELOG.md#2025-05-10-version-170) is now out and supports vision with the OpenAI and Anthropic providers!

You can now mix text and images in the same conversation and everything will be forwarded to the model.

Unfortunately, the library that we use for the OpenAI-compat provider ([etkecc/openai_api_rust](https://github.com/etkecc/openai_api_rust), our patched fork of [openai-rs/openai-api](https://github.com/openai-rs/openai-api)) , which powers most other non-official-OpenAI providers), does not support sending images to the "chat completion" API, so vision support couldn't be added there.


---

## etkecc/synapse-admin ([web](https://github.com/etkecc/synapse-admin))


### [🔀 Bump @mui/utils from 6.4.9 to 7.1.0](https://github.com/etkecc/synapse-admin/pull/545)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump react-router-dom from 7.5.3 to 7.6.0](https://github.com/etkecc/synapse-admin/pull/554)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump react-router from 7.5.3 to 7.6.0](https://github.com/etkecc/synapse-admin/pull/548)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump react-hook-form from 7.56.2 to 7.56.3](https://github.com/etkecc/synapse-admin/pull/549)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump typescript-eslint from 8.31.1 to 8.32.0](https://github.com/etkecc/synapse-admin/pull/550)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump eslint-plugin-prettier from 5.3.1 to 5.4.0](https://github.com/etkecc/synapse-admin/pull/551)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump eslint-config-prettier from 10.1.2 to 10.1.5](https://github.com/etkecc/synapse-admin/pull/546)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump @types/node from 22.15.3 to 22.15.17](https://github.com/etkecc/synapse-admin/pull/547)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump @types/papaparse from 5.3.15 to 5.3.16](https://github.com/etkecc/synapse-admin/pull/553)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump @tanstack/react-query from 5.75.4 to 5.75.7](https://github.com/etkecc/synapse-admin/pull/555)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump @types/react from 19.1.2 to 19.1.3](https://github.com/etkecc/synapse-admin/pull/556)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Bump vite from 6.3.4 to 6.3.5](https://github.com/etkecc/synapse-admin/pull/552)
_You have received this notification about the new pull request because you're watching the repository._


### [🐞 Make synapse-admin work with matrix-authentication-service](https://github.com/etkecc/synapse-admin/issues/38#issuecomment-2871230953)
_You have received this notification about the new issue because you were specifically @mentioned in the content._


> I've figured out the issue. When MSC3861 is enabled, Synapse rejects requests that don't explicitly set `guests=false`. The fix would be to modify the API request in Synapse Admin to always include `guests=false` when building the query parameters for user list requests. This would resolve the error.
>
> curl -X 'GET' 'https://server_name/_synapse/admin/v2/users?from=0&limit=50&deactivated=false&locked=false&suspended=false&guests=false&order_by=name&dir=f

that's unexpected - the initial assumption was the guest filter should be disabled completely, so it should not be present in the request at all. The fix has been pushed, it will be available on admin.etke.cc and in the `latest` docker tag shortly


### [🐞 Use correct API for user suspend/unsuspend](https://github.com/etkecc/synapse-admin/issues/544)
_You have received this notification about the new issue because you're watching the repository._


Currently it looks like the  ["Create or modify account" API](https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html#create-or-modify-account) is used to try to change the suspend status, even though that has its own endpoint: PUT /_synapse/admin/v1/suspend/<user_id>

See [Suspend/Unsuspend Account](https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html#suspendunsuspend-account)


This results in the synapse admin tool not being able to toggle the suspend status of a user


### [🐞 Available on DockerHub?](https://github.com/etkecc/synapse-admin/issues/541#issuecomment-2867829699)
_You have received this notification about the new issue because you're watching the repository._


Now available on https://hub.docker.com/r/etkecc/synapse-admin
Only new releases will be published (alongside `latest` tag), the first one is: https://github.com/etkecc/synapse-admin/releases/tag/v0.10.4-etke40


### [🐞 ``stable``/more general docker tag](https://github.com/etkecc/synapse-admin/issues/542#issuecomment-2867761664)
_You have received this notification about the new issue because you're watching the repository._


Thank you for the idea!
We won't do that for now because the current versioning scheme should be changed first.

Please, keep the issue open - we will return to it in the future for sure

_Long boring history of the reasoning below_


Initially, we've created that fork to solve the most painful problems of our customers _fast_, so we've just took `v<UpstreamRelease>-etke<N>`, assuming that's a temporary solution, and once changed will be accepted into upstream, we can switch back to the original version.

Unfortunately, practice shows that there is nothing more persistent than a temporary solution 🙂 So, we will revisit the versioning scheme, and after that return to your idea!


---

## mother-of-all-self-hosting/ansible-role-changedetection ([web](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection))


### [🔀 chore(deps): update ghcr.io/dgtlmoon/changedetection.io docker tag to v0.49.17](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/pull/7)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 chore(config): migrate renovate config](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/pull/8)
_You have received this notification about the new pull request because you're watching the repository._


---

## mother-of-all-self-hosting/ansible-role-fmd-server ([web](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server))


### [🐞 Rename the role to `ansible-role-fmd`](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/issues/4)
_You have received this notification about the new issue because you're watching the repository._


Apparently the project has been renamed to "FMD":

- https://gitlab.com/fmd-foss/fmd-server/-/commit/e08b8ab45e54a400b870eb3eb001cd613512c0f2
- https://gitlab.com/fmd-foss/fmd-server/-/commit/97a85822600212dbf3e9afa43d5459871702209a

The image registry URL has also been changed to `registry.gitlab.com/fmd-foss/fmd-server` with https://gitlab.com/fmd-foss/fmd-server/-/commit/6d8acbbe3a98e5beeecdfc315146d00fd9125cb0.


---

## mother-of-all-self-hosting/ansible-role-headscale ([web](https://github.com/mother-of-all-self-hosting/ansible-role-headscale))


### [🔀 Maintenance](https://github.com/mother-of-all-self-hosting/ansible-role-headscale/pull/2)
_You have received this notification about the new pull request because you're watching the repository._

---

## mother-of-all-self-hosting/ansible-role-homarr ([web](https://github.com/mother-of-all-self-hosting/ansible-role-homarr))


### [🔀 Update ghcr.io/homarr-labs/homarr Docker tag to v1.19.1](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/pull/6)
_You have received this notification about the new pull request because you're watching the repository._


---

## mother-of-all-self-hosting/ansible-role-linkding ([web](https://github.com/mother-of-all-self-hosting/ansible-role-linkding))


### [🔀 Migrate renovate config](https://github.com/mother-of-all-self-hosting/ansible-role-linkding/pull/4)
_You have received this notification about the new pull request because you're watching the repository._


---

## mother-of-all-self-hosting/ansible-role-matterbridge ([web](https://github.com/mother-of-all-self-hosting/ansible-role-matterbridge))


### [🔀 Maintenance](https://github.com/mother-of-all-self-hosting/ansible-role-matterbridge/pull/1)
_You have received this notification about the new pull request because you're watching the repository._


---

## mother-of-all-self-hosting/ansible-role-qbittorrent ([web](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent))


### [🐞 Dependency Dashboard](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/issues/2#issuecomment-2874988816)
_You have received this notification about the new issue because you're watching the repository._


Renovate was removed with https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/commit/acced7959dade00be38a303d739d6c145abd5aa9 as the upstream project does not support it.


### [🔀 Update lscr.io/linuxserver/qbittorrent Docker tag to v14 - autoclosed](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/pull/3)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Update linuxserver/qbittorrent Docker tag to v14](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/pull/1)
_You have received this notification about the new pull request because you're watching the repository._


---

## mother-of-all-self-hosting/ansible-role-traefik-certs-dumper ([web](https://github.com/mother-of-all-self-hosting/ansible-role-traefik-certs-dumper))


### [🐞 QUESTION: How to steer TLS configs in Traefik](https://github.com/mother-of-all-self-hosting/ansible-role-traefik-certs-dumper/issues/2)
_You have received this notification about the new issue because you're watching the repository._


Hello,

just a question please: how can I steer ssl protocols on the server for the services installed?

I mean, default is already well configured, SSL reports, e.g. by Qualys / SSL Labs shows a A+ and TLS v1.3 an v1.2 support.

Q.: What if I just would like to 

- limit to v1.3 and / or
- have direct control on the choice of cipher suites (e.g. eliminating weak ones in TLS v1.2)
- or just simply configure Traefik as e.g. in Mozilla's SSL Configuration Generator with - say - Modern Configuration?

See:
https://ssl-config.mozilla.org/#server=traefik&version=3.2.1&config=modern&guideline=5.7

Where is the place? 
Thank you for your help and advice!

Best
M.


---

## mother-of-all-self-hosting/ansible-role-valkey ([web](https://github.com/mother-of-all-self-hosting/ansible-role-valkey))


### [🔀 Maintenance](https://github.com/mother-of-all-self-hosting/ansible-role-valkey/pull/6)
_You have received this notification about the new pull request because you're watching the repository._


### [🔀 Migrate renovate config](https://github.com/mother-of-all-self-hosting/ansible-role-valkey/pull/5)
_You have received this notification about the new pull request because you're watching the repository._

---



*(If there are no unread notifications, you’ll get a sweet "No unread notifications! Have a great day!" in the action run log)*
