from flask import Flask, request, jsonify
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    if request.method == 'POST':
        tic_id = request.json.get('tic_id')

        try:
            TIC = f'TIC {tic_id}'
            available_data_select = lk.search_lightcurve(TIC)
            lc_collection = available_data_select.download_all()

            # Create the lightkurve graph
            fig, ax = plt.subplots(figsize=(8, 4))
            lc_collection.plot(ax=ax, linewidth=0, marker='o', color='pink', markersize=2, alpha=0.8)

            # Save the plot as a bytes object
            image_bytes = BytesIO()
            plt.savefig(image_bytes, format='png')
            plt.close()
            image_bytes.seek(0)

            # Convert the bytes object to base64 string for embedding in JSON response
            encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

            response_data = {
                'tic_id': TIC,
                'image_data': encoded_image,
            }

            return jsonify(response_data)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

    return jsonify({'error': 'Invalid request method'}), 400

if __name__ == '__main__':
    app.run()
