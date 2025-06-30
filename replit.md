# AI Educational Content Generator

## Overview

This is a Flask-based web application that generates comprehensive educational content using OpenAI's API. Users can input a course title and receive AI-generated course objectives, syllabi, learning outcomes, assessment methods, and recommended readings aligned with Bloom's Taxonomy.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask for server-side rendering
- **UI Framework**: Bootstrap with dark theme for responsive design
- **Client-side**: Vanilla JavaScript for form validation and interactivity
- **Styling**: Custom CSS with Font Awesome icons

### Backend Architecture
- **Web Framework**: Flask (Python) with minimal routing structure
- **API Integration**: OpenAI API for content generation
- **Session Management**: Flask sessions with configurable secret key
- **Error Handling**: Comprehensive logging and user-friendly error messages

### Application Structure
```
├── main.py          # Application entry point
├── app.py           # Flask application setup and routes
├── openai_service.py # OpenAI API integration
├── templates/       # HTML templates
├── static/          # CSS, JS, and assets
└── pyproject.toml   # Python dependencies
```

## Key Components

### Core Application (`app.py`)
- **Route Handlers**: Main index route and content generation endpoint
- **Input Validation**: Course title validation (3-200 characters)
- **Error Handling**: Flash messages for user feedback
- **Template Rendering**: Dynamic content display with conditional sections

### OpenAI Service (`openai_service.py`)
- **Content Generation**: Structured prompts for educational content creation
- **JSON Response Handling**: Structured output including course objectives, syllabi, learning outcomes, assessments, and readings
- **Bloom's Taxonomy Integration**: Ensures educational content aligns with cognitive learning levels

### Frontend Components
- **Responsive Design**: Bootstrap-based layout with dark theme
- **Form Validation**: Real-time client-side validation with visual feedback
- **Accessibility Features**: ARIA labels and keyboard navigation support
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

## Data Flow

1. **User Input**: Course title entered through web form
2. **Validation**: Client-side and server-side validation
3. **API Request**: Structured prompt sent to OpenAI API
4. **Content Generation**: AI generates comprehensive educational content
5. **Response Processing**: JSON response parsed and formatted
6. **Template Rendering**: Results displayed in user-friendly format
7. **Error Handling**: Graceful error handling with user feedback

## External Dependencies

### Required Services
- **OpenAI API**: Content generation service (requires API key)
- **Environment Variables**: `OPENAI_API_KEY` and optional `SESSION_SECRET`

### Python Dependencies
- **Flask**: Web framework and templating
- **OpenAI**: Official OpenAI Python client
- **Gunicorn**: Production WSGI server
- **Additional**: Email validation, SQLAlchemy (prepared for future database integration)

### Frontend Dependencies
- **Bootstrap**: UI framework with dark theme
- **Font Awesome**: Icon library
- **CDN-hosted**: External resources for styling and icons

## Deployment Strategy

### Development Environment
- **Local Server**: Flask development server with debug mode
- **Hot Reload**: Automatic reloading for development
- **Environment**: Python 3.11 with Nix package management

### Production Deployment
- **Server**: Gunicorn WSGI server
- **Binding**: 0.0.0.0:5000 with port reuse
- **Autoscaling**: Configured for automatic scaling
- **Database Support**: PostgreSQL ready (packages installed)

### Infrastructure
- **Replit Platform**: Configured for Replit deployment
- **Nix Environment**: Stable channel with OpenSSL and PostgreSQL
- **Workflow**: Automated startup with parallel task execution

## Changelog

- June 25, 2025: Initial setup complete
- June 25, 2025: Full AI Educational Content Generator deployed with OpenAI integration
- June 25, 2025: Configured to use Google Gemini API exclusively for AI content generation
- June 25, 2025: Added downloadable content feature with formatted text output

## User Preferences

Preferred communication style: Simple, everyday language.