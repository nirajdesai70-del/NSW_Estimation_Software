# NSW Estimation Software - React Frontend

**New build (canonical going forward)**

This is the React frontend for NSW Estimation Software, designed to work with the FastAPI backend.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Axios** - HTTP client
- **TanStack Query** - Data fetching and caching

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API client and services
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .env.example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Update `VITE_API_BASE_URL` if your backend is running on a different port.

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

## Development Guidelines

1. **Use OpenAPI contract** - The FastAPI backend generates OpenAPI schema at `/docs`
2. **No DB knowledge in UI** - UI only calls API endpoints
3. **Type safety** - Use TypeScript for all components
4. **API client** - Use the `apiClient` from `services/api.ts` for all API calls

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## API Integration

The frontend uses the API client configured in `src/services/api.ts`. It automatically:
- Adds authentication tokens to requests
- Handles 401 errors (token refresh or logout)
- Uses the base URL from environment variables

## Next Steps

1. ✅ React skeleton with routing
2. ⏳ Implement authentication pages (login, etc.)
3. ⏳ Implement catalog management UI
4. ⏳ Implement BOM management UI
5. ⏳ Implement quotation management UI

