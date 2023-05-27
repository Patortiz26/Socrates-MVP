import pandas as pd
import openai
import os
from docx import Document
import datetime as dt

try:
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
except:
    import toml
    config = toml.load("config.toml")
    openai.api_key = config["API_KEY"]


def create_docx(dicc, school_name, teacher_name, subject):
    """
    Creates a Word document with the given information.

    Args:
        dicc (dict): A dictionary with the topics and questions for the subject.
        school_name (str): The name of the school.
        teacher_name (str): The name of the teacher.
        subject (str): The subject that is being generated for (e.g. Math, Biology).

    Returns:
        None
    """
    
    fecha = dt.datetime.now()
    # Create a new Word document
    document = Document()

    # Set the document properties
    document.core_properties.created = fecha
    document.sections[0].header.paragraphs[0].text = f'{school_name} \t\t{fecha.day}-{fecha.month}-{fecha.year} \nTeacher: {teacher_name}'

    # Add the subtitle
    topics = ", ".join(dicc.keys())
    document.add_paragraph(f'Guía de {subject}', style='Title')
    document.add_paragraph(f'Temas revisados: {topics}', style='Subtitle')

    # Add content for each topic and question
    for topic, questions in dicc.items():
        document.add_heading(topic, level=2).bold = True
        for question, content in questions.items():
            document.add_paragraph().add_run(question).bold = True
            document.add_paragraph(content)

    # Save the document
    return document

def generate_guide(excel_file, course, subject, teacher_name, school_name):
    """
    Generates a guide with questions for students based on an Excel file.

    Args:
        excel_file (str): The path to the Excel file containing the subjects and number of questions.
        course (str): The course of the students (e.g. primaria, secundaria).
        subject (int): The subject that is being generated for (e.g. Math, Biology).
        teacher_name (str): The name of the teacher.
        school_name (str): The name of the school.

    Returns:
        None
    """
    # Read Excel file
    df = pd.read_excel(excel_file)
    df.columns = ['topic', 'number']
    
    # Initialize a list to store all the questions
    all_questions = {}
    
    # Iterate over each row in the dataframe
    for _, row in df.iterrows():
        topic = row['topic']
        num_questions = row['number']
        
        # Generate questions using OpenAI API
        questions = generate_openai_questions(topic, num_questions, course, subject)
        
        # Append questions to the list
        all_questions[topic] = questions
   
    # Create a Word document
    doc = create_docx(all_questions, school_name, teacher_name, subject)
    
    # Save the Word document
    doc.save('guide.docx')

def generate_openai_questions(topic, num_questions, course, subject):
    """
    Generates questions using the OpenAI API for a given subject.

    Args:
        topic (str): The topic of the questions.
        num_questions (int): The number of questions to generate.
        course (str): The course of the students (e.g. primaria, secundaria).
        subject (int): The subject that is being generated for (e.g. Math, Biology).

    Returns:
        questions: A dictionary of generated questions.
    """
    # Define the initial system message providing context
    context = {
        "role": "system",
        "content": f"You are a great {subject} professor designing study guides for your {course} students. For the guide, you need to generate multiple-choice questions and include explanations on how to solve each question. Write in spanish"
    }
    messages = [context]

    questions = {}
    for _ in range(num_questions):
        # Prepare the user message as an order prompt for generating a question
        order_prompt = {
            'role': 'user',
            'content': f"Generate a multiple-choice question about {subject}."
        }
        messages.append(order_prompt)

        # Call the OpenAI API to generate the response based on the conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract the generated question from the response and append it to the list
        generated_question = response.choices[0].message.content
        questions[f'Pregunta {_+1}'] = generated_question

    return questions

