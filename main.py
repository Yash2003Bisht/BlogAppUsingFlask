from website import index

app = index()

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
