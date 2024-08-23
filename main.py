from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resumes')

        # Check if both job description and resumes are provided
        if not job_description or len(resume_files) == 0:
            return render_template('matchresume.html', message="Please enter a job description and upload resumes.")

        resumes = []
        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resumes.append(extract_text(filename))

         # Save extracted resume text to a file
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_resumes.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for i, resume_text in enumerate(resumes):
                    output_file.write(f"Resume {i + 1}:\n")
                    output_file.write(resume_text)
                    output_file.write("\n\n" + "-" * 80 + "\n\n")


        # Vectorize job description and resumes
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        # Calculate cosine similarities
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Print job_vectors , resumes_vectors , similarity scores
        print(job_vector)
        print("==================================================================")
        print(resume_vectors)
        print("===================================================================")
        print(similarities)

        # Get top 3 resumes and their similarity scores
        top_indices = similarities.argsort()[-3:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        # Debug: Print top resumes and their scores
        print(f"Top Resumes: {top_resumes}")
        print(f"Similarity Scores (Top): {similarity_scores}")

        return render_template('matchresume.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=similarity_scores)

    return render_template('matchresume.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)