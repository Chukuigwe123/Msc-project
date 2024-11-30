import io
import base64
import seaborn as sns
import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import FileUploadForm
import pandas as pd
import joblib



def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES['file']

            try:
                # Read the file content into a Pandas DataFrame
                data = pd.read_excel(uploaded_file)
                
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

                # Generate Correlation Heatmap
                plt.figure(figsize=(10, 6))
                correlation_matrix = results.corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
                heatmap_buffer = io.BytesIO()
                plt.savefig(heatmap_buffer, format='png')
                heatmap_buffer.seek(0)
                heatmap_base64 = base64.b64encode(heatmap_buffer.read()).decode('utf-8')
                plt.close()

                # Generate Scatter Plot (e.g., Actual vs. Predicted)
                plt.figure(figsize=(8, 6))
                plt.scatter(results['Actual'], results['LR_Density'], label='LR Density', alpha=0.6)
                plt.scatter(results['Actual'], results['RF_Density'], label='RF Density', alpha=0.6)
                plt.xlabel('Actual')
                plt.ylabel('Predicted')
                plt.title('Scatter Plot: Actual vs Predicted')
                plt.legend()
                scatter_buffer = io.BytesIO()
                plt.savefig(scatter_buffer, format='png')
                scatter_buffer.seek(0)
                scatter_base64 = base64.b64encode(scatter_buffer.read()).decode('utf-8')
                plt.close()

                # Convert results to HTML for display
                results_html = results.to_html(classes='table table-striped', index=False)

                return render(request, 'results.html', {
                    'results': results_html,
                    'heatmap_image': heatmap_base64,
                    'scatter_image': scatter_base64
                })

            except Exception as e:
                # Handle any errors (e.g., invalid Excel file format)
                return render(request, 'index.html', {'form': form, 'error': str(e)})
    else:
        form = FileUploadForm()

    return render(request, 'index.html', {'form': form})
