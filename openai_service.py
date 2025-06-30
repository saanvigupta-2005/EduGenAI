from google import genai
from google.genai import types
import json
import os
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini client
gemini_client = None
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    logging.info("Gemini client initialized successfully")
else:
    logging.warning("No Gemini API key found in environment")

def generate_educational_content(course_title):
    """
    Generate comprehensive educational content for a given course title
    using Google Gemini API, aligned with Bloom's Taxonomy levels
    """
    logging.debug(f"Generating content for course: {course_title}")
    
    try:
        prompt = f"""Create comprehensive educational content for the course: "{course_title}"

Please provide a detailed response in JSON format with the following structure:
{{
    "course_objectives": [
        {{"objective": "string", "bloom_level": "string"}},
        {{"objective": "string", "bloom_level": "string"}},
        {{"objective": "string", "bloom_level": "string"}}
    ],
    "syllabus": [
        {{"week": "string", "topic": "string", "description": "string"}},
        {{"week": "string", "topic": "string", "description": "string"}},
        {{"week": "string", "topic": "string", "description": "string"}}
    ],
    "learning_outcomes": [
        {{"outcome": "string", "bloom_level": "string"}},
        {{"outcome": "string", "bloom_level": "string"}},
        {{"outcome": "string", "bloom_level": "string"}}
    ],
    "assessment_methods": [
        {{"method": "string", "description": "string", "weight": "string"}},
        {{"method": "string", "description": "string", "weight": "string"}}
    ],
    "recommended_readings": [
        {{"title": "string", "author": "string", "type": "string", "description": "string"}},
        {{"title": "string", "author": "string", "type": "string", "description": "string"}}
    ]
}}

Ensure all content is academically rigorous, pedagogically sound, and appropriate for higher education."""

        # Use Gemini API for content generation
        if gemini_client:
            try:
                system_prompt = "You are an expert educational content creator. Generate comprehensive course materials aligned with Bloom's Taxonomy levels. Respond in JSON format."
                
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n{prompt}")])
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.7
                    )
                )
                logging.info("Successfully used Gemini for content generation")
                
                # Extract content from Gemini response
                if hasattr(response, 'text') and response.text:
                    content_text = response.text
                else:
                    logging.warning("Empty response from Gemini")
                    return generate_demo_content(course_title)
                    
            except Exception as gemini_error:
                logging.error(f"Gemini API error: {gemini_error}")
                logging.warning("Gemini failed, falling back to demo mode")
                return generate_demo_content(course_title)
        else:
            logging.warning("Gemini client not available, using demo content")
            return generate_demo_content(course_title)
            
        content = json.loads(content_text)
        
        # Validate the structure
        if validate_content_structure(content):
            logging.info(f"Successfully generated educational content for: {course_title}")
            return content
        else:
            logging.warning("Generated content structure invalid, falling back to demo mode")
            return generate_demo_content(course_title)
            
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {str(e)}")
        logging.warning("JSON parsing failed, falling back to demo mode")
        return generate_demo_content(course_title)
    
    except Exception as e:
        logging.error(f"API error: {str(e)}")
        logging.warning(f"API error occurred, falling back to demo mode: {str(e)}")
        return generate_demo_content(course_title)


def generate_demo_content(course_title):
    """
    Generate demo educational content when AI APIs are not available
    This shows the application structure while API key issues are resolved
    """
    logging.info(f"Generated demo content for: {course_title}")
    
    # Create educationally sound demo content based on the course title
    demo_content = {
        "course_objectives": [
            {"objective": f"Students will develop comprehensive understanding of {course_title} through theoretical foundations and practical applications", "bloom_level": "Understanding"},
            {"objective": f"Students will analyze current trends and methodologies in {course_title}", "bloom_level": "Analyzing"},
            {"objective": f"Students will create innovative solutions and projects related to {course_title}", "bloom_level": "Creating"}
        ],
        "syllabus": [
            {"week": "Week 1", "topic": "Introduction and Foundations", "description": f"Overview of {course_title}, historical context, and fundamental concepts"},
            {"week": "Week 2", "topic": "Theoretical Framework", "description": "Core theories and principles underlying the subject matter"},
            {"week": "Week 3", "topic": "Methodology and Approaches", "description": "Research methods and analytical approaches in the field"},
            {"week": "Week 4", "topic": "Case Studies and Applications", "description": "Real-world applications and practical examples"},
            {"week": "Week 5", "topic": "Current Trends and Developments", "description": "Contemporary issues and emerging trends"},
            {"week": "Week 6", "topic": "Advanced Topics", "description": "In-depth exploration of specialized areas"},
            {"week": "Week 7", "topic": "Project Development", "description": "Hands-on project work and implementation"},
            {"week": "Week 8", "topic": "Evaluation and Future Directions", "description": "Assessment of learning and future research opportunities"}
        ],
        "learning_outcomes": [
            {"outcome": f"Demonstrate foundational knowledge of key concepts in {course_title}", "bloom_level": "Understanding"},
            {"outcome": f"Apply theoretical principles to solve practical problems in {course_title}", "bloom_level": "Applying"},
            {"outcome": f"Evaluate different approaches and methodologies used in {course_title}", "bloom_level": "Evaluating"}
        ],
        "assessment_methods": [
            {"method": "Written Examinations", "description": "Comprehensive tests covering theoretical knowledge and application", "weight": "40%"},
            {"method": "Project Portfolio", "description": "Collection of practical projects demonstrating skill application", "weight": "35%"},
            {"method": "Class Participation", "description": "Active engagement in discussions and collaborative activities", "weight": "25%"}
        ],
        "recommended_readings": [
            {"title": f"Fundamentals of {course_title}", "author": "Academic Press", "type": "Textbook", "description": "Comprehensive introduction to core concepts and principles"},
            {"title": f"Advanced {course_title}: Theory and Practice", "author": "Research Publications", "type": "Reference Book", "description": "In-depth coverage of advanced topics and current research"},
            {"title": f"Case Studies in {course_title}", "author": "Industry Press", "type": "Case Study Collection", "description": "Real-world applications and practical examples"},
            {"title": f"Current Trends in {course_title}", "author": "Journal Publications", "type": "Academic Articles", "description": "Latest research findings and emerging developments"},
            {"title": f"Practical Guide to {course_title}", "author": "Professional Publications", "type": "Handbook", "description": "Step-by-step guidance for practical implementation"}
        ]
    }
    
    return demo_content


def validate_content_structure(content):
    """
    Validate that the generated content has the expected structure
    """
    required_keys = ['course_objectives', 'syllabus', 'learning_outcomes', 'assessment_methods', 'recommended_readings']
    
    if not isinstance(content, dict):
        return False
        
    for key in required_keys:
        if key not in content:
            return False
        if not isinstance(content[key], list):
            return False
        if len(content[key]) == 0:
            return False
    
    return True