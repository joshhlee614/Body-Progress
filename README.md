# Body Progress Tracker

A mobile app that helps users track and analyze their bodybuilding progress over time through photo timelines, body composition estimation, and quantitative progress modeling.

## Features

- Upload and organize progress photos
- Log weight and training notes
- Visualize progress with interactive graphs and timelines
- ML-based body composition estimation from images
- Time series analysis for progress modeling

## Tech Stack

- Mobile: React Native
- Backend: FastAPI + PostgreSQL (via Supabase)
- ML: PyTorch
- Data Analysis: Python (Kalman filtering, Bayesian smoothing)

## Development Setup

1. Clone the repository
2. Install dependencies:
   - Mobile app: `cd mobile-app && npm install`
   - Backend: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Start the development servers:
   - Mobile: `cd mobile-app && npm start`
   - Backend: `cd backend && uvicorn main:app --reload`

## Project Structure

```
/
├── mobile-app/     # React Native mobile app
├── backend/        # FastAPI backend
├── ml-server/      # ML model server
└── quant-analysis/ # Quantitative analysis layer
```

## Contributing

1. Create a new branch from `dev`
2. Make your changes
3. Submit a pull request to `dev`
4. After review, changes will be merged to `main`

## License

MIT 