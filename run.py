from app import app

if __name__ == '__main__':
    # use_reloader=False so flask doesn't start twice
    app.run(host='0.0.0.0', port=8080, debug=True)