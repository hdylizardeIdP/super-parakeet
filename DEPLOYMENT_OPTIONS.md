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
