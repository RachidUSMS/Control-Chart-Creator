from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    df = pd.read_csv(file)
    
    # Exemple : Supposons que la colonne 'Values' contient les données
    data = df['Values']
    mean = data.mean()
    std = data.std()
    ucl = mean + 3 * std
    lcl = mean - 3 * std
    
    plt.figure(figsize=(10, 6))
    plt.plot(data, marker='o', label='Data')
    plt.axhline(mean, color='green', linestyle='--', label='Mean')
    plt.axhline(ucl, color='red', linestyle='--', label='UCL (3σ)')
    plt.axhline(lcl, color='red', linestyle='--', label='LCL (3σ)')
    plt.legend()
    plt.title("Carte de Contrôle")
    plt.xlabel("Index")
    plt.ylabel("Values")
    plt.savefig('static/control_chart.png')
    
    return render_template('result.html', chart_url='static/control_chart.png')

if __name__ == '__main__':
    app.run(debug=True)
