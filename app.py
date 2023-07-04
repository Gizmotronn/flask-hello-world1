from flask import Flask, request, render_template
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Use Agg backend for matplotlib
plt.switch_backend('Agg')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']

        try:
            TIC = f'{tic_id}'
            available_data_select = lk.search_lightcurve(TIC, author='SPOC', cadence='short', mission='TESS')
            lc = available_data_select.download()

            if lc is None:
                raise ValueError(f"No data found for TIC ID {tic_id}")

            # Create the lightkurve graph
            fig, ax = plt.subplots(figsize=(8, 4))
            lc.plot(ax=ax, linewidth=0, marker='o', color='pink', markersize=2, alpha=0.8)

            # Save the plot as a bytes object
            image_bytes = BytesIO()
            plt.savefig(image_bytes, format='png')
            plt.close()
            image_bytes.seek(0)

            # Convert the bytes object to base64 string for embedding in HTML
            encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

            return render_template('result.html', tic_id=TIC, image_data=encoded_image)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()