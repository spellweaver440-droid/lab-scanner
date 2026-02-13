"""
Flask Dashboard - Web UI for Lab Scanner
Enhanced with Full Nmap-Style Scanning
"""
from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')

# Backend API URL
API_URL = os.getenv('API_URL', 'http://localhost:8000/api')

logger.info(f"Dashboard connecting to API at: {API_URL}")


@app.route('/')
def index():
    """Dashboard home"""
    return render_template('index.html')


@app.route('/api/dashboard/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        response = requests.get(f'{API_URL}/health', timeout=3)
        is_online = response.status_code == 200
        logger.info(f"API health check: {'ONLINE' if is_online else 'OFFLINE'} (status: {response.status_code})")
        return jsonify({
            'api_status': 'online' if is_online else 'offline',
            'timestamp': datetime.utcnow().isoformat()
        })
    except requests.Timeout:
        logger.warning(f"API health check timeout after 3s")
        return jsonify({'api_status': 'offline', 'error': 'timeout'})
    except requests.ConnectionError:
        logger.warning(f"API health check connection failed")
        return jsonify({'api_status': 'offline', 'error': 'connection'})
    except Exception as e:
        logger.error(f"API health check failed: {str(e)}")
        return jsonify({'api_status': 'offline', 'error': str(e)})


@app.route('/scan', methods=['POST'])
def start_scan():
    """Start full nmap-style scan or other scan types"""
    try:
        data = request.get_json()
        target = data.get('target')
        scan_type = data.get('scan_type', 'full')
        
        logger.info(f"Starting {scan_type} scan on target: {target}")
        
        # Handle different scan types
        if scan_type == 'full':
            # Full comprehensive nmap-style scan
            response = requests.post(
                f'{API_URL}/scan/full',
                json={
                    'target': target,
                    'ports': '1-1024',
                    'threads': 100,
                    'timeout': 2,
                    'scan_type': 'full'
                },
                timeout=180  # 3 minutes timeout for full scan
            )
        elif scan_type == 'port':
            # Port scan only
            response = requests.post(
                f'{API_URL}/scan/port',
                json={
                    'target': target,
                    'ports': '1-1024',
                    'threads': 100,
                    'timeout': 2
                },
                timeout=120
            )
        elif scan_type == 'service':
            # Service detection
            response = requests.get(
                f'{API_URL}/scan/services',
                params={'target': target, 'ports': '22,80,443,3306,5432,8080'},
                timeout=60
            )
        elif scan_type == 'web':
            # Web vulnerability scan
            response = requests.get(
                f'{API_URL}/scan/web',
                params={'target': target, 'port': 80},
                timeout=60
            )
        else:
            # Default to full scan
            response = requests.post(
                f'{API_URL}/scan/full',
                json={
                    'target': target,
                    'ports': '1-1024',
                    'threads': 100,
                    'timeout': 2,
                    'scan_type': 'full'
                },
                timeout=180
            )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Scan completed successfully: {target}")
            return jsonify(result)
        else:
            logger.error(f"API returned status {response.status_code}: {response.text}")
            return jsonify({'error': f'API error: {response.status_code}'}), response.status_code
            
    except requests.exceptions.Timeout:
        logger.error(f"Scan timeout for target: {target}")
        return jsonify({'error': 'Scan timeout - target may be unresponsive'}), 504
    except Exception as e:
        logger.error(f"Scan error: {str(e)}")
        return jsonify({'error': f'Scan error: {str(e)}'}), 400


@app.route('/plugins')
def list_plugins():
    """List available plugins"""
    try:
        response = requests.get(f'{API_URL}/plugins/list')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/discover/network', methods=['POST'])
def discover_network():
    """Discover active hosts on network"""
    try:
        data = request.get_json()
        network_range = data.get('network_range')
        threads = data.get('threads', 50)
        
        if not network_range:
            return jsonify({'error': 'network_range is required'}), 400
        
        logger.info(f"Discovering hosts on {network_range}")
        
        response = requests.post(
            f'{API_URL}/discover/network',
            params={'network_range': network_range, 'threads': threads},
            timeout=300  # 5 minutes for network discovery
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Discovery complete: found {result.get('count', 0)} hosts")
            return jsonify(result)
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), response.status_code
            
    except requests.exceptions.Timeout:
        logger.error("Network discovery timeout")
        return jsonify({'error': 'Discovery timeout - network may be too large'}), 504
    except Exception as e:
        logger.error(f"Network discovery error: {str(e)}")
        return jsonify({'error': f'Discovery error: {str(e)}'}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info(f"Starting Dashboard on 0.0.0.0:5000")
    logger.info(f"Backend API: {API_URL}")
    app.run(debug=True, host='0.0.0.0', port=5000)
