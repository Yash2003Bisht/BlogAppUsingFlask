from website import index

app = index()

if __name__ == "__main__":
    app.run(debug=True, threaded=False, processes=500)
    
