# import pandas as pd
# import joblib
# from django.shortcuts import render
# from .forms import FileUploadForm

import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
from django.shortcuts import render
from django.conf import settings
from .forms import FileUploadForm

def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES['file']

            # Read the file content directly into a Pandas DataFrame
            try:
                data = pd.read_excel(uploaded_file)  # Read the Excel file
                
                # Drop unnecessary columns (adjust based on your dataset)
                X = data.drop(columns=['ROP_AVG'])  # Replace 'ROP_AVG' with actual target column name
                
                # Load pre-trained models
                lr_density = joblib.load('Drill/models/lr_density_model.pkl')
                rf_density = joblib.load('Drill/models/rf_density_model.pkl')
                lr_viscosity = joblib.load('Drill/models/lr_viscosity_model.pkl')
                rf_viscosity = joblib.load('Drill/models/rf_viscosity_model.pkl')
                
                # Make predictions
                predictions_lr_density = lr_density.predict(X)
                predictions_rf_density = rf_density.predict(X)
                predictions_lr_viscosity = lr_viscosity.predict(X)
                predictions_rf_viscosity = rf_viscosity.predict(X)
                
                # Combine results into a DataFrame
                results = pd.DataFrame({
                    'Actual': data['ROP_AVG'],  # Replace with the actual target column name
                    'LR_Density': predictions_lr_density,
                    'RF_Density': predictions_rf_density,
                    'LR_Viscosity': predictions_lr_viscosity,
                    'RF_Viscosity': predictions_rf_viscosity
                })

                # Generate correlation matrix heatmap
                correlation_matrix = results.corr()
                plt.figure(figsize=(8, 6))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
                heatmap_file_path = os.path.join(settings.MEDIA_ROOT, 'correlation_heatmap.png')
                plt.title('Correlation Matrix Heatmap')
                plt.savefig(heatmap_file_path)
                plt.close()

                # Convert the DataFrame to HTML for display in the browser
                results_html = results.to_html(classes='table table-striped', index=False)

                return render(request, 'results.html', {
                    'results': results_html,
                    'heatmap_url': settings.MEDIA_URL + 'correlation_heatmap.png'
                })
            except Exception as e:
                # Handle any errors (e.g., invalid Excel file format)
                return render(request, 'upload.html', {'form': form, 'error': str(e)})
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})

# def upload(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Get the uploaded file
#             uploaded_file = request.FILES['file']

#             # Read the file content directly into a Pandas DataFrame
#             try:
#                 data = pd.read_excel(uploaded_file)  # Read the Excel file
                
#                 # Drop unnecessary columns (adjust based on your dataset)
#                 X = data.drop(columns=['ROP_AVG'])  # Replace 'ROP_AVG' with actual target column name
                
#                 # Load pre-trained models
#                 lr_density = joblib.load('Drill/models/lr_density_model.pkl')
#                 rf_density = joblib.load('Drill/models/rf_density_model.pkl')
#                 lr_viscosity = joblib.load('Drill/models/lr_viscosity_model.pkl')
#                 rf_viscosity = joblib.load('Drill/models/rf_viscosity_model.pkl')
                
#                 # Make predictions
#                 predictions_lr_density = lr_density.predict(X)
#                 predictions_rf_density = rf_density.predict(X)
#                 predictions_lr_viscosity = lr_viscosity.predict(X)
#                 predictions_rf_viscosity = rf_viscosity.predict(X)
                
#                 # Combine results into a DataFrame
#                 results = pd.DataFrame({
#                     'Actual': data['ROP_AVG'],  # Replace with the actual target column name
#                     'LR_Density': predictions_lr_density,
#                     'RF_Density': predictions_rf_density,
#                     'LR_Viscosity': predictions_lr_viscosity,
#                     'RF_Viscosity': predictions_rf_viscosity
#                 })

#                 # Convert the DataFrame to HTML for display in the browser
#                 results_html = results.to_html(classes='table table-striped', index=False)

#                 return render(request, 'results.html', {'results': results_html})
#             except Exception as e:
#                 # Handle any errors (e.g., invalid Excel file format)
#                 return render(request, 'upload.html', {'form': form, 'error': str(e)})
#     else:
#         form = FileUploadForm()

#     return render(request, 'upload.html', {'form': form})
