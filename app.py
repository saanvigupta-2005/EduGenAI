import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, Response, make_response
from openai_service import generate_educational_content
import json
from datetime import datetime

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key")

@app.route('/')
def index():
    """Main page with course title input form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    """Generate educational content based on course title"""
    try:
        # Get course title from form
        course_title = request.form.get('course_title', '').strip()
        
        # Validate input
        if not course_title:
            flash('Please enter a course title.', 'error')
            return redirect(url_for('index'))
        
        if len(course_title) < 3:
            flash('Course title must be at least 3 characters long.', 'error')
            return redirect(url_for('index'))
        
        if len(course_title) > 200:
            flash('Course title must be less than 200 characters.', 'error')
            return redirect(url_for('index'))
        
        # Generate content using OpenAI
        logging.debug(f"Generating content for course: {course_title}")
        content = generate_educational_content(course_title)
        
        # Log successful content generation
        logging.info(f"Successfully generated educational content for: {course_title}")
        
        # Render results page with generated content
        return render_template('index.html', 
                             course_title=course_title, 
                             content=content,
                             show_results=True)
        
    except Exception as e:
        logging.error(f"Error generating content: {str(e)}")
        flash(f'An error occurred while generating content: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/generate', methods=['POST'])
def api_generate_content():
    """API endpoint for generating content (for AJAX requests)"""
    try:
        data = request.get_json()
        course_title = data.get('course_title', '').strip()
        
        # Validate input
        if not course_title:
            return jsonify({'error': 'Course title is required'}), 400
        
        if len(course_title) < 3:
            return jsonify({'error': 'Course title must be at least 3 characters long'}), 400
        
        if len(course_title) > 200:
            return jsonify({'error': 'Course title must be less than 200 characters'}), 400
        
        # Generate content
        content = generate_educational_content(course_title)
        
        return jsonify({
            'success': True,
            'course_title': course_title,
            'content': content
        })
        
    except Exception as e:
        logging.error(f"API error generating content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<course_title>')
def download_content(course_title):
    """Download generated content as a text file"""
    try:
        # Generate content for download
        content = generate_educational_content(course_title)
        
        # Format content as text
        text_content = f"Educational Content for: {course_title}\n"
        text_content += "=" * 50 + "\n\n"
        
        if 'course_objectives' in content:
            text_content += "COURSE OBJECTIVES:\n"
            for i, obj in enumerate(content['course_objectives'], 1):
                text_content += f"{i}. {obj['objective']} ({obj['bloom_level']})\n"
            text_content += "\n"
        
        text_content += "LEARNING OUTCOMES:\n"
        for i, outcome in enumerate(content['learning_outcomes'], 1):
            text_content += f"{i}. {outcome['outcome']} ({outcome['bloom_level']})\n"
        text_content += "\n"
        
        text_content += "SAMPLE SYLLABUS:\n"
        for week in content['syllabus']:
            text_content += f"• {week['week']}: {week['topic']}\n"
            text_content += f"  - {week['description']}\n"
        text_content += "\n"
        
        text_content += "ASSESSMENT METHODS:\n"
        for assessment in content['assessment_methods']:
            text_content += f"• {assessment['method']} ({assessment['weight']})\n"
            text_content += f"  - {assessment['description']}\n"
        text_content += "\n"
        
        text_content += "RECOMMENDED READINGS:\n"
        for reading in content['recommended_readings']:
            text_content += f"• {reading['title']} by {reading['author']}\n"
            text_content += f"  - Type: {reading['type']}\n"
            text_content += f"  - {reading['description']}\n"
        
        # Create response with download headers
        response = make_response(text_content)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename="{course_title.replace(" ", "_")}_content.txt"'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating download: {str(e)}")
        flash(f'Error generating download: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
