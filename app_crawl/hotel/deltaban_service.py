from flask import Flask, request, jsonify
from deltaban import Deltaban
import traceback

app = Flask(__name__)

@app.route('/api/hotel/deltaban/search', methods=['POST'])
def search_hotels():
    try:
        data = request.get_json()
        
        # Extract parameters from request
        target = data.get('target')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        adults = data.get('adults')
        is_analysis = data.get('is_analysis', False)
        hotelstar_analysis = data.get('hotelstar_analysis', [])
        priority_timestamp = data.get('priority_timestamp', 1)
        use_cache = data.get('use_cache', False)

        # Validate required parameters
        if not all([target, start_date, end_date]):
            return jsonify({
                'status': False,
                'message': 'Missing required parameters'
            }), 400

        # Create Deltaban instance and get results
        deltaban = Deltaban(
            target=target,
            start_date=start_date,
            end_date=end_date,
            adults=adults,
            isAnalysiss=is_analysis,
            hotelstarAnalysis=hotelstar_analysis,
            priorityTimestamp=priority_timestamp,
            use_cache=use_cache
        )
        
        result = deltaban.get_result()

        return jsonify({
            'status': True,
            'data': result
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'status': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)