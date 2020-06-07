from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


@app.route("/")
def my_home():
    return render_template("index.html")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open("database.txt", "a") as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f"\n{name},{email},{subject},{message}")  # 此f等同於format用法


def write_to_csv(data):
    with open("database.csv", "a", newline="") as database2:
        # 這裡在開啟 csv 檔案時加上了 newline='' 參數，這是為了讓資料中包含的換行字元可以正確被解析，
        # 所以建議在讀取 csv 檔案時都固定加入這個參數。
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(
            database2, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )  # 建立檔案寫入器
        csv_writer.writerow([name, email, subject, message])


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":  # 記得要大寫
        data = request.form.to_dict()
        write_to_csv(data)
        name = data["name"]
        return render_template("/thankyou.html", name=name)
    else:
        return "Something went wrong. Try again!"


# if __name__ == "__main__":  # 如果以主程式執行
#     app.run()  # 立刻啟動伺服器
