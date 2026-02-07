# Premier Properties - Deployment Options

Deployment cost and architecture recommendations for the Premier Properties real estate platform, organized by anticipated foot traffic and budget.

**Current Stack:** React/Vite frontend, FastAPI backend, PostgreSQL database (all containerized with Docker).

---

## Low Traffic / Low Cost

**Scenario:** < 1,000 daily visitors, small regional agency, MVP/pilot launch.

**Estimated Monthly Cost:** $5 - $30/month

### Option A: Single VPS (Recommended for getting started)

| Component | Service | Cost |
|-----------|---------|------|
| All-in-one | DigitalOcean Droplet (1 vCPU, 1 GB RAM) | $6/mo |
| Database | PostgreSQL on same VPS | $0 (included) |
| Domain + DNS | Cloudflare (free tier) | $0 |
| SSL | Let's Encrypt via Caddy/Nginx | $0 |
| **Total** | | **~$6/mo** |

- Run `docker compose up` on a single VPS with Caddy as a reverse proxy.
- Caddy handles SSL termination and routes `/api/*` to FastAPI and `/` to the Vite static build.
- Back up the PostgreSQL volume to object storage (e.g., DigitalOcean Spaces, $5/mo for 250 GB) on a cron schedule.

### Option B: Platform-as-a-Service (Minimal ops)

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | Vercel or Netlify (free tier) | $0 |
| Backend | Railway or Render (starter) | $5 - $7/mo |
| Database | Neon PostgreSQL (free tier, 0.5 GB) | $0 |
| **Total** | | **~$5 - $7/mo** |

- Build the Vite frontend as static files and deploy to Vercel/Netlify.
- Deploy the FastAPI backend as a container on Railway or Render.
- Use Neon or Supabase free-tier PostgreSQL.

### Considerations

- No high availability - single point of failure is acceptable at this scale.
- Manual deployments or simple CI/CD via GitHub Actions.
- Daily database backups to object storage.
- Vertical scaling (upgrade VPS size) is the primary scaling lever.

---

## Medium Traffic / Medium Cost

**Scenario:** 1,000 - 50,000 daily visitors, growing agency or multi-city operation.

**Estimated Monthly Cost:** $50 - $300/month

### Option A: Managed Container Platform (Recommended)

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | Vercel Pro or Cloudflare Pages | $0 - $20/mo |
| Backend | AWS App Runner or GCP Cloud Run (2 instances) | $30 - $80/mo |
| Database | AWS RDS PostgreSQL (db.t4g.micro) or GCP Cloud SQL | $15 - $30/mo |
| CDN | Cloudflare (free tier) | $0 |
| Object Storage | S3 / GCS for property images | $5 - $10/mo |
| Monitoring | Datadog free tier or Grafana Cloud free | $0 |
| **Total** | | **~$50 - $140/mo** |

- Cloud Run / App Runner auto-scales containers from 0 to N based on request volume.
- Managed PostgreSQL with automated backups, point-in-time recovery, and read replicas available if needed.
- Frontend served from CDN edge nodes globally.
- Property images stored in object storage and served through CDN.

### Option B: Kubernetes-lite (AWS Lightsail Containers / DigitalOcean App Platform)

| Component | Service | Cost |
|-----------|---------|------|
| App Platform | DigitalOcean App Platform (Basic) | $12 - $24/mo per component |
| Database | DigitalOcean Managed PostgreSQL (1 GB) | $15/mo |
| CDN + DNS | Cloudflare Pro | $20/mo |
| Backups + Storage | DO Spaces | $5/mo |
| **Total** | | **~$65 - $90/mo** |

### Architecture Notes

```
                 Cloudflare CDN
                 /            \
    Static Frontend         API Gateway / Load Balancer
    (Vercel/CF Pages)             |
                           Cloud Run / App Runner
                           (2-4 auto-scaled instances)
                                  |
                          Managed PostgreSQL
                          (with automated backups)
```

### Considerations

- Horizontal auto-scaling on the backend handles traffic spikes (e.g., new listing announcements).
- Managed database with automatic failover and daily backups.
- CI/CD pipeline via GitHub Actions: lint, test, build Docker image, deploy.
- Add APM/monitoring (Sentry for errors, basic Datadog/Grafana for metrics).
- Add Redis (e.g., ElastiCache or Upstash) for caching property searches at ~$10-15/mo if query latency becomes an issue.
- Consider a read replica for the database if read-heavy traffic demands it.

---

## High Traffic / High Cost

**Scenario:** 50,000+ daily visitors, national platform, multiple metro areas, high SEO priority.

**Estimated Monthly Cost:** $500 - $3,000+/month

### Option A: AWS Production-Grade (Recommended)

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | CloudFront + S3 (static hosting) | $20 - $50/mo |
| Backend | ECS Fargate (4-8 tasks, auto-scaling) | $150 - $400/mo |
| API Gateway | ALB (Application Load Balancer) | $25 - $50/mo |
| Database | RDS PostgreSQL Multi-AZ (db.r6g.large) | $200 - $400/mo |
| Cache | ElastiCache Redis (cache.t4g.medium) | $50 - $100/mo |
| Search | OpenSearch (if full-text property search needed) | $80 - $200/mo |
| Object Storage | S3 for images + CloudFront | $10 - $30/mo |
| Monitoring | Datadog or New Relic (Pro) | $50 - $150/mo |
| CI/CD | GitHub Actions + ECR | $10 - $20/mo |
| WAF | AWS WAF on ALB | $10 - $30/mo |
| **Total** | | **~$600 - $1,400/mo** |

### Option B: GCP Production-Grade

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | Cloud CDN + Cloud Storage | $15 - $40/mo |
| Backend | GKE Autopilot (3-6 pods) or Cloud Run | $120 - $350/mo |
| Database | Cloud SQL PostgreSQL (HA, 4 vCPU) | $200 - $400/mo |
| Cache | Memorystore Redis | $50 - $100/mo |
| Search | Elasticsearch on GCE or Algolia | $80 - $200/mo |
| Monitoring | Cloud Monitoring + Cloud Trace | $30 - $80/mo |
| **Total** | | **~$500 - $1,200/mo** |

### Architecture

```
        Users
          |
     Cloudflare WAF + DDoS protection
          |
    +-----------+--------------------+
    |                                |
 CloudFront/CDN               ALB / Cloud LB
 (static assets)                    |
                         ECS Fargate / GKE Autopilot
                         (4-8 auto-scaled containers)
                            |              |
                     Redis Cache     Managed PostgreSQL
                     (hot queries)   (Multi-AZ / HA)
                                          |
                                    Read Replica(s)
                                    (for search queries)
```

### Considerations

- Multi-AZ database with automatic failover for zero-downtime resilience.
- Redis caching layer for property listing queries and session data.
- CDN serves all static assets and property images at edge locations.
- Container auto-scaling based on CPU/request count (scale from 4 to 20+ during peaks).
- Full CI/CD: GitHub Actions builds and pushes Docker images to ECR/GCR, deploys via rolling update.
- Blue/green or canary deployments to minimize risk during releases.
- WAF + rate limiting on the API to protect against abuse.
- Structured logging, distributed tracing, and alerting.
- Consider adding a queue (SQS/Pub-Sub) for contact inquiry processing to decouple email notifications.
- Database connection pooling via PgBouncer sidecar or RDS Proxy.

---

## Quick Comparison Matrix

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Monthly Cost** | $5 - $30 | $50 - $300 | $500 - $3,000+ |
| **Daily Visitors** | < 1K | 1K - 50K | 50K+ |
| **Uptime SLA** | Best-effort | ~99.5% | 99.9%+ |
| **Auto-scaling** | No (manual) | Yes (backend) | Yes (all layers) |
| **Database HA** | No | Optional | Multi-AZ / HA |
| **CDN** | Optional | Yes | Yes + WAF |
| **Caching** | None | Optional Redis | Redis required |
| **CI/CD** | Manual / basic | GitHub Actions | Full pipeline + canary |
| **Monitoring** | Logs only | Basic APM | Full observability |
| **Recovery Time** | Hours | < 30 min | < 5 min |
| **Ops Complexity** | Minimal | Moderate | Significant |
| **Best For** | MVP, pilot | Growing business | National platform |

---

## Recommended Migration Path

1. **Start Low** - Deploy on a single VPS or PaaS to validate product-market fit.
2. **Move to Medium** - When traffic exceeds ~500 concurrent users or you need reliability guarantees, migrate to managed containers + managed database.
3. **Scale to High** - When response time, uptime SLA, or traffic volume demands it, adopt full cloud-native architecture with HA database, caching, and auto-scaling.

Each tier builds on the previous one. The Docker Compose setup already in this repo is directly deployable to all three tiers with minimal changes -- the main differences are in the surrounding infrastructure (load balancers, managed databases, CDN, monitoring).

---

## PaaS Deployment Guide (Low-Cost Option B)

Step-by-step instructions for deploying Premier Properties on free/low-cost PaaS services.

### Prerequisites

- A GitHub account with this repo pushed to it
- Free accounts on [Vercel](https://vercel.com), [Railway](https://railway.app), and [Neon](https://neon.tech)

### Step 1: Create the Database (Neon)

1. Sign up at [neon.tech](https://neon.tech) and create a new project.
2. Name the database `realestate`.
3. Copy the connection string. It will look like:
   ```
   postgresql://user:pass@ep-cool-name-123456.us-east-2.aws.neon.tech/realestate?sslmode=require
   ```
4. Neon free tier includes 0.5 GB storage and 100 compute hours/month.

### Step 2: Deploy the Backend (Railway)

1. Sign up at [railway.app](https://railway.app) and click **New Project > Deploy from GitHub Repo**.
2. Select this repository.
3. Railway will detect `backend/Dockerfile`. Set the **Root Directory** to `/backend`.
4. Add these **environment variables** in the Railway dashboard:
   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | Your Neon connection string from Step 1 |
   | `CORS_ORIGINS` | `https://your-app.vercel.app` (update after Step 3) |
5. Railway exposes a public URL like `https://premier-properties-api.up.railway.app`.
6. The first deploy will run `seed.py` automatically (it's in the Dockerfile CMD). Subsequent deploys skip seeding because the script is idempotent.

**Alternative -- Render:** Create a new **Web Service**, connect the repo, set Root Directory to `backend`, and set the same environment variables. Render detects the Dockerfile or you can point it to the `Procfile`.

### Step 3: Deploy the Frontend (Vercel)

1. Sign up at [vercel.com](https://vercel.com) and click **Add New > Project**.
2. Import this GitHub repository.
3. Set the **Root Directory** to `frontend`.
4. Vercel auto-detects Vite via `vercel.json`. No build config changes needed.
5. Add this **environment variable** in the Vercel dashboard:
   | Variable | Value |
   |----------|-------|
   | `VITE_API_URL` | Your Railway backend URL from Step 2 (e.g., `https://premier-properties-api.up.railway.app`) |
6. Deploy. Vercel gives you a URL like `https://premier-properties.vercel.app`.

### Step 4: Connect the Services

1. Go back to Railway and update the `CORS_ORIGINS` env var with your actual Vercel URL from Step 3.
2. Redeploy the backend (Railway does this automatically when env vars change).
3. Visit your Vercel URL -- the app should load and display properties from Neon.

### Step 5: Custom Domain (Optional)

- **Vercel:** Settings > Domains > add your domain. Vercel provisions SSL automatically.
- **Railway:** Settings > Domains > add a custom domain for the API (e.g., `api.yourdomain.com`).
- Update `VITE_API_URL` in Vercel to `https://api.yourdomain.com` and `CORS_ORIGINS` in Railway to `https://yourdomain.com`.

### Architecture Diagram

```
  Browser
    |
    ├── https://yourdomain.com ──────> Vercel (static React/Vite build)
    |                                     |
    |                                  VITE_API_URL
    |                                     |
    └── https://api.yourdomain.com ───> Railway (FastAPI container)
                                          |
                                       DATABASE_URL
                                          |
                                        Neon (PostgreSQL)
```

### Files Added for PaaS Deployment

| File | Purpose |
|------|---------|
| `frontend/vercel.json` | Tells Vercel to use the Vite framework preset and adds SPA routing rewrites |
| `backend/Procfile` | Start command for PaaS platforms that don't use Docker (Render, Heroku-compatible) |
| `backend/.env.example` | Updated with Neon and CORS_ORIGINS examples |
