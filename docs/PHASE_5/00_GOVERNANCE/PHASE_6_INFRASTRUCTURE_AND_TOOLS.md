# Phase-6 Infrastructure & Third-Party Tools Requirements

**Version:** 1.1 (Clarifications Added)  
**Date:** 2025-01-27  
**Status:** REQUIREMENTS DOCUMENT  
**Reference:** Phase-6 Execution Plan v1.4 + NEW_BUILD_ARCHITECTURE.md

---

## 🔒 Critical Stack Decision (LOCKED)

**Backend Stack for Phase-6 is locked as FastAPI (Python).**

- **Backend:** FastAPI + SQLAlchemy 2.0 + Alembic + Pydantic v2
- **Frontend:** React 18 + TypeScript + Vite
- **Database:** PostgreSQL 14+
- **Legacy Reference:** Laravel application in `/nish` is read-only reference only

**Note:** Phase-6 Execution Plan may reference Laravel conventions (Blade views, controllers) in some task descriptions. These should be interpreted as FastAPI endpoints + React components. Legacy Laravel references are deprecated for Phase-6 implementation.

---

## 🏗️ Infrastructure Requirements

### Development Environment

#### 1. Database Infrastructure

**PostgreSQL Database:**
- **Version:** PostgreSQL 14+ (required)
- **Purpose:** Primary database for NSW Estimation Software
- **Port:** 5432 (host) or 5433 (Docker)
- **Deployment Options:**
  - **Option A:** Docker Compose (recommended for dev/staging)
    - Image: `postgres:14-alpine`
    - Container name: `nsw_postgres`
    - Persistent volume for data
  - **Option B:** Host-installed PostgreSQL
    - Direct installation on development machine
    - Requires manual setup and configuration

**Database Requirements:**
- Minimum 10GB storage (for dev/staging)
- Backup strategy (daily snapshots recommended)
- Connection pooling support
- Health checks enabled

**Estimated Cost:**
- **Development:** Free (Docker/local) or $20-50/month (cloud managed)
- **Staging:** $50-100/month (cloud managed, e.g., AWS RDS, DigitalOcean)
- **Production:** $100-300/month (managed service with backups)

---

#### 2. Caching & Background Jobs (Deferred)

**Redis:**
- **Version:** Redis 7+
- **Purpose:** 
  - Background job queue (optional, for future use)
  - Caching (optional, for performance optimization)
- **Port:** 6380 (host) or 6379 (Docker)
- **Deployment:** Docker Compose (optional profile)
- **Status:** ⚠️ **NOT REQUIRED FOR PHASE-6 CORE FUNCTIONALITY**

**Critical Decision:** Redis will only be enabled if performance testing during Track D0 (Costing Engine Foundations) shows blocking issues that require background job processing or caching. This avoids premature infrastructure spend and prevents engineers from building around Redis assumptions.

**Gate:** Redis deployment requires explicit approval after D0 Gate performance review.

**Estimated Cost:**
- **Development:** Free (Docker/local)
- **Staging:** $10-30/month (cloud managed)
- **Production:** $30-100/month (managed service)

---

#### 3. Application Hosting

**Backend (FastAPI):**
- **Port:** 8003 (host) or 8001 (Docker)
- **Runtime:** Python 3.10+
- **Deployment Options:**
  - **Development:** Local machine (uvicorn)
  - **Staging:** Cloud VM (AWS EC2, DigitalOcean Droplet, etc.)
  - **Production:** Cloud VM or container service (AWS ECS, Google Cloud Run, etc.)

**API Contracts vs UI-First Reality:**
- **Phase-6 may operate UI-first with internal service calls.** Public API contracts (B1-B4 from Phase-5) may be deferred with a signed defer memo (P6-API-DECISION task).
- This prevents unnecessary CI/CD and contract-testing pressure early in Phase-6.
- Internal service boundaries (FastAPI endpoints) are still required for React frontend integration.

**Frontend (React):**
- **Port:** 3000 (development)
- **Runtime:** Node.js 18+
- **Deployment Options:**
  - **Development:** Local machine (Vite dev server)
  - **Staging:** Static hosting (AWS S3 + CloudFront, Vercel, Netlify)
  - **Production:** Static hosting with CDN

**Estimated Cost:**
- **Development:** Free (local)
- **Staging:** $20-50/month (VM + static hosting)
- **Production:** $50-200/month (VM + CDN + load balancing)

---

#### 4. Docker Infrastructure

**Docker Compose:**
- **Purpose:** Local development environment orchestration
- **Services:**
  - PostgreSQL (profile: `db`)
  - Redis (profile: `cache`)
- **Requirements:**
  - Docker Desktop or Docker Engine
  - Docker Compose v2.0+

**Estimated Cost:**
- **Development:** Free (Docker Desktop)
- **Staging/Production:** Included in VM costs

---

### Staging Environment Requirements

| Component | Specification | Estimated Cost/Month |
|-----------|---------------|---------------------|
| **PostgreSQL Database** | Managed service, 20GB storage, automated backups | $50-100 |
| **Redis Cache** | Managed service, 1GB memory (optional) | $10-30 |
| **Backend VM** | 2 vCPU, 4GB RAM, 50GB storage | $20-40 |
| **Frontend Hosting** | Static hosting with CDN | $5-10 |
| **Domain/SSL** | Custom domain + SSL certificate | $0-10 (Let's Encrypt free) |
| **Monitoring** | Basic monitoring (optional) | $0-20 |
| **TOTAL (Staging)** | | **$85-210/month** |

---

### Production Environment Requirements (Post-Phase-6)

| Component | Specification | Estimated Cost/Month |
|-----------|---------------|---------------------|
| **PostgreSQL Database** | Managed service, 100GB storage, automated backups, high availability | $100-300 |
| **Redis Cache** | Managed service, 2GB memory | $30-100 |
| **Backend VM/Containers** | 4 vCPU, 8GB RAM, auto-scaling | $50-150 |
| **Frontend CDN** | Global CDN, high bandwidth | $20-50 |
| **Load Balancer** | Application load balancer | $20-50 |
| **Monitoring & Logging** | Application monitoring, error tracking | $50-100 |
| **Backup Storage** | Automated backups, disaster recovery | $20-50 |
| **TOTAL (Production)** | | **$290-800/month** |

**Note:** Production infrastructure is NOT required for Phase-6 (internal product only).

---

## 🛠️ Third-Party Tools & Services

### Development Tools

#### 1. Code Repository & Version Control

**Git + GitHub/GitLab/Bitbucket:**
- **Purpose:** Version control, code collaboration
- **Cost:** Free (public/private repos)
- **Required:** Yes

---

#### 2. Design Tools

**UI/UX Design:**
- **Figma** (recommended)
  - **Purpose:** UI design, wireframes, design system
  - **Cost:** $12-15/user/month (Professional) or Free (Starter)
  - **Required:** Yes (for UI/UX designer)
  - **Alternative:** Adobe XD, Sketch

**Estimated Cost:** $12-15/month (1 designer)

---

#### 3. Project Management & Collaboration

**Project Management:**
- **Options:**
  - **Jira** ($7-14/user/month)
  - **Linear** ($8/user/month)
  - **Asana** ($10-25/user/month)
  - **Trello** (Free - $5/user/month)
  - **GitHub Projects** (Free with GitHub)

**Communication:**
- **Slack** ($7-12/user/month) or **Microsoft Teams** ($4-12/user/month)
- **Alternative:** Discord (Free), Mattermost (Free/self-hosted)

**Estimated Cost:** $50-150/month (team of 7-9 people)

---

#### 4. CI/CD & DevOps Tools

**Continuous Integration:**
- **GitHub Actions** (Free for public, $4/user/month for private)
- **GitLab CI** (Free with GitLab)
- **CircleCI** ($15-30/month)
- **Jenkins** (Free, self-hosted)

**Container Registry:**
- **Docker Hub** (Free for public, $5-7/month for private)
- **GitHub Container Registry** (Free with GitHub)
- **AWS ECR** (Pay per storage/transfer)

**Estimated Cost:** $0-50/month

---

#### 5. Testing & Quality Assurance

**Testing Tools:**
- **pytest** (Python) - Free, open-source
- **Jest** (React/JavaScript) - Free, open-source
- **Playwright/Cypress** (E2E testing) - Free, open-source

**Code Quality:**
- **SonarQube** (Free community edition or $120/month for commercial)
- **CodeClimate** ($4-8/user/month)
- **Snyk** (Free for open-source, $52/month for commercial)

**Estimated Cost:** $0-100/month (depending on tools chosen)

---

#### 6. Monitoring & Error Tracking

**Application Monitoring:**

**Phase-6 Monitoring Scope (LOCKED):**
- **✅ Sentry (Free Tier)** → **REQUIRED** for Phase-6
  - Error tracking and exception monitoring
  - Free tier: 5K events/month (sufficient for Phase-6)
  - Cost: $0/month (Free tier)
  - **Optional:** Sentry Paid Tier ($25-40/month) if Free Tier insufficient or debugging becomes bottleneck

**Phase-7+ Monitoring (DEFERRED):**
- **❌ Datadog** ($15-31/host/month) → Phase-7+
- **❌ New Relic** ($25-99/month) → Phase-7+
- **❌ Rollbar** ($12-99/month) → Phase-7+
- **❌ Full APM (Application Performance Monitoring)** → Phase-7+

**Decision:** Phase-6 monitoring is limited to error tracking (Sentry). Performance/APM tooling deferred to Phase-7 when scale and performance optimization become priorities.

**Logging:**
- **Loggly** ($79-199/month)
- **Papertrail** ($7-50/month)
- **Self-hosted ELK Stack** (Free, infrastructure cost)

**Estimated Cost:** $0-100/month (Sentry free tier sufficient for Phase-6)

---

#### 7. Documentation Tools

**API Documentation:**
- **FastAPI OpenAPI** (Built-in, Free)
- **Swagger UI** (Free, included with FastAPI)

**Documentation Hosting:**
- **GitHub Pages** (Free)
- **Read the Docs** (Free)
- **Confluence** ($5-10/user/month)

**Estimated Cost:** $0-50/month

---

#### 8. Security & Compliance Tools

**Dependency Scanning:**
- **Snyk** (Free for open-source)
- **GitHub Dependabot** (Free with GitHub)
- **WhiteSource** ($50-200/month)

**Secrets Management:**
- **HashiCorp Vault** (Free, self-hosted)
- **AWS Secrets Manager** ($0.40/secret/month)
- **1Password** ($7-20/user/month)

**Estimated Cost:** $0-50/month

---

### Backend Dependencies (Python)

**Core Framework:**
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Python 3.10+

**Database:**
- SQLAlchemy 2.0.25
- Alembic 1.13.1
- psycopg[binary] 3.2+

**Validation:**
- Pydantic 2.5.3
- Pydantic Settings 2.1.0

**Authentication:**
- python-jose[cryptography] 3.3.0
- passlib[bcrypt] 1.7.4

**Background Jobs (Optional):**
- Redis 5.0.1
- RQ 1.15.1

**Development:**
- pytest 7.4.4
- pytest-asyncio 0.23.3
- black 24.1.1 (code formatting)
- ruff 0.1.11 (linting)

**All Backend Dependencies:** Free, open-source

---

### Frontend Dependencies (React/TypeScript)

**Core Framework:**
- React 18.2.0
- React DOM 18.2.0
- TypeScript 5.3.3

**Routing:**
- React Router DOM 6.21.0

**HTTP Client:**
- Axios 1.6.5

**State Management:**
- TanStack React Query 5.17.0

**Build Tool:**
- Vite 5.0.11

**Code Quality:**
- ESLint 8.56.0
- TypeScript ESLint plugins

**All Frontend Dependencies:** Free, open-source

---

## 💰 Total Cost Summary

### Development Phase (3 months)

| Category | Monthly Cost | 3-Month Total |
|----------|--------------|---------------|
| **Infrastructure (Staging)** | $85-210 | $255-630 |
| **Design Tools (Figma)** | $12-15 | $36-45 |
| **Project Management** | $50-150 | $150-450 |
| **CI/CD Tools** | $0-50 | $0-150 |
| **Monitoring** | $0-100 | $0-300 |
| **Documentation** | $0-50 | $0-150 |
| **Security Tools** | $0-50 | $0-150 |
| **TOTAL** | **$147-625/month** | **$441-1,875** |

### Cost Optimization Options

**Minimal Setup (100% Free - Recommended Start):**
- GitHub (Free) - Code, CI/CD, project management
- Docker (Free) - Local development
- Figma Starter (Free) - Basic design
- Sentry Free Tier - Error tracking (5K events/month)
- **Total:** $0/month

**Note:** Phase-6 can succeed with 100% free tools. See `PHASE_6_TOOLING_DECISION_FREE_VS_PAID.md` for detailed analysis.

**Recommended Setup (Optional - If Needed):**
- GitHub (Free) - Sufficient for Phase-6
- Figma Professional ($12/month) - Only if Starter insufficient
- Discord (Free) - Communication
- Sentry Paid Tier ($25-40/month) - Only if Free Tier insufficient or debugging bottleneck
- **Total:** ~$37-52/month (only if tools needed)

**Note:** Start with 100% free, add paid tools only if specific needs arise.

**Full-Featured Setup:**
- All tools from "Recommended Setup" +
- Jira ($7/user/month) - Advanced project management
- Datadog or New Relic ($25-100/month) - Monitoring
- CodeClimate ($4/user/month) - Code quality
- **Total:** ~$200-400/month

---

## 📋 Infrastructure Setup Checklist

### Week 0 (Entry Gate)

- [ ] **Development Environment:**
  - [ ] Docker Desktop installed
  - [ ] PostgreSQL 14+ available (Docker or host)
  - [ ] Python 3.10+ installed
  - [ ] Node.js 18+ installed
  - [ ] Git configured

- [ ] **Code Repository:**
  - [ ] Git repository created (GitHub/GitLab)
  - [ ] Branch protection rules configured
  - [ ] CI/CD pipeline skeleton created

- [ ] **Development Tools:**
  - [ ] IDE/Editor configured (VS Code, PyCharm, etc.)
  - [ ] Code formatting tools installed (black, prettier)
  - [ ] Linting tools configured (ruff, ESLint)

- [ ] **Design Tools:**
  - [ ] Figma account created
  - [ ] Design system workspace set up

- [ ] **Project Management:**
  - [ ] Project management tool selected and configured
  - [ ] Team access granted
  - [ ] Initial project structure created

- [ ] **Communication:**
  - [ ] Team communication tool set up (Slack/Discord)
  - [ ] Channels created for different tracks

---

## 🔒 Security Considerations

### Required Security Measures

1. **Secrets Management:**
   - Environment variables for sensitive data
   - `.env` files excluded from version control
   - Secrets rotation policy

2. **Database Security:**
   - Strong passwords for database users
   - Network isolation (Docker networks)
   - SSL/TLS for production connections

3. **API Security:**
   - JWT token authentication
   - CORS configuration
   - Rate limiting (for production)

4. **Code Security:**
   - Dependency vulnerability scanning
   - Regular dependency updates
   - Code review process

---

## 📝 Notes

- **All costs are estimates** - Actual costs may vary based on usage and provider
- **Development tools** - Most are free/open-source
- **Staging infrastructure** - Can use free tiers initially, scale as needed
- **Production infrastructure** - NOT required for Phase-6 (internal product only)
- **Tool selection** - Choose based on team preferences and budget

---

---

## 📝 Version History

- **v1.0:** Initial infrastructure and tools requirements
- **v1.1 (Clarifications Added):** Added 4 critical clarifications + Infrastructure Readiness Gate

### Changes in v1.1:
1. ✅ **Backend Stack Locked:** FastAPI confirmed as Phase-6 backend (Laravel references deprecated)
2. ✅ **Redis Explicitly Deferred:** Only enabled if D0 Gate performance review shows blocking issues
3. ✅ **Monitoring Scope Locked:** Sentry only for Phase-6, APM tools deferred to Phase-7
4. ✅ **API Contracts Clarified:** UI-first approach allowed, public API contracts may be deferred
5. ✅ **Infrastructure Readiness Gate Added:** Week-0 gate checklist to prevent Week-1–2 infrastructure debugging

---

**Document Status:** ✅ REQUIREMENTS COMPLETE (v1.1)  
**Last Updated:** 2025-01-27  
**Next Review:** Before Phase-6 kickoff, verify Infrastructure Gate checklist
