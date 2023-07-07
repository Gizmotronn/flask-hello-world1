from flask import Flask, request, jsonify
from flask_cors import CORS
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

@app.route('/api/<tic_id>', methods=["POST"])
def get_lightkurve_graph(tic_id):
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

        # Convert the bytes object to base64 string for embedding in HTML
        encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

        return jsonify(tic_id=TIC, image_data=encoded_image)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run()
